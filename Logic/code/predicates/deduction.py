""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/predicates/deduction.py """

from code.predicates.syntax import *
from code.predicates.proofs import *
from code.predicates.prover import *

from copy import copy


def inverse_mp(proof, assumption, print_as_proof_forms=False):
    """ Takes a proof, whose first six assumptions/axioms are Prover.AXIOMS, of
        a conclusion from a list of assumptions/axioms that contains the given
        assumption as a simple formula (i.e., without any templates), where no
        step of the proof is a UG step over a variable that is free in the
        given assumption, and returns a proof of (assumption−>conclusion) from
        the same assumptions except assumption """
    assert type(proof) is Proof
    assert proof.is_valid()
    assert type(assumption) is str
    assert Schema(assumption) in proof.assumptions
    assert proof.assumptions[:len(Prover.AXIOMS)] == Prover.AXIOMS
    # Task 11.1
    assumption = str(assumption) if type(assumption) is Formula else assumption

    new_assumptions = generates_assumptions_without_assumption(proof.assumptions, assumption)
    new_conclusion = generates_implies_str_formula(assumption, str(proof.conclusion))
    prover = Prover(new_assumptions, new_conclusion)

    map_lines = {}
    for line_number, line in enumerate(proof.lines):

        justification_type = line.justification[0]
        new_conclusion = generates_implies_str_formula(assumption, str(line.formula))
        if justification_type == 'A':
            new_line_number = generates_deduction_proof_line_for_a_line(new_conclusion, assumption, proof, line, prover)

        elif justification_type == 'T':
            new_line_number = generates_deduction_proof_line_for_t_line(new_conclusion, prover)

        elif justification_type == 'MP':
            new_line_number = generates_deduction_proof_line_for_mp_line(new_conclusion, line, prover, map_lines)

        # UG line
        else:
            new_line_number = generates_deduction_proof_line_for_ug_line(new_conclusion, assumption, line, prover,
                                                                         proof,map_lines)

        map_lines[line_number] = new_line_number

    return prover.proof


def generates_deduction_proof_line_for_ug_line(new_conclusion, assumption, line, prover, proof, map_lines):
    var = line.formula.variable
    origin_line = prover.proof.lines[map_lines[line.justification[1]]].formula
    ug_step = prover.add_ug(Formula('A', var, origin_line), map_lines[line.justification[1]])
    instantiation_map = {'R(v)': Prover.substitute_term_to_formal_param(proof.lines[line.justification[1]].formula, var),
                         'Q()': assumption, 'x': var}
    us_step = prover.add_instantiated_assumption(Prover.US.instantiate(instantiation_map), Prover.US, instantiation_map)
    return prover.add_mp(new_conclusion, ug_step, us_step)


def generates_deduction_proof_line_for_mp_line(new_conclusion, line, prover, map_lines):
    return prover.add_tautological_inference(new_conclusion,[map_lines[line.justification[1]],
                                             map_lines[line.justification[2]]])


def generates_deduction_proof_line_for_t_line(new_conclusion, prover):
    return prover.add_tautology(new_conclusion)


def generates_deduction_proof_line_for_a_line(new_conclusion, assumption, proof, line, prover):
    conclusion = str(line.formula)
    if conclusion == assumption:
        return prover.add_tautology(generates_implies_str_formula(assumption, assumption))

    # instance of assumption
    prover.add_instantiated_assumption(line.formula,
                                       proof.assumptions[line.justification[1]],
                                       line.justification[2])
    return prover.add_tautological_inference(new_conclusion, [len(prover.proof.lines)-1])


def generates_implies_str_formula(first, second):
    return '(' + first + '->' + second + ')'

def generates_assumptions_without_assumption(assumptions, assumption):
    """ generate list of assumptions from assumptions without assumption """
    from itertools import filterfalse
    return list(filterfalse(lambda assump: len(assump.templates) == 0 and str(assump.formula) == assumption, assumptions))


def proof_by_contradiction(proof, assumption, print_as_proof_forms=False):
    """ Takes a proof, whose first six assumptions/axioms are Prover.AXIOMS, of
        a contradiction (a formula whose negation is a tautology)  a list of
        assumptions/axioms that contains the given assumption as a simple
        formula (i.e., without any templates), where no step of the proof is a
        UG step over a variable that is free in the given assumption, and
        returns a proof of ~assumption from the same assumptions except
        assumption """
    assert type(proof) is Proof
    assert proof.is_valid()
    assert type(assumption) is str
    assert Schema(assumption) in proof.assumptions
    assert proof.assumptions[:len(Prover.AXIOMS)] == Prover.AXIOMS
    # Task 11.2
    assumption = str(assumption) if type(assumption) is Formula else assumption
    neg_assumption = '~' + assumption
    prover_origin_proof = Prover(proof.assumptions, neg_assumption)
    contradiction_line = prover_origin_proof.add_proof(proof.conclusion, proof)

    prover_origin_proof.add_tautological_inference(neg_assumption, [contradiction_line])

    prover = Prover(generates_assumptions_without_assumption(proof.assumptions, assumption), neg_assumption)
    contradiction_line = prover.add_proof(generates_implies_str_formula(assumption, neg_assumption),
                                          inverse_mp(prover_origin_proof.proof, assumption))

    prover.add_tautological_inference(neg_assumption, [contradiction_line])
    return prover.proof
