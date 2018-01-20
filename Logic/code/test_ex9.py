""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/test_ex9.py """

from code.predicates.syntax_test import *
from code.predicates.proofs_test import *

def test_task1(debug=False):
    test_term_substitute(debug)

def test_task2(debug=False):
    test_formula_substitute(debug)

def test_task3(debug=False):
    test_instantiate_formula(debug)

def test_task4(debug=False):
    test_instantiate(debug)

def test_task5(debug=False):
    test_verify_a_justification(debug)

def test_task6(debug=False):
    test_skeleton(debug)

def test_task7(debug=False):
    test_verify_t_justification(debug)

def test_task8(debug=False):
    test_verify_mp_justification(debug)

def test_task9(debug=False):
    test_verify_ug_justification(debug)

def test_combined(debug=False):
    test_is_valid(debug)

test_task1(True)
test_task2(True)
test_task3(True)
test_task4(True)
test_task5(True)
test_task6(True)
test_task7(True)
test_task8(True)
test_task9(True)
test_combined(True)
