""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/test_ex3.py """

from code.propositions.syntax_test import *
from code.propositions.semantics_test import *
from code.propositions.operators_test import *
from code.tests import *

MAX_TASK_TESTING_TIME = 30

def test_task1(debug=False):
    test_infix(debug)
    test_infix_all_operators(debug)
    test_from_infix(debug)
    test_from_infix_all_operators(debug)
    test_prefix(debug)
    test_prefix_all_operators(debug)
    test_from_prefix(debug)
    test_from_prefix_all_operators(debug)
    test_variables(debug)
    test_variables_all_operators(debug)

def test_task2(debug=False):
    test_evaluate(debug)
    test_evaluate_all_operators(debug)
    test_truth_values(debug)
    test_truth_values_all_operators(debug)
    test_is_tautology(debug)
    test_is_tautology_all_operators(debug)
    test_print_truth_table(debug)
    test_print_truth_table_all_operators(debug)

def test_task3(debug=False):
    test_to_not_and_or(debug)

def test_task4(debug=False):
    test_to_not_and(debug)
    test_synthesize_not_and(debug)

def test_task5(debug=False):
    test_to_implies_false(debug)
    test_synthesize_implies_false(debug)

def test_task6(debug=False):
    test_to_nand(debug)
    test_synthesize_nand(debug)

def test_task7(debug=False):
    test_to_nor(debug)
    test_synthesize_nor(debug)

def test_task8(debug=False):
    test_to_mux(debug)
    test_synthesize_mux(debug)

test_task1(True)
test_task2(True)
test_task_timed(MAX_TASK_TESTING_TIME, test_task3, True)
test_task_timed(MAX_TASK_TESTING_TIME, test_task4, True)
test_task_timed(MAX_TASK_TESTING_TIME, test_task5, True)
test_task_timed(MAX_TASK_TESTING_TIME, test_task6, True)
test_task_timed(MAX_TASK_TESTING_TIME, test_task7, True)
test_task_timed(MAX_TASK_TESTING_TIME, test_task8, True)
