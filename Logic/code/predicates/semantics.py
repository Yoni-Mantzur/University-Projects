""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/predicates/semantics.py """

from code.predicates.syntax import *

class Model:
    """ A model for first-order formulae: contains a universe - a set of
        elements, and a dictionary that maps every constant name to an element,
        every k-ary relation name to a set of k-tuples of elements, and every
        k-ary function name to a map from k-tuples of elements to an element """

    def __init__(self, universe, meaning):
        assert type(universe) is set
        assert type(meaning) is dict
        self.universe = universe
        self.meaning = meaning

    def __repr__(self):
        return 'Universe=' + str(self.universe) + '; Meaning=' + str(self.meaning)
        
    def evaluate_term(self, term, assignment={}):
        """ Return the value of the given term in this model, where variables   
            get their value from the given assignment """
        assert term.variables().issubset(assignment.keys())
        # Task 7.7
        if is_constant(term.root):
            return self.meaning[term.root]

        if is_variable(term.root):
            return assignment[term.root]

        # f(t_1,...,t_n)
        args_evaluate = tuple(self.evaluate_term(arg, assignment) for arg in term.arguments)
        return self.meaning[term.root][args_evaluate]

    def evaluate_formula(self, formula, assignment={}):
        """ Return the value of the given formula in this model, where
            variables that are free in the formula get their values from the
            given assignment """
        assert formula.free_variables().issubset(assignment.keys())
        # Task 7.8

        if is_equality(formula.root):
            return self.evaluate_term(formula.first, assignment) == self.evaluate_term(formula.second, assignment)

        if is_unary(formula.root):
            return not self.evaluate_formula(formula.first, assignment)

        if is_binary(formula.root):
            return self.evaluate_binary(assignment, formula)

        if is_relation(formula.root):
            args_evaluate = tuple(self.evaluate_term(arg, assignment) for arg in formula.arguments)
            return args_evaluate in self.meaning[formula.root]

        return self.quantifier_evaluate(formula, assignment)


    def evaluate_binary(self, assignment, formula):
        """ evaluates formula as binary operation """
        assert is_binary(formula.root)

        first = self.evaluate_formula(formula.first, assignment)
        second = self.evaluate_formula(formula.second, assignment)
        if formula.root == '->':
            return not first or second
        if formula.root == '&':
            return first and second
        return first or second

    def quantifier_evaluate(self, formula, assignment):
        """ evaluates formula as quantifier operation """

        def __recover_old_assignment():
            """ Recover old assignment if need to, after went over all assignments """
            if assignment_old_var is not None:
                assignment[formula.variable] = assignment_old_var

        assert is_quantifier(formula.root)

        is_universal_quantifier, is_existential_quantifier = formula.root == 'A', formula.root == 'E'
        assignment_old_var = assignment[formula.variable] if formula.variable in assignment.keys() else None

        for element in self.universe:
            assignment[formula.variable] = element
            eval_predicate = self.evaluate_formula(formula.predicate, assignment)

            if is_existential_quantifier and eval_predicate:
                __recover_old_assignment()
                return True

            if is_universal_quantifier and not eval_predicate:
                __recover_old_assignment()
                return False

        __recover_old_assignment()
        return is_universal_quantifier

    def all_assignments(self, free_vars):
        """ generates all the assignment to the given free vars """
        import itertools
        table = list(itertools.product(list(self.universe), repeat=len(free_vars)))

        for row in table:
            yield {list(free_vars)[k]: row[k] for k in range(len(free_vars))}

    def is_model_of(self, formulae_repr):
        """ Return whether self a model of the formulae represented by the
            given list of strings. For this to be true, each of the formulae
            must be satisfied, if the formula has free variables, then it must
            be satisfied for every assignment of elements of the universe to
            the free variables """
        # Task 7.9
        for formula_rep in formulae_repr:
            formula = Formula.parse(formula_rep)

            for assignment in self.all_assignments(formula.free_variables()):
                if not self.evaluate_formula(formula, assignment):
                    return False
        return True



