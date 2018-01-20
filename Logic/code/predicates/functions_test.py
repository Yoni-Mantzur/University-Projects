""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/predicates/functions_test.py """

from code.predicates.syntax import *
from code.predicates.semantics import *
from code.predicates.functions import *

def test_replace_functions_with_relations_in_model(debug=True):
    model = Model(
        {'a', 'b'},
        {'a': 'a',
         'GT': {('b','a')}, 'f': {('a',):'b', ('b',):'b'},
         'gg': {('a','a'):'b', ('a','b'):'a', ('b','a'):'a', ('b','b'):'b'}})
    if debug:
        print('Replacing functions with relations in model', model, '...')
    new_model = replace_functions_with_relations_in_model(model)
    if debug:
        print('... got', new_model)
    assert new_model.universe == model.universe
    assert new_model.meaning.keys() == {'a', 'F', 'Gg', 'GT'}
    assert new_model.meaning['a'] == 'a'
    assert new_model.meaning['F'] == {('b','a'), ('b','b')}
    assert new_model.meaning['Gg'] == {('b','a','a'), ('a','a','b'),
                                       ('a','b','a'), ('b','b','b')}
    assert new_model.meaning['GT'] == {('b','a')}
    
def test_replace_relations_with_functions_in_model(debug=True):
    model = Model(
        {'a', 'b'},
        {'a': 'a',
         'GT': {('b','a')}, 'F' :{('b','a'), ('b','b')},
         'GG': {('b','a','a'), ('a','a','b'), ('a','b','a'), ('b','b','b')}})

    if debug:
        print('Replacing relations with functions in model', model, '...')
    new_model = replace_relations_with_functions_in_model(model, {'f', 'gG'})
    if debug:
        print('... got', new_model)
    assert new_model.universe == model.universe
    assert new_model.meaning.keys() == {'a', 'f', 'gG', 'GT'}, new_model.meaning.keys()
    assert new_model.meaning['a'] == 'a'
    assert new_model.meaning['f'] == {('a',):'b', ('b',):'b'}
    assert new_model.meaning['gG'] == {('a','a'):'b', ('a','b'):'a',
                                       ('b','a'):'a', ('b','b'):'b'}
    assert new_model.meaning['GT'] == {('b','a')}

    if debug:
        print('Replacing relations F with functions in model', model, '...')
    new_model = replace_relations_with_functions_in_model(model, {'f'})
    if debug:
        print('... got', new_model)
    assert new_model.universe == model.universe
    assert new_model.meaning.keys() == {'a', 'f', 'GG', 'GT'}
    assert new_model.meaning['a'] == 'a'
    assert new_model.meaning['f'] == {('a',):'b', ('b',):'b'}
    assert new_model.meaning['GG'] == {('b','a','a'), ('a','a','b'),
                                       ('a','b','a'), ('b','b','b')}
    assert new_model.meaning['GT'] == {('b','a')}

    # Test faulty models
    model = Model(
        {'a', 'b'},
        {'a': 'a',
         'GT': {('b','a')}, 'F' :{('b','a'), ('b','b'), ('a','b')},
         'GG': {('b','a','a'), ('a','a','b'), ('a','b','a'), ('b','b','b')}})
    if debug:
        print('Replacing relations with functions in model', model, '...')
    new_model = replace_relations_with_functions_in_model(model, {'f', 'gG'})
    assert new_model == None

    model = Model(
        {'a', 'b'},
        {'a': 'a',
         'GT': {('b','a')}, 'F' :{('b','a'), ('b','b')},
         'GG': {('b','a','a'), ('a','a','b'), ('b','b','b')}})
    if debug:
        print('Replacing relations with functions in model', model, '...')
    new_model = replace_relations_with_functions_in_model(model, {'f', 'gG'})
    assert new_model == None

def test_compile_term(debug=True):
    for s,expected in [
            ['f(x,g(0))', ['z1=g(0)', 'z2=f(x,z1)']],
            ['f(g(x,h(0)),f(f(0,g(y)),h(h(x))))',
             ['z3=h(0)', 'z4=g(x,z3)', 'z5=g(y)', 'z6=f(0,z5)', 'z7=h(x)',
              'z8=h(z7)', 'z9=f(z6,z8)', 'z10=f(z4,z9)']],
            ['f(x,g(0))', ['z11=g(0)', 'z12=f(x,z11)']]]:
        term = Term.parse(s)
        if debug:
            print('Compiling', term, '...')
        steps = compile_term(term)
        if debug:
            print('... got', steps)
        assert steps == [Formula.parse(e) for e in expected]

def test_replace_functions_with_relations_in_formula(debug=True):
    for s,valid_model,invalid_model in [

        ['Ax[(Ey[f(y)=x]->GT(x,a))]',
         Model({'a', 'b'},
               {'a': 'a', 'b': 'b', 'GT': {('b','a')},
                'F': {('b','a'), ('b','b')}, 'G': {('b','a'), ('a','b')}}),
         Model({'a', 'b'},
               {'a': 'a', 'b': 'b', 'GT': {('b','a')},
                'F': {('a','a'), ('b','b')}, 'G': {('b','a'), ('a','b')}})]]:
        formula=Formula.parse(s)
        if debug:
            print('Replacing functions with relations in formula', formula,
                  '...')
        new_formula = replace_functions_with_relations_in_formula(formula)
        if debug:
            print('... got', formula)
        for model,validity in [[valid_model,True], [invalid_model,False]]:
            # Will be tested with the course staff's implementation of
            # is_model_of
            is_valid_model = model.is_model_of({str(new_formula)})
            if debug:
                print('which', 'is' if is_valid_model else 'is not',
                      'satisfied by model', model)
            assert is_valid_model == validity

def test_replace_functions_with_relations_in_formulae(debug=True):
    formula = 'GT(f(a),g(b))'
    if debug:
        print('Removing functions from singleton', formula, '...')
    new_formulae = replace_functions_with_relations_in_formulae([formula])
    if debug:
        print('... got', new_formulae)
    new_formulae = set(new_formulae)

    for model,validity in [
            [Model({'a', 'b'},
                   {'a': 'a', 'b': 'b', 'GT': {('b','a')},
                    'F': {('b','a'), ('b','b')}, 'G': {('b','a'), ('a','b')}}),
             True],
            [Model({'a', 'b'},
                   {'a': 'a', 'b': 'b', 'GT': {('b','a')},
                    'F': {('a','a'), ('b','b')}, 'G': {('b','a'), ('a','b')}}),
             False],
            [Model({'a', 'b'},
                   {'a': 'a', 'b': 'b', 'GT': {('b','a')},
                    'F': {('a','a')}, 'G': {('b','a'), ('a','b')}}),
             False],
            [Model({'a', 'b'},
                   {'a': 'a', 'b': 'b', 'GT': {('b','a')},
                    'F': {('a','a'), ('b','b'), ('b','a')},
                    'G': {('b','a'), ('a','b')}}),
             False],
            [Model({'a', 'b'},
                   {'a': 'a', 'b': 'b', 'GT': {('b','a')},
                    'F': {('a','a'), ('b','b')},
                    'G': {('b','a'), ('a','b'), ('b','b')}}),
             False]]:
        if debug:
            print('which',
                  'is' if model.is_model_of(new_formulae) else 'is not',
                  'satisfied by model', model)
        # Will be tested with the course staff's implementation of is_model_of
        assert model.is_model_of(new_formulae) == validity

def test_replace_equality_with_SAME(debug):
    formula = 'Ax[Ay[Az[((S(x,y)&S(x,z))->y=z)]]]'
    if debug:
        print('Removing equalities from singleton', formula, '...')
    new_formulae = replace_equality_with_SAME([formula])
    if debug:
        print('... got', new_formulae)
    new_formulae = set(new_formulae)
    assert 'Ax[Ay[Az[((S(x,y)&S(x,z))->SAME(y,z))]]]' in new_formulae

    for model,validity in [
            [Model({'0', '1', '2'},
                   {'S': {},
                    'SAME': {('0','0'), ('1','1'), ('2','2'), ('0','1')}}),
             False],
            [Model({'0', '1', '2'},
                   {'S': {}, 'SAME': {('0','0'), ('1','1')}}),
             False],
            [Model({'0', '1', '2'},
                   {'S': {}, 'SAME': {('0','0'), ('1','1'), ('2','2')}}),
             True],
            [Model({'0','1','2'},
                   {'S': {('0','1'), ('0','2')},
                    'SAME': {('0','0'), ('1','1'), ('2','2')}}),
             False],
            [Model({'0', '1', '2'},
                   {'S': {('0','1'),('0','2')},
                    'SAME': {('0','0'), ('1','1'), ('2','2'), ('1','2'),
                             ('2','1')}}),
             True],
            [Model({'0', '1', '2'},
                   {'S': {('0','1')},
                    'SAME': {('0','0'), ('1','1'), ('2','2'), ('1','2'),
                             ('2','1')}}),
             False]]:
        if debug:
            print('which',
                  'is' if model.is_model_of(new_formulae) else 'is not',
                  'satisfied by model', model)
        # Will be tested with the course staff's implementation of is_model_of
        assert model.is_model_of(new_formulae) == validity
  
def test_add_SAME_as_equality(debug):
    model = Model({'0', '1', '2'}, {'a': '0', 'Q': {('1')}})
    if debug:
        print('Adding SAME to model', model, '...')
    new_model = add_SAME_as_equality(model)
    if debug:
        print('... got', new_model)
    assert new_model.universe == model.universe
    assert new_model.meaning.keys() == {'a', 'Q', 'SAME'}
    assert new_model.meaning['a'] == model.meaning['a']
    assert new_model.meaning['Q'] == model.meaning['Q']
    assert new_model.meaning['SAME'] == {('0','0'), ('1','1'), ('2','2')}

def test_make_equality_as_SAME(debug):
    model = Model({'0', '1', '2'},
                  {'SAME': {('0','0'), ('1','1'), ('2','2'), ('1','2'),
                            ('2','1')},
                   'a': '0', 'b': '1', 'c': '2',
                   'Q': {('0',), ('1',), ('2',)}})
    if debug:
        print('Making equality as SAME in model', model)
    new_model = make_equality_as_SAME(model)
    if debug:
        print('... got', new_model)
    assert len(new_model.universe)==2
    assert new_model.meaning.keys() == {'a', 'b', 'c', 'Q'}
    assert new_model.meaning['b'] == new_model.meaning['c']
    assert new_model.meaning['a'] != new_model.meaning['b']
    for x in new_model.universe:
        assert (x,) in new_model.meaning['Q']
    assert len(new_model.meaning['Q']) == 2
