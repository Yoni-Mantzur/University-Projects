""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/propositions/semantics.py """

from code.propositions.syntax import *


def evaluate(formula, model):
    """ Return the truth value of the given formula in the given model """

    if is_constant(formula.root):
        return True if formula.root == 'T' else False

    if is_variable(formula.root):
        return model.get(formula.root)

    eval_first = evaluate(formula.first, model)
    if is_unary(formula.root):
        return not eval_first

    eval_sec = evaluate(formula.second, model)
    if is_binary(formula.root):
        if formula.root == '|':
            return eval_first or eval_sec
        if formula.root == '&':
            return eval_first and eval_sec
        if formula.root == '->':
            return not eval_first or (eval_first and eval_sec)
        if formula.root == '-&':
            return not(eval_first and eval_sec)
        if formula.root == '-|':
            return not(eval_first or eval_sec)
        if formula.root == '<->':
            return (eval_first and eval_sec) or (not eval_first and not eval_sec)

    eval_third = evaluate(formula.third, model)
    return eval_sec if eval_first else eval_third



def all_models(variables):
    """ Return an iterator over all possible models over the variables in the
        given list of variables. The order of the models is lexicographic
        according to the order of the variables in the given list, where False
        precedes True """

    import itertools
    table = list(itertools.product([False, True], repeat=len(variables)))
    variables.sort()
    for row in table:
        yield {variables[k]: row[k] for k in range(len(variables))}


def truth_values(formula, models):
    """ Return a list of the truth values of the given formula in each model
        in the given list of models """
    evaluations = []
    for model in models:
        evaluations.append(evaluate(formula, model))

    return evaluations



def is_tautology(formula):
    """ Return whether the given formula is a tautology """
    models = all_models(list(formula.variables()))
    truth_vals = truth_values(formula, models)
    return all(truth_val for truth_val in truth_vals)


def print_var(var):
    print(" " + var + " |", end='')
    return len(var)


def print_formula(formula):
    print(" " + formula.infix() + " |")
    return len(formula.infix())


def print_first_row(vars, formula):
    print('|', end='')
    gaps = []
    for var in vars:
        gaps.append(print_var(var))
    gaps.append(print_formula(formula))
    return gaps


def print_second_row(gaps):
    print("|", end='')
    for gap in gaps:
        for i in range(gap+2): print('-', end='')
        print("|", end='')
    print('')


def print_models(gaps, models, formula, vars):
    k = 0
    for model in models:
        truth_vals = [model[var] for var in vars] + [evaluate(formula, model)]
        print('|', end='')
        for i in range(len(truth_vals)):
            print(" " + ('T' if truth_vals[i] else 'F'), end='')
            for k in range(gaps[i]): print(' ', end='')
            if i < len(truth_vals)-1:
                print('|', end='')
            else:
                print('|')
        k += 1


def print_truth_table(formula):
    """ Print the truth table of the given formula """
    vars = list(formula.variables())
    vars.sort()
    gaps = print_first_row(vars, formula)  # gaps means the size of each cell in column
    print_second_row(gaps)
    print_models(gaps, all_models(vars), formula, vars)

def synthesize_for_model(model):
    """ Return a propositional formula that evaluates to True in the given
        model, and to False in any other model over the same variables """
    list_model = list(model.items())
    param = list_model[0][0]
    f = Formula(param) if list_model[0][1] else Formula('~', Formula(param))
    if len(model) == 1:
        return f
    for i in range(1, len(list_model)):
        param = list_model[i][0]
        f = Formula('&', f, Formula(param) if list_model[i][1] else Formula('~', Formula(param)))

    return f


def find_first_true_row(models, values):
    for i in range(len(values)):
        if values[i]:
            return synthesize_for_model(models[i])
    return None


def contradiction(model):
    list_model = list(model.items())
    param = list_model[0][0]
    return Formula('&', Formula(param), Formula('~', Formula(param)))


def synthesize(models, values):
    """ Return a propositional formula that has the given list of respective
        truth values in the given list of models """
    f = find_first_true_row(models, values)
    if f is None:
        return contradiction(models[0])  # all values are false, means contradiction
    for i in range(1, len(models)):
        if values[i]:
            f = Formula('|', f, synthesize_for_model(models[i]))
    return f

def evaluate_inference(rule, model):
    """ Return whether the given inference rule holds in the given model """
    def eval_assumption():
        for assumption in rule.assumptions:
            if not evaluate(assumption, model):
                return False
        return True

    return evaluate(rule.conclusion, model) if eval_assumption() else True

def is_tautological_inference(rule):
    """ Return whether the given inference rule is a semantically correct
        implication of its assumptions """

    for model in all_models(list(rule.variables())):
        if not evaluate_inference(rule, model):
            return False

    return True
