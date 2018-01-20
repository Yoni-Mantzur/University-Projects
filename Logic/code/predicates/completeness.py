""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/predicates/completeness.py """

from code.predicates.syntax import *
from code.predicates.semantics import *
from code.predicates.proofs import *
from code.predicates.prover import *
from code.predicates.prenex import *
from code.predicates.deduction import *
from code.predicates.util import *

def is_closed(sentences, constants):
    """ Return whether the given set of sentences closed with respect to the
        given set of constant names """
    for sentence in sentences:
        assert type(sentence) is Formula and is_in_prenex_normal_form(sentence)
    for constant in constants:
        assert is_constant(constant)
    return is_primitively_closed(sentences, constants) and \
           is_universally_closed(sentences, constants) and \
           is_existentially_closed(sentences, constants)

def is_primitively_closed(sentences, constants):
    """ Return whether the given set of prenex-normal-form sentences is
        primitively closed with respect to the given set of constant names """
    for sentence in sentences:
        assert type(sentence) is Formula and is_in_prenex_normal_form(sentence)
    for constant in constants:
        assert is_constant(constant)
    # Task 12.1.1
    from itertools import product

    relations = set()
    for formula in sentences:
        relations.update(formula.relations())

    for relation, arity in relations:
        c_combs = product(constants, repeat=arity)
        for c_comb in c_combs:
            relation_format = (relation + '(' + ','.join(c_comb) + ')')
            neg_relation_format = '~' + relation_format
            is_in_s = any([(relation_format == formula) or (neg_relation_format == formula) for formula in sentences])
            if not is_in_s:
                return False
    return True

def is_universally_closed(sentences, constants):
    """ Return whether the given set of prenex-normal-form sentences is
        universally closed with respect to the given set of constant names """
    for sentence in sentences:
        assert type(sentence) is Formula and is_in_prenex_normal_form(sentence)
    for constant in constants:
        assert is_constant(constant)
    # Task 12.1.2
    for sentence in sentences:
        formula = sentence
        if is_quantifier(formula.root) and formula.root == 'A':
                for c in constants:
                    if not formula.predicate.substitute({formula.variable: Term(c)}) in sentences:
                        return False
    return True


def is_existentially_closed(sentences, constants):
    """ Return whether the given set of prenex-normal-form sentences is
        existentially closed with respect to the given set of constant names """
    for sentence in sentences:
        assert type(sentence) is Formula and is_in_prenex_normal_form(sentence)
    for constant in constants:
        assert is_constant(constant)
    # Task 12.1.3

    for sentence in sentences:
        formula = sentence
        if is_quantifier(formula.root) and formula.root == 'E':
            exists_c = False
            for c in constants:
                if formula.predicate.substitute({formula.variable: Term(c)}) in sentences:
                    exists_c = True
                    break

            if not exists_c:
                return False

    return True

def find_unsatisfied_quantifier_free_sentence(sentences, constants, model,
                                              unsatisfied):
    """ Given a set of prenex-normal-form sentences that is closed with respect
        to the given set of constants names, given a model whose universe is
        the given set of constant names, and given a sentence (which possibly
        contains quantifiers) from the given set that the given model does not
        satisfy, return a quantifier-free sentence from the given set that the
        given model does not satisfy. The set sentences may only be accessed
        using containment queries, i.e., using the "in" operator as in:
        if sentence in sentences """
    for constant in constants:
        assert is_constant(constant)
    assert type(model) is Model
    assert model.universe == constants
    assert type(unsatisfied) is Formula
    assert unsatisfied in sentences
    assert not model.evaluate_formula(unsatisfied)
    # Task 12.2

    if is_quantifier_free(unsatisfied):
        return unsatisfied

    for c in constants:
        unsatisfied_new = unsatisfied.predicate.substitute({unsatisfied.variable: Term(c)})

        # Must reach one of these branches
        if (unsatisfied.root == 'A') and (not model.evaluate_formula(unsatisfied_new)):
            # must be true for some c
            return find_unsatisfied_quantifier_free_sentence(sentences, constants, model, unsatisfied_new)

        elif (unsatisfied.root == 'E') and (unsatisfied_new in sentences):
                # must be true for some c
                return find_unsatisfied_quantifier_free_sentence(sentences, constants, model, unsatisfied_new)


def get_primitives(quantifier_free):
    """ Return a set containing the primitive formulae (i.e., relation
        instantiations) that appear in the given quantifier-free formula. For
        example, if quantifier_free is '(R(c1,d)|~(Q(c1)->~R(c2,a))', then the
        returned set should be {'R(c1,d)', 'Q(c1)', 'R(c2,a)'} """
    assert type(quantifier_free) is Formula and \
           is_quantifier_free(quantifier_free)
    # Task 12.3.1

    def _get_primitives(quantifier_free):

        if is_relation(quantifier_free.root):
            primitive_set.add(quantifier_free)
            return

        _get_primitives(quantifier_free.first)
        if is_binary(quantifier_free.root):
            _get_primitives(quantifier_free.second)

    primitive_set = set()
    _get_primitives(quantifier_free)
    return primitive_set

def build_model(sentences, constants):
    """ build model where the universe is the constants (also the meaning of them) and the positive relation
        in sentences """
    meaning = {constant: constant for constant in constants}

    for sentence in sentences:
        if is_relation(sentence.root):
            if sentence.root not in meaning:
                meaning[sentence.root] = set()

            relation_set = meaning[sentence.root]
            relation_set.add(tuple(sentence.arguments))

    return Model(constants, meaning)


def check_all_satisfied(model, sentences):
    """ checks if the model satisfied all the sentences """
    for formula in sentences:
        if not model.evaluate_formula(formula):
            return formula
    return None


def proof_contradiction(sentences, primitive_assumptions, phi_tag):
    """ proof contradiction from inconsistent set"""
    for assump in primitive_assumptions:
        assert assump in sentences

    assumptions = [Schema(str(assump)) for assump in primitive_assumptions] + [Schema(str(phi_tag))]
    neg_phi_tag = Formula('~', phi_tag)
    conclusion = Formula('&', phi_tag, neg_phi_tag)
    prover = Prover(assumptions, conclusion)
    refs = []
    for assump in assumptions:
        refs.append(prover.add_assumption(assump.formula))

    phi_line = len(assumptions) - 1
    neg_phi_line = prover.add_tautological_inference(neg_phi_tag, refs)
    prover.add_tautological_inference(conclusion, [phi_line, neg_phi_line])
    return prover.proof


def model_or_inconsistent(sentences, constants):
    """ Given a set of prenex-normal-form sentences that is closed with respect
        to the given set of constants names, return either a model for the
        given set of sentences, or a proof of a contradiction from these
        sentences as assumptions """
    assert is_closed(sentences, constants)
    # Task 12.3.2
    model = build_model(sentences, constants)

    unsatisfied = check_all_satisfied(model, sentences)
    if unsatisfied is None:
        return model

    unsatisfied_quantifier_free = find_unsatisfied_quantifier_free_sentence(sentences, constants, model, unsatisfied)

    primitives_in_unsatisfied_quantifier_free = get_primitives(unsatisfied_quantifier_free)

    # from primitively closed, each primitive or neg primitive in sentences
    primitive_in_sentences = list(map(lambda primitive: primitive if primitive in sentences else Formula('~', primitive)
                                      , primitives_in_unsatisfied_quantifier_free))

    return proof_contradiction(sentences, primitive_in_sentences, unsatisfied_quantifier_free)


def combine_contradictions(proof_true, proof_false):
    """ Given two proofs of contradictions from two lists of assumptions that
        differ only in the last assumption, where the last assumption of
        proof_false is the negation of that of proof_true, return a proof of a
        contradiction from only the assupmtions common to both proofs (without
        the last assumption of each proof). You can assume that each of the
        given proofs has Prover.AXIOMS (in order) as its first six
        axioms/assumptions, and that all of its axioms/assumptions are
        sentences """
    assert type(proof_true) is Proof and type(proof_false) is Proof
    assert proof_true.assumptions[:-1] == proof_false.assumptions[:-1]
    assert proof_false.assumptions[-1].templates == set()
    assert proof_true.assumptions[-1].templates == set()
    assert proof_false.assumptions[-1].formula == \
           Formula('~', proof_true.assumptions[-1].formula)
    # Task 12.4

    phi, neg_phi = proof_true.assumptions[-1].formula, proof_false.assumptions[-1].formula

    assumptions = proof_true.assumptions[:-1]
    conclusion = Formula('&', phi, neg_phi)

    prover = Prover(assumptions, conclusion)

    proof_neg_phi = proof_by_contradiction(proof_true, str(phi))
    proof_phi = proof_by_contradiction(proof_false, str(neg_phi))

    neg_phi_line = prover.add_proof(proof_neg_phi.conclusion, proof_neg_phi)
    phi_line = prover.add_proof(proof_phi.conclusion, proof_phi)

    prover.add_tautological_inference(conclusion, [phi_line, neg_phi_line])
    return prover.proof


def eliminate_universal_instance_assumption(proof, constant):
    """ Given a proof of a contradiction from a list of assumptions, where the
        last assumption is an instantiation of the form 'formula(consatnt)'
        (for the given constant name) of the universal assumption of the form
        'Ax[formula(x)]' that immediately precedes it, return a proof of a
        contradiction from the same assumptions without the last (universally
        instantiated) one. You can assume that the given proof has
        Prover.AXIOMS (in order) as its first six axioms/assumptions, and that
        all of its axioms/assumptions are sentences """
    assert type(proof) is Proof
    assert proof.assumptions[-2].templates == set()
    assert proof.assumptions[-1].templates == set()
    assert proof.assumptions[-2].formula.root == "A"
    assert proof.assumptions[-1].formula == \
           proof.assumptions[-2].formula.predicate.substitute(
               {proof.assumptions[-2].formula.variable:Term(constant)})
    # Task 12.5
    phi_c = proof.assumptions[-1].formula
    neg_phi_c = Formula('~', phi_c)

    assumptions = proof.assumptions[:-1]
    conclusion = Formula('&', phi_c, neg_phi_c)

    prover = Prover(assumptions, conclusion)

    proof_neg_phi_c = proof_by_contradiction(proof, str(phi_c))
    neg_phi_line = prover.add_proof(proof_neg_phi_c.conclusion, proof_neg_phi_c)

    A_phi_line = prover.add_assumption(assumptions[-1].formula)
    phi_c_line = prover.add_universal_instantiation(phi_c, A_phi_line, Term(constant))

    prover.add_tautological_inference(conclusion, [phi_c_line, neg_phi_line])
    return prover.proof


def universally_close(sentences, constants):
    """ Return a set of sentences that contains the given set of
        prenex-normal-form sentences and is universally closed with respect to
        the given set of constant names. For example, if sentences is the
        singleton {'Ax[Ay[R(x,y)]]'} and constants is {a,b}, then the returned
        set should be: {'Ax[Ay[R(x,y)]]', 'Ay[R(a,y)]', 'Ay[R(b,y)]', 'R(a,a)',
        'R(a,b)', 'R(b,a)', 'R(b,b)'} """
    for sentence in sentences:
        assert type(sentence) is Formula and is_in_prenex_normal_form(sentence)
    for constant in constants:
        assert is_constant(constant)
    # Task 12.6

    def create_sentences(current_sentence):
        curr_set = {current_sentence}
        if current_sentence.root != 'A':
            return curr_set

        for c in constants:
            substituted = current_sentence.predicate.substitute({current_sentence.variable: Term(c)})
            curr_set = curr_set | create_sentences(substituted)
        return curr_set

    final_set = set()
    for sentence in sentences:
        final_set = final_set | create_sentences(sentence)

    return final_set

def subtitute_assumptions(assumptions, constant, variable):
    """ substitutes the assumption with the new (substituted) one"""
    new_assumptions = []
    for assump in assumptions:
        if not (assump in Prover.AXIOMS):
            new_assump = assump.formula.substitute({constant: Term(variable)})
            new_assumptions.append(str(new_assump))

    return new_assumptions

def create_dict_for_assumption(origin_dict, constant, variable):
    """ creates dictionary for the new assumptions """
    new_dict = {}
    for key in origin_dict:
        if not is_constant(key) and not is_variable(key):
            subs = Formula.parse(origin_dict[key]).substitute({constant: Term(variable)})
        else:
            subs = Term.parse(origin_dict[key]).substitute({constant: Term(variable)})

        new_dict[key] = str(subs)
    return new_dict

def replace_constant(proof, constant, variable='zz'):
    """ Given a proof, a constant name that (potentially) appears in the
        assumptions and/or proof, and a variable name that does not appear
        anywhere in the proof or assumptions, return a "similar" (and also
        valid) proof where every occurrence of the given constant name in the
        assumptions and proof is replaced with the given variable name. You may
        assume that the given constant name only appears in the assumption
        schemata of the given proof as a non-template constant name """
    assert is_constant(constant)
    assert is_variable(variable)
    assert type(proof) is Proof
    # Task 12.7
    new_assumptions = subtitute_assumptions(proof.assumptions, constant, variable)

    conclusion = copy(proof.conclusion)
    if constant in str(proof.conclusion):
        conclusion = conclusion.substitute({constant:Term(variable)})

    new_proof = Prover(new_assumptions, conclusion)

    for line in proof.lines:
        new_line = copy(line)
        if line.justification[0] == 'T':
            new_proof.add_tautology(line.formula.substitute({constant:Term(variable)}))
        elif line.justification[0] == 'A':
            new_dict = create_dict_for_assumption(new_line.justification[2], constant, variable)
            new_proof.add_instantiated_assumption(new_line.formula.substitute({constant:Term(variable)}),
                                                  new_proof.proof.assumptions[new_line.justification[1]], new_dict)
        elif line.justification[0] == 'MP':
            new_proof.add_mp(line.formula.substitute({constant:Term(variable)}), new_line.justification[1],
                             new_line.justification[2])
        elif line.justification[0] == 'UG':
            new_proof.add_ug(Formula('A', new_line.formula.variable,
                                     new_line.formula.predicate.substitute({constant:Term(variable)})),
                             new_line.justification[1])

    return new_proof.proof

def eliminate_existential_witness_assumption(proof, constant):
    """ Given a proof of a contradiction from a list of assumptions, where the
        last assumption is a witness of the form 'formula(constant)' (for the
        given constant name) for the existential assumption of the form
        'Ex[formula(x)]' that immediately precedes it, and where the given
        constant name does not appear anywhere else in the assumptions, return
        a proof of a contradiction from the same assumptions without the last
        (witness) one. You can assume that the given proof has Prover.AXIOMS
        (in order) as its first six axioms/assumptions, and that all of its
        axioms/assumptions are sentences """
    assert type(proof) is Proof
    assert proof.assumptions[-2].templates == set()
    assert proof.assumptions[-1].templates == set()
    assert proof.assumptions[-2].formula.root == "E"
    assert proof.assumptions[-1].formula == \
           proof.assumptions[-2].formula.predicate.substitute(
               {proof.assumptions[-2].formula.variable:Term(constant)})
    # Task 12.8
    new_proof = replace_constant(proof, constant)
    phi_zz = new_proof.assumptions[-1].formula

    assumptions = new_proof.assumptions[:-1]
    neg_exists_phi_x = Formula('~', assumptions[-1].formula)
    conclusion = Formula('&', neg_exists_phi_x.first, neg_exists_phi_x)

    prover = Prover(assumptions, conclusion)

    proof_neg_phi_zz = proof_by_contradiction(new_proof, str(phi_zz))
    neg_phi_zz_line = prover.add_proof(proof_neg_phi_zz.conclusion, proof_neg_phi_zz)

    phi_x = neg_exists_phi_x.first.predicate
    zz_to_x = {'zz': Term('x')}
    neg_phi_x = proof_neg_phi_zz.conclusion.substitute(zz_to_x)
    neg_phi_x_line = prover.add_free_instantiation(neg_phi_x, neg_phi_zz_line, zz_to_x)

    phi_implies_not_exists_phi = prover.add_tautological_inference(Formula('->', Formula('~', neg_phi_x),
                                                                           neg_exists_phi_x), [neg_phi_x_line])
    neg_neg_phi_is_phi = prover.add_tautology(Formula('->', Formula('~', neg_phi_x), phi_x))
    phi_implies_not_exists_phi = prover.add_tautological_inference(Formula('->', phi_x, neg_exists_phi_x),
                                                                   [neg_neg_phi_is_phi, phi_implies_not_exists_phi])

    exists_phi_x_line = prover.add_assumption(neg_exists_phi_x.first)
    neg_exists_phi_x_line = prover.add_existential_derivation(neg_exists_phi_x, exists_phi_x_line,
                                                              phi_implies_not_exists_phi)

    prover.add_tautological_inference(conclusion, [exists_phi_x_line, neg_exists_phi_x_line])
    return prover.proof


def existentially_close(sentences, constants):
    """ Return a pair of a set of sentences that contains the given set of
        prenex-normal-form sentences and a set of constant names that contains
        the given set of constant names, such that the returned set of
        sentences is universally closed with respect to the returned set of
        constants names. For example, if sentences is the singleton
        {'Ex[Ey[R(x,y)]]'} and constants is {a,b}, then the returned set could
        be: {'Ex[Ey[R(x,y)]]', 'Ey[R(c1,y)]', 'R(c1,c2)'}. New constant names
        should be generated using next(fresh_constant_name_generator) """
    for sentence in sentences:
        assert type(sentence) is Formula and is_in_prenex_normal_form(sentence)
    for constant in constants:
        assert is_constant(constant)
    # Task 12.9

    def create_sentences(current_sentence):
        curr_set = {current_sentence}
        if current_sentence.root != 'E':
            return curr_set

        new_c = next(fresh_constant_name_generator)
        final_constants_set.add(new_c)
        substituted = current_sentence.predicate.substitute({current_sentence.variable: Term(new_c)})
        curr_set = curr_set | create_sentences(substituted)

        return curr_set

    final_sentences_set = set()
    final_constants_set = copy(constants)
    for sentence in sentences:
        final_sentences_set = final_sentences_set | create_sentences(sentence)

    return final_sentences_set, final_constants_set

