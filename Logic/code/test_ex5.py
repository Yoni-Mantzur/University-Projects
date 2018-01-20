""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/test_ex5.py """

from code.propositions.proofs_test import *
from code.propositions.provers_test import *

def test_task1(debug=False):
    test_prove_implies_self(debug)

def test_task2(debug=False):
    test_instantiate(debug)
    test_prove_instance(debug)
    test_inline_proof(debug)
    test_inline_proof_extended(debug)

def test_task3(debug=False):
    test_inverse_mp(debug)

def test_task4(debug=False):
    test_prove_hypothetical_syllogism(debug)

test_task1(True)
test_task2(True)
test_task3(True)
test_task4(True)
