""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/predicates/prover_test.py """

from code.predicates.prover import *

# Proofs used in the tests below

def syllogism_proof(print_as_proof_forms=False):
    """ Return a proof that from the assumptions (in addition to Prover.AXIOMS):
        1) All men are mortal, and
        2) Socrates is a man
        derives the conclusion:
        Socrates is mortal.
        The Boolean flag print_as_proof_forms specifies whether the proof being
        constructed is to be printed in real time as it is being constructed """
    prover = Prover(['Ax[(Man(x)->Mortal(x))]', 'Man(aristotle)'],
                    'Mortal(aristotle)', print_as_proof_forms)
    step1 = prover.add_assumption('Ax[(Man(x)->Mortal(x))]')
    step2 = prover.add_instantiated_assumption(
        '(Ax[(Man(x)->Mortal(x))]->(Man(aristotle)->Mortal(aristotle)))',
        Prover.UI, {'R(v)':'(Man(v)->Mortal(v))','c':'aristotle'})
    step3 = prover.add_mp('(Man(aristotle)->Mortal(aristotle))', step1, step2)
    step4 = prover.add_assumption('Man(aristotle)')
    step5 = prover.add_mp('Mortal(aristotle)', step4, step3)
    return prover.proof

def syllogism_proof_with_universal_instantiation(print_as_proof_forms=False):
    """ Return a proof, constructed using the method
        Prover.add_universal_instantiation, that from the assumptions (in
        addition to Prover.AXIOMS):
        1) All men are mortal, and
        2) Socrates is a man
        derives the conclusion:
        Socrates is mortal.
        The Boolean flag print_as_proof_forms specifies whether the proof being
        constructed is to be printed in real time as it is being constructed """
    prover = Prover(['Ax[(Man(x)->Mortal(x))]', 'Man(aristotle)'],
                    'Mortal(aristotle)', print_as_proof_forms)
    step1 = prover.add_assumption('Ax[(Man(x)->Mortal(x))]')
    step2 = prover.add_universal_instantiation(
        '(Man(aristotle)->Mortal(aristotle))', step1, 'aristotle')
    step3 = prover.add_assumption('Man(aristotle)')
    step4 = prover.add_mp('Mortal(aristotle)', step3, step2)
    return prover.proof

def syllogism_all_all_proof(print_as_proof_forms=False):
    """ Return a proof that from the assumptions (in addition to Prover.AXIOMS):
        1) All greeks are human, and
        2) All humans are mortal
        derives the conclusion:
        All Greeks are mortal.
        The Boolean flag print_as_proof_forms specifies whether the proof being
        constructed is to be printed in real time as it is being constructed """
    prover = Prover(['Ax[(Greek(x)->Human(x))]', 'Ax[(Human(x)->Mortal(x))]'],
                     'Ax[(Greek(x)->Mortal(x))]', print_as_proof_forms)
    step1 = prover.add_assumption('Ax[(Greek(x)->Human(x))]')
    step2 = prover.add_universal_instantiation(
        '(Greek(x)->Human(x))', step1, 'x')
    step3 = prover.add_assumption('Ax[(Human(x)->Mortal(x))]')
    step4 = prover.add_universal_instantiation(
        '(Human(x)->Mortal(x))', step3, 'x')
    step5 = prover.add_tautology(
        '((Greek(x)->Human(x))->((Human(x)->Mortal(x))->(Greek(x)->Mortal(x))))')
    step6 = prover.add_mp('((Human(x)->Mortal(x))->(Greek(x)->Mortal(x)))', step2, step5)
    step7 = prover.add_mp('(Greek(x)->Mortal(x))', step4, step6)
    step8 = prover.add_ug('Ax[(Greek(x)->Mortal(x))]', step7)
    return prover.proof

def syllogism_all_all_proof_with_tautological_inference(print_as_proof_forms=False):
    """ Return a proof, constructed using the method
        Prover.add_tautological_inference, that from the assumptions (in
        addition to Prover.AXIOMS):
        1) All greeks are human, and
        2) All humans are mortal
        derives the conclusion:
        All Greeks are mortal.
        The Boolean flag print_as_proof_forms specifies whether the proof being
        constructed is to be printed in real time as it is being constructed """
    prover = Prover(['Ax[(Greek(x)->Human(x))]', 'Ax[(Human(x)->Mortal(x))]'],
                     'Ax[(Greek(x)->Mortal(x))]', print_as_proof_forms)
    step1 = prover.add_assumption('Ax[(Greek(x)->Human(x))]')
    step2 = prover.add_universal_instantiation('(Greek(x)->Human(x))', step1,
                                               'x')
    step3 = prover.add_assumption('Ax[(Human(x)->Mortal(x))]')
    step4 = prover.add_universal_instantiation('(Human(x)->Mortal(x))', step3,
                                               'x')
    step5 = prover.add_tautological_inference('(Greek(x)->Mortal(x))',
                                              [step2, step4])
    step6 = prover.add_ug('Ax[(Greek(x)->Mortal(x))]', step5)
    return prover.proof

def syllogism_all_exists_proof(print_as_proof_forms=False):
    """ Return a proof that from the assumptions (in addition to Prover.AXIOMS):
        1) All men are mortal, and
        2) Some men exist
        derives the conclusion:
        Some mortals exist.
        The Boolean flag print_as_proof_forms specifies whether the proof being
        constructed is to be printed in real time as it is being constructed """
    prover = Prover(['Ax[(Man(x)->Mortal(x))]', 'Ex[Man(x)]'], 'Ex[Mortal(x)]',
                    print_as_proof_forms)
    step1 = prover.add_assumption('Ax[(Man(x)->Mortal(x))]')
    step2 = prover.add_assumption('Ex[Man(x)]')
    step3 = prover.add_universal_instantiation('(Man(x)->Mortal(x))', step1,
                                               'x')
    step4 = prover.add_instantiated_assumption(
        '(Mortal(x)->Ex[Mortal(x)])', Prover.EI,
        {'R(v)':'Mortal(v)', 'c':'x'})
    step5 = prover.add_tautological_inference('(Man(x)->Ex[Mortal(x)])',
                                              [step3, step4])
    step6 = prover.add_ug('Ax[(Man(x)->Ex[Mortal(x)])]', step5)
    step7 = prover.add_instantiated_assumption(
        '((Ax[(Man(x)->Ex[Mortal(x)])]&Ex[Man(x)])->Ex[Mortal(x)])', Prover.ES,
        {'R(v)':'Man(v)', 'Q()':'Ex[Mortal(x)]'})
    step8 = prover.add_tautological_inference('Ex[Mortal(x)]',
                                              [step2, step6, step7])
    return prover.proof

def syllogism_all_exists_proof_with_existential_derivation(print_as_proof_forms=False):
    """ Return a proof, constructed using the method
        Prover.add_existential_derivation, that from the assumptions (in
        addition to Prover.AXIOMS):
        1) All men are mortal, and
        2) Some men exist
        derives the conclusion:
        Some mortals exist.
        The Boolean flag print_as_proof_forms specifies whether the proof being
        constructed is to be printed in real time as it is being constructed """
    prover = Prover(['Ax[(Man(x)->Mortal(x))]', 'Ex[Man(x)]'], 'Ex[Mortal(x)]',
                    print_as_proof_forms)
    step1 = prover.add_assumption('Ax[(Man(x)->Mortal(x))]')
    step2 = prover.add_assumption('Ex[Man(x)]')
    step3 = prover.add_universal_instantiation('(Man(x)->Mortal(x))', step1,
                                               'x')
    step4 = prover.add_instantiated_assumption(
        '(Mortal(x)->Ex[Mortal(x)])', Prover.EI, {'R(v)':'Mortal(v)', 'c':'x'})
    step5 = prover.add_tautological_inference('(Man(x)->Ex[Mortal(x)])',
                                              [step3, step4])
    step6 = prover.add_existential_derivation('Ex[Mortal(x)]', step2, step5)
    return prover.proof

def right_neutral_proof(stop_before_flipped_equality,
                        stop_before_free_instantiation,
                        stop_before_substituted_equality,
                        stop_before_chained_equality,
                        print_as_proof_forms=False):
    """ Return a proof that from the group axioms (in addition to Prover.AXIOMS)
        proves x+0=x. If the Boolean flag step_before_flipped_equality is True,
        then construction of the proof (including verification of all
        justifications) is stopped just before the first call to
        Prover.add_flipped_equality, and None is returned. If the Boolean flag
        stop_before_free_instantiation is True, then construction of the proof
        (including verification of all justifications) is stopped just before
        the first call to Prover.add_free_instantiation, and None is returned.
        If the Boolean flag stop_before_substituted_equality is True, then
        construction of the proof (including verification of all
        justifications) is stopped just before the first call to
        Prover.add_substituted_equality, and None is returned. If the Boolean
        flag stop_before_chained_equality is True, then construction of the
        proof (including verification of all justifications) is stopped just
        before the (first) call to Prover.add_chained_equality, and None is
        returned. The Boolean flag print_as_proof_forms specifies whether the
        proof being constructed is to be printed in real time as it is being
        constructed """

    from code.predicates.some_proofs import GROUP_AXIOMS

    prover = Prover(GROUP_AXIOMS, 'plus(x,0)=x', print_as_proof_forms)
    zero = prover.add_assumption('plus(0,x)=x')
    negation = prover.add_assumption('plus(minus(x),x)=0')
    associativity = prover.add_assumption('plus(plus(x,y),z)=plus(x,plus(y,z))')
    if stop_before_flipped_equality:
        return None
    flipped_zero = prover.add_flipped_equality('x=plus(0,x)', zero)
    flipped_negation = prover.add_flipped_equality('0=plus(minus(x),x)',
                                                   negation)
    flipped_associativity = prover.add_flipped_equality(
        'plus(x,plus(y,z))=plus(plus(x,y),z)', associativity)
    if stop_before_free_instantiation:
        return None
    step7 = prover.add_free_instantiation(
        '0=plus(minus(minus(x)),minus(x))', flipped_negation, {'x':'minus(x)'})
    step8 = prover.add_flipped_equality('plus(minus(minus(x)),minus(x))=0',
                                        step7)
    step9 = prover.add_free_instantiation(
        'plus(plus(minus(minus(x)),minus(x)),x)=plus(minus(minus(x)),plus(minus(x),x))',
        associativity, {'x':'minus(minus(x))','y':'minus(x)','z':'x'})
    step10 = prover.add_free_instantiation('plus(0,0)=0', zero, {'x':'0'})
    step11 = prover.add_free_instantiation('plus(x,0)=plus(0,plus(x,0))',
                                           flipped_zero, {'x':'plus(x,0)'})
    step12 = prover.add_free_instantiation(
        'plus(0,plus(x,0))=plus(plus(0,x),0)', flipped_associativity,
        {'x':'0','y':'x','z':'0'})
    if stop_before_substituted_equality:
        return None
    step13 = prover.add_substituted_equality(
        'plus(plus(0,x),0)=plus(plus(plus(minus(minus(x)),minus(x)),x),0)',
        step7, 'plus(plus(v,x),0)')
    step14 = prover.add_substituted_equality(
        'plus(plus(plus(minus(minus(x)),minus(x)),x),0)=plus(plus(minus(minus(x)),plus(minus(x),x)),0)',
        step9, 'plus(v,0)')
    step15 = prover.add_substituted_equality(
        'plus(plus(minus(minus(x)),plus(minus(x),x)),0)=plus(plus(minus(minus(x)),0),0)',
        negation, 'plus(plus(minus(minus(x)),v),0)')
    step16 = prover.add_free_instantiation(
        'plus(plus(minus(minus(x)),0),0)=plus(minus(minus(x)),plus(0,0))',
        associativity, {'x':'minus(minus(x))', 'y':'0', 'z':'0'})
    step17 = prover.add_substituted_equality(
        'plus(minus(minus(x)),plus(0,0))=plus(minus(minus(x)),0)',
        step10, 'plus(minus(minus(x)),v)')
    step18 = prover.add_substituted_equality(
        'plus(minus(minus(x)),0)=plus(minus(minus(x)),plus(minus(x),x))',
        flipped_negation, 'plus(minus(minus(x)),v)')
    step19 = prover.add_free_instantiation(
        'plus(minus(minus(x)),plus(minus(x),x))=plus(plus(minus(minus(x)),minus(x)),x)',
        flipped_associativity, {'x':'minus(minus(x))','y':'minus(x)','z':'x'})
    step20 = prover.add_substituted_equality(
        'plus(plus(minus(minus(x)),minus(x)),x)=plus(0,x)', step8, 'plus(v,x)')
    if stop_before_chained_equality:
        return None
    step21 = prover.add_chained_equality(
        'plus(x,0)=x',
        [step11,step12,step13,step14,step15,step16,step17,step18,step19,step20,zero])
    return prover.proof
    
# Tests

def test_prover_basic(debug=True):
    proof = syllogism_proof(debug)
    # Will be tested with the course staff's implementation of is_valid
    assert proof.is_valid()

    # Partial run - verifies all steps until stopped
    right_neutral_proof(True, True, True, True, debug)

def test_add_universal_instantiation(debug=True):
    proof = syllogism_proof_with_universal_instantiation(debug)
    # Will be tested with the course staff's implementation of is_valid
    assert proof.is_valid()

    proof = syllogism_all_all_proof(debug)
    # Will be tested with the course staff's implementation of is_valid
    assert proof.is_valid()

def test_add_tautological_inference(debug=True):
    proof = syllogism_all_all_proof_with_tautological_inference(debug)
    # Will be tested with the course staff's implementation of is_valid
    assert proof.is_valid()

    proof = syllogism_all_exists_proof()
    # Will be tested with the course staff's implementation of is_valid
    assert proof.is_valid()

def test_add_existential_derivation(debug=True):
    proof = syllogism_all_exists_proof_with_existential_derivation(debug)
    # Will be tested with the course staff's implementation of is_valid
    assert proof.is_valid()

def test_add_flipped_equality(debug=True):
    # Partial run - verifies all steps until stopped
    right_neutral_proof(False, True, True, True, debug)

def test_add_free_instantiation(debug=True):
    right_neutral_proof(False, False, True, True, debug)    

def test_add_substituted_equality(debug=True):
    # Partial run - verifies all steps until stopped
    right_neutral_proof(False, False, False, True, debug)

def test_add_chained_equality(debug=True):
    proof = right_neutral_proof(False, False, False, False, debug)
    # Will be tested with the course staff's implementation of is_valid
    assert proof.is_valid()
