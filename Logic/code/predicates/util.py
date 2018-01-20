""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/predicates/util.py """

def __prefix_with_index_sequence_generator(prefix):
    """ A generator for a sequence of the form 'z1', 'z2', 'z3', ..., where the
        prefix 'z' is customizable """
    i=0
    while True:
        i = i+1
        yield prefix+str(i)


""" A generator for fresh variables names. The first call to: 
    next(fresh_variable_name_generator)
    will return 'z1', the second call to:
    next(fresh_variable_name_generator)
    will return 'z2', and so on. """
fresh_variable_name_generator = __prefix_with_index_sequence_generator('z')

""" A generator for fresh constant names. The first call to: 
    next(fresh_constant_name_generator)
    will return 'c1', the second call to:
    next(fresh_constant_name_generator)
    will return 'c2', and so on. """
fresh_constant_name_generator = __prefix_with_index_sequence_generator('c')
