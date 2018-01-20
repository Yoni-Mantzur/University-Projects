""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/predicates/completeness_test.py """

from code.propositions.semantics import is_tautology
from code.predicates.syntax import *
from code.predicates.semantics import *
from code.predicates.completeness import *

# Tests for is_***_closed functions

def test_is_primitively_closed(debug=True):
    _test_is_closed(test_primitively=True,debug=debug)
    
def test_is_universally_closed(debug=True):
    _test_is_closed(test_universally=True,debug=debug)

def test_is_existentially_closed(debug=True):
    _test_is_closed(test_existentially=True,debug=debug)

def _test_is_closed(test_primitively=False, test_universally=False,
                    test_existentially=False, debug=False):
    def _test_closures(sentences_str, primitively, universally, existentially):
        sentences = {Formula.parse(sentence) for sentence in sentences_str}
        constants = SIX_ELEMENTS
        if test_primitively:
            assert is_primitively_closed(sentences, constants) == primitively
        if test_universally:
                assert is_universally_closed(sentences, constants) == universally
        if test_existentially:
            assert is_existentially_closed(sentences, constants) == existentially

    for six_element_group_primitives in [
            SIX_ELEMENT_COMMUTATIVE_GROUP_PRIMITIVES,
            SIX_ELEMENT_NON_COMMUTATIVE_GROUP_PRIMITIVES]:
        if debug:
            print('Testing is_closed for the six-element',
                  'non-commutative'
                  if six_element_group_primitives ==
                     SIX_ELEMENT_NON_COMMUTATIVE_GROUP_PRIMITIVES
                  else 'commutative',
                  'group...')
        if debug:
            print('Testing on primitives')
        _test_closures(six_element_group_primitives, True, True, True)
        
        if debug:
            print('Testing on primitives + zero axiom')
        _test_closures(six_element_group_primitives.union({ZERO_AXIOM}),
                       True, True, True)
        if debug:
            print('Testing on primitives + zero axiom + commutativity')
        _test_closures(six_element_group_primitives.union(
                           {ZERO_AXIOM, COMMUTATIVITY_AXIOM},
                           SIX_ELEMENT_COMMUTATIVITY_CLOSURE),
                       True, True, True)
        if debug:
            print('Testing on primitives + negation closure')
        _test_closures(six_element_group_primitives.union(
                           SIX_ELEMENT_NEGATION_CLOSURE),
                       True, True, True)
        if debug:
            print('Testing on primitives + negation')
        _test_closures(six_element_group_primitives.union(
                           {NEGATION_AXIOM}, SIX_ELEMENT_NEGATION_CLOSURE),
                       True, True, True)
        if debug:
            print('Testing on primitives + non-commutativity closure')
        _test_closures(six_element_group_primitives.union(
                           SIX_ELEMENT_NON_COMMUTATIVE_GROUP_NON_COMMUTATIVITY_CLOSURE),
                       True, True, True)
        if debug:
            print('Testing on primitives + non-commutativity')
        _test_closures(six_element_group_primitives.union(
                           {NON_COMMUTATIVITY},
                           SIX_ELEMENT_NON_COMMUTATIVE_GROUP_NON_COMMUTATIVITY_CLOSURE),
                       True, True, True)
        if debug:
            print('Testing on primitives + zero axiom + negation + '
                  'commutativity + non-commutativity')
        _test_closures(six_element_group_primitives.union(
                           {ZERO_AXIOM, NEGATION_AXIOM, COMMUTATIVITY_AXIOM,
                            NON_COMMUTATIVITY},
                           SIX_ELEMENT_NEGATION_CLOSURE,
                           SIX_ELEMENT_COMMUTATIVITY_CLOSURE,
                           SIX_ELEMENT_NON_COMMUTATIVE_GROUP_NON_COMMUTATIVITY_CLOSURE),
                       True, True, True)

    for six_element_group_primitives in [
            SIX_ELEMENT_COMMUTATIVE_GROUP_PRIMITIVES,
            SIX_ELEMENT_NON_COMMUTATIVE_GROUP_PRIMITIVES]:
        if debug:
            print('Testing is_closed for the six-element',
                  'non-commutative'
                  if six_element_group_primitives ==
                     SIX_ELEMENT_NON_COMMUTATIVE_GROUP_PRIMITIVES
                  else 'commutative',
                  'group...')
        if debug:
            print('Testing on closed except primitively')
        _test_closures(six_element_group_primitives.difference(
                           {'~Plus(4,3,5)'}),
                       False, True, True)
        _test_closures(six_element_group_primitives.difference(
                           {'Plus(2,3,5)', 'Plus(1,3,5)'}),
                       False, True, True)
        if debug:
            print('Testing on closed except universally')
        _test_closures(six_element_group_primitives.difference(
                           {'Plus(3,0,3)'}).union(
                           {'~Plus(3,0,3)'},
                           {ZERO_AXIOM}),
                       True, False, True)
        _test_closures(six_element_group_primitives.union(
                           {ZERO_AXIOM, NEGATION_AXIOM, COMMUTATIVITY_AXIOM},
                           SIX_ELEMENT_NEGATION_CLOSURE,
                           SIX_ELEMENT_COMMUTATIVITY_CLOSURE.difference(
                               {'Ay[Az[(Plus(z,2,y)->Plus(z,y,2))]]'})),
                       True, False, True)
        _test_closures(six_element_group_primitives.union(
                           {ZERO_AXIOM, NEGATION_AXIOM, COMMUTATIVITY_AXIOM},
                           SIX_ELEMENT_NEGATION_CLOSURE,
                           SIX_ELEMENT_COMMUTATIVITY_CLOSURE.difference(
                               {'Az[(Plus(z,5,4)->Plus(z,4,5))]'})),
                       True, False, True)
        _test_closures(six_element_group_primitives.union(
                           {ZERO_AXIOM, NEGATION_AXIOM, COMMUTATIVITY_AXIOM},
                           SIX_ELEMENT_NEGATION_CLOSURE,
                           SIX_ELEMENT_COMMUTATIVITY_CLOSURE.difference(
                               {'(Plus(4,3,1)->Plus(4,1,3))'})),
                       True, False, True)
        _test_closures(six_element_group_primitives.union(
                           {ZERO_AXIOM, NEGATION_AXIOM, COMMUTATIVITY_AXIOM},
                           SIX_ELEMENT_NEGATION_CLOSURE.difference(
                               {'Ey[Plus(0,y,3)]'}),
                           SIX_ELEMENT_COMMUTATIVITY_CLOSURE),
                       True, False, True)
        if debug:
            print('Testing on closed except existentially')
        _test_closures(six_element_group_primitives.difference(
                           {'Plus(0,4,2)','Plus(0,4,5)'}).union(
                           {'~Plus(0,4,2)', '~Plus(0,4,5)'},
                           SIX_ELEMENT_NEGATION_CLOSURE),
                       True, True, False)
        _test_closures(six_element_group_primitives.union(
                           {ZERO_AXIOM, NEGATION_AXIOM, NON_COMMUTATIVITY},
                           SIX_ELEMENT_NEGATION_CLOSURE,
                           SIX_ELEMENT_NON_COMMUTATIVE_GROUP_NON_COMMUTATIVITY_CLOSURE.difference(
                               {'Ey[Ez[(Plus(z,1,y)&~Plus(z,y,1))]]'})),
                       True, True, False)
        _test_closures(six_element_group_primitives.union(
                           {ZERO_AXIOM, NEGATION_AXIOM, NON_COMMUTATIVITY},
                           SIX_ELEMENT_NEGATION_CLOSURE,
                           SIX_ELEMENT_NON_COMMUTATIVE_GROUP_NON_COMMUTATIVITY_CLOSURE.difference(
                               {'Ez[(Plus(z,1,2)&~Plus(z,2,1))]'})),
                       True, True, False)
        _test_closures(six_element_group_primitives.union(
                           {ZERO_AXIOM, NEGATION_AXIOM, NON_COMMUTATIVITY},
                           SIX_ELEMENT_NEGATION_CLOSURE,
                           SIX_ELEMENT_NON_COMMUTATIVE_GROUP_NON_COMMUTATIVITY_CLOSURE.difference(
                               {'(Plus(5,1,2)&~Plus(5,2,1))'})),
                       True, True, False)

def test_find_unsatisfied_quantifier_free_sentence(debug=True):
    class non_iterable_set:
        def __init__(self, set_):
            self._contains = lambda x:x in set_
        def __contains__(self, a):
            return self._contains(a)

    assert SIX_ELEMENT_NON_COMMUTATIVE_GROUP_MODEL.is_model_of(
        SIX_ELEMENT_NON_COMMUTATIVE_GROUP_PRIMITIVES)
    sentences = {Formula.parse(sentence) for sentence in
                 SIX_ELEMENT_NON_COMMUTATIVE_GROUP_PRIMITIVES.union(
                     {COMMUTATIVITY_AXIOM},
                     SIX_ELEMENT_COMMUTATIVITY_CLOSURE)}
    assert is_closed(sentences, SIX_ELEMENTS)
    if debug:
        print('Testing find_unsatisfied_quantifier_free_sentence for the '
              'six-element non-commutative group and the commutativity axiom')
    quantifier_free = find_unsatisfied_quantifier_free_sentence(
        non_iterable_set(sentences), SIX_ELEMENTS,
        SIX_ELEMENT_NON_COMMUTATIVE_GROUP_MODEL,
        Formula.parse(COMMUTATIVITY_AXIOM))
    # Will be tested with the course staff's implementation of is_quantifier_free
    assert is_quantifier_free(quantifier_free)
    assert quantifier_free in sentences
    # Will be tested with the course staff's implementation of evaluate_formula
    assert not SIX_ELEMENT_NON_COMMUTATIVE_GROUP_MODEL.evaluate_formula(
        quantifier_free)

    assert SIX_ELEMENT_COMMUTATIVE_GROUP_MODEL.is_model_of(
        SIX_ELEMENT_COMMUTATIVE_GROUP_PRIMITIVES)
    sentences = {Formula.parse(sentence) for sentence in
                 SIX_ELEMENT_COMMUTATIVE_GROUP_PRIMITIVES.union(
                     {NON_COMMUTATIVITY},
                     SIX_ELEMENT_NON_COMMUTATIVE_GROUP_NON_COMMUTATIVITY_CLOSURE)}
    assert is_closed(sentences, SIX_ELEMENTS)
    if debug:
        print('Testing find_unsatisfied_quantifier_free_sentence for the '
              'six-element commutative group and the non-commutativity axiom')
    quantifier_free = find_unsatisfied_quantifier_free_sentence(
        non_iterable_set(sentences), SIX_ELEMENTS,
        SIX_ELEMENT_COMMUTATIVE_GROUP_MODEL,
        Formula.parse(NON_COMMUTATIVITY))
    # Will be tested with the course staff's implementation of is_quantifier_free
    assert is_quantifier_free(quantifier_free)
    assert quantifier_free in sentences
    assert not is_quantifier(quantifier_free.root)
    # Will be tested with the course staff's implementation of evaluate_formula
    assert not SIX_ELEMENT_COMMUTATIVE_GROUP_MODEL.evaluate_formula(
        quantifier_free)

def test_model_or_inconsistent(debug=True):
    for six_element_group_primitives in [
            SIX_ELEMENT_COMMUTATIVE_GROUP_PRIMITIVES,
            SIX_ELEMENT_NON_COMMUTATIVE_GROUP_PRIMITIVES]:
        for commutativity in [
            {COMMUTATIVITY_AXIOM}.union(SIX_ELEMENT_COMMUTATIVITY_CLOSURE),
            {NON_COMMUTATIVITY}.union(SIX_ELEMENT_NON_COMMUTATIVE_GROUP_NON_COMMUTATIVITY_CLOSURE)]:
            sentences = {Formula.parse(sentence) for sentence in
                         six_element_group_primitives.union(
                             {ZERO_AXIOM,
                              NEGATION_AXIOM},
                             SIX_ELEMENT_NEGATION_CLOSURE,
                             commutativity)}
            if (debug):
                print('Testing model_or_inconsistent for the six-element',
                      'non-commutative'
                      if six_element_group_primitives ==
                         SIX_ELEMENT_NON_COMMUTATIVE_GROUP_PRIMITIVES
                      else 'commutative',
                      'group with the zero, negation, and ',
                      'commutativity'
                      if COMMUTATIVITY_AXIOM in commutativity
                      else 'non-commutativity',
                      'axioms')
            result = model_or_inconsistent(sentences, SIX_ELEMENTS)
            if type(result) is Model:
                if debug:
                    print('Verifying returned model:', result)
                # Will be tested with the course staff's implementation of is_model_of
                assert result.is_model_of({str(sentence)
                                           for sentence in sentences})
            else:
                assert type(result) is Proof
                assert set(result.assumptions).issubset(
                    {Schema(str(s)) for s in sentences}.union(Prover.AXIOMS))
                # Will be tested with the course staff's implementation of is_tautology
                assert is_tautology(
                    Formula('~', result.conclusion).propositional_skeleton())
                if debug:
                    print('Verifying returned proof (' +
                          '{:,}'.format(len(result.lines)),
                          'lines) of', result.conclusion)
                # Will be tested with the course staff's implementation of is_valid
                assert result.is_valid()

def test_combine_contradictions(debug=True):
    common_assumptions = [
        Schema('(~Ax[R(x)]->Ex[~R(x)])', {'x', 'R'}),
        Schema('Ex[~R(x)]'), Schema('Ax[R(x)]')]

    # Contradiction from 'Ex[~R(x)]' and 'Ax[(~R(x)->(Q()&~Q()))]'
    prover_true = Prover(common_assumptions + ['Ax[(~R(x)->(Q()&~Q()))]'],
                         '(Q()&~Q())')
    step1 = prover_true.add_assumption('Ex[~R(x)]')
    step2 = prover_true.add_assumption('Ax[(~R(x)->(Q()&~Q()))]')
    step3 = prover_true.add_instantiated_assumption(
        '((Ax[(~R(x)->(Q()&~Q()))]&Ex[~R(x)])->(Q()&~Q()))', Prover.ES,
        {'R(v)':'~R(v)', 'Q()':'(Q()&~Q())'})
    prover_true.add_tautological_inference('(Q()&~Q())', [step1, step2, step3])

    # Contradiction from 'Ax[R(x)]' and '~Ax[(~R(x)->(Q()&~Q()))]'
    prover_false = Prover(common_assumptions + ['~Ax[(~R(x)->(Q()&~Q()))]'],
                          '(Ax[R(x)]&~Ax[R(x)])')
    step1 = prover_false.add_assumption('Ax[R(x)]')
    step2 = prover_false.add_assumption('~Ax[(~R(x)->(Q()&~Q()))]')
    step3 = prover_false.add_instantiated_assumption(
        '(~Ax[(~R(x)->(Q()&~Q()))]->Ex[~(~R(x)->(Q()&~Q()))])',
        common_assumptions[0], {'R(v)':'(~R(v)->(Q()&~Q()))'})
    step4 = prover_false.add_tautological_inference(
        'Ex[~(~R(x)->(Q()&~Q()))]', [step2, step3])
    step5 = prover_false.add_instantiated_assumption(
        '(Ax[R(x)]->R(x))', Prover.UI, {'c':'x'})
    step6 = prover_false.add_tautological_inference(
        '(~(~R(x)->(Q()&~Q()))->~Ax[R(x)])', [step5])
    step7 = prover_false.add_existential_derivation(
        '~Ax[R(x)]', step4, step6)
    step8 = prover_false.add_tautological_inference(
        '(Ax[R(x)]&~Ax[R(x)])', [step1, step7])

    if (debug):
        print('Testing combine_contradictions for the following two proofs:\n',
              prover_true.proof, '\n', prover_false.proof)
    combined = combine_contradictions(prover_true.proof, prover_false.proof)
    assert combined.assumptions == Prover.AXIOMS + common_assumptions
    # Will be tested with the course staff's implementation of is_tautology
    assert is_tautology(
        Formula('~', combined.conclusion).propositional_skeleton())
    if debug:
        print('Verifying returned proof (' +
              '{:,}'.format(len(combined.lines)),
              'lines) of', combined.conclusion)
    # Will be tested with the course staff's implementation of is_valid
    assert combined.is_valid()

def test_eliminate_universal_instance_assumption(debug=True):
    assumptions = [Schema('~R(c)'), Schema('Ax[R(x)]'), Schema('R(c)')]
    prover = Prover(assumptions, '(R(c)&~R(c))')
    step1 = prover.add_assumption('~R(c)')
    step2 = prover.add_assumption('R(c)')
    prover.add_tautological_inference('(R(c)&~R(c))', [step1, step2])

    if (debug):
        print('Testing eliminate_universal_instance_assumption for the '
              'following proof:\n',
              prover.proof)
    eliminated = eliminate_universal_instance_assumption(prover.proof, 'c')
    assert eliminated.assumptions == Prover.AXIOMS + assumptions[:-1]
    # Will be tested with the course staff's implementation of is_tautology
    assert is_tautology(
        Formula('~', eliminated.conclusion).propositional_skeleton())
    if debug:
        print('Verifying returned proof (' +
              '{:,}'.format(len(eliminated.lines)),
              'lines) of', eliminated.conclusion)
    # Will be tested with the course staff's implementation of is_valid
    assert eliminated.is_valid()

def test_universally_close(debug=True):
    if debug:
        print('Testing universally_close on zero axiom with six elements...')
    closed = universally_close({Formula.parse(ZERO_AXIOM)}, SIX_ELEMENTS)
    assert closed == {Formula.parse(sentence) for sentence in [
        ZERO_AXIOM, 'Plus(0,0,0)', 'Plus(1,0,1)', 'Plus(2,0,2)',
        'Plus(3,0,3)', 'Plus(4,0,4)', 'Plus(5,0,5)']}
    # Will be tested with the course staff's implementation of is_universally_closed
    assert is_universally_closed(closed, SIX_ELEMENTS)

    if debug:
        print('Testing universally_close on negation axiom with six '
              'elements...')
    closed = universally_close({Formula.parse(NEGATION_AXIOM)}, SIX_ELEMENTS)
    assert closed == {Formula.parse(sentence) for sentence in
                      {NEGATION_AXIOM}.union(SIX_ELEMENT_NEGATION_CLOSURE)}
    # Will be tested with the course staff's implementation of is_universally_closed
    assert is_universally_closed(closed, SIX_ELEMENTS)

    if debug:
        print('Testing universally_close on commutativity axiom with six '
              'elements...')
    closed = universally_close({Formula.parse(COMMUTATIVITY_AXIOM)},
                               SIX_ELEMENTS)
    assert closed == {Formula.parse(sentence) for sentence in
                      {COMMUTATIVITY_AXIOM}.union(
                          SIX_ELEMENT_COMMUTATIVITY_CLOSURE)}
    # Will be tested with the course staff's implementation of is_universally_closed
    assert is_universally_closed(closed, SIX_ELEMENTS)

    if debug:
        print('Testing universally_close on zero axiom + negation + '
              'commutativity with six elements...')
    closed = universally_close({Formula.parse(sentence) for sentence in
                                [ZERO_AXIOM, NEGATION_AXIOM,
                                 COMMUTATIVITY_AXIOM]},
                               SIX_ELEMENTS)
    assert {Formula.parse(sentence) for sentence in
            [ZERO_AXIOM, NEGATION_AXIOM, COMMUTATIVITY_AXIOM]}.issubset(closed)
    assert len(closed) == 273
    # Will be tested with the course staff's implementation of is_universally_closed
    assert is_universally_closed(closed, SIX_ELEMENTS)
    for sentence in closed:
        # Will be tested with the course staff's implementation of evaluate_formula
        assert SIX_ELEMENT_COMMUTATIVE_GROUP_MODEL.evaluate_formula(sentence)

    if debug:
        print('Testing universally_close on zero axiom + negation + '
              'commutativity with ten elements...')
    closed = universally_close({Formula.parse(sentence) for sentence in
                                [ZERO_AXIOM, NEGATION_AXIOM,
                                 COMMUTATIVITY_AXIOM]},
                               ['0','1','2','3','4','5','6','7','8','9'])
    assert {Formula.parse(sentence) for sentence in
            [ZERO_AXIOM, NEGATION_AXIOM, COMMUTATIVITY_AXIOM]}.issubset(closed)
    assert len(closed) == 1133
    # Will be tested with the course staff's implementation of is_universally_closed
    assert is_universally_closed(closed,
                                 ['0','1','2','3','4','5','6','7','8','9'])

    if debug:
        print('Testing universally_close on group axioms with six elements...')
    closed = universally_close({Formula.parse(sentence) for sentence in
                                [ZERO_AXIOM, NEGATION_AXIOM,
                                 ASSOCIATIVITY_AXIOM]},
                               SIX_ELEMENTS)
    assert {Formula.parse(sentence) for sentence in
            [ZERO_AXIOM, NEGATION_AXIOM, ASSOCIATIVITY_AXIOM]}.issubset(closed)
    assert len(closed) == 56001
    # Will be tested with the course staff's implementation of is_universally_closed
    assert is_universally_closed(closed, SIX_ELEMENTS)
    for model in [SIX_ELEMENT_COMMUTATIVE_GROUP_MODEL,
                  SIX_ELEMENT_NON_COMMUTATIVE_GROUP_MODEL]:
        for sentence in closed:
            # Will be tested with the course staff's implementation of evaluate_formula
            assert model.evaluate_formula(sentence)

def test_replace_constant(debug=True):
    from  code.predicates.prover_test import syllogism_proof,\
                                       syllogism_proof_with_universal_instantiation
    from code.predicates.some_proofs import unique_zero_proof,GROUP_AXIOMS

    # Replace in assumptions formulae, constant instantiation maps, mp
    if debug:
        print('Testing replace_constant for replacing aristotle with z in '
              'syllogism proof')
    for proof in [syllogism_proof(),
                  syllogism_proof_with_universal_instantiation()]:
        replaced = replace_constant(proof, 'aristotle', 'z')
        assert replaced.assumptions == \
               Prover.AXIOMS + [Schema('Ax[(Man(x)->Mortal(x))]'),
                                Schema('Man(z)')]
        assert str(replaced.conclusion) == 'Mortal(z)'
        if debug:
            print('Verifying returned proof (' +
                  '{:,}'.format(len(replaced.lines)),
                  'lines) of', replaced.conclusion)
        # Will be tested with the course staff's implementation of is_valid
        assert replaced.is_valid()

    # Replace in ug, tautology, relation instantiation maps
    proof = unique_zero_proof()
    if debug:
        print('Testing replace_constant for replacing a with zz in '
              'unique-zero proof')
    replaced = replace_constant(proof, 'a')
    assert replaced.assumptions == \
           Prover.AXIOMS + [Schema(a) for a in GROUP_AXIOMS] + \
           [Schema('plus(zz,c)=zz')]
    assert str(replaced.conclusion) == 'c=0'
    if debug:
        print('Verifying returned proof (' +
              '{:,}'.format(len(replaced.lines)),
              'lines) of', replaced.conclusion)
    # Will be tested with the course staff's implementation of is_valid
    assert replaced.is_valid()

def test_eliminate_existential_witness_assumption(debug=True):
    assumptions = [Schema('Ax[(R(x)->(Q(x)&~Q(x)))]'),
                   Schema('Ex[R(x)]'), Schema('R(c17)')]
    prover = Prover(assumptions, '(Q(c17)&~Q(c17))')
    step1 = prover.add_assumption('R(c17)')
    step2 = prover.add_assumption('Ax[(R(x)->(Q(x)&~Q(x)))]')
    step3 = prover.add_universal_instantiation(
        '(R(c17)->(Q(c17)&~Q(c17)))', step2, 'c17')
    prover.add_tautological_inference('(Q(c17)&~Q(c17))', [step1, step3])

    if (debug):
        print('Testing eliminate_existential_witness_assumption for the '
              'following proof:\n',
              prover.proof)
    eliminated = eliminate_existential_witness_assumption(prover.proof, 'c17')
    assert eliminated.assumptions == Prover.AXIOMS + assumptions[:-1]
    # Will be tested with the course staff's implementation of is_tautology
    assert is_tautology(
        Formula('~', eliminated.conclusion).propositional_skeleton())
    if debug:
        print('Verifying returned proof (' +
              '{:,}'.format(len(eliminated.lines)),
              'lines) of', eliminated.conclusion)
    # Will be tested with the course staff's implementation of is_valid
    assert eliminated.is_valid()

def test_existentially_close(debug=True):
    if debug:
        print('Testing existentially_close on negation axiom universal '
              'closure with six elements...')
    closed,new_constants = existentially_close(
        {Formula.parse(sentence) for sentence in SIX_ELEMENT_NEGATION_CLOSURE},
        SIX_ELEMENTS)
    assert all(is_constant(constant) for constant in new_constants)
    assert SIX_ELEMENTS.issubset(new_constants)
    assert len(new_constants) == 12
    assert len(closed) == 12
    assert {Formula.parse(sentence)
            for sentence in SIX_ELEMENT_NEGATION_CLOSURE}.issubset(closed)
    witnessed = set()
    witnessing_constants = []
    for sentence in closed:
        if sentence.root == 'E':
            continue
        assert sentence.root == 'Plus'
        assert sentence.arguments[0] == '0'
        witnessed.add(sentence.arguments[2])
        witnessing_constants.append(sentence.arguments[1])
    assert witnessed == SIX_ELEMENTS
    assert set(witnessing_constants) == new_constants - SIX_ELEMENTS
    # Will be tested with the course staff's implementation of is_existentially_closed
    assert is_existentially_closed(closed, new_constants)

    if debug:
        print('Testing existentially_close on non-commutativity axiom with '
              'six elements...')
    closed,new_constants = existentially_close(
        {Formula.parse(NON_COMMUTATIVITY)}, SIX_ELEMENTS)
    assert all(is_constant(constant) for constant in new_constants)
    assert SIX_ELEMENTS.issubset(new_constants)
    assert len(new_constants) == 9
    assert len(closed) == 4
    closed_sorted = sorted(list(closed), key=str) # '(Plus' < 'Ex' < 'Ey' < 'Ez'
    assert str(closed_sorted[1]) == NON_COMMUTATIVITY
    witness_x = closed_sorted[0].first.arguments[1]
    witness_y = closed_sorted[0].first.arguments[2]
    witness_z = closed_sorted[0].first.arguments[0]
    assert closed_sorted[0] == \
           Formula('&',
                   Formula('Plus', [witness_z, witness_x, witness_y]),
                   Formula('~',
                           Formula('Plus', [witness_z, witness_y, witness_x])))
    assert closed_sorted[3] == \
           Formula('E', 'z',
                   Formula('&',
                           Formula('Plus', [Term('z'), witness_x, witness_y]),
                           Formula('~',
                                   Formula('Plus', [Term('z'), witness_y,
                                                    witness_x]))))
    assert closed_sorted[2] == \
           Formula('E', 'y',
                   Formula('E', 'z',
                           Formula('&',
                                   Formula('Plus', [Term('z'), witness_x,
                                                    Term('y')]),
                                   Formula('~',
                                           Formula('Plus', [Term('z'),
                                                            Term('y'),
                                                            witness_x])))))
    assert {str(witness_x), str(witness_y), str(witness_z)} == \
           new_constants - SIX_ELEMENTS
    # Will be tested with the course staff's implementation of is_existentially_closed
    assert is_existentially_closed(closed, new_constants)

ZERO_AXIOM = 'Ax[Plus(x,0,x)]'
NEGATION_AXIOM = 'Ax[Ey[Plus(0,y,x)]]'
ASSOCIATIVITY_AXIOM = 'Ax[Ay[Az[Axy[Ayz[Axyz[((Plus(xy,x,y)&Plus(yz,y,z))->((Plus(xyz,xy,z)->Plus(xyz,x,yz))&(Plus(xyz,x,yz)->Plus(xyz,xy,z))))]]]]]]'
COMMUTATIVITY_AXIOM = 'Ax[Ay[Az[(Plus(z,x,y)->Plus(z,y,x))]]]'
NON_COMMUTATIVITY = 'Ex[Ey[Ez[(Plus(z,x,y)&~Plus(z,y,x))]]]'

SIX_ELEMENTS = {'0', '1', '2', '3', '4', '5'}
SIX_ELEMENT_NEGATION_CLOSURE = {'Ey[Plus(0,y,0)]', 'Ey[Plus(0,y,1)]', 'Ey[Plus(0,y,2)]',
                                'Ey[Plus(0,y,3)]', 'Ey[Plus(0,y,4)]', 'Ey[Plus(0,y,5)]'}
SIX_ELEMENT_COMMUTATIVITY_CLOSURE = {
    'Ay[Az[(Plus(z,0,y)->Plus(z,y,0))]]', 'Ay[Az[(Plus(z,1,y)->Plus(z,y,1))]]', 'Ay[Az[(Plus(z,2,y)->Plus(z,y,2))]]',
    'Ay[Az[(Plus(z,3,y)->Plus(z,y,3))]]', 'Ay[Az[(Plus(z,4,y)->Plus(z,y,4))]]', 'Ay[Az[(Plus(z,5,y)->Plus(z,y,5))]]',
    'Az[(Plus(z,0,0)->Plus(z,0,0))]', 'Az[(Plus(z,0,1)->Plus(z,1,0))]', 'Az[(Plus(z,0,2)->Plus(z,2,0))]', 
    'Az[(Plus(z,0,3)->Plus(z,3,0))]', 'Az[(Plus(z,0,4)->Plus(z,4,0))]', 'Az[(Plus(z,0,5)->Plus(z,5,0))]', 
    'Az[(Plus(z,1,0)->Plus(z,0,1))]', 'Az[(Plus(z,1,1)->Plus(z,1,1))]', 'Az[(Plus(z,1,2)->Plus(z,2,1))]', 
    'Az[(Plus(z,1,3)->Plus(z,3,1))]', 'Az[(Plus(z,1,4)->Plus(z,4,1))]', 'Az[(Plus(z,1,5)->Plus(z,5,1))]', 
    'Az[(Plus(z,2,0)->Plus(z,0,2))]', 'Az[(Plus(z,2,1)->Plus(z,1,2))]', 'Az[(Plus(z,2,2)->Plus(z,2,2))]', 
    'Az[(Plus(z,2,3)->Plus(z,3,2))]', 'Az[(Plus(z,2,4)->Plus(z,4,2))]', 'Az[(Plus(z,2,5)->Plus(z,5,2))]', 
    'Az[(Plus(z,3,0)->Plus(z,0,3))]', 'Az[(Plus(z,3,1)->Plus(z,1,3))]', 'Az[(Plus(z,3,2)->Plus(z,2,3))]', 
    'Az[(Plus(z,3,3)->Plus(z,3,3))]', 'Az[(Plus(z,3,4)->Plus(z,4,3))]', 'Az[(Plus(z,3,5)->Plus(z,5,3))]', 
    'Az[(Plus(z,4,0)->Plus(z,0,4))]', 'Az[(Plus(z,4,1)->Plus(z,1,4))]', 'Az[(Plus(z,4,2)->Plus(z,2,4))]', 
    'Az[(Plus(z,4,3)->Plus(z,3,4))]', 'Az[(Plus(z,4,4)->Plus(z,4,4))]', 'Az[(Plus(z,4,5)->Plus(z,5,4))]', 
    'Az[(Plus(z,5,0)->Plus(z,0,5))]', 'Az[(Plus(z,5,1)->Plus(z,1,5))]', 'Az[(Plus(z,5,2)->Plus(z,2,5))]', 
    'Az[(Plus(z,5,3)->Plus(z,3,5))]', 'Az[(Plus(z,5,4)->Plus(z,4,5))]', 'Az[(Plus(z,5,5)->Plus(z,5,5))]',
    '(Plus(0,0,0)->Plus(0,0,0))', '(Plus(1,0,0)->Plus(1,0,0))', '(Plus(2,0,0)->Plus(2,0,0))', 
    '(Plus(3,0,0)->Plus(3,0,0))', '(Plus(4,0,0)->Plus(4,0,0))', '(Plus(5,0,0)->Plus(5,0,0))', 
    '(Plus(0,0,1)->Plus(0,1,0))', '(Plus(1,0,1)->Plus(1,1,0))', '(Plus(2,0,1)->Plus(2,1,0))', 
    '(Plus(3,0,1)->Plus(3,1,0))', '(Plus(4,0,1)->Plus(4,1,0))', '(Plus(5,0,1)->Plus(5,1,0))', 
    '(Plus(0,0,2)->Plus(0,2,0))', '(Plus(1,0,2)->Plus(1,2,0))', '(Plus(2,0,2)->Plus(2,2,0))', 
    '(Plus(3,0,2)->Plus(3,2,0))', '(Plus(4,0,2)->Plus(4,2,0))', '(Plus(5,0,2)->Plus(5,2,0))', 
    '(Plus(0,0,3)->Plus(0,3,0))', '(Plus(1,0,3)->Plus(1,3,0))', '(Plus(2,0,3)->Plus(2,3,0))', 
    '(Plus(3,0,3)->Plus(3,3,0))', '(Plus(4,0,3)->Plus(4,3,0))', '(Plus(5,0,3)->Plus(5,3,0))', 
    '(Plus(0,0,4)->Plus(0,4,0))', '(Plus(1,0,4)->Plus(1,4,0))', '(Plus(2,0,4)->Plus(2,4,0))', 
    '(Plus(3,0,4)->Plus(3,4,0))', '(Plus(4,0,4)->Plus(4,4,0))', '(Plus(5,0,4)->Plus(5,4,0))', 
    '(Plus(0,0,5)->Plus(0,5,0))', '(Plus(1,0,5)->Plus(1,5,0))', '(Plus(2,0,5)->Plus(2,5,0))', 
    '(Plus(3,0,5)->Plus(3,5,0))', '(Plus(4,0,5)->Plus(4,5,0))', '(Plus(5,0,5)->Plus(5,5,0))', 
    '(Plus(0,1,0)->Plus(0,0,1))', '(Plus(1,1,0)->Plus(1,0,1))', '(Plus(2,1,0)->Plus(2,0,1))', 
    '(Plus(3,1,0)->Plus(3,0,1))', '(Plus(4,1,0)->Plus(4,0,1))', '(Plus(5,1,0)->Plus(5,0,1))', 
    '(Plus(0,1,1)->Plus(0,1,1))', '(Plus(1,1,1)->Plus(1,1,1))', '(Plus(2,1,1)->Plus(2,1,1))', 
    '(Plus(3,1,1)->Plus(3,1,1))', '(Plus(4,1,1)->Plus(4,1,1))', '(Plus(5,1,1)->Plus(5,1,1))', 
    '(Plus(0,1,2)->Plus(0,2,1))', '(Plus(1,1,2)->Plus(1,2,1))', '(Plus(2,1,2)->Plus(2,2,1))', 
    '(Plus(3,1,2)->Plus(3,2,1))', '(Plus(4,1,2)->Plus(4,2,1))', '(Plus(5,1,2)->Plus(5,2,1))', 
    '(Plus(0,1,3)->Plus(0,3,1))', '(Plus(1,1,3)->Plus(1,3,1))', '(Plus(2,1,3)->Plus(2,3,1))', 
    '(Plus(3,1,3)->Plus(3,3,1))', '(Plus(4,1,3)->Plus(4,3,1))', '(Plus(5,1,3)->Plus(5,3,1))', 
    '(Plus(0,1,4)->Plus(0,4,1))', '(Plus(1,1,4)->Plus(1,4,1))', '(Plus(2,1,4)->Plus(2,4,1))', 
    '(Plus(3,1,4)->Plus(3,4,1))', '(Plus(4,1,4)->Plus(4,4,1))', '(Plus(5,1,4)->Plus(5,4,1))', 
    '(Plus(0,1,5)->Plus(0,5,1))', '(Plus(1,1,5)->Plus(1,5,1))', '(Plus(2,1,5)->Plus(2,5,1))', 
    '(Plus(3,1,5)->Plus(3,5,1))', '(Plus(4,1,5)->Plus(4,5,1))', '(Plus(5,1,5)->Plus(5,5,1))', 
    '(Plus(0,2,0)->Plus(0,0,2))', '(Plus(1,2,0)->Plus(1,0,2))', '(Plus(2,2,0)->Plus(2,0,2))', 
    '(Plus(3,2,0)->Plus(3,0,2))', '(Plus(4,2,0)->Plus(4,0,2))', '(Plus(5,2,0)->Plus(5,0,2))', 
    '(Plus(0,2,1)->Plus(0,1,2))', '(Plus(1,2,1)->Plus(1,1,2))', '(Plus(2,2,1)->Plus(2,1,2))', 
    '(Plus(3,2,1)->Plus(3,1,2))', '(Plus(4,2,1)->Plus(4,1,2))', '(Plus(5,2,1)->Plus(5,1,2))', 
    '(Plus(0,2,2)->Plus(0,2,2))', '(Plus(1,2,2)->Plus(1,2,2))', '(Plus(2,2,2)->Plus(2,2,2))', 
    '(Plus(3,2,2)->Plus(3,2,2))', '(Plus(4,2,2)->Plus(4,2,2))', '(Plus(5,2,2)->Plus(5,2,2))', 
    '(Plus(0,2,3)->Plus(0,3,2))', '(Plus(1,2,3)->Plus(1,3,2))', '(Plus(2,2,3)->Plus(2,3,2))', 
    '(Plus(3,2,3)->Plus(3,3,2))', '(Plus(4,2,3)->Plus(4,3,2))', '(Plus(5,2,3)->Plus(5,3,2))', 
    '(Plus(0,2,4)->Plus(0,4,2))', '(Plus(1,2,4)->Plus(1,4,2))', '(Plus(2,2,4)->Plus(2,4,2))', 
    '(Plus(3,2,4)->Plus(3,4,2))', '(Plus(4,2,4)->Plus(4,4,2))', '(Plus(5,2,4)->Plus(5,4,2))', 
    '(Plus(0,2,5)->Plus(0,5,2))', '(Plus(1,2,5)->Plus(1,5,2))', '(Plus(2,2,5)->Plus(2,5,2))', 
    '(Plus(3,2,5)->Plus(3,5,2))', '(Plus(4,2,5)->Plus(4,5,2))', '(Plus(5,2,5)->Plus(5,5,2))', 
    '(Plus(0,3,0)->Plus(0,0,3))', '(Plus(1,3,0)->Plus(1,0,3))', '(Plus(2,3,0)->Plus(2,0,3))', 
    '(Plus(3,3,0)->Plus(3,0,3))', '(Plus(4,3,0)->Plus(4,0,3))', '(Plus(5,3,0)->Plus(5,0,3))', 
    '(Plus(0,3,1)->Plus(0,1,3))', '(Plus(1,3,1)->Plus(1,1,3))', '(Plus(2,3,1)->Plus(2,1,3))', 
    '(Plus(3,3,1)->Plus(3,1,3))', '(Plus(4,3,1)->Plus(4,1,3))', '(Plus(5,3,1)->Plus(5,1,3))', 
    '(Plus(0,3,2)->Plus(0,2,3))', '(Plus(1,3,2)->Plus(1,2,3))', '(Plus(2,3,2)->Plus(2,2,3))', 
    '(Plus(3,3,2)->Plus(3,2,3))', '(Plus(4,3,2)->Plus(4,2,3))', '(Plus(5,3,2)->Plus(5,2,3))', 
    '(Plus(0,3,3)->Plus(0,3,3))', '(Plus(1,3,3)->Plus(1,3,3))', '(Plus(2,3,3)->Plus(2,3,3))', 
    '(Plus(3,3,3)->Plus(3,3,3))', '(Plus(4,3,3)->Plus(4,3,3))', '(Plus(5,3,3)->Plus(5,3,3))', 
    '(Plus(0,3,4)->Plus(0,4,3))', '(Plus(1,3,4)->Plus(1,4,3))', '(Plus(2,3,4)->Plus(2,4,3))', 
    '(Plus(3,3,4)->Plus(3,4,3))', '(Plus(4,3,4)->Plus(4,4,3))', '(Plus(5,3,4)->Plus(5,4,3))', 
    '(Plus(0,3,5)->Plus(0,5,3))', '(Plus(1,3,5)->Plus(1,5,3))', '(Plus(2,3,5)->Plus(2,5,3))', 
    '(Plus(3,3,5)->Plus(3,5,3))', '(Plus(4,3,5)->Plus(4,5,3))', '(Plus(5,3,5)->Plus(5,5,3))', 
    '(Plus(0,4,0)->Plus(0,0,4))', '(Plus(1,4,0)->Plus(1,0,4))', '(Plus(2,4,0)->Plus(2,0,4))', 
    '(Plus(3,4,0)->Plus(3,0,4))', '(Plus(4,4,0)->Plus(4,0,4))', '(Plus(5,4,0)->Plus(5,0,4))', 
    '(Plus(0,4,1)->Plus(0,1,4))', '(Plus(1,4,1)->Plus(1,1,4))', '(Plus(2,4,1)->Plus(2,1,4))', 
    '(Plus(3,4,1)->Plus(3,1,4))', '(Plus(4,4,1)->Plus(4,1,4))', '(Plus(5,4,1)->Plus(5,1,4))', 
    '(Plus(0,4,2)->Plus(0,2,4))', '(Plus(1,4,2)->Plus(1,2,4))', '(Plus(2,4,2)->Plus(2,2,4))', 
    '(Plus(3,4,2)->Plus(3,2,4))', '(Plus(4,4,2)->Plus(4,2,4))', '(Plus(5,4,2)->Plus(5,2,4))', 
    '(Plus(0,4,3)->Plus(0,3,4))', '(Plus(1,4,3)->Plus(1,3,4))', '(Plus(2,4,3)->Plus(2,3,4))', 
    '(Plus(3,4,3)->Plus(3,3,4))', '(Plus(4,4,3)->Plus(4,3,4))', '(Plus(5,4,3)->Plus(5,3,4))', 
    '(Plus(0,4,4)->Plus(0,4,4))', '(Plus(1,4,4)->Plus(1,4,4))', '(Plus(2,4,4)->Plus(2,4,4))', 
    '(Plus(3,4,4)->Plus(3,4,4))', '(Plus(4,4,4)->Plus(4,4,4))', '(Plus(5,4,4)->Plus(5,4,4))', 
    '(Plus(0,4,5)->Plus(0,5,4))', '(Plus(1,4,5)->Plus(1,5,4))', '(Plus(2,4,5)->Plus(2,5,4))', 
    '(Plus(3,4,5)->Plus(3,5,4))', '(Plus(4,4,5)->Plus(4,5,4))', '(Plus(5,4,5)->Plus(5,5,4))', 
    '(Plus(0,5,0)->Plus(0,0,5))', '(Plus(1,5,0)->Plus(1,0,5))', '(Plus(2,5,0)->Plus(2,0,5))', 
    '(Plus(3,5,0)->Plus(3,0,5))', '(Plus(4,5,0)->Plus(4,0,5))', '(Plus(5,5,0)->Plus(5,0,5))', 
    '(Plus(0,5,1)->Plus(0,1,5))', '(Plus(1,5,1)->Plus(1,1,5))', '(Plus(2,5,1)->Plus(2,1,5))', 
    '(Plus(3,5,1)->Plus(3,1,5))', '(Plus(4,5,1)->Plus(4,1,5))', '(Plus(5,5,1)->Plus(5,1,5))', 
    '(Plus(0,5,2)->Plus(0,2,5))', '(Plus(1,5,2)->Plus(1,2,5))', '(Plus(2,5,2)->Plus(2,2,5))', 
    '(Plus(3,5,2)->Plus(3,2,5))', '(Plus(4,5,2)->Plus(4,2,5))', '(Plus(5,5,2)->Plus(5,2,5))', 
    '(Plus(0,5,3)->Plus(0,3,5))', '(Plus(1,5,3)->Plus(1,3,5))', '(Plus(2,5,3)->Plus(2,3,5))', 
    '(Plus(3,5,3)->Plus(3,3,5))', '(Plus(4,5,3)->Plus(4,3,5))', '(Plus(5,5,3)->Plus(5,3,5))', 
    '(Plus(0,5,4)->Plus(0,4,5))', '(Plus(1,5,4)->Plus(1,4,5))', '(Plus(2,5,4)->Plus(2,4,5))', 
    '(Plus(3,5,4)->Plus(3,4,5))', '(Plus(4,5,4)->Plus(4,4,5))', '(Plus(5,5,4)->Plus(5,4,5))', 
    '(Plus(0,5,5)->Plus(0,5,5))', '(Plus(1,5,5)->Plus(1,5,5))', '(Plus(2,5,5)->Plus(2,5,5))', 
    '(Plus(3,5,5)->Plus(3,5,5))', '(Plus(4,5,5)->Plus(4,5,5))', '(Plus(5,5,5)->Plus(5,5,5))'}

SIX_ELEMENT_COMMUTATIVE_GROUP_PRIMITIVES = {
    'Plus(0,0,0)', '~Plus(1,0,0)', '~Plus(2,0,0)', '~Plus(3,0,0)', '~Plus(4,0,0)', '~Plus(5,0,0)',
    '~Plus(0,0,1)', 'Plus(1,0,1)', '~Plus(2,0,1)', '~Plus(3,0,1)', '~Plus(4,0,1)', '~Plus(5,0,1)',
    '~Plus(0,0,2)', '~Plus(1,0,2)', 'Plus(2,0,2)', '~Plus(3,0,2)', '~Plus(4,0,2)', '~Plus(5,0,2)',
    '~Plus(0,0,3)', '~Plus(1,0,3)', '~Plus(2,0,3)', 'Plus(3,0,3)', '~Plus(4,0,3)', '~Plus(5,0,3)',
    '~Plus(0,0,4)', '~Plus(1,0,4)', '~Plus(2,0,4)', '~Plus(3,0,4)', 'Plus(4,0,4)', '~Plus(5,0,4)',
    '~Plus(0,0,5)', '~Plus(1,0,5)', '~Plus(2,0,5)', '~Plus(3,0,5)', '~Plus(4,0,5)', 'Plus(5,0,5)',
    '~Plus(0,1,0)', 'Plus(1,1,0)', '~Plus(2,1,0)', '~Plus(3,1,0)', '~Plus(4,1,0)', '~Plus(5,1,0)',
    '~Plus(0,1,1)', '~Plus(1,1,1)', 'Plus(2,1,1)', '~Plus(3,1,1)', '~Plus(4,1,1)', '~Plus(5,1,1)',
    '~Plus(0,1,2)', '~Plus(1,1,2)', '~Plus(2,1,2)', 'Plus(3,1,2)', '~Plus(4,1,2)', '~Plus(5,1,2)',
    '~Plus(0,1,3)', '~Plus(1,1,3)', '~Plus(2,1,3)', '~Plus(3,1,3)', 'Plus(4,1,3)', '~Plus(5,1,3)',
    '~Plus(0,1,4)', '~Plus(1,1,4)', '~Plus(2,1,4)', '~Plus(3,1,4)', '~Plus(4,1,4)', 'Plus(5,1,4)',
    'Plus(0,1,5)', '~Plus(1,1,5)', '~Plus(2,1,5)', '~Plus(3,1,5)', '~Plus(4,1,5)', '~Plus(5,1,5)',
    '~Plus(0,2,0)', '~Plus(1,2,0)', 'Plus(2,2,0)', '~Plus(3,2,0)', '~Plus(4,2,0)', '~Plus(5,2,0)',
    '~Plus(0,2,1)', '~Plus(1,2,1)', '~Plus(2,2,1)', 'Plus(3,2,1)', '~Plus(4,2,1)', '~Plus(5,2,1)',
    '~Plus(0,2,2)', '~Plus(1,2,2)', '~Plus(2,2,2)', '~Plus(3,2,2)', 'Plus(4,2,2)', '~Plus(5,2,2)',
    '~Plus(0,2,3)', '~Plus(1,2,3)', '~Plus(2,2,3)', '~Plus(3,2,3)', '~Plus(4,2,3)', 'Plus(5,2,3)',
    'Plus(0,2,4)', '~Plus(1,2,4)', '~Plus(2,2,4)', '~Plus(3,2,4)', '~Plus(4,2,4)', '~Plus(5,2,4)',
    '~Plus(0,2,5)', 'Plus(1,2,5)', '~Plus(2,2,5)', '~Plus(3,2,5)', '~Plus(4,2,5)', '~Plus(5,2,5)',
    '~Plus(0,3,0)', '~Plus(1,3,0)', '~Plus(2,3,0)', 'Plus(3,3,0)', '~Plus(4,3,0)', '~Plus(5,3,0)',
    '~Plus(0,3,1)', '~Plus(1,3,1)', '~Plus(2,3,1)', '~Plus(3,3,1)', 'Plus(4,3,1)', '~Plus(5,3,1)',
    '~Plus(0,3,2)', '~Plus(1,3,2)', '~Plus(2,3,2)', '~Plus(3,3,2)', '~Plus(4,3,2)', 'Plus(5,3,2)',
    'Plus(0,3,3)', '~Plus(1,3,3)', '~Plus(2,3,3)', '~Plus(3,3,3)', '~Plus(4,3,3)', '~Plus(5,3,3)',
    '~Plus(0,3,4)', 'Plus(1,3,4)', '~Plus(2,3,4)', '~Plus(3,3,4)', '~Plus(4,3,4)', '~Plus(5,3,4)',
    '~Plus(0,3,5)', '~Plus(1,3,5)', 'Plus(2,3,5)', '~Plus(3,3,5)', '~Plus(4,3,5)', '~Plus(5,3,5)',
    '~Plus(0,4,0)', '~Plus(1,4,0)', '~Plus(2,4,0)', '~Plus(3,4,0)', 'Plus(4,4,0)', '~Plus(5,4,0)',
    '~Plus(0,4,1)', '~Plus(1,4,1)', '~Plus(2,4,1)', '~Plus(3,4,1)', '~Plus(4,4,1)', 'Plus(5,4,1)',
    'Plus(0,4,2)', '~Plus(1,4,2)', '~Plus(2,4,2)', '~Plus(3,4,2)', '~Plus(4,4,2)', '~Plus(5,4,2)',
    '~Plus(0,4,3)', 'Plus(1,4,3)', '~Plus(2,4,3)', '~Plus(3,4,3)', '~Plus(4,4,3)', '~Plus(5,4,3)',
    '~Plus(0,4,4)', '~Plus(1,4,4)', 'Plus(2,4,4)', '~Plus(3,4,4)', '~Plus(4,4,4)', '~Plus(5,4,4)',
    '~Plus(0,4,5)', '~Plus(1,4,5)', '~Plus(2,4,5)', 'Plus(3,4,5)', '~Plus(4,4,5)', '~Plus(5,4,5)',
    '~Plus(0,5,0)', '~Plus(1,5,0)', '~Plus(2,5,0)', '~Plus(3,5,0)', '~Plus(4,5,0)', 'Plus(5,5,0)',
    'Plus(0,5,1)', '~Plus(1,5,1)', '~Plus(2,5,1)', '~Plus(3,5,1)', '~Plus(4,5,1)', '~Plus(5,5,1)',
    '~Plus(0,5,2)', 'Plus(1,5,2)', '~Plus(2,5,2)', '~Plus(3,5,2)', '~Plus(4,5,2)', '~Plus(5,5,2)',
    '~Plus(0,5,3)', '~Plus(1,5,3)', 'Plus(2,5,3)', '~Plus(3,5,3)', '~Plus(4,5,3)', '~Plus(5,5,3)',
    '~Plus(0,5,4)', '~Plus(1,5,4)', '~Plus(2,5,4)', 'Plus(3,5,4)', '~Plus(4,5,4)', '~Plus(5,5,4)',
    '~Plus(0,5,5)', '~Plus(1,5,5)', '~Plus(2,5,5)', '~Plus(3,5,5)', 'Plus(4,5,5)', '~Plus(5,5,5)'}

SIX_ELEMENT_COMMUTATIVE_GROUP_MODEL = Model(
    SIX_ELEMENTS,
    {'0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5',
     'Plus': {('0','0','0'), ('1','0','1'), ('2','0','2'), ('3','0','3'), ('4','0','4'), ('5','0','5'), 
              ('1','1','0'), ('2','1','1'), ('3','1','2'), ('4','1','3'), ('5','1','4'), ('0','1','5'), 
              ('2','2','0'), ('3','2','1'), ('4','2','2'), ('5','2','3'), ('0','2','4'), ('1','2','5'), 
              ('3','3','0'), ('4','3','1'), ('5','3','2'), ('0','3','3'), ('1','3','4'), ('2','3','5'), 
              ('4','4','0'), ('5','4','1'), ('0','4','2'), ('1','4','3'), ('2','4','4'), ('3','4','5'), 
              ('5','5','0'), ('0','5','1'), ('1','5','2'), ('2','5','3'), ('3','5','4'), ('4','5','5')}})

SIX_ELEMENT_NON_COMMUTATIVE_GROUP_PRIMITIVES = {
    'Plus(0,0,0)', '~Plus(1,0,0)', '~Plus(2,0,0)', '~Plus(3,0,0)', '~Plus(4,0,0)', '~Plus(5,0,0)', 
    '~Plus(0,0,1)', 'Plus(1,0,1)', '~Plus(2,0,1)', '~Plus(3,0,1)', '~Plus(4,0,1)', '~Plus(5,0,1)', 
    '~Plus(0,0,2)', '~Plus(1,0,2)', 'Plus(2,0,2)', '~Plus(3,0,2)', '~Plus(4,0,2)', '~Plus(5,0,2)', 
    '~Plus(0,0,3)', '~Plus(1,0,3)', '~Plus(2,0,3)', 'Plus(3,0,3)', '~Plus(4,0,3)', '~Plus(5,0,3)', 
    '~Plus(0,0,4)', '~Plus(1,0,4)', '~Plus(2,0,4)', '~Plus(3,0,4)', 'Plus(4,0,4)', '~Plus(5,0,4)', 
    '~Plus(0,0,5)', '~Plus(1,0,5)', '~Plus(2,0,5)', '~Plus(3,0,5)', '~Plus(4,0,5)', 'Plus(5,0,5)', 
    '~Plus(0,1,0)', 'Plus(1,1,0)', '~Plus(2,1,0)', '~Plus(3,1,0)', '~Plus(4,1,0)', '~Plus(5,1,0)', 
    'Plus(0,1,1)', '~Plus(1,1,1)', '~Plus(2,1,1)', '~Plus(3,1,1)', '~Plus(4,1,1)', '~Plus(5,1,1)', 
    '~Plus(0,1,2)', '~Plus(1,1,2)', '~Plus(2,1,2)', '~Plus(3,1,2)', '~Plus(4,1,2)', 'Plus(5,1,2)', 
    '~Plus(0,1,3)', '~Plus(1,1,3)', '~Plus(2,1,3)', '~Plus(3,1,3)', 'Plus(4,1,3)', '~Plus(5,1,3)', 
    '~Plus(0,1,4)', '~Plus(1,1,4)', '~Plus(2,1,4)', 'Plus(3,1,4)', '~Plus(4,1,4)', '~Plus(5,1,4)', 
    '~Plus(0,1,5)', '~Plus(1,1,5)', 'Plus(2,1,5)', '~Plus(3,1,5)', '~Plus(4,1,5)', '~Plus(5,1,5)', 
    '~Plus(0,2,0)', '~Plus(1,2,0)', 'Plus(2,2,0)', '~Plus(3,2,0)', '~Plus(4,2,0)', '~Plus(5,2,0)', 
    '~Plus(0,2,1)', '~Plus(1,2,1)', '~Plus(2,2,1)', '~Plus(3,2,1)', 'Plus(4,2,1)', '~Plus(5,2,1)', 
    'Plus(0,2,2)', '~Plus(1,2,2)', '~Plus(2,2,2)', '~Plus(3,2,2)', '~Plus(4,2,2)', '~Plus(5,2,2)', 
    '~Plus(0,2,3)', '~Plus(1,2,3)', '~Plus(2,2,3)', '~Plus(3,2,3)', '~Plus(4,2,3)', 'Plus(5,2,3)', 
    '~Plus(0,2,4)', 'Plus(1,2,4)', '~Plus(2,2,4)', '~Plus(3,2,4)', '~Plus(4,2,4)', '~Plus(5,2,4)', 
    '~Plus(0,2,5)', '~Plus(1,2,5)', '~Plus(2,2,5)', 'Plus(3,2,5)', '~Plus(4,2,5)', '~Plus(5,2,5)', 
    '~Plus(0,3,0)', '~Plus(1,3,0)', '~Plus(2,3,0)', 'Plus(3,3,0)', '~Plus(4,3,0)', '~Plus(5,3,0)', 
    '~Plus(0,3,1)', '~Plus(1,3,1)', '~Plus(2,3,1)', '~Plus(3,3,1)', '~Plus(4,3,1)', 'Plus(5,3,1)', 
    '~Plus(0,3,2)', '~Plus(1,3,2)', '~Plus(2,3,2)', '~Plus(3,3,2)', 'Plus(4,3,2)', '~Plus(5,3,2)', 
    'Plus(0,3,3)', '~Plus(1,3,3)', '~Plus(2,3,3)', '~Plus(3,3,3)', '~Plus(4,3,3)', '~Plus(5,3,3)', 
    '~Plus(0,3,4)', '~Plus(1,3,4)', 'Plus(2,3,4)', '~Plus(3,3,4)', '~Plus(4,3,4)', '~Plus(5,3,4)', 
    '~Plus(0,3,5)', 'Plus(1,3,5)', '~Plus(2,3,5)', '~Plus(3,3,5)', '~Plus(4,3,5)', '~Plus(5,3,5)', 
    '~Plus(0,4,0)', '~Plus(1,4,0)', '~Plus(2,4,0)', '~Plus(3,4,0)', 'Plus(4,4,0)', '~Plus(5,4,0)', 
    '~Plus(0,4,1)', '~Plus(1,4,1)', 'Plus(2,4,1)', '~Plus(3,4,1)', '~Plus(4,4,1)', '~Plus(5,4,1)', 
    '~Plus(0,4,2)', '~Plus(1,4,2)', '~Plus(2,4,2)', 'Plus(3,4,2)', '~Plus(4,4,2)', '~Plus(5,4,2)', 
    '~Plus(0,4,3)', 'Plus(1,4,3)', '~Plus(2,4,3)', '~Plus(3,4,3)', '~Plus(4,4,3)', '~Plus(5,4,3)', 
    '~Plus(0,4,4)', '~Plus(1,4,4)', '~Plus(2,4,4)', '~Plus(3,4,4)', '~Plus(4,4,4)', 'Plus(5,4,4)', 
    'Plus(0,4,5)', '~Plus(1,4,5)', '~Plus(2,4,5)', '~Plus(3,4,5)', '~Plus(4,4,5)', '~Plus(5,4,5)', 
    '~Plus(0,5,0)', '~Plus(1,5,0)', '~Plus(2,5,0)', '~Plus(3,5,0)', '~Plus(4,5,0)', 'Plus(5,5,0)', 
    '~Plus(0,5,1)', '~Plus(1,5,1)', '~Plus(2,5,1)', 'Plus(3,5,1)', '~Plus(4,5,1)', '~Plus(5,5,1)', 
    '~Plus(0,5,2)', 'Plus(1,5,2)', '~Plus(2,5,2)', '~Plus(3,5,2)', '~Plus(4,5,2)', '~Plus(5,5,2)', 
    '~Plus(0,5,3)', '~Plus(1,5,3)', 'Plus(2,5,3)', '~Plus(3,5,3)', '~Plus(4,5,3)', '~Plus(5,5,3)', 
    'Plus(0,5,4)', '~Plus(1,5,4)', '~Plus(2,5,4)', '~Plus(3,5,4)', '~Plus(4,5,4)', '~Plus(5,5,4)', 
    '~Plus(0,5,5)', '~Plus(1,5,5)', '~Plus(2,5,5)', '~Plus(3,5,5)', 'Plus(4,5,5)', '~Plus(5,5,5)'}

SIX_ELEMENT_NON_COMMUTATIVE_GROUP_NON_COMMUTATIVITY_CLOSURE = \
    {'Ey[Ez[(Plus(z,1,y)&~Plus(z,y,1))]]',
     'Ez[(Plus(z,1,2)&~Plus(z,2,1))]',
     '(Plus(5,1,2)&~Plus(5,2,1))'}

SIX_ELEMENT_NON_COMMUTATIVE_GROUP_MODEL = Model(
    SIX_ELEMENTS,
    {'0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5',
     'Plus': {('0','0','0'), ('1','0','1'), ('2','0','2'), ('3','0','3'), ('4','0','4'), ('5','0','5'), 
              ('1','1','0'), ('0','1','1'), ('5','1','2'), ('4','1','3'), ('3','1','4'), ('2','1','5'), 
              ('2','2','0'), ('4','2','1'), ('0','2','2'), ('5','2','3'), ('1','2','4'), ('3','2','5'), 
              ('3','3','0'), ('5','3','1'), ('4','3','2'), ('0','3','3'), ('2','3','4'), ('1','3','5'), 
              ('4','4','0'), ('2','4','1'), ('3','4','2'), ('1','4','3'), ('5','4','4'), ('0','4','5'), 
              ('5','5','0'), ('3','5','1'), ('1','5','2'), ('2','5','3'), ('0','5','4'), ('4','5','5')}})
