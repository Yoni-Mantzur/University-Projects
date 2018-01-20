""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/propositions/semantics_test.py """

from code.propositions.syntax import *
from code.propositions.semantics import *

def test_evaluate(debug=True):
    infix1 = '~(p&q7)'
    models_values1 = [
        ({'p': True,  'q7': False}, True),
        ({'p': False, 'q7': False}, True),
        ({'p': True,  'q7': True},  False)
    ]
    infix2 = '~~~x'
    models_values2 = [
        ({'x': True}, False),
        ({'x': False}, True)
    ]
    for infix,models_values in [[infix1, models_values1],
                                [infix2, models_values2]]:
        formula = Formula.from_infix(infix)
        for model,value in models_values:
            if debug:
                print('Testing evaluation of formula', formula, 'in model',
                      model)
            assert evaluate(formula, model) == value

def test_all_models(debug=False):
    variables1 = ['p', 'q']
    models1 = [{'p': False, 'q': False}, \
               {'p': False, 'q': True},  \
               {'p': True,  'q': False}, \
               {'p': True,  'q': True} ]
    variables2  = ['x']
    models2 = [{'x': False}, {'x': True}]
    for variables,models in [[variables1, models1], [variables2, models2]]:
        if debug:
            print('Testing all models over', variables)
        assert list(all_models(variables)) == models

def test_truth_values(debug=False):
    for infix,variables,values in [
            ['~(p&q7)', ['p', 'q7'], [True, True, True, False]],
            ['(y|~x)',  ['y', 'x'],  [True, False, True, True]],
            ['~~~p',    ['p'],       [True, False]]]:
        formula = Formula.from_infix(infix)
        if debug:
            print('Testing the evaluation of', formula,
                  'on all models over its variables')
        assert truth_values(formula, all_models(variables)) == values

def test_is_tautology(debug=False):
    for infix,tautology in [['~(p&q7)',   False], ['(x|~x)',       True],
                            ['(F|T)',     True],  ['((y1|~y1)&T)', True],
                            ['((T&T)|F)', True],  ['F',            False],
                            ['x',         False], ['~y',           False]]:
        formula = Formula.from_infix(infix)
        if debug:
            print('Testing whether', formula, 'is a tautology')
        assert is_tautology(formula) == tautology



def test_print_truth_table(debug=False):
    infix1 = '~r'
    table1 = '| r | ~r |\n' \
             '|---|----|\n' \
             '| F | T  |\n' \
             '| T | F  |\n'

    infix2 = '~(p&q7)'
    table2 = '| p | q7 | ~(p&q7) |\n' \
             '|---|----|---------|\n' \
             '| F | F  | T       |\n' \
             '| F | T  | T       |\n' \
             '| T | F  | T       |\n' \
             '| T | T  | F       |\n'

    infix3 = '~(q7&p)'
    table3 = '| p | q7 | ~(q7&p) |\n' \
             '|---|----|---------|\n' \
             '| F | F  | T       |\n' \
             '| F | T  | T       |\n' \
             '| T | F  | T       |\n' \
             '| T | T  | F       |\n'

    infix4 = '(x&(~z|y))'
    table4 = '| x | y | z | (x&(~z|y)) |\n' \
             '|---|---|---|------------|\n' \
             '| F | F | F | F          |\n' \
             '| F | F | T | F          |\n' \
             '| F | T | F | F          |\n' \
             '| F | T | T | F          |\n' \
             '| T | F | F | T          |\n' \
             '| T | F | T | F          |\n' \
             '| T | T | F | T          |\n' \
             '| T | T | T | T          |\n'

    __test_print_truth_table([infix1, infix2, infix3, infix4],
                             [table1, table2, table3, table4], debug)

def __test_print_truth_table(infixes, tables, debug):

    from io import StringIO
    import sys

    class PrintCapturer:
        """ A helper class for capturing text printed to the standard output """
        def __enter__(self):
            """ Save the standard output and replace it with a mock """
            self._stdout = sys.stdout
            sys.stdout = self._stringio = StringIO()
            return self
        def __exit__(self, *args):
            """ Store the captured text, and restore the original the standard
                output """
            self.captured = self._stringio.getvalue()
            sys.stdout = self._stdout

    capturer = PrintCapturer()
    for infix,table in zip(infixes, tables):
        formula = Formula.from_infix(infix)
        if debug:
            print('Testing truth table of', formula)
        with capturer as output:
            print_truth_table(formula)
        if debug:
            print ('Printed:\n' + capturer.captured)
            print ('Expected:\n' + table)
        import re
        assert re.sub('[ -]+', ' ', capturer.captured) == \
               re.sub('[ -]+', ' ', table)

def test_synthesize_for_model(debug=False):
    all_models1 = [{'x': False},
                   {'x': True}]
    all_models2 = [{'p': False, 'q': False},
                   {'p': False, 'q': True},
                   {'p': True,  'q': False},
                   {'p': True,  'q': True} ]

    for all_models in [all_models1, all_models2]:
        for idx in range(len(all_models)):
            if debug:
                print('Testing synthesis of formula for model', all_models[idx])
            formula = synthesize_for_model(all_models[idx])
            all_values = [False] * len(all_models)
            all_values[idx] = True
            for model,value in zip(all_models, all_values):
                assert evaluate(formula, model) == value

def test_synthesize(debug=False):
    all_models1 = [{'p': False}, {'p': True}]
    value_lists1 = [[False, False], [False, True], [True, False], [True, True]]

    all_models2 = [{'p': False, 'q': False},
                   {'p': False, 'q': True},
                   {'p': True,  'q': False},
                   {'p': True,  'q': True}]
    value_lists2 = [[True,  False, False, True],
                    [False, False, False, False],
                    [True,  True,  True,  True]]

    for all_models,value_lists in [[all_models1, value_lists1],
                                   [all_models2, value_lists2]]:
        for all_values in value_lists:
            if debug:
                print('Testing synthesis of formula for models', all_models,
                      'with values', all_values)
            formula = synthesize(all_models, all_values)
            for model,value in zip(all_models, all_values):
                assert evaluate(formula, model) == value

def test_evaluate_all_operators(debug=False):
    formula = Formula('<->',
                      Formula('~',
                              Formula('&',
                                      Formula('|', Formula('p1'), Formula('p2')),
                                      Formula('?:', Formula('p3'), Formula('p4'), Formula('p5')))),
                      Formula('->',
                              Formula('-&', Formula('p6'), Formula('p7')),
                              Formula('-|', Formula('p8'), Formula('p9'))))

    model_true = {
        'p1': True, 'p2': False, 'p3': False, 'p4': False, 'p5': True,
        'p6': True, 'p7': False, 'p8': False, 'p9': True}

    model_false = {
        'p1': True, 'p2': False, 'p3': False, 'p4': False, 'p5': True,
        'p6': True, 'p7': True, 'p8': False, 'p9': True}

    if debug:
        print('Testing evaluation of formula', formula, 'in model', model_true)
    assert evaluate(formula, model_true)
    if debug:
        print('Testing evaluation of formula', formula, 'in model', model_false)
    assert not evaluate(formula, model_false)

def test_truth_values_all_operators(debug=False):
    formula = Formula('<->',
                      Formula('~',
                              Formula('?:', Formula('p1'), Formula('p2'), Formula('p3'))),
                      Formula('->',
                              Formula('-&', Formula('p4'), Formula('p5')),
                              Formula('-|', Formula('p6'), Formula('p7'))))
    models = all_models(['p'+str(i) for i in range(1,8)])
    if debug:
        print('Testing the evaluation of', formula,
              'in all models over its variables')
    assert truth_values(formula, models) == [
        True, False, False, False, True, False, False, False,
        True, False, False, False, True, True, True, True,
        False, True, True, True, False, True, True, True,
        False, True, True, True, False, False, False, False,
        True, False, False, False, True, False, False, False,
        True, False, False, False, True, True, True, True,
        False, True, True, True, False, True, True, True,
        False, True, True, True, False, False, False, False,
        True, False, False, False, True, False, False, False,
        True, False, False, False, True, True, True, True,
        True, False, False, False, True, False, False, False,
        True, False, False, False, True, True, True, True,
        False, True, True, True, False, True, True, True,
        False, True, True, True, False, False, False, False,
        False, True, True, True, False, True, True, True,
        False, True, True, True, False, False, False, False]

def test_is_tautology_all_operators(debug=False):
    for infix,tautology in [['(T->z)',                             False],
                            ['(x<->x)',                            True],
                            ['(x->y)',                             False],
                            ['(T?(x|~x):((x->y)->z))',             True],
                            ['(x-&x)',                             False],
                            ['((x-&x)|x)',                         True],
                            ['((x-|x)&T)',                         False],
                            ['~(F-|(~((x<->x)-&(F->y))&(z?T:T)))', True]]:
        formula = Formula.from_infix(infix)
        if debug:
            print('Testing whether', formula, 'is a tautology')
        assert is_tautology(formula) == tautology

def test_print_truth_table_all_operators(debug=False):
    infix1 = '(p?T:q7)'
    table1 = '| p | q7 | (p?T:q7) |\n' \
             '|---|----|----------|\n' \
             '| F | F  | F        |\n' \
             '| F | T  | T        |\n' \
             '| T | F  | T        |\n' \
             '| T | T  | T        |\n'

    infix2 = '((q7->p)?T:p)'
    table2 = '| p | q7 | ((q7->p)?T:p) |\n' \
             '|---|----|---------------|\n' \
             '| F | F  | T             |\n' \
             '| F | T  | F             |\n' \
             '| T | F  | T             |\n' \
             '| T | T  | T             |\n'

    __test_print_truth_table([infix1, infix2], [table1, table2], debug)

def test_evaluate_inference(debug=False):
    from code.propositions.proofs import InferenceRule

    # Test 1
    rule1 = InferenceRule([Formula.from_infix('p'), Formula.from_infix('q')],
                          Formula.from_infix('r'))
    for model in all_models(['p', 'q', 'r']):
        if debug:
            print('Testing evaluation of inference rule', rule1, 'in model',
                  model)
        assert evaluate_inference(rule1, model) == \
               (not model['p']) or (not model['q']) or model['r']

    # Test 2
    rule2 = InferenceRule([Formula.from_infix('(x|y)')],
                          Formula.from_infix('x'))
    for model in all_models(['x', 'y']):
        if debug:
            print('Testing evaluation of inference rule', rule2, 'in model',
                  model)
        assert evaluate_inference(rule2, model) == \
               (not model['y']) or model['x']

    # Test 3
    rule3 = InferenceRule([Formula.from_infix(s) for s in ['(p->q)', '(q->r)']],
                           Formula.from_infix('r'))
    for model in all_models(['p', 'q', 'r']):
        if debug:
            print('Testing evaluation of inference rule', rule3, 'in model',
                  model)
        assert evaluate_inference(rule3, model) == \
               (model['p'] and not model['q']) or \
               (model['q'] and not model['r']) or model['r']

def test_is_tautological_inference(debug=False):
    from code.propositions.proofs import InferenceRule

    for assumptions,conclusion,tautological in [
            [[], '(~p|p)', True],
            [[], '(p|p)', False],
            [[], '(~p|q)', False],
            [['(~p|q)', 'p'], 'q', True],
            [['(p|q)', 'p'], 'q', False],
            [['(p|q)', '(~p|r)'], '(q|r)', True],
            [['(p->q)', '(q->r)'], 'r', False],
            [['(p->q)', '(q->r)'], '(p->r)', True],
            [['(x|y)'], '(y|x)', True],
            [['x'], '(x|y)', True],
            [['(x&y)'], 'x', True],
            [['x'], '(x&y)', False]]:
        rule = InferenceRule(
            [Formula.from_infix(assumption) for assumption in assumptions],
            Formula.from_infix(conclusion))
        if debug:
            print('Testing whether', rule, 'is a tautological inference')
        assert is_tautological_inference(rule) == tautological
