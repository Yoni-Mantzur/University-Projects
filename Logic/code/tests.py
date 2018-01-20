""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/tests.py """

import time

def test_task_timed(max_testing_time, test_task, debug=False):
    if debug:
        print('Timing the execution of', test_task.__qualname__ + ':')
    start_time = time.process_time()
    test_task(debug)
    testing_time = time.process_time() - start_time
    if debug:
        print('Executing', test_task.__qualname__, 'took', testing_time, 'seconds')
        print()
    assert testing_time < max_testing_time, \
           'Maximum allowed task testing time (' + str(max_testing_time) + \
               ' seconds) exceeded'
