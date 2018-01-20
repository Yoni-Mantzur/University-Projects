""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/propositions/tautology.py """

from code.propositions.syntax import *
from code.propositions.semantics import *
from code.propositions.proofs import *
from code.propositions.provers import MP,I1,I2,inverse_mp

# Axiomatic Inference Rules (MP, I1, and I2 are imported from provers.py)
I3 = InferenceRule([], Formula.from_infix('(~p->(p->q))'))
NI = InferenceRule([], Formula.from_infix('(p->(~q->~(p->q)))'))

NN = InferenceRule([], Formula.from_infix('(p->~~p)'))

R = InferenceRule([], Formula.from_infix('((q->p)->((~q->p)->p))'))

AXIOMATIC_SYSTEM_IMPLIES_NOT = [MP, I1, I2, I3, NI, NN, R]

A = InferenceRule([], Formula.from_infix('(p->(q->(p&q)))'))
NA1 = InferenceRule([], Formula.from_infix('(~p->~(p&q))'))
NA2 = InferenceRule([], Formula.from_infix('(~q->~(p&q))'))

O1 = InferenceRule([], Formula.from_infix('(p->(p|q))'))
O2 = InferenceRule([], Formula.from_infix('(q->(p|q))'))

NO = InferenceRule([], Formula.from_infix('(~p->(~q->~(p|q)))'))

T  = InferenceRule([], Formula.from_infix('T'))

NF  = InferenceRule([], Formula.from_infix('~F'))

AXIOMATIC_SYSTEM = [MP, I1, I2, I3, NI, NN, A, NA1, NA2, O1, O2, NO, T, NF, R]

def comper(f1):
    return f1.root if is_variable(f1.root) else f1.first.root

def extract_assumptions(model):
    assumptions = []
    for param, value in model.items():
        assumptions.append(Formula(param) if value else neg_param(param))

    return sorted(assumptions, key=comper)


def neg_param(param):
    return neg_formula(Formula(param))


def neg_formula(formula):
    return Formula('~', formula)

def create_lines_unary_case(formula, model, lines):
    if is_variable(formula.first.root):
            lines += [DeductiveProof.Line(neg_param(formula.first.root))]

    # ~F
    elif is_constant(formula.first.root):
        lines += [DeductiveProof.Line(NF.conclusion, AXIOMATIC_SYSTEM.index(NF), [])]

    # ~~p
    elif is_unary(formula.first.root):
        create_proof_lines(formula.first.first, model, lines)
        mp(formula, lines, instantiate(NN.conclusion, {'p': formula.first.first}), NN)

    # ~(p->q)
    elif formula.first.root == "->":
        neg_second = neg_formula(formula.first.second)
        create_proof_lines(formula.first.first, model, lines)
        mp(Formula('->', neg_second, formula), lines, instantiate(NI.conclusion,
                                                                  {'p': formula.first.first, 'q':formula.first.second}), NI)
        old_lines_len = len(lines)
        create_proof_lines(neg_second, model, lines)
        lines.append(DeductiveProof.Line(formula, 0, [len(lines) - 1, old_lines_len -1]))

    elif is_constant(formula.first.root):
        create_lines_advanced(formula.first, model, lines)

    elif formula.first.root == "&":
        create_lines_and_case(formula, model, lines)

    elif formula.first.root == "|":
        create_lines_or_case(formula, model, lines)

def create_lines_implies_case(formula,model, lines):
    evaluate_first = evaluate(formula.first, model)
    if evaluate_first:
        create_proof_lines(formula.second, model, lines)
        mp(formula, lines, instantiate(I1.conclusion, {'p': formula.second, 'q':formula.first}), I1)
    else:
        create_proof_lines(neg_formula(formula.first), model, lines)
        mp(formula, lines, instantiate(I3.conclusion, {'p': formula.first, 'q':formula.second}), I3)

def create_proof_lines(formula, model, lines):

    if is_variable(formula.root):
        lines += [DeductiveProof.Line(formula)]

    elif is_unary(formula.root):
        create_lines_unary_case(formula, model, lines)

    # (p->q)
    elif formula.root == "->":
        create_lines_implies_case(formula, model, lines)
    else:
        create_lines_advanced(formula, model, lines)


def lines_from_statments(statement):
    return [DeductiveProof.Line(assump) for assump in statement.assumptions]

def prove_in_model_implies_not(formula, model):
    """ Return a proof of formula via AXIOMATIC_SYSTEM_IMPLIES_NOT from the
        assumptions that all variables are valued as in model, with the
        assumptions being ordered alphabetically by the names of the variables.
        It is assumed that formula is true in model, and may only have the
        operators implies and not in it """
    statement = InferenceRule(extract_assumptions(model), formula)
    lines = lines_from_statments(statement)
    create_proof_lines(formula, model, lines)
    return DeductiveProof(statement, AXIOMATIC_SYSTEM_IMPLIES_NOT, lines)


def mp(formula, lines, conclusion, inferer_rule):
    lines += [DeductiveProof.Line(conclusion, AXIOMATIC_SYSTEM.index(inferer_rule), []),
              DeductiveProof.Line(formula, 0, [len(lines) - 1, len(lines)])]


def update_lines_by_factor(proof, factor):
    for line in proof.lines:
        if line.justification is not None:
            line.justification = [j + factor for j in line.justification]
    return proof

def reduce_assumption(proof_true, proof_false):
    """ Return a proof of the same formula that is proved in both proof_true
        and proof_false, via the same inference rules used in both proof_true
        and proof_false, from the assumptions common to proof_true and
        proof_false. The first three of the inference rules in the given proofs
        are assumed to be M,I1,I2, any additional inference rules are assumed
        to have no assumptions, the inference rules in the given proofs are
        assumed to contain R, and the assumptions of both proofs are assumed to
        coincide, except for the last assumption, where that of proof_false is
        the negation of that of proof_true """
    pi_n = proof_true.statement.assumptions[-1]
    ksi = proof_true.statement.conclusion

    deduct_true = inverse_mp(proof_true, pi_n)
    factor = len(deduct_true.lines)
    deduct_false = update_lines_by_factor(inverse_mp(proof_false, neg_formula(pi_n)), factor)
    lines = deduct_true.lines + deduct_false.lines

    lines += [DeductiveProof.Line(instantiate(R.conclusion, {'q':pi_n, 'p':ksi}), proof_true.rules.index(R), []),
              DeductiveProof.Line(Formula('->', deduct_false.statement.conclusion, ksi), 0, [factor-1, len(lines)]),
              DeductiveProof.Line(ksi, 0, [len(lines) -1, len(lines) +1])]

    return DeductiveProof(InferenceRule(proof_true.statement.assumptions[:-1], ksi), proof_true.rules, lines)


def create_lines_or_case(formula, model, lines):
    if is_unary(formula.root):
        neg_second = neg_formula(formula.first.second)
        create_lines_advanced(neg_second, model, lines)
        line_q = len(lines)
        create_lines_advanced(neg_formula(formula.first.first), model, lines)
        mp(Formula("->", neg_second, formula), lines, instantiate(NO.conclusion, {'p': formula.first.first, 'q': formula.first.second}), NO)
        lines.append(DeductiveProof.Line(formula, 0, [line_q - 1, len(lines) - 1]))
    else:
        evaluate_first = evaluate(formula.first, model)
        evaluate_second = evaluate(formula.second, model)
        if evaluate_first:
            create_lines_advanced(formula.first, model, lines)
            mp(formula, lines, instantiate(O1.conclusion, {'p': formula.first, 'q':formula.second}), O1)

        elif evaluate_second: #(p|q), q is True
            create_lines_advanced(formula.second, model, lines)
            mp(formula, lines, instantiate(O2.conclusion, {'p': formula.first, 'q':formula.second}), O2)

def create_lines_and_case(formula, model, lines):
    # ~(p&q)
    if is_unary(formula.root):
        if evaluate(formula.first.first, model):
            neg_second = neg_formula(formula.first.second)
            create_lines_advanced(neg_second, model, lines)
            mp(formula, lines, instantiate(NA2.conclusion,
                                                          {'p': formula.first.first, 'q': formula.first.second}), NA2)
        else:
            neg_first = neg_formula(formula.first.first)
            create_lines_advanced(neg_first, model, lines)
            mp(formula, lines, instantiate(NA1.conclusion,
                                                          {'p': formula.first.first, 'q': formula.first.second}), NA1)
    #(p&q)
    else:
        create_lines_advanced(formula.second, model, lines)
        line_q = len(lines)
        create_lines_advanced(formula.first, model, lines)
        # line_p = len(lines)
        mp(Formula("->", formula.second, formula), lines, instantiate(A.conclusion, {'p': formula.first, 'q': formula.second}), A)
        lines.append(DeductiveProof.Line(formula, 0, [line_q - 1, len(lines) - 1]))


def create_lines_advanced(formula, model, lines):
    if is_variable(formula.root):
        lines += [DeductiveProof.Line(formula)]

    elif is_constant(formula.root):  # Must to be T
        lines += [DeductiveProof.Line(T.conclusion, AXIOMATIC_SYSTEM.index(T), [])]

    elif is_unary(formula.root):
        create_lines_unary_case(formula, model, lines)

    elif is_binary(formula.root):
        # (p->q)
        if formula.root == "->":
            create_lines_implies_case(formula, model, lines)
        # (p|q)
        elif formula.root == "|":
            create_lines_or_case(formula, model, lines)
        # (p&q)
        elif formula.root == "&":
            create_lines_and_case(formula, model, lines)

def prove_in_model(formula, model):
    """ Return a proof of formula via AXIOMATIC_SYSTEM from the assumptions
        that all variables are valued as in model, with the assumptions being
        ordered alphabetically by the names of the variables. It is assumed
        that formula is true in model """
    # Task 6.4
    statement = InferenceRule(extract_assumptions(model), formula)
    lines = lines_from_statments(statement)
    create_lines_advanced(formula, model, lines)
    return DeductiveProof(statement, AXIOMATIC_SYSTEM, lines)


def proof_or_counterexample_with_func(formula, func):

    list_proofs = []
    prev_model = None
    for model in all_models(sorted(list(formula.variables()))):
        if not evaluate(formula, model):
            return model

        if prev_model is None:
            prev_model = model
            continue

        proof_false = func(formula, prev_model)
        proof_true = func(formula, model)

        list_proofs.append(reduce_assumption(proof_true, proof_false))

        prev_model = None

    while len(list_proofs) > 1:
        new_proofs = []
        for i in range(0, len(list_proofs), 2):
            new_proofs.append(reduce_assumption(list_proofs[i+1], list_proofs[i]))
        list_proofs = new_proofs

    return list_proofs[0]


def proof_or_counterexample_implies_not(formula):
    """ Return either a proof of formula via AXIOMATIC_SYSTEM_IMPLIES_NOT, or a
        model where formula does not hold. It is assumed that formula may only
        have the operators implies and not in it """
    return proof_or_counterexample_with_func(formula, prove_in_model_implies_not)

def proof_or_counterexample(formula):
    """ Return either a proof of formula via AXIOMATIC_SYSTEM, or a model where
        formula does not hold """
    return proof_or_counterexample_with_func(formula, prove_in_model)


def create_formula_with_no_assumptions(rule):

    formula = rule.conclusion
    for assump_i in rule.assumptions[::-1]:
        formula = Formula('->', assump_i, formula)

    return formula


def proof_with_mps(rule, formula_encoded):
    new_formula = formula_encoded
    lines = [DeductiveProof.Line(assump) for assump in rule.assumptions] \
            +[DeductiveProof.Line(new_formula, len(AXIOMATIC_SYSTEM), [])]

    for i in range(len(rule.assumptions)):
        lines.append(DeductiveProof.Line(new_formula.second, 0, [i, len(lines) - 1]))
        new_formula = new_formula.second

    return DeductiveProof(rule, AXIOMATIC_SYSTEM + [InferenceRule([], formula_encoded)], lines)


def proof_or_counterexample_for_inference(rule):
    """ Return either a proof of rule via AXIOMATIC_SYSTEM, or a model where
        rule does not hold """
    for model in all_models(list(rule.variables())):
        if not evaluate_inference(rule, model):
            return model

    formula_encoded = create_formula_with_no_assumptions(rule)
    lemma_proof_rule_encoded = proof_or_counterexample(formula_encoded)
    main_proof_with_formula_encoded = proof_with_mps(rule, formula_encoded)

    return inline_proof(main_proof_with_formula_encoded, lemma_proof_rule_encoded)


def proof_chain_and(formulae):
    phi = formulae[0]
    lines = [DeductiveProof.Line(formula) for formula in formulae]
    lines += [DeductiveProof.Line(formulae[0])]
    for i in range(1, len(formulae)):
        next_phi = Formula('&', phi, formulae[i])
        lines += [DeductiveProof.Line(instantiate(A.conclusion, {'p': phi, 'q': formulae[i]}), AXIOMATIC_SYSTEM.index(A), []),
                  DeductiveProof.Line(Formula('->', formulae[i], next_phi), 0, [len(lines)-1, len(lines)]),
                  DeductiveProof.Line(next_phi, 0, [i, len(lines) + 1])]
        phi = next_phi

    return DeductiveProof(InferenceRule(formulae, phi), AXIOMATIC_SYSTEM, lines)


def model_or_inconsistent(formulae):
    """ Return either a model where all of formulae hold, or a list of two
        proofs, both from formulae via AXIOMATIC_SYSTEM, the first of some
        formula and the second of the negation of the same formula """
    vars = set()
    for formula in formulae:
        vars.update(formula.variables())

    for model in all_models(list(vars)):
        if all(evaluate(formula, model) for formula in formulae): return model

    phi = formulae[0]
    for i in range(1, len(formulae)):
        phi = Formula('&', phi, formulae[i])

    return [proof_chain_and(formulae), proof_or_counterexample_for_inference(InferenceRule(formulae, neg_formula(phi)))]
