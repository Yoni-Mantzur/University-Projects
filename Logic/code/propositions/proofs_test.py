""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/propositions/proofs_test.py """

from code.propositions.syntax import *
from code.propositions.proofs import *

# Tests for InferenceRule:

def test_variables(debug=False):
    for assumptions, conclusion, variables in [
            [[], 'T', set()],
            [['p', 'q'], 'r', {'p', 'q', 'r'}],
            [['(p|q)', '(q|r)', '(r|p)'], '(p?q:s)', {'p', 'q', 'r', 's'}],
            [['(x1-&x2)', '(x3-|x4)'], '(x1->x11)', {'x1', 'x2', 'x3', 'x4', 'x11'}],
            [['~z', '~y', '~x'], '(((x|y)|z)|w)', {'z', 'y', 'x', 'w'}],
            [['~~z'], '(~~z?z:z)', {'z'}]]:
        rule = InferenceRule([Formula.from_infix(a) for a in assumptions],
                             Formula.from_infix(conclusion))
        if debug:
            print('Testing variables of the inference rule', rule)
        assert rule.variables() == variables

def test_update_instantiation_map(debug=False):
    for template_infix, candidate_infix, instantiation_map_infix, conflicting_map_infix in [
            ['(~p|p)', '(~q|q)', {'p': 'q'}, {'p': 'q7'}],
            ['(~p|p)', '(~p|p)', {'p': 'p'}, {'p': 'p1'}],
            ['(~p|p)', '(~p4|p4)', {'p': 'p4'}, {'p': '~p4'}],
            ['(~p|p)', '(~r7|r7)', {'p': 'r7'}, {'p': 'r71'}],
            ['(~p|p)', '(~~(p|q)|~(p|q))', {'p': '~(p|q)'}, {'p': '~(p|p)'}],
            ['(~p|p)', '(~p|q)', None, {'p': 'p'}],
            ['(~p|p)', '(~p1|p2)', None, {'p': 'p2'}],
            ['(~p|p)', '(~~(p|p)|~(p|q))', None, {'p': '(p|q)'}],
            ['~(x?((p->(q-&x))|((p-|y)<->(r&q))):y)',
             '~(y?((p->((q?x:y)-&y))|((p-|x)<->((r|q)&(q?x:y)))):x)',
             {'x': 'y', 'y': 'x', 'p': 'p', 'q': '(q?x:y)', 'r': '(r|q)'},
             {'x': 'y', 'y': 'x', 'p': 'p', 'q': '(q?x:z)', 'r': '(r|q)'}],
            ['~(x?((p->(q-&x))|((p-|y)<->(r&q))):y)',
             '~(y?((p->((q?x:y)-&y))|((p-|x1)<->((r|q)&(q?x:y)))):x)',
             None,
             {'x': 'y', 'y': 'x1', 'p': 'p', 'q': '(q?x:y)', 'r': '(r|q)'}]]:
        template = Formula.from_infix(template_infix)
        candidate = Formula.from_infix(candidate_infix)
        if instantiation_map_infix is not None:
            instantiation_map = \
                {variable: Formula.from_infix(instantiation_map_infix[variable])
                 for variable in instantiation_map_infix}
        # No initial map
        if debug:
            print('Testing _update_instantiation_map for', candidate, 'and',
                  template, 'with empty initial map')
        if instantiation_map_infix is None:
            assert not InferenceRule._update_instantiation_map(
                candidate, template, {})
        else:
            map_ = {}
            assert InferenceRule._update_instantiation_map(
                candidate, template, map_)
            assert map_ == instantiation_map

        # Partial initial map
        if instantiation_map_infix is not None:
            variables = sorted(list(template.variables()))
            for i in range(1, len(variables)+1):
                map_ = {variable: instantiation_map[variable]
                        for variable in variables[:i]}
                if debug:
                    print('Testing _update_instantiation_map for', candidate,
                          'and', template, 'with initial map', map_)
                assert InferenceRule._update_instantiation_map(
                    candidate, template, map_)
                assert map_ == instantiation_map
            
        # Conflicting initial map
        conflicting_map = \
            {variable: Formula.from_infix(conflicting_map_infix[variable])
             for variable in conflicting_map_infix}
        if debug:
            print('Testing _update_instantiation_map for', candidate, 'and',
                  template, 'with (conflicting) initial map', conflicting_map)
        assert not InferenceRule._update_instantiation_map(
            candidate, template, conflicting_map)
    
def test_is_instance_of(debug=False):
    # Test 1
    rule = InferenceRule([], Formula.from_infix('(~p|p)'))
    for conclusion, instantiation_map_infix in [
            ['(~q|q)', {'p': 'q'}],
            ['(~p|p)', {'p': 'p'}],
            ['(~p4|p4)', {'p': 'p4'}],
            ['(~r7|r7)', {'p': 'r7'}],
            ['(~~(p|q)|~(p|q))', {'p': '~(p|q)'}],
            ['(~p|q)', None],
            ['(~p1|p2)', None],
            ['(~~(p|p)|~(p|q))', None]]:
        candidate = InferenceRule([], Formula.from_infix(conclusion))
        if debug:
            print('Testing whether', candidate, 'is an instance of', rule)
        assert candidate.is_instance_of(rule) == \
               (instantiation_map_infix is not None)
        map_ = {}
        assert candidate.is_instance_of(rule, map_) == \
               (instantiation_map_infix is not None)
        if instantiation_map_infix is not None:
            instantiation_map = \
                {variable: Formula.from_infix(instantiation_map_infix[variable])
                 for variable in instantiation_map_infix}
            assert map_ == instantiation_map
        else:
            assert map_ == {}

    # Test 2
    rule = InferenceRule(
        [], Formula.from_infix('~(x?((p->(q-&x))|((p-|y)<->(r&q))):y)'))
    for conclusion, value in [
            ['~(y?((p->((q?x:y)-&y))|((p-|x)<->((r|q)&(q?x:y)))):x)', True],
            ['~(y?((p->((q?x:y)-&y))|((p-|x1)<->((r|q)&(q?x:y)))):x)', False]]:
        candidate = InferenceRule([], Formula.from_infix(conclusion))
        if debug:
            print('Testing whether', candidate, 'is an instance of', rule)
        assert candidate.is_instance_of(rule) == value

    # Test 2
    a = Formula.from_infix('(~p|q)')
    b = Formula.from_infix('p')
    c = Formula.from_infix('q')
    aa = Formula.from_infix('(~x|y)')
    bb = Formula.from_infix('x')
    cc = Formula.from_infix('y')
    rule = InferenceRule([a, b], c)
    instantiation_map = {'p': Formula.from_infix('x'),
                         'q': Formula.from_infix('y')}
    for assumptions, conclusion, value in [[[aa, bb], cc, True],
                                           [[aa, bb], c, False],
                                           [[aa, b], cc, False],
                                           [[a, bb], cc, False]]:
        candidate = InferenceRule(assumptions, conclusion)
        if debug:
            print('Testing whether', candidate, 'is an instance of', rule)
        assert candidate.is_instance_of(rule) == value
        if value:
            map_ = {}
            assert candidate.is_instance_of(rule, map_)
            assert map_ == instantiation_map
            
    # Test 3
    a = Formula.from_infix('(p|q)')
    b = Formula.from_infix('(~p|r)')
    c = Formula.from_infix('(q|r)')
    aa = Formula.from_infix('((x1&x2)|((p|q)|r))')
    bb = Formula.from_infix('(~(x1&x2)|~y)')
    cc = Formula.from_infix('(((p|q)|r)|~y)')
    rule = InferenceRule([a, b], c)
    instantiation_map = {'p': Formula.from_infix('(x1&x2)'),
                         'q': Formula.from_infix('((p|q)|r)'),
                         'r': Formula.from_infix('~y')}
    for assumptions, conclusion, value in [[[aa, bb], cc, True],
                                           [[aa, bb], Formula.from_infix('(((p|q)|r)|r)'), False],
                                           [[aa, bb], c, False],
                                           [[aa, b], cc, False],
                                           [[a, bb], cc, False]]:
        candidate = InferenceRule(assumptions, conclusion)
        if debug:
            print('Testing whether', candidate, 'is an instance of', rule)
        assert candidate.is_instance_of(rule) == value
        if value:
            map_ = {}
            assert candidate.is_instance_of(rule, map_)
            assert map_ == instantiation_map

    # Test 4
    a = Formula.from_infix('((x->y)->x)')
    b = Formula.from_infix('((y->x)->y)')
    c = Formula.from_infix('y')
    aa = Formula.from_infix('((~x->x)->~x)')
    bb = Formula.from_infix('((x->~x)->x)')
    cc = Formula.from_infix('x')
    rule = InferenceRule([a, b], c)
    instantiation_map = {'x': Formula.from_infix('~x'),
                         'y': Formula.from_infix('x')}
    for assumptions, conclusion, value in [[[aa, bb], cc, True],
                                           [[bb, aa], cc, False],
                                           [[a, bb], cc, False],
                                           [[aa, b], cc, False],
                                           [[aa, bb], c, False]]:
        candidate = InferenceRule(assumptions, conclusion)
        if debug:
            print('Testing whether', candidate, 'is an instance of', rule)
        assert candidate.is_instance_of(rule) == value
        if value:
            map_ = {}
            assert candidate.is_instance_of(rule, map_)
            assert map_ == instantiation_map

    # Test 5
    a = Formula.from_infix('(((p&q)&p)&p)')
    b = Formula.from_infix('(((q&p)&q)&q)')
    c = Formula.from_infix('(p<->q)')
    aa = Formula.from_infix('((((p->F)&~p)&(p->F))&(p->F))')
    bb = Formula.from_infix('(((~p&(p->F))&~p)&~p)')
    cc = Formula.from_infix('((p->F)<->~p)')
    rule = InferenceRule([a, b], c)
    instantiation_map = {'p': Formula.from_infix('(p->F)'),
                         'q': Formula.from_infix('~p')}
    for assumptions, conclusion, value in [[[aa, bb], cc, True],
                                           [[bb, aa], cc, False],
                                           [[a, bb], cc, False],
                                           [[aa, b], cc, False],
                                           [[aa, bb], c, False]]:
        candidate = InferenceRule(assumptions, conclusion)
        if debug:
            print('Testing whether', candidate, 'is an instance of', rule)
        assert candidate.is_instance_of(rule) == value
        if value:
            map_ = {}
            assert candidate.is_instance_of(rule, map_)
            assert map_ == instantiation_map

# Two proofs for use in various tests below:

DISJUNCTION_COMMUTATIVITY_PROOF = DeductiveProof(
    InferenceRule([Formula.from_infix('(x|y)')], Formula.from_infix('(y|x)')),
    [InferenceRule([Formula.from_infix('(p|q)'), Formula.from_infix('(~p|r)')],
                   Formula.from_infix('(q|r)')),
     InferenceRule([], Formula.from_infix('(~p|p)'))],
    [DeductiveProof.Line(Formula.from_infix('(x|y)')),
     DeductiveProof.Line(Formula.from_infix('(~x|x)'), 1, []),
     DeductiveProof.Line(Formula.from_infix('(y|x)'), 0, [0, 1])])

DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF = DeductiveProof(
    InferenceRule([Formula.from_infix('((x|y)|z)')],
                  Formula.from_infix('(x|(y|z))')),
    [InferenceRule([Formula.from_infix('(x|y)')], Formula.from_infix('(y|x)')),
     InferenceRule([Formula.from_infix('(x|(y|z))')],
                   Formula.from_infix('((x|y)|z)'))],
    [DeductiveProof.Line(Formula.from_infix('((x|y)|z)')),
     DeductiveProof.Line(Formula.from_infix('(z|(x|y))'), 0, [0]),
     DeductiveProof.Line(Formula.from_infix('((z|x)|y)'), 1, [1]),
     DeductiveProof.Line(Formula.from_infix('(y|(z|x))'), 0, [2]),
     DeductiveProof.Line(Formula.from_infix('((y|z)|x)'), 1, [3]),
     DeductiveProof.Line(Formula.from_infix('(x|(y|z))'), 0, [4])])

# Tests for DeductiveProof:

def test_instance_for_line(debug=False):
    # Test over lines of DISJUNCTION_COMMUTATIVITY_PROOF
    for line, assumptions, conclusion in [[1, [], '(~x|x)'],
                                          [2, ['(x|y)', '(~x|x)'], '(y|x)']]:
        if debug:
            print('Testing instance for line', line,
                  'of the following deductive proof:\n' +
                  str(DISJUNCTION_COMMUTATIVITY_PROOF))
        assert DISJUNCTION_COMMUTATIVITY_PROOF.instance_for_line(line) == \
            InferenceRule([Formula.from_infix(a) for a in assumptions],
                          Formula.from_infix(conclusion))

    # Test over lines of DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF
    for line, assumptions, conclusion in [[1, ['((x|y)|z)'], '(z|(x|y))'],
                                          [2, ['(z|(x|y))'], '((z|x)|y)'],
                                          [3, ['((z|x)|y)'], '(y|(z|x))'],
                                          [4, ['(y|(z|x))'], '((y|z)|x)'],
                                          [5, ['((y|z)|x)'], '(x|(y|z))']]:
        if debug:
            print('Testing instance for line', line,
                  'of the following deductive proof:\n' +
                  str(DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF))
        assert DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF.instance_for_line(line) == \
               InferenceRule([Formula.from_infix(a) for a in assumptions],
                             Formula.from_infix(conclusion))

def test_is_valid(debug=False):
    # Test variations on DISJUNCTION_COMMUTATIVITY_PROOF

    proof = DISJUNCTION_COMMUTATIVITY_PROOF
    if debug:
        print('Testing validity of the following deductive proof:\n' + str(proof))
    assert proof.is_valid()

    proof = DeductiveProof(InferenceRule([Formula.from_infix('(x|y)')],
                                         Formula.from_infix('(x|y)')),
                           DISJUNCTION_COMMUTATIVITY_PROOF.rules,
                           DISJUNCTION_COMMUTATIVITY_PROOF.lines)
    if debug:
        print('Testing validity of the following deductive proof:\n' + str(proof))
    assert not proof.is_valid()

    proof = DeductiveProof(DISJUNCTION_COMMUTATIVITY_PROOF.statement,
                           [DISJUNCTION_COMMUTATIVITY_PROOF.rules[0],
                            InferenceRule([], Formula.from_infix('(~x|~x)'))],
                           DISJUNCTION_COMMUTATIVITY_PROOF.lines)
    if debug:
        print('Testing validity of the following deductive proof:\n' + str(proof))
    assert not proof.is_valid()

    proof = DeductiveProof(DISJUNCTION_COMMUTATIVITY_PROOF.statement,
                           DISJUNCTION_COMMUTATIVITY_PROOF.rules,
                           [DeductiveProof.Line(Formula.from_infix('(x|y)')),
                            DeductiveProof.Line(Formula.from_infix('(y|x)'),
                                                0, [0, 0])])
    if debug:
        print('Testing validity of the following deductive proof:\n' + str(proof))
    assert not proof.is_valid()

    # Test variations on DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF

    proof = DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF
    if debug:
        print('Testing validity of the following deductive proof:\n' + str(proof))
    assert proof.is_valid()

    proof = DeductiveProof(InferenceRule([Formula.from_infix('(x|y)')],
                                         Formula.from_infix('(y|x)')),
                           DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF.rules,
                           DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF.lines)
    if debug:
        print('Testing validity of the following deductive proof:\n' + str(proof))
    assert not proof.is_valid()

    proof = DeductiveProof(DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF.statement,
                           [DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF.rules[0],
                            InferenceRule([], Formula('F'))],
                           DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF.lines)
    if debug:
        print('Testing validity of the following deductive proof:\n' + str(proof))
    assert not proof.is_valid()

    proof = DeductiveProof(DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF.statement,
                           DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF.rules,
                           [DeductiveProof.Line(Formula.from_infix('((x|y)|z)')),
                            DeductiveProof.Line(Formula.from_infix('(x|(y|z))'),
                                                0, [0])])
    if debug:
        print('Testing validity of the following deductive proof:\n' + str(proof))
    assert not proof.is_valid()

# Tests for functions:

def test_instantiate(debug=True):
    for template_infix, instantiation_map_infix, instance_infix in [
            ['(~p|p)', {'p': 'q'}, '(~q|q)'],
            ['(~p|p)', {'p': 'p'}, '(~p|p)'],
            ['(~p|p)', {'p': 'p4'}, '(~p4|p4)'],
            ['(~p|p)', {'p': 'r7'}, '(~r7|r7)'],
            ['(~p|p)', {'p': '~(p|q)'}, '(~~(p|q)|~(p|q))'],
            ['~(x?((p->(q-&x))|((p-|y)<->(r&q))):y)',
             {'x': 'y', 'y': 'x', 'p': 'p', 'q': '(q?x:y)', 'r': '(r|q)'},
             '~(y?((p->((q?x:y)-&y))|((p-|x)<->((r|q)&(q?x:y)))):x)']]:
        template = Formula.from_infix(template_infix)
        instance = Formula.from_infix(instance_infix)
        instantiation_map = \
            {variable: Formula.from_infix(instantiation_map_infix[variable])
             for variable in instantiation_map_infix}
        if debug:
            print('Testing instantiation of', template,
                  'with instantiation map', instantiation_map)
        assert instantiate(template, instantiation_map) == instance

def test_prove_instance(debug=True):
    # Test instantiations of DISJUNCTION_COMMUTATIVITY_PROOF
    for instance_infix in [['(w|z)', '(z|w)'],
                           ['(p|q)', '(q|p)'],
                           ['(q|x)', '(x|q)'],
                           ['((p|y)|(~r|y))', '((~r|y)|(p|y))']]:
        instance = InferenceRule([Formula.from_infix(instance_infix[0])],
                                 Formula.from_infix(instance_infix[1]))
        if debug:
            print('Testing prove_instance for the instance',
                  str(instance) + '\nand the following proof:\n' +
                  str(DISJUNCTION_COMMUTATIVITY_PROOF))
        instance_proof = prove_instance(DISJUNCTION_COMMUTATIVITY_PROOF,
                                        instance)
        assert instance_proof.statement == instance
        assert instance_proof.rules == DISJUNCTION_COMMUTATIVITY_PROOF.rules
        # Will be tested with the course staff's implementation of is_valid()
        assert instance_proof.is_valid()

    # Test instantiations of DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF
    for instance_infix in [['((x|y)|z)', '(x|(y|z))'],
                           ['((p|q)|r)', '(p|(q|r))'],
                           ['((x|x)|x)', '(x|(x|x))'],
                           ['((~x|x)|(x|~x))', '(~x|(x|(x|~x)))'],
                           ['(((p->p)|(p|p))|(p&p))', '((p->p)|((p|p)|(p&p)))']]:
        instance = InferenceRule([Formula.from_infix(instance_infix[0])],
                                 Formula.from_infix(instance_infix[1]))
        if debug:
            print('Testing prove_instance for the instance',
                  str(instance) + '\nand the following proof:\n' +
                  str(DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF))
        instance_proof = prove_instance(DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF,
                                        instance)
        assert instance_proof.statement == instance
        assert instance_proof.rules == DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF.rules
        # Will be tested with the course staff's implementation of is_valid()
        assert instance_proof.is_valid()

def test_inline_proof(debug=True):
    lemma1_proof = DISJUNCTION_COMMUTATIVITY_PROOF
    lemma2_proof = DISJUNCTION_RIGHT_ASSOCIATIVITY_PROOF

    # A proof that uses both disjunction commutativity (lemma 1) and
    # disjunction right associativity (lemma2), whose proof in turn also uses
    # disjunction commutativity (lemma 1).
    proof = DeductiveProof(
        InferenceRule([Formula.from_infix('((p|q)|r)')],
                      Formula.from_infix('((r|p)|q)')),
        [InferenceRule([Formula.from_infix('((x|y)|z)')],
                       Formula.from_infix('(x|(y|z))')),
         InferenceRule([Formula.from_infix('(x|y)')],
                       Formula.from_infix('(y|x)')),
         InferenceRule([], Formula.from_infix('(~p|p)'))],
        [DeductiveProof.Line(Formula.from_infix('((p|q)|r)')),
         DeductiveProof.Line(Formula.from_infix('(p|(q|r))'), 0, [0]),
         DeductiveProof.Line(Formula.from_infix('((q|r)|p)'), 1, [1]),
         DeductiveProof.Line(Formula.from_infix('(q|(r|p))'), 0, [2]),
         DeductiveProof.Line(Formula.from_infix('((r|p)|q)'), 1, [3])])

    # Test inlining lemma1_proof into (lemma2_proof into proof)

    if debug:
        print('Testing inline_proof for the following main proof:\n' +
              str(proof) + '\nand the following lemma proof:\n' +
              str(lemma2_proof))
    inlined_proof = inline_proof(proof, lemma2_proof)
    assert inlined_proof.statement == proof.statement
    assert inlined_proof.rules == [proof.rules[1], proof.rules[2],
                                   lemma2_proof.rules[1]]
    # Will be tested with the course staff's implementation of is_valid()
    assert inlined_proof.is_valid()

    if debug:
        print('Testing inline_proof for the following main proof:\n' +
              str(inlined_proof) + '\nand the following lemma proof:\n' +
              str(lemma1_proof))
    inlined_proof = inline_proof(inlined_proof, lemma1_proof)
    assert inlined_proof.statement == proof.statement
    assert inlined_proof.rules == [proof.rules[2], lemma2_proof.rules[1],
                                   lemma1_proof.rules[0]]
    # Will be tested with the course staff's implementation of is_valid()
    assert inlined_proof.is_valid()

    # Test inlining lemma1_proof into (lemma2_proof into (lemma1_proof into proof))

    if debug:
        print('Testing inline_proof for the following main proof:\n' +
              str(proof) + '\nand the following lemma proof:\n' +
              str(lemma1_proof))
    inlined_proof = inline_proof(proof, lemma1_proof)
    assert inlined_proof.statement == proof.statement
    assert inlined_proof.rules == [proof.rules[0], proof.rules[2],
                                   lemma1_proof.rules[0]]
    # Will be tested with the course staff's implementation of is_valid()
    assert inlined_proof.is_valid()

    if debug:
        print('Testing inline_proof for the following main proof:\n' +
              str(inlined_proof) + '\nand the following lemma proof:\n' +
              str(lemma2_proof))
    inlined_proof = inline_proof(inlined_proof, lemma2_proof)
    assert inlined_proof.statement == proof.statement
    assert inlined_proof.rules == [proof.rules[2], lemma1_proof.rules[0],
                                   lemma2_proof.rules[0], lemma2_proof.rules[1]]
    # Will be tested with the course staff's implementation of is_valid()
    assert inlined_proof.is_valid()

    if debug:
        print('Testing inline_proof for the following main proof:\n' +
              str(inlined_proof) + '\nand the following lemma proof:\n' +
              str(lemma1_proof))
    inlined_proof = inline_proof(inlined_proof, lemma1_proof)
    assert inlined_proof.statement == proof.statement
    assert inlined_proof.rules == [proof.rules[2], lemma1_proof.rules[0],
                                   lemma2_proof.rules[1]]
    # Will be tested with the course staff's implementation of is_valid()
    assert inlined_proof.is_valid()

    # Test inlining (lemma1_proof into lemma2_proof) into (lemma1_proof into proof)

    inlined_proof = inline_proof(proof, lemma1_proof) # Already tested above

    if debug:
        print('Testing inline_proof for the following main proof:\n' +
              str(lemma2_proof) + '\nand the following lemma proof:\n',
              str(lemma1_proof))
    inlined_lemma = inline_proof(lemma2_proof, lemma1_proof)
    assert inlined_lemma.statement == lemma2_proof.statement
    assert inlined_lemma.rules == [lemma2_proof.rules[1], lemma1_proof.rules[0],
                                   lemma1_proof.rules[1]]
    # Will be tested with the course staff's implementation of is_valid()
    assert inlined_lemma.is_valid()

    if debug:
        print('Testing inline_proof for the following main proof:\n' +
              str(inlined_proof) + '\nand the following lemma proof:\n' +
              str(inlined_lemma))
    inlined_proof = inline_proof(inlined_proof, inlined_lemma)
    assert inlined_proof.statement == proof.statement
    assert inlined_proof.rules == [proof.rules[2], lemma1_proof.rules[0],
                                   lemma2_proof.rules[1]]
    # Will be tested with the course staff's implementation of is_valid()
    assert inlined_proof.is_valid()

    # Test inlining lemma1_proof into ((lemma1_proof into lemma2_proof) into proof)

    if debug:
        print('Testing inline_proof for the following main proof:\n' +
              str(proof) + '\nand the following lemma proof:\n' +
              str(inlined_lemma))
    inlined_proof = inline_proof(proof, inlined_lemma)
    assert inlined_proof.statement == proof.statement
    assert inlined_proof.rules == [proof.rules[1], proof.rules[2],
                                   lemma2_proof.rules[1], lemma1_proof.rules[0]]
    # Will be tested with the course staff's implementation of is_valid()
    assert inlined_proof.is_valid()

    if debug:
        print('Testing inline_proof for the following main proof:\n' +
              str(inlined_proof) + '\nand the following lemma proof:\n' +
              str(lemma1_proof))
    inlined_proof = inline_proof(inlined_proof, lemma1_proof)
    assert inlined_proof.statement == proof.statement
    assert inlined_proof.rules == [proof.rules[2], lemma2_proof.rules[1],
                                   lemma1_proof.rules[0]]
    # Will be tested with the course staff's implementation of is_valid()
    assert inlined_proof.is_valid()

def test_inline_proof_extended(debug=True):
    from code.propositions.provers import MP, I1, I2

    # Test inlining the proof of a lemma with two assumptions
    I2_decomposed = InferenceRule(
            [Formula.from_infix('(p->(q->r))'), Formula.from_infix('(p->q)')],
            Formula.from_infix('(p->r)'))
    I2_decomposed_proof = DeductiveProof(I2_decomposed, [MP, I1, I2],
        [DeductiveProof.Line(Formula.from_infix('(p->(q->r))')),
         DeductiveProof.Line(Formula.from_infix('(p->q)')),
         DeductiveProof.Line(Formula.from_infix('((p->(q->r))->((p->q)->(p->r)))'), 2, []),
         DeductiveProof.Line(Formula.from_infix('((p->q)->(p->r))'), 0, [0, 2]),
         DeductiveProof.Line(Formula.from_infix('(p->r)'), 0, [1, 3])])

    statement = InferenceRule([Formula.from_infix('((x|y)->(z->r))'),
                               Formula.from_infix('((x|y)->z)')],
                              Formula.from_infix('((x|y)->r)'))
    proof = DeductiveProof(statement, [I2_decomposed],
        [DeductiveProof.Line(Formula.from_infix('((x|y)->(z->r))')),
         DeductiveProof.Line(Formula.from_infix('((x|y)->z)')),
         DeductiveProof.Line(Formula.from_infix('((x|y)->r)'), 0, [0, 1])])
    if debug:
        print('Testing inline_proof for the following main proof:\n' +
              str(proof) + '\nand the following lemma proof:\n' +
              str(I2_decomposed_proof))
    inlined_proof = inline_proof(proof, I2_decomposed_proof)
    assert inlined_proof.statement == proof.statement
    assert inlined_proof.rules == [MP, I1, I2]
    # Will be tested with the course staff's implementation of is_valid()
    assert inlined_proof.is_valid()

    # Test inlining the proof of a lemma with no assumptions
    I1_renamed = InferenceRule([], Formula.from_infix('(x->(y->x))'))
    I1_renamed_degenerate_proof = DeductiveProof(I1_renamed, [I1],
                                                 [DeductiveProof.Line(I1_renamed.conclusion, 0, [])])
    proof = DeductiveProof(
        InferenceRule([Formula('p')], Formula.from_infix('(q->p)')), [MP, I1_renamed],
        [DeductiveProof.Line(Formula('p')),
         DeductiveProof.Line(Formula.from_infix('(p->(q->p))'), 1, []),
         DeductiveProof.Line(Formula.from_infix('(q->p)'), 0, [0, 1])])
    if debug:
        print('Testing inline_proof for the following main proof:\n' +
              str(proof) + '\nand the following lemma proof:\n' +
              str(I1_renamed_degenerate_proof))
    inlined_proof = inline_proof(proof, I1_renamed_degenerate_proof)
    assert inlined_proof.statement == proof.statement
    assert inlined_proof.rules == [MP, I1]
    # Will be tested with the course staff's implementation of is_valid()
    assert inlined_proof.is_valid()
