""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/test_ex7.py """

from code.predicates.syntax_test import *
from code.predicates.semantics_test import *

def test_task1(debug=False):
    test_term_repr(debug)

def test_task2(debug=False):
    test_formula_repr(debug)

def test_task3(debug=False):
    test_term_parse_prefix(debug)
    test_term_parse(debug)

def test_task4(debug=False):
    test_formula_parse_prefix(debug)
    test_formula_parse(debug)

def test_task5(debug=False):
    test_variables(debug)

def test_task6(debug=False):
    test_free_variables(debug)

def test_task7(debug=False):
    test_evaluate_term(debug)

def test_task8(debug=False):
    test_evaluate_formula(debug)

def test_task9(debug=False):
    test_is_model_of(debug)

test_task1(True)
test_task2(True)
test_task3(True)
test_task4(True)
test_task5(True)
test_task6(True)
test_task7(True)
test_task8(True)
test_task9(True)
