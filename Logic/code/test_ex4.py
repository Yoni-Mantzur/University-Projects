from code.propositions.proofs_test import *
from code.propositions.semantics_test import *

def test_task1(debug=False):
    test_variables(debug)

def test_task2(debug=False):
    test_evaluate_inference(debug)

def test_task3(debug=False):
    test_is_tautological_inference(debug)

def test_task4(debug=False):
    test_update_instantiation_map(debug)
    test_is_instance_of(debug)

def test_task5(debug=False):
    test_instance_for_line(debug)

def test_task6(debug=False):
    test_is_valid(debug)

test_task1(True)
test_task2(True)
test_task3(True)
test_task4(True)
test_task5(True)
test_task6(True)
