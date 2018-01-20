""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/test_ex1.py """

from code.propositions.syntax_test import *

def test_task1(debug=False):
    test_infix(debug)

def test_task2(debug=False):
    test_from_infix(debug)

def test_task3(debug=False):
    test_prefix(debug)

def test_task4(debug=False):
    test_from_prefix(debug)

def test_task5(debug=False):
    test_variables(debug)

test_task1(True)
test_task2(True)
test_task3(True)
test_task4(True)
test_task5(True)
