""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/propositions/tautology_test.py """

from code.propositions.syntax import *
from code.propositions.semantics import *
from code.propositions.proofs import *
from code.propositions.provers import MP,I1,I2
from code.propositions.tautology import *

# Tests for prove_in_model*** methods

def test_prove_in_model_implies_not(debug=True):
    __test_prove_in_model(prove_in_model_implies_not,
                          ['p', '~~p', '(p->q)', '~~(~q->(~p->~r))'],
                          AXIOMATIC_SYSTEM_IMPLIES_NOT, debug)

def test_prove_in_model(debug=True):
    __test_prove_in_model(prove_in_model,
                          ['p', '~~p', '(p->q)', '~~(~q->(~p->~r))',
                           'T', 'F', '(p&q)', '(p|q)', '~(~(q|p)&(r->~(s|q)))'],
                          AXIOMATIC_SYSTEM, debug)

def __test_prove_in_model(prover, infixes, rules, debug):
    for infix in infixes:
        formula = Formula.from_infix(infix)
        notformula = Formula('~', formula)
        for model in all_models(list(formula.variables())):
            if evaluate(formula, model):
                f = formula
            else:
                f = notformula
            if debug:
                print('Testing', prover.__qualname__, 'for', f, 'in', model)
            proof = prover(f, model)
            for assumption in proof.statement.assumptions:
                variables = assumption.variables()
                assert len(variables) == 1
                variable = list(variables)[0]
                if model[variable]:
                    assert assumption == Formula(variable)
                else:
                    assert assumption == Formula('~', Formula(variable))
            for v in list(f.variables()):
                if model[v]:
                    assert Formula(v) in proof.statement.assumptions
                else:
                    assert Formula('~', Formula(v)) in proof.statement.assumptions
            variables = [list(a.variables())[0] for a in proof.statement.assumptions]
            assert variables == sorted(variables)
            assert proof.statement.conclusion == f
            assert proof.rules == rules
            # Will be tested with the course staff's implementation of is_valid
            assert proof.is_valid()

def test_reduce_assumption(debug=True):
    formula = Formula.from_infix('(q&(p|~p))')
    rules = [MP, I1, I2, NN, O1, O2, A, R]
    proof_true = DeductiveProof(
        InferenceRule([Formula.from_infix('(r->q)'), Formula.from_infix('r'),
                       Formula.from_infix('p')],
                      formula),
        rules,
        [DeductiveProof.Line(Formula.from_infix('(r->q)')),
         DeductiveProof.Line(Formula.from_infix('r')),
         DeductiveProof.Line(Formula.from_infix('p')),
         DeductiveProof.Line(Formula.from_infix('q'), 0, [1, 0]),
         DeductiveProof.Line(Formula.from_infix('(p->(p|~p))'), 4, []),
         DeductiveProof.Line(Formula.from_infix('(p|~p)'), 0, [2,4]),
         DeductiveProof.Line(Formula.from_infix('(q->((p|~p)->(q&(p|~p))))'), 6, []),
         DeductiveProof.Line(Formula.from_infix('((p|~p)->(q&(p|~p)))'), 0, [3, 6]),
         DeductiveProof.Line(Formula.from_infix('(q&(p|~p))'), 0, [5, 7])])

    proof_false = DeductiveProof(
        InferenceRule([Formula.from_infix('(r->q)'), Formula.from_infix('r'),
                       Formula.from_infix('~p')],
                      formula),
        rules,
        [DeductiveProof.Line(Formula.from_infix('(r->q)')),
         DeductiveProof.Line(Formula.from_infix('r')),
         DeductiveProof.Line(Formula.from_infix('~p')),
         DeductiveProof.Line(Formula.from_infix('(q->((p|~p)->(q&(p|~p))))'), 6, []),
         DeductiveProof.Line(Formula.from_infix('q'), 0, [1, 0]),
         DeductiveProof.Line(Formula.from_infix('((p|~p)->(q&(p|~p)))'), 0, [4, 3]),
         DeductiveProof.Line(Formula.from_infix('(~p->(p|~p))'), 5, []),
         DeductiveProof.Line(Formula.from_infix('(p|~p)'), 0, [2,6]),
         DeductiveProof.Line(Formula.from_infix('(q&(p|~p))'), 0, [7, 5])])

    if debug:
        print('Testing reduce_assumption for the following proof:', proof_true,
              '\nand the following proof:', proof_false)

    proof = reduce_assumption(proof_true, proof_false)
    assert proof.statement.conclusion == formula
    assert proof.statement.assumptions == proof_true.statement.assumptions[:-1]
    assert proof.rules == rules
    # Will be tested with the course staff's implementation of is_valid
    assert proof.is_valid()

# Tests for proof_or_counterexample*** methods

def test_proof_or_counterexample_implies_not(debug=True ):
    __test_proof_or_counterexample(proof_or_counterexample_implies_not,
                                   ['((~p->~q)->((~p->q)->p))',
                                    '((q->~p)->((~~~p->r)->(q->r)))',
                                    '((q->p)->((~q->p)->p))',
                                    '((p->~q)->(q->~p))',
                                    '((p->q)->(~p->~q))'],
                                   AXIOMATIC_SYSTEM_IMPLIES_NOT, debug)

def test_proof_or_counterexample(debug=True):
    __test_proof_or_counterexample(proof_or_counterexample,
                                   ['((~p->~q)->((~p->q)->p))',
                                    '((q->~p)->((~~~p->r)->(q->r)))',
                                    '((q->p)->((~q->p)->p))',
                                    '((p->~q)->(q->~p))',
                                    '((p->q)->(~p->~q))',
                                    '(p|~p)',
                                    '(p|~q)',
                                    '(~(p|q)&(r->~(s|q)))',
                                    '((p&(q|~r))->(p&(~r|q)))',
                                    '(((p&q)->~(~p|~q))&(~(~p|~q)->(p&q)))',
                                    '(((p|q)->~(~p&~q))&(~(~p&~q)->(p|q)))',
                                    '((p&q)->(p|q))',
                                    '((p|q)->(p&q))',
                                    '(T->p)',
                                    '(F->p)',
                                    '(p->T)'],
                                   AXIOMATIC_SYSTEM, debug)

def __test_proof_or_counterexample(prover, infixes, rules, debug):
    for infix in infixes:
        formula = Formula.from_infix(infix)
        if debug:
            print('Testing', prover.__qualname__, 'for', formula)
        result = prover(formula)
        if type(result) is DeductiveProof:
            assert result.statement.assumptions == []
            assert result.statement.conclusion == formula
            assert result.rules == rules, "got " + str(result.rules) + ", expected " + str(rules)
            if debug:
                print('Verifying returned proof (' +
                      '{:,}'.format(len(result.lines)), 'lines)')
            # Will be tested with the course staff's implementation of is_valid
            assert result.is_valid()
        else:
            if debug:
                print('Verifying returned counterexample:', result)
            # Will be tested with the course staff's implementation of evaluate
            assert not evaluate(formula, result)

def test_proof_or_counterexample_for_inference(debug=True):
    __test_proof_or_counterexample_for_inference(
                                   proof_or_counterexample_for_inference,
                                   ['((~p->~q)->((~p->q)->p))',
                                    '((q->~p)->((~~~p->r)->(q->r)))',
                                    '((q->p)->((~q->p)->p))',
                                    '((p->~q)->(q->~p))',
                                    '((p->q)->(~p->~q))',
                                    '(p|~p)',
                                    '(p|~q)',
                                    '(~(p|q)&(r->~(s|q)))',
                                    '((p&(q|~r))->(p&(~r|q)))',
                                    '(((p&q)->~(~p|~q))&(~(~p|~q)->(p&q)))',
                                    '(((p|q)->~(~p&~q))&(~(~p&~q)->(p|q)))',
                                    '((p&q)->(p|q))',
                                    '((p|q)->(p&q))',
                                    '(T->p)',
                                    '(F->p)',
                                    '(p->T)',
                                    [['(p&q)'],'(p|q)'],
                                    [['(p|q)'],'(p&q)'],
                                    [['(p&q)'],'~(~p|~q)'],
                                    [['(p|q)'],'~(~p&~q)'],
                                    [['(p|q)', '(q|r)'],'(q|(p&r))'],
                                    [['(p|q)', '(q|r)'],'(q&(p&r))']],
                                   AXIOMATIC_SYSTEM, debug)

def __test_proof_or_counterexample_for_inference(prover, tests, rules, debug):
    for test in tests:
        if type(test) is str:
            assumptions = []
            infix = test
        else:
            assumptions = [Formula.from_infix(i) for i in test[0]]
            infix = test[1]
        rule = InferenceRule(assumptions, Formula.from_infix(infix))
        if debug:
            print('Testing', prover.__qualname__, 'for', rule)
        result = prover(rule)
        if type(result) is DeductiveProof:
            assert result.statement == rule
            assert result.rules == rules, "got " + str(result.rules) + ", expected " + str(rules)
            if debug:
                print('Verifying returned proof (' +
                      '{:,}'.format(len(result.lines)), 'lines)')
            # Will be tested with the course staff's implementation of is_valid
            assert result.is_valid()
        else:
            if debug:
                print('Verifying returned counterexample:', result)
            # Will be tested with the course staff's implementation of
            # evaluate_inference
            assert not evaluate_inference(rule, result)

def test_model_or_inconsistent(debug=True):
    __test_model_or_inconsistent(
        model_or_inconsistent,
        [
         ['(p->~q)', '(~q->p)', '(q->~r)', '(~r->q)', '(r->~p)', '(~p->r)'],
         ['(p->~q)', '(~q->p)', '(q->~r)', '(~r->q)', '(r->~s)', '(~s->r)',
          '(s->~p)', '(~p->s)']],
        AXIOMATIC_SYSTEM, debug)

def __test_model_or_inconsistent(prover, tests, rules, debug):
    for test in tests:
        formulae = [Formula.from_infix(i) for i in test]
        if (debug):
            print('Testing', prover.__qualname__, 'for:', formulae)
        result = prover(formulae)
        if type(result) is dict:
            if debug:
                print('Verifying returned model:', result)
            # Will be tested with the course staff's implementation of evaluate
            assert all(evaluate(f, result) for f in formulae)
        else:
            assert len(result) == 2
            for proof in result:
                assert proof.statement.assumptions == formulae
                assert proof.rules == rules, "got " + str(proof.rules) + ", expected " + str(rules)
                if debug:
                    print('Verifying returned proof (' +
                          '{:,}'.format(len(proof.lines)),
                          'lines) of ', proof.statement.conclusion)
                # Will be tested with the course staff's implementation of is_valid
                assert proof.is_valid()
            assert result[1].statement.conclusion == \
                   Formula('~', result[0].statement.conclusion)
