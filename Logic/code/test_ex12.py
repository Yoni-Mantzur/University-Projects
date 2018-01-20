""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/test_ex12.py """

from code.predicates.completeness_test import *

def test_task1(debug=True):
    test_is_primitively_closed(debug)
    test_is_universally_closed(debug)
    test_is_existentially_closed(debug)

def test_task2(debug=False):
    test_find_unsatisfied_quantifier_free_sentence(debug)

def test_task3(debug=False):
    test_model_or_inconsistent(debug)

def test_task4(debug=False):
    test_combine_contradictions(debug)

def test_task5(debug=False):
    test_eliminate_universal_instance_assumption(debug)

def test_task6(debug=False):
    test_universally_close(debug)

def test_task7(debug=False):
    test_replace_constant(debug)

def test_task8(debug=False):
    test_eliminate_existential_witness_assumption(debug)

def test_task9(debug=False):
    test_existentially_close(debug)

test_task1(True)
test_task2(True)
test_task3(True)
test_task4(True)
test_task5(True)
test_task6(True)
test_task7(True)
test_task8(True)
test_task9(True)
