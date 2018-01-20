""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/test_ex11.py """

from code.predicates.deduction_test import *
from code.predicates.prenex_test import *

def test_task1(debug=False):
    test_inverse_mp(debug)

def test_task2(debug=False):
    test_proof_by_contradiction(debug)

def test_task3(debug=False):
    test_is_quantifier_free(debug)
    test_is_in_prenex_normal_form(debug)

def test_task4(debug=False):
    test_make_quantified_variables_unique(debug)

def test_task5(debug=False):
    test_pull_out_quantifications_across_negation(debug)

def test_task6(debug=False):
    test_pull_out_quantifications_from_left_across_binary_operator(debug)
    test_pull_out_quantifications_from_right_across_binary_operator(debug)

def test_task7(debug=False):
    test_pull_out_quantifications_across_binary_operator(debug)

def test_task8(debug=False):
    test_to_prenex_normal_form_from_unique_quantified_variables(debug)

def test_task9(debug=False):
    test_to_prenex_normal_form(debug)

test_task1(True)
test_task2(True)
test_task3(True)
test_task4(True)
test_task5(True)
test_task6(True)
test_task7(True)
test_task8(True)
test_task9(True)
