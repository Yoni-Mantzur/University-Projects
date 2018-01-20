""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/test_ex6.py """

from code.propositions.tautology_test import *

def test_task1(debug=False):
    test_prove_in_model_implies_not(debug)

def test_task2(debug=False):
    test_reduce_assumption(debug)

def test_task3(debug=False):
    test_proof_or_counterexample_implies_not(debug)

def test_task4(debug=False):
    test_prove_in_model(debug)

def test_task5(debug=False):
    test_proof_or_counterexample(debug)

def test_task6(debug=False):
    test_proof_or_counterexample_for_inference(debug)

def test_task7(debug=False):
    test_model_or_inconsistent(debug)

test_task1(True)
test_task2(True)
test_task3(True)
test_task4(True)
test_task5(True)
test_task6(True)
test_task7(True)
