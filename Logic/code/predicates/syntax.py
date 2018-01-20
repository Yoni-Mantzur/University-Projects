""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/predicates/syntax.py """

from code.propositions.syntax import Formula as PropositionalFormula
from code.predicates.util import *
from re import search
from copy import  copy

ALPHA_NUMERIC_REGEX = '[a-zA-Z0-9]*'

def is_unary(s):
    """ Is s a unary operator? """
    return s == '~'

def is_binary(s):
    """ Is s a binary boolean operator? """
    return s == '&' or s == '|' or s == '->'

def is_equality(s):
    """ Is s the equality relation? """
    return s == "="

def is_quantifier(s):
    """ Is s a quantifier? """
    return s == "A" or s == "E"

def is_relation(s):
    """ Is s a relation name? """
    return s[0] >= 'F' and s[0] <= 'T' and s.isalnum()

def is_constant(s):
    """ Is s a constant name? """
    return  ((s[0] >= '0' and s[0] <= '9') or (s[0] >= 'a' and s[0] <= 'd')) and s.isalnum()

def is_function(s):
    """ Is s a function name? """
    return s[0] >= 'f' and s[0] <= 't' and s.isalnum()

def is_variable(s):
    """ Is s a variable name? """
    return s[0] >= 'u' and s[0] <= 'z' and s.isalnum()

def extract_name(s):
    """ return the first name that of variable/function/constant/relation
        that s[0] is prefix of """
    return s[0] + search(ALPHA_NUMERIC_REGEX, s[1:]).group(0)

class Term:
    """ A term in a first order logical formula, composed from constant names
        and variable names, and function names applied to them """

    def __init__(self, root, arguments=None):
        if is_constant(root) or is_variable(root):
            assert arguments is None
            self.root = root
        else:
            assert is_function(root)
            for x in arguments:
                assert type(x) is Term
            self.root = root
            self.arguments = arguments

    def __repr__(self):
        """ Return the usual (functional) representation of self """
        if is_constant(self.root) or is_variable(self.root):
            return self.root

        # self.root is function
        assert is_function(self.root)

        return self.root + Term.repr_args(self.arguments)


    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return not self == other
        
    def __hash__(self):
        return hash(str(self))

    @staticmethod
    def repr_args(args):
        """ represents a arguments list as string """
        args_str = ''
        if len(args) != 0:
            args_str = str(args[0])
            for i in range(1, len(args)):
                args_str += ',' + (str(args[i]))
        return '(' + args_str + ')'

    @staticmethod
    def parse_prefix(s):
        """ Parse a term from the prefix of a given string. Return a pair: the
            parsed term, and the unparsed remainder of the string """
        # Task 7.3.1
        if s[0] == ',':
            return Term.parse_prefix(s[1:])

        if is_constant(s[0]) or is_variable(s[0]):
            name_const = extract_name(s)
            return [Term(name_const), s[len(name_const):]]

        func_name = extract_name(s)
        args, s = Term.extract_args(func_name, s)

        return [Term(func_name, args), s[1:]]

    @staticmethod
    def extract_args(operator_name, s):
        """ extract args from s and it's reminder"""
        args = []
        s = s[len(operator_name) + 1:]
        while s[0] != ')':
            term, s = Term.parse_prefix(s)
            args.append(term)

        return args, s

    @staticmethod
    def parse(s):
        """ Return a term parsed from its given string representation """
        # Task 7.3.2
        return Term.parse_prefix(s)[0]

    def variables(self):
        """ Return the set of variables in this term """
        # Task 7.5
        set_vars = set()
        if is_variable(self.root):
            set_vars.add(self.root)

        if is_function(self.root):
            for arg in self.arguments:
                set_vars.update(arg.variables())

        return set_vars


    def functions(self):
        """ Return a set of pairs (function_name, arity) for all function names
            that appear in this term """
        # Task 8.1.1
        set_func_arity = set()

        def _functions_helper(term):
            if is_function(term.root):
                set_func_arity.add((term.root, len(term.arguments)))
                for arg in term.arguments:
                    _functions_helper(arg)

        _functions_helper(self)
        return set_func_arity

    def substitute(self, substitution_map):
        """ Return a term obtained from this term where all the occurrences of
            each constant name or variable name element_name that appears as a
            key in the dictionary substitution_map are replaced with the term
            substitution_map[element_name] """
        for element_name in substitution_map:
            assert (is_constant(element_name) or is_variable(element_name)) and \
                   type(substitution_map[element_name]) is Term
        # Task 9.1

        if is_constant(self.root) or is_variable(self.root):
            if self.root in substitution_map:
                return substitution_map[self.root]
            return self

        #  means function
        new_args = []
        for arg in self.arguments:
            new_args.append(arg.substitute(substitution_map))

        return Term(self.root, new_args)

class Formula:
    """ A Formula in first-order logic """
    
    def __init__(self, root, first=None, second=None):
        if is_relation(root): # Populate self.root and self.arguments
            assert second is None
            for x in first:
                assert type(x) is Term
            self.root, self.arguments = root, first
        elif is_equality(root): # Populate self.first and self.second
            assert type(first) is Term and type(second) is Term
            self.root, self.first, self.second = root, first, second
        elif is_quantifier(root): # Populate self.variable and self.predicate
            assert is_variable(first) and type(second) is Formula
            self.root, self.variable, self.predicate = root, first, second
        elif is_unary(root): # Populate self.first
            assert type(first) is Formula and second is None
            self.root, self.first = root, first
        else: # Populate self.first and self.second
            assert is_binary(root) and type(first) is Formula and type(second) is Formula
            self.root, self.first, self.second = root, first, second           

    def __repr__(self):
        """ Return the usual (infix for operators and equality, functional for
            other relations) representation of self """
        if is_equality(self.root):
            return str(self.first) + '=' + str(self.second)

        if is_relation(self.root):
            return self.root + Term.repr_args(self.arguments)

        if is_unary(self.root):
            return '~' + str(self.first)

        if is_binary(self.root):
            return '(' + str(self.first) + self.root + str(self.second) + ')'

        assert is_quantifier(self.root)
        return self.root + self.variable + '[' + str(self.predicate) + ']'

    def __eq__(self, other):
        return str(self) == str(other)
        
    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(str(self))

    @staticmethod
    def parse_prefix(s):
        """ Parse a first-order formula from the prefix of a given string.
            Return a pair: the parsed formula, and unparsed remainder of the
            string """
        # Task 7.4.1
        if is_relation(s[0]):
            relation_name = extract_name(s)
            args, s = Term.extract_args(relation_name, s)
            return [Formula(relation_name, args), s[1:]]

        if is_unary(s[0]):
            unary_operation = s[0]
            formula, s = Formula.parse_prefix(s[1:])
            return [Formula(unary_operation, formula), s]

        if is_quantifier(s[0]):
            quantifier = s[0]
            variable = extract_name(s[1:])
            formula, s = Formula.parse_prefix(s[len(variable) + 2:])
            return [Formula(quantifier, variable, formula), s[1:]]

        if s[0] == '(':  # Means binary operation
            formula_first, s = Formula.parse_prefix(s[1:])
            binary_operation = s[:2] if s[0] == '-' else s[0]
            formula_second, s = Formula.parse_prefix(s[len(binary_operation):])
            return [Formula(binary_operation, formula_first, formula_second), s[1:]]

        t1, s = Term.parse_prefix(s)
        equation_sign = s[0]
        t2, s = Term.parse_prefix(s[1:])
        return [Formula(equation_sign, t1, t2), s]


    @staticmethod
    def parse(s):
        """ Return a first-order formula parsed from its given string
            representation """
        # Task 7.4.2
        return Formula.parse_prefix(s)[0]

    def free_variables(self):
        """ Return the set of variables that are free in this formula """
        # Task 7.6
        def _free_variables_helper(formula, un_free_vars):
            set_free_vars = set()
            if is_equality(formula.root):
                # calc (t1 union t2)
                set_free_vars.update(formula.first.variables())
                set_free_vars.update(formula.second.variables())

            elif is_relation(formula.root):
                for arg in formula.arguments:
                    set_free_vars.update(arg.variables())

            elif is_unary(formula.root):
                set_free_vars.update(_free_variables_helper(formula.first, un_free_vars))

            elif is_binary(formula.root):
                set_free_vars.update(_free_variables_helper(formula.first, un_free_vars))
                set_free_vars.update(_free_variables_helper(formula.second, un_free_vars))

            # quantifier
            else:
                un_free_vars.add(formula.variable)
                set_free_vars.update(_free_variables_helper(formula.predicate, un_free_vars))
                set_free_vars = set_free_vars.difference(un_free_vars)

            return set_free_vars

        return _free_variables_helper(self, set())

    def functions(self):
        """ Return a set of pairs (function_name, arity) for all function names
            that appear in this formula """
        # Task 8.1.2
        set_func_arity = set()

        def _functions_helper(formula):
            if is_equality(formula.root):
                set_func_arity.update(formula.first.functions())
                set_func_arity.update(formula.second.functions())

            elif is_relation(formula.root):
                for arg in formula.arguments:
                    set_func_arity.update(arg.functions())

            elif is_unary(formula.root):
                _functions_helper(formula.first)

            elif is_binary(formula.root):
                _functions_helper(formula.first)
                _functions_helper(formula.second)

            elif is_quantifier(formula.root):
                _functions_helper(formula.predicate)

        _functions_helper(self)
        return set_func_arity


    def relations(self):
        """ Return a set of pairs (relation_name, arity) for all relation names
            that appear in this formula """
        # Task 8.1.3
        set_rel_arity = set()

        def _relations_helper(formula):
            if is_relation(formula.root):
                set_rel_arity.add((formula.root, len(formula.arguments)))

            elif is_unary(formula.root):
                _relations_helper(formula.first)

            elif is_binary(formula.root):
                _relations_helper(formula.first)
                _relations_helper(formula.second)

            elif is_quantifier(formula.root):
                _relations_helper(formula.predicate)

        _relations_helper(self)
        return set_rel_arity


    def substitute(self, substitution_map):
        """ Return a first-order formula obtained from this formula where all
            occurrences of each constant name element_name and all *free*
            occurrences of each variable name element_name for element_name
            that appears as a key in the dictionary substitution_map are
            replaced with substitution_map[element_name] """
        if is_equality(self.root):
            return Formula(self.root, self.first.substitute(substitution_map), self.second.substitute(substitution_map))

        if is_relation(self.root):
            new_args = []
            for arg in self.arguments:
                new_args.append(arg.substitute(substitution_map))
            return Formula(self.root, new_args)

        if is_unary(self.root):
            return Formula(self.root, self.first.substitute(substitution_map))

        if is_binary(self.root):
            return Formula(self.root, self.first.substitute(substitution_map), self.second.substitute(substitution_map))

        if is_quantifier(self.root):
            # Delete if self.variable is in map
            new_map = copy(substitution_map)
            if self.variable in new_map:
                del new_map[self.variable]
            return Formula(self.root, self.variable, self.predicate.substitute(new_map))

    def propositional_skeleton(self):
        """ Return a PropositionalFormula that is the skeleton of this one.
            The variables in the propositional formula will have the names
            z1,z2,... (obtained by calling next(fresh_variable_name_generator)),
            starting from left to right """
        # Task 9.5

        def _propositional_skeleton_helper(formula):
            if is_variable(formula.root) or is_constant(formula.root) or is_quantifier(formula.root) or is_relation(formula.root) \
                    or is_equality(formula.root):
                if formula not in map_formula_to_var:
                    map_formula_to_var[formula] = next(fresh_variable_name_generator)
                return PropositionalFormula(map_formula_to_var[formula])

            first = _propositional_skeleton_helper(formula.first)
            if is_unary(formula.root):
                return PropositionalFormula(formula.root, first)

            # Binary
            second = _propositional_skeleton_helper(formula.second)
            return PropositionalFormula(formula.root, first, second)

        map_formula_to_var = {}
        return _propositional_skeleton_helper(self)




