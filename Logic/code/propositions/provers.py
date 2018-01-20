""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/propositions/provers.py """

from functools import lru_cache

from code.propositions.syntax import *
from code.propositions.proofs import *

# Tautological Inference Rules
MP = InferenceRule([Formula.from_infix('p'), Formula.from_infix('(p->q)')],
                   Formula.from_infix('q'))

I1 = InferenceRule([], Formula.from_infix('(p->(q->p))'))
I2 = InferenceRule([], Formula.from_infix('((p->(q->r))->((p->q)->(p->r)))'))

N  = InferenceRule([], Formula.from_infix('((~p->~q)->(q->p))'))

A1 = InferenceRule([], Formula.from_infix('(p->(q->(p&q)))'))
A2 = InferenceRule([], Formula.from_infix('((p&q)->p)'))
A3 = InferenceRule([], Formula.from_infix('((p&q)->q)'))

O1 = InferenceRule([], Formula.from_infix('(p->(p|q))'))
O2 = InferenceRule([], Formula.from_infix('(q->(p|q))'))
O3 = InferenceRule([], Formula.from_infix('((p->r)->((q->r)->((p|q)->r)))'))

T  = InferenceRule([], Formula.from_infix('T'))

F  = InferenceRule([], Formula.from_infix('~F'))

AXIOMATIC_SYSTEM = [MP, I1, I2, N, A1, A2, A3, O1, O2, O3, T, F]

@lru_cache(maxsize=1) # Cache the return value of prove_implies_self
def prove_implies_self():
    """ Return a valid deductive proof for '(p->p)' via MP,I1,I2 """
    return DeductiveProof(
        InferenceRule([], Formula.from_infix('(p->p)')),
        [MP, I1, I2],
        [DeductiveProof.Line(Formula.from_infix('(p->((q->p)->p))'), 1, []),
         DeductiveProof.Line(Formula.from_infix('((p->((q->p)->p))->((p->(q->p))->(p->p))'), 2, []),
         DeductiveProof.Line(Formula.from_infix('(p->(q->p))'), 1, []),
         DeductiveProof.Line(Formula.from_infix('((p->(q->p))->(p->p))'), 0, [0, 1]),
         DeductiveProof.Line(Formula.from_infix('(p->p)'), 0, [2, 3])])


def create_new_statement(proof, assumption):
    assumptions = copy.copy(proof.statement.assumptions)
    assumptions.remove(assumption)
    return InferenceRule(assumptions, Formula('->', assumption, proof.statement.conclusion))


def create_im_assump_line(assumption, line, cur_line_num):
    return [DeductiveProof.Line(line.conclusion, line.rule, line.justification),
            DeductiveProof.Line(Formula('->', copy.deepcopy(line.conclusion),
                                        Formula('->', assumption, copy.deepcopy(line.conclusion))), 1, []),
            DeductiveProof.Line(Formula('->', assumption, line.conclusion), 0, [cur_line_num, cur_line_num+1])]


def create_im_assump_self(assumption, line_idx):
    lines = prove_instance(prove_implies_self(), InferenceRule([], Formula('->', assumption, assumption))).lines
    for line in lines:
        if line.justification is not None:
            line.justification = [line_idx + j for j in line.justification]
    return lines


def create_im_mp_line(proof_lines, assumption, line, line_idx, map_lines):
    p, r, q = assumption, line.conclusion, proof_lines[line.justification[0]].conclusion
    a = Formula('->', p, Formula('->', q, r))
    b = Formula('->', Formula('->', p, q), Formula('->', p, r))
    return [DeductiveProof.Line(Formula('->', a, b), 2, []),
            DeductiveProof.Line(b, 0, [map_lines[line.justification[1]], line_idx]),
            DeductiveProof.Line(Formula('->', p, r), 0, [map_lines[line.justification[0]], line_idx + 1])]


def create_inverse_mp_proof(proof, assumption):
    lines = []
    map_lines = {}
    line_idx = 0
    for i in range(len(proof.lines)):
        line = proof.lines[i]

        if line.conclusion == assumption:
            lines += create_im_assump_self(assumption, line_idx)


        elif line.rule is None or line.rule != 0:  # Means assumption or instance (rule != MP)
            lines += create_im_assump_line(assumption, line, line_idx)

        else:
            lines += create_im_mp_line(proof.lines, assumption, line, line_idx, map_lines)

        line_idx = len(lines)
        map_lines.update({i: line_idx-1})

    return lines



def inverse_mp(proof, assumption):
    """ Return a valid deductive proof for '(assumption->conclusion)', where
        conclusion is the conclusion of proof, from the assumptions of proof
        except assumption, via MP,I1,I2 """
    statement = create_new_statement(proof, assumption)
    rules = proof.rules
    lines = create_inverse_mp_proof(proof, assumption)
    return DeductiveProof(statement, rules, lines)

@lru_cache(maxsize=1) # Cache the return value of prove_hypothetical_syllogism
def prove_hypothetical_syllogism():
    """ Return a valid deductive proof for '(p->r)' from the assumptions
        '(p->q)' and '(q->r)' via MP,I1,I2 """
    return inverse_mp(DeductiveProof(InferenceRule([Formula.from_infix('(p->q)'),
                                                    Formula.from_infix('(q->r)'),
                                                    Formula.from_infix('p')], Formula.from_infix('r')),
                          [MP, I1, I2],
                          [DeductiveProof.Line(Formula.from_infix('p')),
                           DeductiveProof.Line(Formula.from_infix('(p->q)')),
                           DeductiveProof.Line(Formula.from_infix('(q->r)')),
                           DeductiveProof.Line(Formula.from_infix('q'), 0, [0, 1]),
                           DeductiveProof.Line(Formula.from_infix('r'), 0, [3, 2])
                           ]), Formula.from_infix('p'))
