""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/propositions/operators_test.py """

from code.propositions.syntax import *
from code.propositions.semantics import *
from code.propositions.operators import *

# Tests for to_*** methods

def test_to_not_and_or(debug=False):
    __test_to(to_not_and_or, ['~', '&', '|', 'T', 'F'], debug)

def test_to_not_and(debug=False):
    __test_to(to_not_and, ['~', '&'], debug)

def test_to_implies_false(debug=False):
    __test_to(to_implies_false, ['->', 'F'], debug)

def test_to_nand(debug=False):
    __test_to(to_nand, ['-&'], debug)

def test_to_nor(debug=False):
    __test_to(to_nor, ['-|'], debug)

def test_to_mux(debug=False):
    __test_to(to_mux, ['?:', 'F', 'T'], debug)
    for infix in ['p', '~p', '(p&q)', '(p|q)', '(p->q)', '(p?q:r)']:
        if debug:
            print('Testing number of operators in reduction of', infix);
        formula = Formula.from_infix(infix)
        assert __count_operators(to_mux(formula)) <= __count_operators(formula)

def __test_to(reducer, allowed_tokens, debug):
    if debug:
        print('Testing reduction function' + reducer.__qualname__ + ':')

    # Thoroughly test reduction of single-operator formulae.
    for infix in ['p', '~p', '(p&q)', '(p|q)', '(p->q)', '(p<->q)', '(p-&q)',
                  '(p-|q)', '(p?q:r)']:
        if debug:
            print('Testing reduction of', infix);
        formula = Formula.from_infix(infix)
        reduced = reducer(formula)
        variables = list(formula.variables())
        __test_only_contains(reduced, allowed_tokens + variables, debug)
        models = list(all_models(variables)) 
        assert truth_values(formula, models) == truth_values(reduced, models)

    # A long formula at a truth model and a false model
    formula = Formula('<->',
                      Formula('~',
                              Formula('&',
                                      Formula('|',
                                              Formula('p1'),
                                              Formula('p2')),
                                      Formula('?:',
                                              Formula('p3'),
                                              Formula('p4'),
                                              Formula('p5')))),
                      Formula('->',
                              Formula('-&', Formula('p6'), Formula('p7')),
                              Formula('-|', Formula('p8'), Formula('p9'))))
    model_true = {'p1': True, 'p2': False, 'p3': False, 'p4': False,
                  'p5': True, 'p6': True, 'p7': False, 'p8': False, 'p9': True}
    model_false = {'p1': True, 'p2': False, 'p3': False, 'p4': False,
                   'p5': True, 'p6': True, 'p7': True, 'p8': False, 'p9': True}

    # Duplicate to have 18 variables
    formula = Formula.from_prefix(
        '&~~' + formula.prefix() + formula.prefix().replace('p', 'q'))
    # Duplicate to have 36 variables
    formula = Formula.from_prefix(
        '|~~' + formula.prefix() +
        formula.prefix().replace('p', 'r').replace('q', 's'))
    # Duplicate to have 72 variables
    formula = Formula.from_prefix(
        '&' + formula.prefix() +
        formula.prefix().replace('p', 't').replace('q', 'u')
                        .replace('r', 'v').replace('s', 'w'))
    # Adjust models to duplicated variables
    model_true = {var + str(i): model_true['p' + str(i)]
                  for var in ['p', 'q', 'r', 's', 't', 'u', 'v', 'w']
                  for i in range(1, 10)}
    model_false = {var + str(i): model_false['p' + str(i)]
                   for var in ['p','q','r','s','t','u','v','w']
                   for i in range(1, 10)}
    # Test at a truth model and at a false model
    if debug:
        print('Testing reduction of formula with 72 variables')
    reduced = reducer(formula)
    __test_only_contains(reduced, allowed_tokens + list(formula.variables()),
                         debug)
    assert evaluate(reduced, model_true)
    assert not evaluate(reduced, model_false)

# Tests for synthesize_*** methods

def test_synthesize_not_and(debug=False):
    __test_synthesize(synthesize_not_and, ['~', '&'], debug)

def test_synthesize_implies_false(debug=False):
    __test_synthesize(synthesize_implies_false, ['->', 'F'], debug)

def test_synthesize_nand(debug=False):
    __test_synthesize(synthesize_nand, ['-&'], debug)

def test_synthesize_nor(debug=False):
    __test_synthesize(synthesize_nor, ['-|'], debug)

def test_synthesize_mux(debug=False):
    __test_synthesize(synthesize_mux, ['?:', 'F', 'T'], debug, True)

def __test_synthesize(synthesizer, allowed_tokens, debug, count=False):
    if debug:
        print('Testing synthesis function ' + synthesizer.__qualname__ + ':')
    max_variables = 3
    for num_variables in range(1, max_variables + 1):
        variables = ['p' + str(i) for i in range(1, num_variables + 1)]
        models = list(all_models(variables))
        from itertools import product
        for values in product([False, True], repeat=2**num_variables):
            if debug:
                print('Testing synthesis for values', values);
            formula = synthesizer(models, values)
            __test_only_contains(formula, allowed_tokens + variables, debug)
            assert truth_values(formula, models) == list(values)
            if count:
                with_not_and_or = synthesize(models, values)
                assert __count_operators(formula) <= \
                       __count_operators(with_not_and_or)

#

def __test_only_contains(formula, tokens, debug=False):
    assert formula.root in tokens
    for attr in ('first', 'second', 'third'):
        if hasattr(formula, attr):
            __test_only_contains(getattr(formula, attr), tokens)   

def __count_operators(formula):
    if not hasattr(formula, 'first'):
        return 0
    else:
        from functools import reduce
        from operator import add
        return 1 + reduce(add, [__count_operators(getattr(formula, attr))
                                for attr in ('first', 'second', 'third')
                                if hasattr(formula, attr)])
