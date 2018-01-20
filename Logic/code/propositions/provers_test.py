""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/propositions/provers_test.py """

from code.propositions.syntax import *
from code.propositions.semantics import *
from code.propositions.proofs import *
from code.propositions.provers import *

def test_prove_implies_self(debug=True):
    if debug:
        print('Testing prove_implies_self')
    proof = prove_implies_self()
    assert proof.statement.assumptions == []
    assert proof.statement.conclusion == Formula.from_infix('(p->p)')
    assert proof.rules == [MP, I1, I2]
    # Will be tested with the course staff's implementation of is_valid
    assert proof.is_valid()

def test_inverse_mp(debug=True):
    # Test 1
    proof = DeductiveProof(
        InferenceRule([Formula.from_infix('(x|y)')], Formula.from_infix('(y|x)')),
        [MP, I1, I2,
         InferenceRule([], Formula.from_infix('((p|q)->((~p|r)->(q|r)))')),
         InferenceRule([], Formula.from_infix('(~p|p)'))],
        [DeductiveProof.Line(Formula.from_infix('(x|y)')),
         DeductiveProof.Line(Formula.from_infix('((x|y)->((~x|x)->(y|x)))'), 3, []),
         DeductiveProof.Line(Formula.from_infix('((~x|x)->(y|x))'), 0, [0, 1]),
         DeductiveProof.Line(Formula.from_infix('(~x|x)'), 4, []),
         DeductiveProof.Line(Formula.from_infix('(y|x)'), 0, [3, 2])])
    assumption = proof.statement.assumptions[0]
    if debug:
        print('Testing inverse_mp for assumption', assumption,
              'of the following proof:', proof)
    implication_proof = inverse_mp(proof, assumption)
    assert implication_proof.statement.assumptions == []
    assert implication_proof.statement.conclusion == \
           Formula.from_infix('((x|y)->(y|x))')
    assert implication_proof.rules == proof.rules
    # Will be tested with the course staff's implementation of is_valid
    assert implication_proof.is_valid()

    # Test 2
    proof = DeductiveProof(
        InferenceRule([Formula.from_infix('((p|q)|r)')],
                      Formula.from_infix('((r|p)|q)')),
        [MP, I1, I2,
         InferenceRule([], Formula.from_infix('(((x|y)|z)->(x|(y|z)))')),
         InferenceRule([], Formula.from_infix('((x|y)->(y|x))')),
         InferenceRule([], Formula.from_infix('(~p|p)'))],
        [DeductiveProof.Line(Formula.from_infix('((p|q)|r)')),
         DeductiveProof.Line(Formula.from_infix('(((p|q)|r)->(p|(q|r)))'), 3, []),
         DeductiveProof.Line(Formula.from_infix('(p|(q|r))'), 0, [0, 1]),
         DeductiveProof.Line(Formula.from_infix('((p|(q|r))->((q|r)|p))'), 4, []),
         DeductiveProof.Line(Formula.from_infix('((q|r)|p)'), 0, [2, 3]),
         DeductiveProof.Line(Formula.from_infix('(((q|r)|p)->(q|(r|p)))'), 3, []),
         DeductiveProof.Line(Formula.from_infix('(q|(r|p))'), 0, [4, 5]),
         DeductiveProof.Line(Formula.from_infix('((q|(r|p))->((r|p)|q))'), 4, []),
         DeductiveProof.Line(Formula.from_infix('((r|p)|q)'), 0, [6, 7])])
    assumption = proof.statement.assumptions[0]
    if debug:
        print('Testing inverse_mp for assumption', assumption,
              'of the following proof:', proof)
    implication_proof = inverse_mp(proof, assumption)
    assert implication_proof.statement.assumptions == []
    assert implication_proof.statement.conclusion == \
           Formula.from_infix('(((p|q)|r)->((r|p)|q))')
    assert implication_proof.rules == proof.rules
    # Will be tested with the course staff's implementation of is_valid
    assert implication_proof.is_valid()

    # Test 3: sequential elimination of two assumptions in both possible orders
    proof = DeductiveProof(
        InferenceRule([Formula.from_infix('(x&~y)'),
                       Formula.from_infix('(z->y)')],
                      Formula.from_infix('~z')),
        [MP, I1, I2, A3,
         InferenceRule([], Formula.from_infix('((p->q)->(~q->~p))'))],
        [DeductiveProof.Line(Formula.from_infix('(x&~y)')),
         DeductiveProof.Line(Formula.from_infix('(z->y)')),
         DeductiveProof.Line(Formula.from_infix('((x&~y)->~y)'), 3, []),
         DeductiveProof.Line(Formula.from_infix('~y'), 0, [0, 2]),
         DeductiveProof.Line(Formula.from_infix('((z->y)->(~y->~z))'), 4, []),
         DeductiveProof.Line(Formula.from_infix('(~y->~z)'), 0, [1, 4]),
         DeductiveProof.Line(Formula.from_infix('~z'), 0, [3, 5])])

    for elimination_order in [[0,1], [1,0]]:
        assumption = proof.statement.assumptions[elimination_order[0]]
        if debug:
            print('Testing inverse_mp for assumption', assumption,
                  'of the following proof:', proof)
        implication_proof = inverse_mp(proof, assumption)
        assert implication_proof.statement.assumptions == \
               [proof.statement.assumptions[elimination_order[1]]]
        assert implication_proof.statement.conclusion == \
               Formula('->', assumption, proof.statement.conclusion)
        assert implication_proof.rules == proof.rules
        # Will be tested with the course staff's implementation of is_valid
        assert implication_proof.is_valid()

        assumption = proof.statement.assumptions[elimination_order[1]]
        if debug:
            print('Testing inverse_mp for assumption', assumption,
                  'of the following proof:', implication_proof)
        double_implication_proof = inverse_mp(implication_proof, assumption)
        assert double_implication_proof.statement.assumptions == []
        assert double_implication_proof.statement.conclusion == \
               Formula('->', assumption, implication_proof.statement.conclusion)
        assert double_implication_proof.rules == proof.rules
        # Will be tested with the course staff's implementation of is_valid
        assert double_implication_proof.is_valid()

def test_prove_hypothetical_syllogism(debug=False):
    if debug:
        print('Testing prove_hypothetical_syllogism')
    proof = prove_hypothetical_syllogism()
    assert proof.statement.assumptions == [Formula.from_infix('(p->q)'),
                                           Formula.from_infix('(q->r)')]
    assert proof.statement.conclusion == Formula.from_infix('(p->r)')
    assert proof.rules == [MP, I1, I2]
    # Will be tested with the course staff's implementation of is_valid
    assert proof.is_valid()
