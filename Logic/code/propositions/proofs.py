""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/propositions/proofs.py """
import copy

from code.propositions.syntax import *

class InferenceRule:
    """ An inference rule, i.e., a list of zero or more assumed formulae, and
        a conclusion formula """

    def __init__(self, assumptions, conclusion):
        assert type(conclusion) == Formula
        for assumption in assumptions:
            assert type(assumption) == Formula
        self.assumptions = assumptions
        self.conclusion = conclusion

    def __eq__(self, other):
        if (len(self.assumptions) != len(other.assumptions)):
            return False
        if self.conclusion != other.conclusion:
            return False
        for assumption1, assumption2 in zip(self.assumptions, other.assumptions):
            if assumption1 != assumption2:
                return False
        return True

    def __ne__(self, other):
        return not self == other
        
    def __repr__(self):
        return str([assumption.infix() for assumption in self.assumptions]) + \
               ' ==> ' + self.conclusion.infix()

    def variables(self):
        """ Return the set of atomic propositions (variables) used in the
            assumptions and in the conclusion of self. """
        vars_inference_rule = self.conclusion.variables()
        for assumption in self.assumptions:
            vars_inference_rule = vars_inference_rule.union(assumption.variables())

        return vars_inference_rule
        
    def is_instance_of(self, rule, instantiation_map=None):
        """ Return whether there exist formulae f1,...,fn and variables
            v1,...,vn such that self is obtained by simultaneously substituting
            each occurrence of f1 with v1, each occurrence of f2 with v2, ...,
            in all of the assumptions of rule as well as in its conclusion.
            If so, and if instantiation_map is given, then it is (cleared and)
            populated with the mapping from each vi to the corresponding fi """

        if len(rule.assumptions) != len(self.assumptions):
            return False

        instantiation_map = {} if instantiation_map is None else instantiation_map
        for i in range(len(rule.assumptions)):
            if not InferenceRule._update_instantiation_map(self.assumptions[i], rule.assumptions[i], instantiation_map):
                return False

        if not InferenceRule._update_instantiation_map(self.conclusion, rule.conclusion, instantiation_map):
            instantiation_map.clear()
            return False

        return True


    @staticmethod
    def _update_instantiation_map(formula, template, instantiation_map):
        """ Return whether the given formula can be obtained from the given
            template formula by simultaneously and consistantly substituting,
            for every variable in the given template formula, every occurrence
            of this variable with some formula, while respecting the
            correspondence already in instantiation_map (which maps from
            variables to formulae). If so, then instantiation_map is updated
            with any additional substitutions dictated by this matching. If
            not, then instantiation_map may be modified arbitrarily """

        if is_constant(formula.root):
            return True

        if is_variable(template.root):
            if template.root in instantiation_map:
                if instantiation_map[template.root] != formula:
                    return False
            instantiation_map[template.root] = formula if instantiation_map is not None else None
            return True

        if template.root != formula.root:
            return False

        is_first = InferenceRule._update_instantiation_map(formula.first, template.first, instantiation_map)
        is_second, is_third = True, True

        if is_first and is_binary(template.root):
            is_second = InferenceRule._update_instantiation_map(formula.second, template.second, instantiation_map)

        if is_first and is_ternary(template.root):
            is_second = InferenceRule._update_instantiation_map(formula.second, template.second, instantiation_map)
            is_third = InferenceRule._update_instantiation_map(formula.third, template.third, instantiation_map)

        return is_first and is_second and is_third


class DeductiveProof:
    """ A deductive proof, i.e., a statement of an inference rule, a list of
        assumed inference rules, and a list of lines that prove the former from
        the latter """
    
    class Line:
        """ A line, i.e., a formula, the index of the inference rule whose
            instance justifies the formula from previous lines, and the list
            of indices of these previous lines """
        def __init__(self, conclusion, rule=None, justification=None):
            self.conclusion = conclusion
            self.rule = rule
            self.justification = justification

        def __repr__(self):
            if (self.rule is None):
                return self.conclusion.infix()
            r = self.conclusion.infix() + ' (Inference Rule ' + str(self.rule)
            sep = ';'
            for i in range(len(self.justification)):
                r += sep + ' Assumption ' + str(i) + ': Line ' + \
                     str(self.justification[i])
                sep = ','
            r += '.)' if len(self.justification) > 0 else ')'
            return r

    def __init__(self, statement, rules, lines):
        self.statement = statement
        self.rules = rules
        self.lines = lines

    def __repr__(self):
        r = 'Proof for ' + str(self.statement) + ':\n'
        for i in range(len(self.rules)):
            r += 'Inference Rule ' + str(i) + ': ' + str(self.rules[i]) + '\n'
        for i in range(len(self.lines)):
            r += str(i) + ') ' + str(self.lines[i]) + '\n'
        return r

    def instance_for_line(self, line):
        """ Return the instantiated inference rule that corresponds to the
            given line number """
        conclusion = self.lines[line].conclusion
        assumptions = [self.lines[assLine].conclusion for assLine in self.lines[line].justification]

        return InferenceRule(assumptions, conclusion)
        
    def is_valid(self):
        """ Return whether lines are a valid proof of statement from rules """
        num_lines = len(self.lines)
        if self.statement.conclusion != self.lines[num_lines-1].conclusion:
            return False
        for line_num in range(num_lines):
            line = self.lines[line_num]
            if line.rule is None:
                if line.conclusion not in self.statement.assumptions:
                    return False
            if (line.rule is not None and not self.instance_for_line(line_num).is_instance_of(self.rules[line.rule])) \
                    or (line.justification is not None and any(i >= line_num for i in line.justification)):
                return False

        return True


def instantiate(formula, instantiation_map):
    """ Return a formula obtained from the given formula by simultaneously
        substituting, for each variable v that is a key of instantiation_map,
        each occurrence v with the formula instantiation_map[v] """
    if is_constant(formula.root):
        return Formula(formula.root)

    if is_variable(formula.root):
        return instantiation_map[formula.root] if formula.root in instantiation_map else formula

    first = instantiate(formula.first, instantiation_map)
    if is_unary(formula.root):
        return Formula(formula.root, first)

    second = instantiate(formula.second, instantiation_map)
    if is_binary(formula.root):
        return Formula(formula.root, first, second)

    return Formula(formula.root, first, second, instantiate(formula.third, instantiation_map))


def instance_lines(proof, instance):
    in_map = {}
    if not instance.is_instance_of(proof.statement, in_map):
        return None

    len_lines = len(proof.lines)
    new_lines = [None] * len_lines
    for i in range(len_lines):
        line = proof.lines[i]
        new_lines[i] = DeductiveProof.Line(instantiate(line.conclusion, in_map), line.rule, line.justification)

    return new_lines


def prove_instance(proof, instance):
    """ Return a proof of the given instance of the inference rule that proof
        proves, via the same inference rules used by proof """
    return DeductiveProof(instance, proof.rules, instance_lines(proof, instance))


def get_rules_union(main_proof, lemma_proof, rule_idx):
    rules = copy.deepcopy(main_proof.rules)
    rules.pop(rule_idx)
    map_idx = {i:i for i in range(rule_idx)}
    map_idx.update({i: i-1 for i in range(rule_idx + 1, len(main_proof.rules))})

    for i in range(len(lemma_proof.rules)):
        l_rule = lemma_proof.rules[i]
        if l_rule not in main_proof.rules:
            rules.append(l_rule)
            map_idx.update({len(main_proof.rules) + i : len(rules) - 1})
        else:
            map_idx.update({len(main_proof.rules) + i: rules.index(l_rule)})

    return rules, map_idx


def update_lemma_lines(lemma_lines, map_rules, factor_mapping, cur_line_num):
    count_assum = 0
    pop = []
    for line in lemma_lines:
        if line.rule is None:
            pop.append(line)
            count_assum += 1
        else:
            line.rule = map_rules[factor_mapping + line.rule]
            if line.justification is not None and len(line.justification) > 0:
                line.justification = [cur_line_num + j - count_assum for j in line.justification]
    for p in pop:
        lemma_lines.remove(p)


def update_line(main_line, map_rules, map_lines):
    rule = None if main_line.rule is None else map_rules[main_line.rule]
    justification = None if main_line.justification is None else [map_lines[jus] for jus in main_line.justification]
    return DeductiveProof.Line(main_line.conclusion, rule, justification)


def merge_proofs(main, lemma, rule_idx, map_rules):
    lambda_rule = main.rules[rule_idx]
    map_lines = {}
    new_lines = []
    for i in range(len(main.lines)):
        main_line = main.lines[i]

        if main_line.rule is not None and main.rules[main_line.rule].is_instance_of(lambda_rule):
            lemma_in = prove_instance(lemma, main.instance_for_line(i))
            update_lemma_lines(lemma_in.lines, map_rules, len(main.rules), len(new_lines))
            new_lines += lemma_in.lines
        else:
            new_lines.append(update_line(main_line, map_rules, map_lines))

        map_lines.update({i: len(new_lines)-1})

    return new_lines




def inline_proof(main_proof, lemma_proof):
    """ Return a proof of the inference rule that main_proof proves, via the
        inference rules used in main_proof except for the one proven by
        lemma_proof, as well as via the inference rules used in lemma_proof
        (with duplicates removed) """
    lambda_rule_idx = main_proof.rules.index(lemma_proof.statement)
    rules, map_rules = get_rules_union(main_proof, lemma_proof, lambda_rule_idx)
    lines = merge_proofs(main_proof, lemma_proof, lambda_rule_idx, map_rules)
    return DeductiveProof(main_proof.statement, rules, lines)
