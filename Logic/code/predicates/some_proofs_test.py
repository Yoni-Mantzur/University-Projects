""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/predicates/some_proofs_test.py """

from code.predicates.some_proofs import *

def test_lovers_proof(debug=True):
    proof = lovers_proof(debug)
    assert proof.assumptions == \
           Prover.AXIOMS + [Schema('Ax[Ey[Loves(x,y)]]'),
                            Schema('Ax[Az[Ay[(Loves(x,y)->Loves(z,x))]]]')]
    assert str(proof.conclusion) == 'Ax[Az[Loves(z,x)]]'
    # Will be tested with the course staff's implementation of is_valid
    assert proof.is_valid()

def test_homework_proof(debug=True):
    proof = homework_proof(debug)
    assert proof.assumptions == \
           Prover.AXIOMS + [Schema('~Ex[(Homework(x)&Fun(x))]'),
                            Schema('Ex[(Homework(x)&Reading(x))]')]
    assert str(proof.conclusion) == 'Ex[(Reading(x)&~Fun(x))]'
    # Will be tested with the course staff's implementation of is_valid
    assert proof.is_valid()

def test_unique_zero_proof(debug=True):
    proof = unique_zero_proof(debug)
    assert proof.assumptions == \
           Prover.AXIOMS + [Schema(a) for a in GROUP_AXIOMS] + \
           [Schema('plus(a,c)=a')]
    assert str(proof.conclusion) == 'c=0'
    # Will be tested with the course staff's implementation of is_valid
    assert proof.is_valid()

def test_multiply_zero_proof(debug=True):
    proof = multiply_zero_proof(debug)
    assert proof.assumptions == \
           Prover.AXIOMS + [Schema(a) for a in FIELD_AXIOMS]
    assert str(proof.conclusion) == 'times(0,x)=0'
    # Will be tested with the course staff's implementation of is_valid
    assert proof.is_valid()

def test_peano_zero_proof(debug=True):
    proof = peano_zero_proof(debug)
    assert proof.assumptions == \
           Prover.AXIOMS + \
           [Schema(a) if type(a) is str else a for a in PEANO_AXIOMS]
    assert str(proof.conclusion) == 'plus(0,x)=x'
    # Will be tested with the course staff's implementation of is_valid
    assert proof.is_valid()

def test_russell_paradox_proof(debug=True):
    proof = russell_paradox_proof(debug)
    assert proof.assumptions == Prover.AXIOMS + [COMPREHENSION_AXIOM]
    assert str(proof.conclusion) == '(z=z&~z=z)'
    # Will be tested with the course staff's implementation of is_valid
    assert proof.is_valid()


