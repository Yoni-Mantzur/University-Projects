""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/predicates/prenex.py """

from code.predicates.syntax import *
from code.predicates.proofs import *
from code.predicates.prover import *
from code.predicates.util import *

ADDITIONAL_QUANTIFICATION_AXIOMS = [
    Schema('((~Ax[R(x)]->Ex[~R(x)])&(Ex[~R(x)]->~Ax[R(x)]))', {'x', 'R'}),
    Schema('((~Ex[R(x)]->Ax[~R(x)])&(Ax[~R(x)]->~Ex[R(x)]))', {'x', 'R'}),
    Schema('(((Ax[R(x)]&Q())->Ax[(R(x)&Q())])&(Ax[(R(x)&Q())]->(Ax[R(x)]&Q())))', {'x','R','Q'}),
    Schema('(((Ex[R(x)]&Q())->Ex[(R(x)&Q())])&(Ex[(R(x)&Q())]->(Ex[R(x)]&Q())))', {'x','R','Q'}),
    Schema('(((Q()&Ax[R(x)])->Ax[(Q()&R(x))])&(Ax[(Q()&R(x))]->(Q()&Ax[R(x)])))', {'x','R','Q'}),
    Schema('(((Q()&Ex[R(x)])->Ex[(Q()&R(x))])&(Ex[(Q()&R(x))]->(Q()&Ex[R(x)])))', {'x','R','Q'}),
    Schema('(((Ax[R(x)]|Q())->Ax[(R(x)|Q())])&(Ax[(R(x)|Q())]->(Ax[R(x)]|Q())))', {'x','R','Q'}),
    Schema('(((Ex[R(x)]|Q())->Ex[(R(x)|Q())])&(Ex[(R(x)|Q())]->(Ex[R(x)]|Q())))', {'x','R','Q'}),
    Schema('(((Q()|Ax[R(x)])->Ax[(Q()|R(x))])&(Ax[(Q()|R(x))]->(Q()|Ax[R(x)])))', {'x','R','Q'}),
    Schema('(((Q()|Ex[R(x)])->Ex[(Q()|R(x))])&(Ex[(Q()|R(x))]->(Q()|Ex[R(x)])))', {'x','R','Q'}),
    Schema('(((Ax[R(x)]->Q())->Ex[(R(x)->Q())])&(Ex[(R(x)->Q())]->(Ax[R(x)]->Q())))', {'x','R','Q'}),
    Schema('(((Ex[R(x)]->Q())->Ax[(R(x)->Q())])&(Ax[(R(x)->Q())]->(Ex[R(x)]->Q())))', {'x','R','Q'}),
    Schema('(((Q()->Ax[R(x)])->Ax[(Q()->R(x))])&(Ax[(Q()->R(x))]->(Q()->Ax[R(x)])))', {'x','R','Q'}),
    Schema('(((Q()->Ex[R(x)])->Ex[(Q()->R(x))])&(Ex[(Q()->R(x))]->(Q()->Ex[R(x)])))', {'x','R','Q'}),
    Schema('(((R(x)->Q(x))&(Q(x)->R(x)))->((Ax[R(x)]->Ay[Q(y)])&(Ay[Q(y)]->Ax[R(x)])))', {'x', 'y', 'R', 'Q'}),
    Schema('(((R(x)->Q(x))&(Q(x)->R(x)))->((Ex[R(x)]->Ey[Q(y)])&(Ey[Q(y)]->Ex[R(x)])))', {'x', 'y', 'R', 'Q'})]

DEFAULT_PROOF_ASSUMPTIONS = Prover.AXIOMS + ADDITIONAL_QUANTIFICATION_AXIOMS
EQUIVALENCE_FORMAT = '(({0}->{1})&({1}->{0}))'

def equivalence_of(formula1, formula2):
    """ Return the formula '((formula1->formula2)&(formula2->formula1))', which
        states the equivalence of the two given formulae """
    return Formula('&', Formula('->', formula1, formula2),
                   Formula('->', formula2, formula1))

def is_quantifier_free(formula):
    """ Return whether the given formula contains any quantifiers """
    assert type(formula) is Formula
    # Task 11.3.1
    if is_constant(formula.root) or is_variable(formula.root) or is_relation(formula.root) or is_equality(formula.root):
        return True

    if is_quantifier(formula.root):
        return False

    is_first = is_quantifier_free(formula.first)
    if is_binary(formula.root):
        return is_first and is_quantifier_free(formula.second)

    return is_first

def is_in_prenex_normal_form(formula):
    """ Return whether the given formula is in prenex normal form """
    assert type(formula) is Formula
    # Task 11.3.2
    if is_constant(formula.root) or is_variable(formula.root) or is_relation(formula.root) or is_equality(formula.root):
        return True

    if is_quantifier(formula.root):
        return is_in_prenex_normal_form(formula.predicate)

    is_first = is_quantifier_free(formula.first)
    if is_binary(formula.root):
        return is_first and is_quantifier_free(formula.second)

    return is_first


def proof_of_formula_eq_formula(formula):
    """ return proof of formula<->formula """
    formula = str(formula)
    prover = Prover(DEFAULT_PROOF_ASSUMPTIONS, EQUIVALENCE_FORMAT.format(formula, formula))
    prover.add_tautology(EQUIVALENCE_FORMAT.format(formula, formula))
    return prover.proof


def proof_of_formula_eq_unary(formula, eq_first, proof_eq_first):
    """ return proof of ~formula.first <-> ~eq_first """
    eq_first = str(eq_first)
    want_to_proof = EQUIVALENCE_FORMAT.format(formula, '~' + eq_first)
    prover = Prover(DEFAULT_PROOF_ASSUMPTIONS, want_to_proof)
    endl = prover.add_proof(proof_eq_first.conclusion, proof_eq_first)
    prover.add_tautological_inference(want_to_proof, [endl])
    return prover.proof


def proof_of_formula_eq_binary(formula, eq_bin_sons, proof_eq_bin_sons):
    """ return proof of Bin(formula) <->  Bin(eq_bin_sons) """
    eq_first, eq_second = map(lambda x: str(x), eq_bin_sons)
    want_to_proof = EQUIVALENCE_FORMAT.format(formula, '(' + eq_first + formula.root + eq_second + ')')
    prover = Prover(DEFAULT_PROOF_ASSUMPTIONS, want_to_proof)

    endl_first, endl_second = map(lambda proof: prover.add_proof(proof.conclusion, proof), proof_eq_bin_sons)
    prover.add_tautological_inference(want_to_proof, [endl_first, endl_second])
    return prover.proof


def proof_eq_quantifier(formula, eq_pred, proof_eq_pred, substitute_formula, z_i):
    """ return proof for formula <-> A/Ez_i[eq_pred] """
    eq_pred = str(eq_pred)
    want_to_proof = EQUIVALENCE_FORMAT.format(formula, formula.root + z_i + '[' + str(substitute_formula) + ']')
    prover = Prover(DEFAULT_PROOF_ASSUMPTIONS, want_to_proof)
    endl_proof = prover.add_proof(proof_eq_pred.conclusion, proof_eq_pred)
    x = formula.variable
    endl = apply_15_or_16_axiom(formula, prover, eq_pred, formula.predicate, x, z_i)
    prover.add_tautological_inference(want_to_proof, [endl_proof, endl])
    return prover.proof


def apply_15_or_16_axiom(formula, prover, Q, R, x, y):
    """ add assump to prover """
    assump = ADDITIONAL_QUANTIFICATION_AXIOMS[14] if formula.root == 'A' else ADDITIONAL_QUANTIFICATION_AXIOMS[15]
    instantiation_map = {
        'R(v)': prover.substitute_term_to_formal_param(R, x),
        'Q(v)': prover.substitute_term_to_formal_param(Q, x),
        'x': x,
        'y': y
    }
    endl = prover.add_instantiated_assumption(assump.instantiate(instantiation_map), assump, instantiation_map)
    return endl

def make_quantified_variables_unique(formula):
    """ Takes a formula and returns a pair: an equivalent formula with the
        exact same structure with the additional property that no two
        quantified variables, and no pair of quantified variable and free
        variable, in that formula have the same name, and a proof of the
        equivalence (i.e., a proof of equivalence_of(formula, returned_formula))
        from Prover.AXIOMS as well as from ADDITIONAL_QUANTIFICATION_AXIOMS.
        All quantified variable names should be replaced by new variable names,
        each generated using next(fresh_variable_name_generator) - you can
        assume that the original formula does not contain variable names that
        you have generated this way """
    assert type(formula) is Formula
    # Task 11.4
    if is_equality(formula.root) or is_relation(formula.root):
        return formula, proof_of_formula_eq_formula(formula)

    if is_quantifier(formula.root):
        eq_pred, proof_eq_pred = make_quantified_variables_unique(formula.predicate)
        z_i = next(fresh_variable_name_generator)
        substitute_formula = Formula(formula.root, z_i, eq_pred.substitute({formula.variable: Term(z_i)}))
        return substitute_formula, proof_eq_quantifier(formula, eq_pred, proof_eq_pred, substitute_formula.predicate,z_i)

    eq_first, proof_eq_first = make_quantified_variables_unique(formula.first)
    if is_unary(formula.root):
        return Formula('~', eq_first), proof_of_formula_eq_unary(formula, eq_first, proof_eq_first)

    # Binary case
    eq_second, proof_eq_second = make_quantified_variables_unique(formula.second)
    return Formula(formula.root, eq_first, eq_second), proof_of_formula_eq_binary(formula, (eq_first, eq_second),
                                                                                  (proof_eq_first, proof_eq_second))

def pull_out_quantifications_across_negation(formula):
    """ Takes a formula whose root is a negation, i.e., a formula of the form
        ~Q1x1[Q2x2[...Qnxn[inner_formula]...]] (where n>=0, each Qi is a
        quantifier, each xi is a variable name, and inner_formula does not
        start with a quantifier), and returns a pair:
        an equivalent formula of the form
        Q'1x1[Q'2x2[...Q'nxn[~inner_formula]...]] (where each Q'i is a
        quantifier, and where the xi's and inner_formula are the same as in the
        given formula), and a proof of the equivalence (i.e., a proof of
        equivalence_of(formula, returned_formula)) from Prover.AXIOMS as well
        as from ADDITIONAL_QUANTIFICATION_AXIOMS """
    assert type(formula) == Formula and formula.root == '~'
    # Task 11.5

    if not is_quantifier(formula.first.root):
        return formula, proof_of_formula_eq_formula(formula)

    eq_neg_pred, proof_eq_neg_pred = pull_out_quantifications_across_negation(Formula('~', formula.first.predicate))

    new_quantifier = 'A' if formula.first.root == 'E' else 'E'
    x = formula.first.variable

    eq_formula = new_quantifier + x + '[' + str(eq_neg_pred) + ']'
    want_to_proof = EQUIVALENCE_FORMAT.format(formula, eq_formula)
    prover = Prover(DEFAULT_PROOF_ASSUMPTIONS, want_to_proof)
    endl_proof = prover.add_proof(proof_eq_neg_pred.conclusion, proof_eq_neg_pred)
    formula_with_neg_inside = Formula(new_quantifier, x, Formula('~', formula.first.predicate))

    endl = apply_15_or_16_axiom(formula_with_neg_inside, prover, formula_with_neg_inside.predicate, eq_neg_pred, x, x)
    endl_first = prover.add_tautological_inference(prover.proof.lines[endl].formula.second, [endl_proof, endl])

    assump = ADDITIONAL_QUANTIFICATION_AXIOMS[0] if new_quantifier == 'E' else ADDITIONAL_QUANTIFICATION_AXIOMS[1]
    instantiation_map = {
        'R(v)': prover.substitute_term_to_formal_param(formula.first.predicate, x),
        'x': x,
    }
    endl_second = prover.add_instantiated_assumption(assump.instantiate(instantiation_map), assump, instantiation_map)
    prover.add_tautological_inference(want_to_proof, [endl_first, endl_second])

    return Formula.parse(eq_formula), prover.proof


def get_new_quantifier_and_axioms(binary_op, old_quantifier, is_left):
    """ get the new quantifier and axioms relevant to the given binary operation"""
    new_quantifier = old_quantifier
    if binary_op == '&':
        axioms = [2, 3] if is_left else [4, 5]

    elif binary_op == '|':
        axioms = [6, 7] if is_left else [8, 9]

    # ->
    else:
        if is_left:
            new_quantifier = 'A' if old_quantifier == 'E' else 'E'
            axioms = [10, 11]
        else:
            axioms = [12, 13]

    axioms = tuple(map(lambda axiom_num: ADDITIONAL_QUANTIFICATION_AXIOMS[axiom_num], axioms))
    return new_quantifier, axioms[0] if old_quantifier == 'A' else axioms[1]

def pull_out_quantifications_from_left_across_binary_operator(formula):
    """ Takes a formula whose root is a binary operator, i.e., a formula of the
        form (Q1x1[Q2x2[...Qnxn[inner_first]...]]*second) (where * is a binary
        operator, n>=0, each Qi is a quantifier, each xi is a variable name,
        and inner_first does not start with a quantifier), and returns a pair:
        an equivalent formula of the form
        Q'1x1[Q'2x2[...Q'nxn[(inner_first*second)]...]] (where each Q'i is a
        quantifier, and where the operator *, the xi's, inner_first, and second
        are the same as in the given formula), and a proof of the equivalence
        (i.e., a proof of equivalence_of(formula, returned_formula)) from
        Prover.AXIOMS as well as from ADDITIONAL_QUANTIFICATION_AXIOMS. You may
        assume that no two quantified variables, and no pair of quantified
        variable and free variable, in formula have the same name """
    assert type(formula) == Formula and is_binary(formula.root)
    # Task 11.6.1
    if not is_quantifier(formula.first.root):
        return formula, proof_of_formula_eq_formula(formula)

    inner_formula = Formula(formula.root, formula.first.predicate, formula.second)
    eq_bin_pred, proof_eq_bin_pred = pull_out_quantifications_from_left_across_binary_operator(inner_formula)

    new_quantifier, axiom = get_new_quantifier_and_axioms(formula.root, formula.first.root, True)
    x = formula.first.variable

    eq_formula = new_quantifier + x + '[' + str(eq_bin_pred) + ']'
    want_to_proof = EQUIVALENCE_FORMAT.format(formula, eq_formula)
    prover = Prover(DEFAULT_PROOF_ASSUMPTIONS, want_to_proof)
    endl_proof = prover.add_proof(proof_eq_bin_pred.conclusion, proof_eq_bin_pred)

    formula_with_bin_inside = Formula(new_quantifier, x, inner_formula)

    endl = apply_15_or_16_axiom(formula_with_bin_inside, prover, eq_bin_pred, formula_with_bin_inside.predicate, x, x)
    endl_first = prover.add_tautological_inference(prover.proof.lines[endl].formula.second, [endl_proof, endl])

    instantiation_map = {
        'R(v)': prover.substitute_term_to_formal_param(formula.first.predicate, x),
        'Q()': str(formula.second),
        'x': x,
    }
    endl_second = prover.add_instantiated_assumption(axiom.instantiate(instantiation_map), axiom, instantiation_map)
    prover.add_tautological_inference(want_to_proof, [endl_first, endl_second])

    return Formula.parse(eq_formula), prover.proof

def pull_out_quantifications_from_right_across_binary_operator(formula):
    """ Takes a formula whose root is a binary operator, i.e., a formula of the
        form (first*Q1x1[Q2x2[...Qnxn[inner_second]...]]) (where * is a binary
        operator, n>=0, each Qi is a quantifier, each xi is a variable name,
        and inner_second does not start with a quantifier), and returns a pair:
        an equivalent formula of the form
        Q'1x1[Q'2x2[...Q'nxn[(first*inner_second)]...]] (where each Q'i is a
        quantifier, and where the operator *, the xi's, first, and inner_second
        are the same as in the given formula), and a proof of the equivalence
        (i.e., a proof of equivalence_of(formula, returned_formula)) from
        Prover.AXIOMS as well as from ADDITIONAL_QUANTIFICATION_AXIOMS. You may
        assume that no two quantified variables, and no pair of quantified
        variable and free variable, in formula have the same name """
    assert type(formula) == Formula and is_binary(formula.root)
    # Task 11.6.2
    if not is_quantifier(formula.second.root):
        return formula, proof_of_formula_eq_formula(formula)

    inner_formula = Formula(formula.root, formula.first, formula.second.predicate)
    eq_bin_pred, proof_eq_bin_pred = pull_out_quantifications_from_right_across_binary_operator(inner_formula)

    new_quantifier, axiom = get_new_quantifier_and_axioms(formula.root, formula.second.root, False)
    x = formula.second.variable

    eq_formula = new_quantifier + x + '[' + str(eq_bin_pred) + ']'
    want_to_proof = EQUIVALENCE_FORMAT.format(formula, eq_formula)
    prover = Prover(DEFAULT_PROOF_ASSUMPTIONS, want_to_proof)
    endl_proof = prover.add_proof(proof_eq_bin_pred.conclusion, proof_eq_bin_pred)

    formula_with_bin_inside = Formula(new_quantifier, x, inner_formula)

    endl = apply_15_or_16_axiom(formula_with_bin_inside, prover, eq_bin_pred, formula_with_bin_inside.predicate, x, x)
    endl_first = prover.add_tautological_inference(prover.proof.lines[endl].formula.second, [endl_proof, endl])

    instantiation_map = {
        'R(v)': prover.substitute_term_to_formal_param(formula.second.predicate, x),
        'Q()': str(formula.first),
        'x': x,
    }
    endl_second = prover.add_instantiated_assumption(axiom.instantiate(instantiation_map), axiom, instantiation_map)
    prover.add_tautological_inference(want_to_proof, [endl_first, endl_second])

    return Formula.parse(eq_formula), prover.proof

def pull_out_quantifications_across_binary_operator(formula):
    """ Takes a formula whose root is a binary operator, i.e., a formula of the
        form (Q1x1[Q2x2[...Qnxn[inner_first]...]]*
              P1y1[P2y2[...Pmym[inner_second]...]]) (where * is a binary
        operator, n>=0, m>=0, each Qi and each Pi is a quantifier, each xi and
        each yi is a variable name,  and neither inner_first nor inner_second
        starts with a quantifier), and returns a pair: an equivalent formula of
        the form
        Q'1x1[Q'2x2[...Q'nxn[P'1x1[P'2x2[...P'nxn[(inner_first*inner_second)]...]]]...]]
        (where each Q'i and each P'i is a quantifier, and where the operator *,
        the xi's, the yi's, inner_first, and inner_second are the same as in
        the given formula), and a proof of the equivalence (i.e., a proof of
        equivalence_of(formula, returned_formula)) from Prover.AXIOMS as well
        as from ADDITIONAL_QUANTIFICATION_AXIOMS. You may assume that no two
        quantified variables, and no pair of quantified variable and free
        variable, in formula have the same name """
    assert type(formula) is Formula and is_binary(formula.root)
    # Task 11.7
    def get_inner_quantifiers(f):
        """this functio nreturns the innest quantifier on the formula"""
        inner = f
        while is_quantifier(inner.root):
            quantifiers.append((inner.root, inner.variable))
            inner = inner.predicate
        return inner

    def build_conclusion():
        """this function build the conclusion to the proof using 15,16 assumptions"""
        conclusion = eq_right_inner
        for quantifier, var in quantifiers[::-1]:
            conclusion = Formula(quantifier, var, conclusion)
        return conclusion

    def apply_15_16():
        """ apply 15 or 16 assumption due to the root(A or E) on the given elements."""

        Q = eq_right_inner
        R = inner_of_left
        endl = endl_second
        for quantifier, x in quantifiers[::-1]:
            Q = Formula(quantifier, x, Q)
            R = Formula(quantifier, x, R)
            endl_proof = apply_15_or_16_axiom(Q, prover, Q.predicate, R.predicate, x, x)
            endl = prover.add_tautological_inference(prover.proof.lines[endl_proof].formula.second, [endl_proof, endl])
        return endl

    eq_left, proof_left = pull_out_quantifications_from_left_across_binary_operator(formula)
    quantifiers = []
    inner_of_left = get_inner_quantifiers(eq_left)
    eq_right_inner, proof_right_inner = pull_out_quantifications_from_right_across_binary_operator(inner_of_left)

    want_to_proof = EQUIVALENCE_FORMAT.format(formula, build_conclusion())
    prover = Prover(DEFAULT_PROOF_ASSUMPTIONS, want_to_proof)
    endl_first = prover.add_proof(proof_left.conclusion, proof_left)
    endl_second = prover.add_proof(proof_right_inner.conclusion, proof_right_inner)
    endl_third = apply_15_16()
    prover.add_tautological_inference(want_to_proof, [endl_first, endl_third])
    return build_conclusion(), prover.proof

def to_prenex_normal_form_from_unique_quantified_variables(formula):
    """ Takes a formula and returns a pair: an equivalent formula in prenex
        normal form, and a proof of the equivalence (i.e., a proof of
        equivalence_of(formula, returned_formula)) from Prover.AXIOMS as well
        as from ADDITIONAL_QUANTIFICATION_AXIOMS. You may assume that no two
        quantified variables, and no pair of quantified variable and free
        variable, in formula have the same name """
    assert type(formula) is Formula
    # Task 11.8

    if is_equality(formula.root) or is_relation(formula.root):
        return formula, proof_of_formula_eq_formula(formula)

    if is_quantifier(formula.root):
        B, A_eq_B_proof = to_prenex_normal_form_from_unique_quantified_variables(formula.predicate)

        conclusion = Formula.parse(EQUIVALENCE_FORMAT.format(formula, Formula(formula.root, formula.variable, B)))
        prover = Prover(DEFAULT_PROOF_ASSUMPTIONS, conclusion)
        endl = prover.add_proof(A_eq_B_proof.conclusion, A_eq_B_proof)  # proof of A<->B
        end2 = apply_15_or_16_axiom(formula, prover, formula.predicate, B, formula.variable, formula.variable)
        prover.add_tautological_inference(conclusion, [end2, endl])
        return Formula(formula.root, formula.variable, B), prover.proof

    if is_unary(formula.root):
        B, A_eq_B_proof = to_prenex_normal_form_from_unique_quantified_variables(formula.first)
        C, neg_B_eq_C_proof = pull_out_quantifications_across_negation(Formula("~", B))

        conclusion = Formula.parse((EQUIVALENCE_FORMAT.format(formula, C)))
        prover = Prover(DEFAULT_PROOF_ASSUMPTIONS, conclusion)

        end1 = prover.add_proof(A_eq_B_proof.conclusion, A_eq_B_proof)
        neg_A_eq_neg_B = Formula.parse((EQUIVALENCE_FORMAT.format(formula, Formula("~", B))))

        end2 = prover.add_tautological_inference(neg_A_eq_neg_B, [end1]) # A<->B --> ~A<->~B

        end3 = prover.add_proof(neg_B_eq_C_proof.conclusion, neg_B_eq_C_proof)
        prover.add_tautological_inference(Formula.parse(EQUIVALENCE_FORMAT.format(formula, C)), [end2, end3])
        return C, prover.proof

    if is_binary(formula.root):
        B, A_eq_B_proof = to_prenex_normal_form_from_unique_quantified_variables(formula.first)
        D, C_eq_D_proof = to_prenex_normal_form_from_unique_quantified_variables(formula.second)

        A_op_C = Formula(formula.root, formula.first, formula.second)
        B_op_D = Formula(formula.root, B, D)
        E, B_op_D_eq_E = pull_out_quantifications_across_binary_operator(B_op_D)

        conclusion = Formula.parse(EQUIVALENCE_FORMAT.format(formula, E))
        prover = Prover(DEFAULT_PROOF_ASSUMPTIONS, conclusion)

        end1 = prover.add_proof(A_eq_B_proof.conclusion, A_eq_B_proof)
        end2 = prover.add_proof(C_eq_D_proof.conclusion, C_eq_D_proof)
        end3 = prover.add_tautological_inference(EQUIVALENCE_FORMAT.format(A_op_C, B_op_D), [end1, end2])

        end4 = prover.add_proof(B_op_D_eq_E.conclusion, B_op_D_eq_E)
        prover.add_tautological_inference(Formula.parse(EQUIVALENCE_FORMAT.format(A_op_C, E)), [end3, end4])

        return E, prover.proof

def to_prenex_normal_form(formula):
    """ Takes a formula and returns a pair: an equivalent formula in prenex
        normal form, and a proof of the equivalence (i.e., a proof of
        equivalence_of(formula, retunred_formula)) from Prover.AXIOMS as well
        as from ADDITIONAL_QUANTIFICATION_AXIOMS. All quantified variable names
        should be replaced by new variable names, each generated using
        next(fresh_variable_name_generator) - you can assume that the original
        formula does not contain variable names that you have generated this
        way  """
    assert type(formula) is Formula
    # Task 11.9
    formula_unique_vars, uniqe_vars_proof = make_quantified_variables_unique(formula)
    eq_formula, proof = to_prenex_normal_form_from_unique_quantified_variables(formula_unique_vars)
    prover = Prover(DEFAULT_PROOF_ASSUMPTIONS, EQUIVALENCE_FORMAT.format(formula, eq_formula))
    end1 = prover.add_proof(uniqe_vars_proof.conclusion, uniqe_vars_proof)
    end2 = prover.add_proof(proof.conclusion, proof)
    prover.add_tautological_inference(EQUIVALENCE_FORMAT.format(formula, eq_formula), [end1, end2])
    return eq_formula, prover.proof