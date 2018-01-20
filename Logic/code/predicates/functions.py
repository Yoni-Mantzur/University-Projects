""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/predicates/functions.py """
import copy
from itertools import combinations

from code.predicates.syntax import *
from code.predicates.semantics import *
from code.predicates.util import *


def from_func_to_relation_in_meaning(function_name, func_dict):
    """ Casting the syntax of function to relation in model  """
    relation_name = function_name_to_relation_name(function_name)
    relation_set = set()

    for k_ary in func_dict.keys():
        relation_set.add((func_dict[k_ary],) + k_ary)

    return {relation_name: relation_set}


def replace_functions_with_relations_in_model(model):
    """ Return a new model obtained from the given model by replacing every
        function meaning with the corresponding relation meaning (i.e.,
        (x1,...,xn) is in the meaning if and only if x1 is the output of the
        function meaning for the arguments x2,...,xn), assigned to a relation
        with the same name as the function, except that the first letter is
        capitalized """
    assert type(model) is Model
    # Task 8.2
    new_model = copy.deepcopy(model)
    for item in model.meaning.keys():
        if is_function(item):
            new_model.meaning.update(from_func_to_relation_in_meaning(item, model.meaning[item]))
            del new_model.meaning[item]

    return new_model


def from_relation_to_func_in_meaning(function_name, relation_set):
    """ create map for function from relation set """
    function_dict = {}

    for k_ary in relation_set:
        function_dict[k_ary[1:]] = k_ary[0]

    return {function_name: function_dict}


def replace_relations_with_functions_in_model(model, original_functions):
    """ Return a new model original_model with function names
        original_functions such that:
        model == replace_functions_with_relations_in_model(original_model)
        or None if no such original_model exists """
    assert type(model) is Model
    # Task 8.3
    new_model = copy.deepcopy(model)

    for function_name in original_functions:
        relation_name = function_name_to_relation_name(function_name)
        relation_set = model.meaning[relation_name]

        if pow(len(model.universe), len(next(iter(relation_set))) - 1) != len(relation_set):
            return None

        new_model.meaning.update(from_relation_to_func_in_meaning(function_name, relation_set))
        del new_model.meaning[relation_name]

    return new_model


def function_name_to_relation_name(function_name):
    """ Upper the first letter for the relation name """
    return function_name[0].upper() + function_name[1:]


def compile_term(term):
    """ Return a list of steps that result from compiling the given term,
        whose root is a function invocation (possibly with nested function
        invocations down the term tree). Each of the returned steps is a
        Formula of the form y=f(x1,...,xk), where the y is a new variable name
        obtained by calling next(fresh_variable_name_generator) (you may assume
        that such variables do not occur in the given term), f is a
        single function invocation, and each of the xi is either a constant or
        a variable. The steps should be ordered left-to-right between the
        arguments, and within each argument, the computation of a variable
        value should precede its usage. The left-hand-side variable of the last
        step should evaluate to the value of the given term """
    assert type(term) is Term and is_function(term.root)
    # Task 8.4
    list_steps = []

    def __compile_term_helper(term):

        args = []
        for arg in term.arguments:
            if is_function(arg.root):
                __compile_term_helper(arg)
                args.append(list_steps[-1].first)

            else:
                args.append(arg)

        func = Term(term.root, args)
        step = Formula('=', Term(next(fresh_variable_name_generator)), func)
        list_steps.append(step)

    __compile_term_helper(term)
    return list_steps


def replace_functions_with_relations_in_formula(formula):
    """ Return a function-free analog of the given formula. Every k-ary
        function that is used in the given formula should be replaced with a
        k+1-ary relation with the same name except that the first letter is
        capitalized (e.g., the function plus(x,y) should be replaced with the
        relation Plus(z,x,y) that stands for z=plus(x,y)). (You may assume
        that such relation names do not occur in the given formula, which
        furthermore does not contain any variables names starting with z.) The
        returned formula need only be equivalent to the given formula for
        models where each new relations encodes a function, i.e., is guaranteed
        to have single possible value for the first relation argument for every
        k-tuple of the other arguments """
    assert type(formula) is Formula
    # Task 8.5

    if len(formula.functions()) == 0:
        return formula

    if is_unary(formula.root):
        return Formula('~', replace_functions_with_relations_in_formula(formula.first))

    if is_binary(formula.root):
        return Formula(formula.root, replace_functions_with_relations_in_formula(formula.first),
                       replace_functions_with_relations_in_formula(formula.second))

    if is_quantifier(formula.root):
        return Formula(formula.root, formula.variable,
                       replace_functions_with_relations_in_formula(formula.predicate))

    if is_relation(formula.root):
        return relation_to_relation_with_no_functions(formula)

    return equation_to_equation_with_no_functions(formula)


def func_to_relation(function, first_arg):
    """ return function to relation """
    return Formula(function_name_to_relation_name(function.root), [first_arg] + function.arguments)



def relation_to_relation_with_no_functions(relation):
    """ convert relation with functions to relation without"""

    def __relation_to_relation_with_no_functions(root, args):
        return Formula(root, args)

    return relation_or_equation_to_with_no_functions(relation.root, relation.arguments,
                                                     __relation_to_relation_with_no_functions)


def equation_to_equation_with_no_functions(equation):
    """ convert relation with functions to relation without"""

    def __equation_to_equation_with_no_functions_helper(root, args):
        return Formula(root, args[1], args[0])
    
    return relation_or_equation_to_with_no_functions(equation.root, [equation.first, equation.second],
                                                     __equation_to_equation_with_no_functions_helper)


def relation_or_equation_to_with_no_functions(root, arguments, initial_formula):
    """ convert relation with functions to relation without"""

    def __relation_to_relation_with_no_functions(relation_or_equation_arguments):
        if len(relation_or_equation_arguments) == 0:
            return None

        arg = relation_or_equation_arguments[0]
        # Isn't function doesn't require handling
        if not is_function(arg.root):
            args.append(arg)
            return __relation_to_relation_with_no_functions(relation_or_equation_arguments[1:])

        steps = compile_term(arg)
        args.append(steps[-1].first)
        second = __relation_to_relation_with_no_functions(relation_or_equation_arguments[1:])
        if second is None:
            second = initial_formula(root, args)

        for i in range(len(steps)-1, -1, -1):
            first = func_to_relation(steps[i].second, steps[i].first)
            second = create_for_all_from_function_to_relation(steps[i].first, Formula('->', first, second))
        return second

    args = []
    return __relation_to_relation_with_no_functions(arguments)



def create_for_all_from_function_to_relation(z_i, second):
    """ create the quantifier for all, when convert function to relation """
    return Formula('A', z_i.root, second)


def each_y_unique_x(function_name, num_args):
    vars = [Term(next(fresh_variable_name_generator)) for i in range(1, num_args)]

    z1 = Term(next(fresh_variable_name_generator))
    z2 = Term(next(fresh_variable_name_generator))

    relation_first = Formula(function_name_to_relation_name(function_name), [z1] + vars)
    relation_second = Formula(function_name_to_relation_name(function_name), [z2] + vars)

    formula_for_def = Formula('A', z2.root, Formula('A', z1.root, Formula('->',
                                            Formula('&', relation_first, relation_second), Formula('=', z1, z2))))

    for var in vars[-1::]:
        formula_for_def = Formula('A', var.root, formula_for_def)

    return formula_for_def


def create_formulae_for_function_definitions(formula):
    functions = formula.functions()
    formulae_for_functions_def = []
    for function in functions:
        formulae_for_functions_def.append(each_x_exists_y(function[0], function[1]+1))
        formulae_for_functions_def.append(each_y_unique_x(function[0], function[1]+1))

    return formulae_for_functions_def


def each_x_exists_y(function_name, num_args):
    vars = [Term(next(fresh_variable_name_generator)) for i in range(1, num_args)]
    z = Term(next(fresh_variable_name_generator))
    relation = Formula(function_name_to_relation_name(function_name), [z] + vars)
    formula_for_def = Formula('E', z.root, relation)
    for var in vars[-1::]:
        formula_for_def = Formula('A', var.root, formula_for_def)

    return formula_for_def


def replace_functions_with_relations_in_formulae(formulae):
    """ Return a list of function-free formulae (as strings) that is equivalent
        to the given formulae list (also of strings) that may contain function
        invocations. This equivalence is in the following sense:
        for every model of the given formulae,
        replace_functions_with_relations_in_model(model) should be a model
        of the returned formulae, and for every model of the returned formulae,
        replace_relations_with_functions_in_model(model) should be a model
        of the given formulae. Every k-ary function that is used in the given
        formulae should be replaced with a k+1-ary relation with the same name
        except that the first letter is capitalized (e.g., the function
        plus(x,y) should be replaced with the relation Plus(z,x,y) that stands
        for z=plus(x,y)). (You may assume that such relation names do not occur
        in the given formulae, which furthermore does not contain any variables
        names starting with z.) The returned list should have one formula for
        each formula in the given list, as well as one additional formula for
        every relation that replaces a function name from the given list """
    for formula in formulae:
        assert type(formula) is str
    # task 8.6

    analog_free_formulae = []
    for str_formula in formulae:
        formula = Formula.parse(str_formula)
        analog_free_formula = replace_functions_with_relations_in_formula(formula)
        formulae_for_function_definition = create_formulae_for_function_definitions(formula)
        analog_free_formulae += [analog_free_formula] + formulae_for_function_definition

    return [str(analog_free_formula) for analog_free_formula in analog_free_formulae]

def create_properties_formulae():
    x = Term("x")
    y = Term("y")
    z = Term("z")
    reflexivity = Formula('A', "x", Formula("SAME", [x, x]))
    symmetry = Formula('A', "x", Formula('A', "y", Formula("->", Formula("SAME", [x, y]), Formula("SAME", [y, x]))))
    transitivity = Formula('A', "x", Formula('A', "y", Formula('A', "z",Formula("->", Formula("&", Formula("SAME", [x, y]), Formula("SAME", [y, z])),
                                                                                Formula("SAME", [x, z])))))
    return [reflexivity, symmetry, transitivity]


def create_formula_for_relation(relations_set):
    relations_list = []
    for relation in relations_set:
        relation_name = relation[0]
        num_arguments = relation[1]
        if num_arguments > 0:  #relation with no variables
            vars = [Term(next(fresh_variable_name_generator)) for i in range(0, 2 * num_arguments)]

            same_and = Formula("SAME", [vars[0], vars[num_arguments]])
            for i in range(1, num_arguments):
                same_and = Formula("&", same_and, Formula("SAME", [vars[i], vars[i + num_arguments]]))
            relations = Formula("->", Formula(relation_name, vars[0:num_arguments]), Formula(relation_name, vars[num_arguments:]))
            formula = Formula("->", same_and, relations)
            for var in vars:
                formula = Formula("A", var.root, formula)
            relations_list.append(formula)
    return relations_list


def replace_equality_with_SAME(formulae):
    """ Return a list of equality-free formulae (as strings) that is equivalent
        to the given formulae list (also of strings) that may contain the
        equality symbol. Every occurrence of equality should be replaced with a
        matching instantiation of the relation SAME, which you may assume
        does not occur in the given formulae. You may assume that the given
        formulae do not contain any function invocations. The returned list
        should have one formula for each formula in the given list, as well as
        additional formulae that ensure that SAME is reflexive, symmetric,
        transitive, and respected by all relations in the given formulae """
    for formula in formulae:
        assert type(formula) is str
    # Task 8.7

    is_equal_sign = False
    relations_formulae = []
    for str_formula in formulae:
        if '=' in str_formula:
            is_equal_sign = True
        formula = Formula.parse(str_formula)
        relations_formulae.append(create_formula_without_equality(formula))
        relations_formulae += create_formula_for_relation(formula.relations())
    if is_equal_sign:
        relations_formulae += create_properties_formulae()  # add reflexivity, symmetry, transitivity.
    return [str(formulae_object) for formulae_object in relations_formulae]


def create_formula_without_equality(formula):
    if is_variable(formula.root) or is_constant(formula.root):
        return formula

    if is_unary(formula.root):
        return Formula("~", create_formula_without_equality(formula.first))

    if is_binary(formula.root):
        return Formula(formula.root, create_formula_without_equality(formula.first), create_formula_without_equality(formula.second))

    if is_relation(formula.root):
        return formula

    if is_quantifier(formula.root):
        return Formula(formula.root, formula.variable, create_formula_without_equality(formula.predicate))

    if is_equality(formula.root):
        return Formula("SAME", [formula.first, formula.second])

def add_SAME_as_equality(model):
    """ Return a new model obtained from the given model by adding the relation
        SAME that behaves like equality """
    assert type(model) is Model
    # Task 8.8
    SAME_relation = set()
    new_model = copy.deepcopy(model)
    for var in model.universe:
        SAME_relation.add((var, var))
    new_model.meaning["SAME"] = SAME_relation
    return new_model

def is_var_exist(var, classes_list):
    """ return if the variable exist in the class list already or not"""
    for eq_set in classes_list:
            if var in eq_set:
                return True
    return False

def add_pair(pair, elements_sets):
    """ create a pair of values from universe"""
    pair_0 = is_var_exist(pair[0], elements_sets)
    pair_1 = is_var_exist(pair[1], elements_sets)
    if not pair_0 and not pair_1:
        new_set = set()
        new_set.add(pair[0])
        new_set.add(pair[1])
        elements_sets.append(new_set)
    else:
        if pair_0:
            for set_var in elements_sets:
                if pair[0] in set_var:
                    set_var.add(pair[1])
        elif pair_1 :
            for set_var in elements_sets:
                if pair[1] in set_var:
                    set_var.add(pair[0])
    return elements_sets

def union_sets(elements_sets):
    """ returns a list of sets such that if there is intersection between sets, they are getting into one set"""
    while True:
        has_intersection = False
        for s1, s2 in combinations(elements_sets, r=2):
            if s1 & s2:
                s1 |= s2
                elements_sets.remove(s2)
                has_intersection = True
                break
        if not has_intersection:
            break
    return elements_sets

def partition_to_eq_classes(model):
    """ return a list of sets that represent the equivalence classes"""
    elements_sets = []
    same_relations = model.meaning['SAME']
    for pair in same_relations:
        elements_sets = add_pair(pair, elements_sets)

    return union_sets(elements_sets)

def get_universe_var(var, elements_sets):
    """ gets variable and return the new value of it(from the new universe)"""
    for set_var in elements_sets:
        list_var = list(set_var)
        if var in list_var:
            return list_var[0] if list_var[0] != var else list_var[1]

def update_relation_args(relation_name, args, universe, equivalence_classes):
    """return the updated arguments(just from the set of the updated universe)"""
    new_tuple = tuple()
    if len(args) > 0:
        for arg in args:
            if arg not in universe:
                new_arg = (get_universe_var(arg, equivalence_classes),)
            else:
                new_arg = (arg,)
            new_tuple = new_tuple + new_arg
    return new_tuple

def make_equality_as_SAME(model):
    """ Return a new model where equality is made to coincide with the
        reflexive, symmetric, transitive, and respected by all relations,
        relation SAME in the the given model. The requirement is that for every
        model and every list formulae_list, if we take
        new_formulae=replace_equality_with_SAME(formulae) and
        new_model=make_equality_as_SAME(model) then model is a valid model
        of new_formulae if and only if new_model is a valid model of formulae.
        The universe of the returned model should correspond to the equivalence
        classes of the SAME relation in the given model. You may assume that
        there are no function meanings in the given model """
    assert type(model) is Model
    # Task 8.9
    if 'SAME' not in model.meaning.keys():
        return model
    equivalence_classes = partition_to_eq_classes(model)
    new_model = copy.deepcopy(model)
    new_model.universe = set()
    for set_var in equivalence_classes:
        new_model.universe.add(list(set_var)[0])

    new_meaning = {}
    for var in model.meaning:

        if is_relation(var) and var != 'SAME':  # is a relation
            new_set = set()
            if len(model.meaning[var]) > 0:
                for args in model.meaning[var]:
                    new_tuple = update_relation_args(var, args, new_model.universe, equivalence_classes)
                    new_set.add(new_tuple)
                new_meaning[var] = new_set
            else:
                new_meaning[var] = model.meaning[var]
        else:
            if model.meaning[var] not in new_model.universe:
                for set_var in equivalence_classes:
                    list_var = list(set_var)
                    if model.meaning[var] in list_var:
                         new_meaning[var] = list_var[0] if list_var[0] != var else list_var[1]
            else:
                new_meaning[var] = model.meaning[var]

    new_model.meaning = new_meaning
    return new_model