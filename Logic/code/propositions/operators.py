""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/propositions/operators.py """

from code.propositions.syntax import *
from code.propositions.semantics import *

def to_not_and_or(formula):
    """ Return an equivalent formula that has no operators beyond not, and, and
        or """
    if is_variable(formula.root) or is_constant(formula.root):
        return Formula(formula.root)

    first = to_not_and_or(formula.first)
    if is_unary(formula.root):
        return neg_formula(first)

    second = to_not_and_or(formula.second)
    if is_binary(formula.root):
        if formula.root == '->':
            return conditional_to_not_and_or(first, second)
        if formula.root == '<->':

            return Formula('&', conditional_to_not_and_or(first, second),
                           conditional_to_not_and_or(second, first))
        if formula.root == '-|':
            return neg_formula(Formula('|', first, second))
        if formula.root == '-&':
            return neg_formula(Formula('&', first, second))
        else:
            return Formula(formula.root, first, second)
    else:
        third = to_not_and_or(formula.third)
        return Formula('|', Formula('&', first, second), Formula('&', neg_formula(first), third))

def conditional_to_not_and_or(A, B):
    return Formula('|', neg_formula(A), B)

def conditional_to_not_and(A, B):
    return neg_formula(Formula('&', A, neg_formula(B)))

def neg_formula(f):
    return Formula('~', f)

def to_not_and(formula):
    """ Return an equivalent formula that has no operators beyond not and and,
        and has no constants """
    if is_variable(formula.root) or is_constant(formula.root):
        return Formula(formula.root)

    first = to_not_and(formula.first)
    if is_unary(formula.root):
        return neg_formula(first)

    second = to_not_and(formula.second)
    if is_binary(formula.root):
        if formula.root == '->':
            return conditional_to_not_and(first, second)
        if formula.root == '<->':
            return Formula('&', conditional_to_not_and(first, second),
                           conditional_to_not_and(second, first))
        if formula.root == '-|':
            return neg_formula(neg_formula(Formula('&', neg_formula(first), neg_formula(second))))
        if formula.root == '-&':
            return neg_formula(Formula('&', first, second))
        if formula.root == '|':
            return neg_formula(Formula('&', neg_formula(first), neg_formula(second)))
        else:
            return Formula(formula.root, first, second)
    else:
        third = to_not_and_or(formula.third)
        return neg_formula(Formula('&', neg_formula(Formula('&', first, second)),
                                   neg_formula(Formula('&', neg_formula(first), third))))

def synthesize_not_and(models, values):
    """ Return a propositional formula that has the given list of respective
        truth values in the given list of models, has no operators beyond not
        and and, and has no constants """
    return to_not_and(synthesize(models, values))


def neg_formula_with_implies_false(f):
    return Formula('->', f, Formula('F'))


def to_implies_false(formula):
    """ Return an equivalent formula that has no operators beyond implies, and
        has no constants beyond false """
    if is_variable(formula.root) or is_constant(formula.root):
        return Formula(formula.root)

    first = to_implies_false(formula.first)
    if is_unary(formula.root):
        return neg_formula_with_implies_false(first)

    second = to_implies_false(formula.second)
    if is_binary(formula.root):
        if formula.root == '<->':
            return and_with_implies_false(Formula('->', first, second), Formula('->', second, first))
        if formula.root == '&':
            return and_with_implies_false(first, second)
        if formula.root == '|':
            return or_with_implies_false(first, second)
        if formula.root == '-|':
            return neg_formula_with_implies_false(or_with_implies_false(first, second))
        if formula.root == '-&':
            return neg_formula_with_implies_false(and_with_implies_false(first, second))
        else:
            return Formula(formula.root, first, second)
    else:
        third = to_implies_false(formula.third)
        return or_with_implies_false(and_with_implies_false(first, second),
                                     and_with_implies_false(neg_formula_with_implies_false(first), third))


def or_with_implies_false(first, second):
    return Formula('->', neg_formula_with_implies_false(first),
                   Formula('->', neg_formula_with_implies_false(second), Formula('F')))


def and_with_implies_false(first, second):
    return neg_formula_with_implies_false(Formula('->', first, Formula('->', second, Formula('F'))))


def synthesize_implies_false(models, values):
    """ Return a propositional formula that has the given list of respective
        truth values in the given list of models, has no operators beyond
        implies, and has no constants beyond false """
    return to_implies_false(synthesize(models, values))


def to_nand(formula):
    """ Return an equivalent formula that has no operators beyond nand, and has
        no constants """
    return to_func(formula, neg_to_nand, or_to_nand, and_to_nand, false_to_nand, true_to_nand)


def or_to_nand(first, second, some_var):
    return Formula('-&', neg_to_nand(first, some_var), neg_to_nand(second, some_var))


def and_to_nand(first, second, some_var):
    return neg_to_nand(Formula('-&', first, second), some_var)

def true_to_nand(some_var):
    return Formula('-&', Formula(some_var), Formula('-&', Formula(some_var), Formula(some_var)))

def false_to_nand(some_var):
    return neg_to_nand(true_to_nand(some_var), some_var)

def neg_to_nand(first, some_var):
    return Formula('-&', first, true_to_nand(some_var))


def synthesize_nand(models, values):
    """ Return a propositional formula that has the given list of respective
        truth values in the given list of models, has no operators beyond nand,
        and has no constants """
    return to_nand(synthesize(models, values))


def false_to_nor(var):
    return Formula('-|', Formula(var), Formula('-|', Formula(var), Formula(var)))

def true_to_nor(var):
    return neg_to_nor(false_to_nor(var), var)

def neg_to_nor(first, var):
    return Formula('-|', first, false_to_nor(var))


def or_to_nor(first, second, var):
    return neg_to_nor(Formula('-|', first, second), var)


def and_to_nor(first, second, var):
    return Formula('-|', neg_to_nor(first, var), neg_to_nor(second, var))


def to_func(formula, neg_to, or_to, and_to, false_to, true_to):
    var = formula.variables().pop()

    def to_func_helper(formula):
        if is_variable(formula.root):
            return Formula(formula.root)

        if is_constant(formula.root):
            return false_to(var) if formula.root == 'F' else true_to(var)
        first = to_func_helper(formula.first)
        if is_unary(formula.root):
            return neg_to(first, var)

        second = to_func_helper(formula.second)
        if is_binary(formula.root):
            if formula.root == '->':
                return or_to(neg_to(first, var), second, var)
            if formula.root == '<->':
                return and_to(or_to(neg_to(first, var), second, var),
                                   or_to(neg_to(second, var), first, var), var)
            if formula.root == '&':
                return and_to(first, second, var)
            if formula.root == '|':
                return or_to(first, second, var)
            if formula.root == '-|':
                return neg_to(or_to(first, second, var), var)
            else:
                return neg_to(and_to(first, second, var), var)
        else:
            third = to_func_helper(formula.third)
            return or_to(and_to(first, second, var), and_to(neg_to(first, var), third, var), var)

    return to_func_helper(formula)

def to_nor(formula):
    """ Return an equivalent formula that has no operators beyond nor, and has
        no constants """
    return to_func(formula, neg_to_nor, or_to_nor, and_to_nor, false_to_nor, true_to_nor)

def synthesize_nor(models, values):
    """ Return a propositional formula that has the given list of respective
        truth values in the given list of models, has no operators beyond nor,
        and has no constants """
    return to_nor(synthesize(models, values))


def to_mux(formula):
    """ Return an equivalent formula that has no operators beyond mux """

    if is_variable(formula.root) or is_constant(formula.root):
        return Formula(formula.root)

    first = to_mux(formula.first)
    if is_unary(formula.root):
        return neg_to_mux(first)

    second = to_mux(formula.second)
    if is_binary(formula.root):
        if formula.root == '->':
            return Formula('?:', first, second, Formula('T'))
        if formula.root == '<->':
            return Formula('?:', first, second, neg_to_mux(second))
        if formula.root == '&':
            return Formula('?:', first, second, Formula('F'))
        if formula.root == '|':
            return Formula('?:', first, Formula('T'), second)
        if formula.root == '-|':
            return Formula('?:', first, Formula('F'), neg_to_mux(second))
        else:
            return Formula('?:', first, neg_to_mux(second), Formula('T'))
    else:
        third = to_mux(formula.third)
        return Formula(formula.root, first, second, third)

def neg_to_mux(first):
    return Formula('?:', first, Formula('F'), Formula('T'))


def synthesize_mux(models, values):
    """ Return a propositional formula that has the given list of respective
        truth values in the given list of models, has no operators beyond
        mux """
    return to_mux(synthesize(models, values))
