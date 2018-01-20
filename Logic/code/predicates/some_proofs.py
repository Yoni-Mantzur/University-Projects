""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/predicates/some_proofs.py """

from code.predicates.prover import *

def lovers_proof(print_as_proof_forms=False):
    """ Return a proof that from assumptions (in addition to Prover.AXIOMS):
        1) Everybody loves somebody and
        2) Everybody loves a lover
        derives the conclusion:
        Everybody loves everybody.
        The Boolean flag print_as_proof_forms specifies whether the proof being
        constructed is to be printed in real time as it is being constructed """
    prover = Prover(['Ax[Ey[Loves(x,y)]]',
                     'Ax[Az[Ay[(Loves(x,y)->Loves(z,x))]]]'],
                    'Ax[Az[Loves(z,x)]]', print_as_proof_forms)
    # Task 10.4

    step1 = prover.add_assumption('Ax[Ey[Loves(x,y)]]')
    step2 = prover.add_assumption('Ax[Az[Ay[(Loves(x,y)->Loves(z,x))]]]')
    step3 = prover.add_universal_instantiation('Ey[Loves(x,y)]', step1, 'x')
    step4 = prover.add_universal_instantiation('Az[Ay[(Loves(x,y)->Loves(z,x))]]', step2, 'x')
    step5 = prover.add_universal_instantiation('Ay[(Loves(x,y)->Loves(z,x))]', step4, 'z')
    step6 = prover.add_universal_instantiation('(Loves(x,y)->Loves(z,x))', step5, 'y')
    step7 = prover.add_existential_derivation('Loves(z,x)', step3, step6)
    step8 = prover.add_ug('Az[Loves(z,x)]', step7)
    step9 = prover.add_ug('Ax[Az[Loves(z,x)]]', step8)

    return prover.proof

def homework_proof(print_as_proof_forms=False):
    """ Return a proof that from the assumptions (in addition to Prover.AXIOMS):
        1) No homework is fun, and
        2) Some reading is homework
        derives the conclusion:
        Some reading is not fun.
        The Boolean flag print_as_proof_forms specifies whether the proof being
        constructed is to be printed in real time as it is being constructed """
    prover = Prover(['~Ex[(Homework(x)&Fun(x))]',
                     'Ex[(Homework(x)&Reading(x))]'],
                    'Ex[(Reading(x)&~Fun(x))]', print_as_proof_forms)
    # Task 10.5
    step1 = prover.add_instantiated_assumption('((Homework(x)&Fun(x))->Ex[(Homework(x)&Fun(x))])',
                                               Prover.EI, {'R(v)': '(Homework(v)&Fun(v))', 'x': 'x','c': 'x'})
    step2 = prover.add_assumption('~Ex[(Homework(x)&Fun(x))]')
    step3 = prover.add_tautological_inference('(~Ex[(Homework(x)&Fun(x))]->~(Homework(x)&Fun(x)))', [step1])
    step4 = prover.add_tautological_inference('~(Homework(x)&Fun(x))', [step2, step3])
    step5 = prover.add_tautology('(~(Homework(x)&Fun(x))->(Homework(x)->~Fun(x)))')
    step6 = prover.add_tautological_inference('(Homework(x)->~Fun(x))', [step4, step5])
    step7 = prover.add_instantiated_assumption('((Reading(x)&~Fun(x))->Ex[(Reading(x)&~Fun(x))])',
                                               Prover.EI, {'R(v)': '(Reading(v)&~Fun(v))', 'x': 'x','c': 'x'})
    step8 = prover.add_tautology('((Homework(x)->~Fun(x))->((Homework(x)&Reading(x))->(Reading(x)&~Fun(x))))')
    step9 = prover.add_tautological_inference('((Homework(x)&Reading(x))->(Reading(x)&~Fun(x)))', [step6, step8])
    step10 = prover.add_tautological_inference('((Homework(x)&Reading(x))->Ex[(Reading(x)&~Fun(x))])', [step7, step9])
    step11 = prover.add_assumption('Ex[(Homework(x)&Reading(x))]')
    step12 = prover.add_existential_derivation('Ex[(Reading(x)&~Fun(x))]', step11, step10)

    return prover.proof

GROUP_AXIOMS = ['plus(0,x)=x', 'plus(minus(x),x)=0',
                'plus(plus(x,y),z)=plus(x,plus(y,z))']

def unique_zero_proof(print_as_proof_forms=False):
    """ Return a proof that from the group axioms (in addition to Prover.AXIOMS)
        and from the assumption a+c=a proves c=0. The Boolean flag
        print_as_proof_forms specifies whether the proof being constructed is
        to be printed in real time as it is being constructed """
    prover = Prover(GROUP_AXIOMS + ['plus(a,c)=a'], 'c=0', print_as_proof_forms)
    # Task 10.10
    step0 = prover.add_assumption('plus(0,x)=x')
    step1 = prover.add_flipped_equality('x=plus(0,x)', step0)
    step2 = prover.add_free_instantiation('c=plus(0,c)', step1, {'x': 'c'})
    step3 = prover.add_assumption('plus(minus(x),x)=0')
    step4 = prover.add_flipped_equality('0=plus(minus(x),x)', step3)
    step5 = prover.add_free_instantiation('0=plus(minus(a),a)', step4, {'x': 'a'})
    step6 = prover.add_substituted_equality('plus(0,c)=plus(plus(minus(a),a),c)', step5, 'plus(v,c)')
    step7 = prover.add_assumption('plus(plus(x,y),z)=plus(x,plus(y,z))')
    step8 = prover.add_free_instantiation('plus(plus(minus(a),a),c)=plus(minus(a),plus(a,c))', step7, {'x': 'minus(a)',
                                                                                                       'y': 'a',
                                                                                                       'z': 'c'})
    step9 = prover.add_assumption('plus(a,c)=a')
    step10 = prover.add_substituted_equality('plus(minus(a),plus(a,c))=plus(minus(a),a)', step9, 'plus(minus(a),v)')
    step11 = prover.add_flipped_equality('plus(minus(a),a)=0', step5)
    step12= prover.add_chained_equality('c=0', [step2, step6, step8, step10, step11])

    return prover.proof


FIELD_AXIOMS = GROUP_AXIOMS + ['plus(x,y)=plus(y,x)', 'times(x,1)=x',
                               'times(x,y)=times(y,x)',
                               'times(times(x,y),z)=times(x,times(y,z))',
                               '(~x=0->Ey[times(y,x)=1])',
                               'times(x,plus(y,z))=plus(times(x,y),times(x,z))']

def multiply_zero_proof(print_as_proof_forms=False):
    """ Return a proof that from the field axioms (in addition to Prover.AXIOMS)
        proves 0*x=0. The Boolean flag print_as_proof_forms specifies whether
        the proof being constructed is to be printed in real time as it is
        being constructed """
    prover = Prover(FIELD_AXIOMS, 'times(0,x)=0', print_as_proof_forms)
    # Task 10.11

    step0 = prover.add_assumption('plus(0,x)=x')
    step1 = prover.add_assumption('plus(x,y)=plus(y,x)')
    step2 = prover.add_free_instantiation('plus(x,0)=plus(0,x)', step1, {'x': 'x', 'y': '0'})
    step3 = prover.add_chained_equality('plus(x,0)=x', [step2, step0])

    step3 = prover.add_free_instantiation('plus(times(x,0),0)=times(x,0)', step3, {'x': 'times(x,0)'})
    step3a = prover.add_assumption('times(x,y)=times(y,x)')
    step3b = prover.add_free_instantiation('times(0,x)=times(x,0)', step3a, {'x': '0', 'y': 'x'})
    step4 = prover.add_flipped_equality('times(x,0)=plus(times(x,0),0)', step3)  # x0 = x0 + 0

    step5 = prover.add_assumption('plus(minus(x),x)=0')
    step6 = prover.add_free_instantiation('plus(x,minus(x))=plus(minus(x),x)', step1, {'x':'x', 'y':'minus(x)'})
    step7 = prover.add_chained_equality('plus(x,minus(x))=0', [step6, step5])  # x-x = 0
    step8 = prover.add_substituted_equality('plus(times(x,0),plus(x,minus(x)))=plus(times(x,0),0)', step7, 'plus(times(x,0),v)')
    step9 = prover.add_flipped_equality('plus(times(x,0),0)=plus(times(x,0),plus(x,minus(x)))', step8)  # x0 + 0 = x0 + x-x

    step10 = prover.add_assumption('times(x,1)=x')
    step11 = prover.add_flipped_equality('x=times(x,1)', step10)
    step12 = prover.add_substituted_equality('plus(x,minus(x))=plus(times(x,1),minus(x))', step11, 'plus(v,minus(x))')
    step13 = prover.add_substituted_equality('plus(times(x,0),plus(x,minus(x)))=plus(times(x,0),plus(times(x,1),minus(x)))', step12, 'plus(times(x,0),v)')

    step14 = prover.add_assumption('times(x,plus(y,z))=plus(times(x,y),times(x,z))')
    step15 = prover.add_flipped_equality('plus(times(x,y),times(x,z))=times(x,plus(y,z))', step14)
    step16 = prover.add_substituted_equality('plus(plus(times(x,y),times(x,z)),minus(x))=plus(times(x,plus(y,z)),minus(x))', step15, 'plus(v,minus(x))')
    step17 = prover.add_free_instantiation('plus(plus(times(x,0),times(x,1)),minus(x))=plus(times(x,plus(0,1)),minus(x))', step16, {'x': 'x', 'y':'0', 'z':'1'})
    step18 = prover.add_assumption('plus(plus(x,y),z)=plus(x,plus(y,z))')
    step19 = prover.add_free_instantiation('plus(plus(times(x,0),times(x,1)),minus(x))=plus(times(x,0),plus(times(x,1),minus(x)))', step18,{'x': 'times(x,0)', 'y': 'times(x,1)', 'z': 'minus(x)'})
    step20 = prover.add_flipped_equality('plus(times(x,0),plus(times(x,1),minus(x)))=plus(plus(times(x,0),times(x,1)),minus(x))', step19)
    step21 = prover.add_chained_equality('plus(times(x,0),plus(times(x,1),minus(x)))=plus(times(x,plus(0,1)),minus(x))', [step20, step17])

    step22 = prover.add_assumption('plus(0,x)=x')
    step23 = prover.add_free_instantiation('plus(0,1)=1', step22, {'x': '1'})
    step24 = prover.add_substituted_equality('times(x,plus(0,1))=times(x,1)', step23, 'times(x,v)')
    step25 = prover.add_substituted_equality('plus(times(x,plus(0,1)),minus(x))=plus(times(x,1),minus(x))', step24, 'plus(v,minus(x))')

    step26 = prover.add_substituted_equality('plus(times(x,1),minus(x))=plus(x,minus(x))', step10, 'plus(v,minus(x))')
    step27 = prover.add_free_instantiation('plus(x,minus(x))=plus(minus(x),x)', step1, {'x': 'x', 'y': 'minus(x)'})
    step28 = prover.add_chained_equality('plus(x,minus(x))=0', [step27, step5])

    step29 = prover.add_chained_equality('times(0,x)=0', [step3b, step4, step9, step13, step21, step25, step26, step28])

    return prover.proof

PEANO_AXIOMS = ['(s(x)=s(y)->x=y)', '(~x=0->Ey[s(y)=x])', '~s(x)=0',
                'plus(x,0)=x', 'plus(x,s(y))=s(plus(x,y))', 'times(x,0)=0',
                'times(x,s(y))=plus(times(x,y),x)',
                Schema('((R(0)&Ax[(R(x)->R(s(x)))])->Ax[R(x)])', 'R')]

def peano_zero_proof(print_as_proof_forms=False):
    """ Return a proof that from the Peano axioms (in addition to Prover.AXIOMS)
        proves 0+x=x. The Boolean flag print_as_proof_forms specifies whether
        the proof being constructed is to be printed in real time as it is
        being constructed """
    prover = Prover(PEANO_AXIOMS, 'plus(0,x)=x', print_as_proof_forms)
    # Task 10.12

    step1 = prover.add_assumption('plus(x,0)=x')
    step2 = prover.add_free_instantiation('plus(0,0)=0', step1, {'x':'0'})
    step3 = prover.apply_equality_axiom(Prover.ME, {'c': 'plus(0,x)', 'd':'x', 'R(v)': 's(plus(0,x))=s(v)'})
    step4 = prover.apply_equality_axiom(Prover.RX, {'c': 's(plus(0,x))'})
    step5 = prover.add_tautological_inference('(plus(0,x)=x->s(plus(0,x))=s(x))', [step4, step3])
    step6 = prover.add_assumption('plus(x,s(y))=s(plus(x,y))')
    step7 = prover.add_flipped_equality('s(plus(x,y))=plus(x,s(y))', step6)
    step8 = prover.add_free_instantiation('s(plus(0,x))=plus(0,s(x))', step7, {'x':'0', 'y':'x'})
    step9 = prover.apply_equality_axiom(Prover.ME, {'d': 'plus(0,s(x))', 'c':'s(plus(0,x))',
                                                    'R(v)': '(plus(0,x)=x->v=s(x))'})
    step10 = prover.add_tautological_inference('(plus(0,x)=x->plus(0,s(x))=s(x))', [step9, step8, step5])
    step11 = prover.add_ug('Ax[(plus(0,x)=x->plus(0,s(x))=s(x))]', step10)
    step12 = prover.add_tautological_inference('(plus(0,0)=0&Ax[(plus(0,x)=x->plus(0,s(x))=s(x))])', [step2, step11])
    step13 = prover.add_instantiated_assumption(
        ('((plus(0,0)=0&Ax[(plus(0,x)=x->plus(0,s(x))=s(x))])->Ax[plus(0,x)=x])'),
        Schema('((R(0)&Ax[(R(x)->R(s(x)))])->Ax[R(x)])', 'R'), {'R(v)':'plus(0,v)=v'})
    step14 = prover.add_tautological_inference('Ax[plus(0,x)=x]', [step12, step13])
    step15 = prover.add_universal_instantiation('plus(0,x)=x', step14, 'x')

    return prover.proof


COMPREHENSION_AXIOM = Schema('Ey[Ax[((In(x,y)->R(x))&(R(x)->In(x,y)))]]', {'R'})

def russell_paradox_proof(print_as_proof_forms=False):
    """ Return a proof that from the axiom schema of (unrestricted)
        comprehension (in addition to Prover.AXIOMS) proves the falsehood
        (z=z&~z=z). The Boolean flag print_as_proof_forms specifies whether the
        proof being constructed is to be printed in real time as it is being
        constructed """
    prover = Prover([COMPREHENSION_AXIOM], '(z=z&~z=z)', print_as_proof_forms)
    step1 = prover.add_instantiated_assumption('Ey[Ax[((In(x,y)->~In(x,x))&(~In(x,x)->In(x,y)))]]',
                                               Schema('Ey[Ax[((In(x,y)->R(x))&(R(x)->In(x,y)))]]', {'R'}),
                                               {'R(v)':'~In(v,v)'})
    step2 = prover.add_instantiated_assumption('(Ax[((In(x,y)->~In(x,x))&(~In(x,x)->In(x,y)))]->'
                                               + '((In(y,y)->~In(y,y))&(~In(y,y)->In(y,y)))',
                                               Prover.UI, {'R(v)': '((In(v,y)->~In(v,v))&(~In(v,v)->In(v,y)))', 'x':'x',
                                                           'c': 'y'})

    step3 = prover.add_tautological_inference('(((In(y,y)->~In(y,y))&(~In(y,y)->In(y,y)))->(z=z&~z=z))', [])
    step4 = prover.add_tautological_inference('(Ax[((In(x,y)->~In(x,x))&(~In(x,x)->In(x,y)))]->(z=z&~z=z))',
                                              [step2, step3])
    step5 = prover.add_existential_derivation('(z=z&~z=z)', step1, step4)
    # Task 10.13
    return prover.proof
