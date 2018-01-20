""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/predicates/semantics_test.py """

from code.predicates.syntax import *
from code.predicates.semantics import *

def test_evaluate_term(debug=True):
    model = Model({'0', '1'},
                  {'plus': {('0', '0'): '0', ('0', '1'): '1', ('1', '1'): '0',
                            ('1', '0'): '1'},
                   'c': '1'})
    if debug:
        print('In the model', model)
    for s,expected_value in [['c', '1'], ['plus(c,c)', '0'],
                             ['plus(c,plus(c,c))', '1']]:
        term = Term.parse(s)
        value = model.evaluate_term(term)
        if debug:
            print('The value of', term, 'is', value)
        assert value == expected_value

    assignment = {'x': '1', 'y': '0'}
    for s,expected_value in [['x', '1'], ['plus(x,c)', '0'],
                             ['plus(x,y)', '1']]:
        term = Term.parse(s)
        value = model.evaluate_term(term, assignment)
        if debug:
            print('The value of', term, 'with assignment x=1 y=0 is', value)
        assert value == expected_value

def test_evaluate_formula(debug=True):
    model = Model({'0', '1', '2'},
                  {'0': '0',
                   'Pz': {('0',)},
                   'p1': {('0',): '1', ('1',): '2', ('2',): '0'}})
    if debug:
        print('In the model', model)
    for s,assignment,expected_value in [
            ('Pz(0)',{},True), ('0=p1(0)', {}, False),
            ('Pz(p1(x))', {'x': '2'}, True), ('(p1(0)=0|0=p1(0))', {}, False),
            ('Ax[Ey[p1(y)=x]]', {}, True)]:
        formula = Formula.parse(s)
        value = model.evaluate_formula(formula, assignment)
        if debug:
            print('The value of', formula, 'with assignment', assignment, 'is',
                  value)
        assert value == expected_value

def test_is_model_of(debug=True):
    pairs = {('a', 'a'), ('a', 'b'), ('b', 'a')}
    model = Model({'a', 'b'}, {'Friends': pairs, 'bob': 'a'})
    f1 = 'Friends(bob,y)'
    f2 = 'Friends(x,bob)'
    f3 = 'Friends(x,y)'
    if debug:
        print('The model', model, '...')
    for formulas,expected_result in [
            ([f1], True), ([f2],True), ([f1, f2], True), ([f3], False),
            ([f1,f2,f3], False)]:
        result = model.is_model_of(formulas)
        if debug:
            print('... is said', '' if result else 'not', 'to satisfy',
                  formulas)
        assert result == expected_result
    formula = '(F(z,a)->z=b)'
    model = Model({'a', 'b'},
                  {'a': 'a', 'b': 'b', 'F': {('a', 'a'), ('b', 'b')}})
    if debug:
        print('The model', model, '...')
    result = model.is_model_of([formula])
    if debug:
        print('... is said', '' if result else 'not', 'to satisfy', formula)
    assert not result
