""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/test_ex8.py """

from code.predicates.syntax_test import *
from code.predicates.functions_test import *

def test_task1(debug=False):
    test_term_functions(debug)
    test_formula_functions(debug)
    test_relations(debug)

def test_task2(debug=False):
    test_replace_functions_with_relations_in_model(debug)

def test_task3(debug=False):
    test_replace_relations_with_functions_in_model(debug)

def test_task4(debug=False):
    test_compile_term(debug)

def test_task5(debug=False):
    test_replace_functions_with_relations_in_formula(debug)

def test_task6(debug=False):
    test_replace_functions_with_relations_in_formulae(debug)

def test_task7(debug=False):
    test_replace_equality_with_SAME(debug)

def test_task8(debug=False):
    test_add_SAME_as_equality(debug)

def test_task9(debug=False):
    test_make_equality_as_SAME(debug)

test_task1(True)
test_task2(True)
test_task3(True)
test_task4(True)
test_task5(True)
test_task6(True)
test_task7(True)
test_task8(True)
test_task9(True)
