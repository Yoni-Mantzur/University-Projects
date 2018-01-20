""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/predicates/prover.py """

from code.predicates.syntax import *
from code.predicates.proofs import *
from code.predicates.util import *

class Prover:
    """ A class for gradually constructing a first-order Proof for a given
        conclusion, from given assumptions as well as from the six AXIOMS
        Universal Instantiation (UI), Existential Introduction (EI), Universal
        Simplification (US), Existential Simplification (ES), Reflexivity (RX),
        and Meaning of Equality (ME) """
    UI = Schema('(Ax[R(x)]->R(c))', {'R','x','c'})
    EI = Schema('(R(c)->Ex[R(x)])', {'R','x','c'})
    US = Schema('(Ax[(Q()->R(x))]->(Q()->Ax[R(x)]))', {'x','Q','R'})
    ES = Schema('((Ax[(R(x)->Q())]&Ex[R(x)])->Q())', {'x','Q','R'})
    RX = Schema('c=c', {'c'})
    ME = Schema('(c=d->(R(c)->R(d)))', {'c','d','R'})
    AXIOMS = [UI, EI, US, ES, RX, ME]

    def __init__(self, assumptions, conclusion, print_as_proof_forms=False):
        """ Constructs a new Prover. Each element in assumptions may either be
            a Schema or a string, with the latter interpreted as a schema with
            no templates whose unique instance is the given string. Any
            element in assumptions that is already in Prover.AXIOMS is ignored
            as an element of assumptions, to avoid duplication. conclusion
            is the conclusion or its string representation. The Boolean flag
            print_as_proof_forms specifies whether the proof being constructed
            is to be printed in real time as it is being constructed """
        self.proof = Proof(Prover.AXIOMS +
                           [Schema(assumption)
                            if type(assumption) is str else assumption
                            for assumption in assumptions
                            if assumption not in Prover.AXIOMS],
                            Formula.parse(conclusion)
                            if type(conclusion) is str else conclusion, [])
        self.print_as_proof_forms = print_as_proof_forms
        if self.print_as_proof_forms:
            print("Starting Proof")
            print("Assumptions: AXIOMS +", assumptions)
            print("Conclusion:", self.proof.conclusion)

    def _add_line(self, statement, justification):
        """ Append to the proof being constructed the validly justified line
            whose formula is statement and whose justification is given. The
            validity of the added line is asserted, and its number in this
            proof is returned """
        assert type(statement) is Formula or type(statement) is str
        if type(statement) is str:
            statement = Formula.parse(statement)
        line = len(self.proof.lines)
        self.proof.lines.append(Proof.Line(statement, justification))
        assert self.proof.verify_justification(line)
        if self.print_as_proof_forms:
            print(str(line) + ")", statement)
        return line

    def add_instantiated_assumption(self, instance, schema, instantiation_map):
        """ Append to the proof being constructed a validly justified line
            whose formula is instance, which is the result of an instantiation
            via instantiation_map of the given schema, which must be one of the
            assumptions/axioms of this proof. The number of the added line in
            this proof is returned """
        assert type(instance) is Formula or type(instance) is str
        assert type(schema) is Schema
        return self._add_line(instance,
                              ('A', self.proof.assumptions.index(schema),
                               instantiation_map))
        
    def add_assumption(self, assumption):
        """ Append to the proof being constructed a validly justified line
            whose formula is assumption, which is the (unique) instance of a
            schema with no templates that is one of the assumptions/axioms of
            this proof. The number of the added line in this proof is returned
        """
        assert type(assumption) is Formula or type(assumption) is str
        return self.add_instantiated_assumption(
            assumption, Schema(str(assumption)), {})

    def add_tautology(self, tautology):
        """ Append to the proof being constructed a validly justified line
            whose formula is tautology, which is a tautology. The number of the
            added line in this proof is returned """
        assert type(tautology) is Formula or type(tautology) is str
        return self._add_line(tautology, ('T',))

    def add_mp(self, consequent, antecedent_line, conditional_line):
        """ Append to the proof being constructed a validly justified line
            whose formula is consequent, and which is a return of applying
            Modus Ponens over lines atecedent_line and conditional_line in this
            proof. The number of the added line in this proof is returned """
        assert type(consequent) is Formula or type(consequent) is str
        return self._add_line(consequent,
                              ('MP', antecedent_line, conditional_line))

    def add_ug(self, quantified, unquantified_line):
        """ Append to the proof being constructed a validly justified line
            whose formula is quantified, and which is a return of universal
            generalization over line unquantified_line in this proof. The
            number of the added line in this proof is returned """
        assert type(quantified) is Formula or type(quantified) is str
        return self._add_line(quantified, ('UG', unquantified_line))

    def add_proof(self, conclusion, proof):
        """ Append to the proof being constructed a whole copy of the
            given proof, where the formula of the last line is conclusion.
            The given proof must have the same list of assumptions, and
            this method takes care of the required line-shift in the
            justifications.  The number of the (new) line in this proof
            containing conclusion is returned """
        assert proof.assumptions == self.proof.assumptions
        line_shift = len(self.proof.lines)
        for line in proof.lines:
            if line.justification[0] == 'A' or line.justification[0] == 'T':
                self._add_line(line.formula, line.justification)
            if line.justification[0] == 'MP':
                self.add_mp(line.formula, line.justification[1] + line_shift,
                            line.justification[2] + line_shift)
            if line.justification[0] == 'UG':
                self.add_ug(line.formula, line.justification[1] + line_shift)
        line_number = len(self.proof.lines)-1
        assert str(self.proof.lines[line_number].formula) == str(conclusion)
        return line_number




    def add_universal_instantiation(self, instantiation, line_number, term):
        """ Append a sequence of validly justified lines to the proof being
            constructed, where the formula of the last line is statement, which
            is an instantiation of the formula in line line_number in this
            proof, where the instantiation is to the universally
            quantified variable appearing at the beginning of the formula in
            the given line number. Example: if line line_number has the formula
            'Ay[Az[f(x,y)=g(z,y)]]', then when calling this method with the
            term 'h(w)', the instantiation should be
            'Az[f(x,h(w))=g(z,h(w))]'. The number of the (new) line in this
            proof containing instantiation is returned """
        # Task 10.1
        instantiation = Formula.parse(instantiation) if type(instantiation) is str else instantiation
        term = term if type(term) is str else str(term)
        formula = self.get_line_conclusion(line_number)
        x = formula.variable
        instantiation_map = {'R(v)': self.substitute_term_to_formal_param(formula.predicate, x), 'x': x, 'c': term}
        endl = self.add_instantiated_assumption(Prover.UI.instantiate(instantiation_map), Prover.UI, instantiation_map)
        endl = self.add_mp(instantiation, line_number, endl)
        return self.assert_end_proof(endl, instantiation)

    def assert_end_proof(self, expected_line_number, actual_line):
        assert self.get_line_conclusion(expected_line_number) == \
               (actual_line if type(actual_line) is Formula else Formula.parse(actual_line))
        return expected_line_number

    @staticmethod
    def substitute_term_to_formal_param(formula, term):
        formula = Formula.parse(formula) if type(formula) is str else formula
        return str(formula.substitute({str(term): Term('v')}))

    def get_line_conclusion(self, line_number):
        return self.proof.lines[line_number].formula

    def add_tautological_inference(self, conclusion, line_numbers):
        """ Add a sequence of validly justified lines to the proof being
            constructed, where the formula of the last line is conclusion,
            which is a tautological inference of the formulae in the lines in
            this proof whose numbers are given in the list line_numbers. The
            number of the (new) line in this proof containing conclusion is
            returned """
        # Task 10.2

        # create tautological
        tautological = Formula.parse(conclusion) if type(conclusion) is str else conclusion
        for line_number in line_numbers[::-1]:
            tautological = Formula('->', self.get_line_conclusion(line_number), tautological)

        endl = self.add_tautology(tautological)

        # decompose tautological
        for line_number in line_numbers:
            endl = self.add_mp(tautological.second, line_number, endl)
            tautological = tautological.second

        return self.assert_end_proof(endl, conclusion)

    def add_existential_derivation(self, statement, line1, line2):
        """ Add a sequence of validly justified lines to the proof being
            constructed, where the formula of the last line is statement.
            The formula in line line1 must be of the form 'Ex[cond(x)]' (for
            some variable x), and the formula in line line2 must be of the form
            'cond(x)->statement' (where x is not free is statement). The number
            of the (new) line in this proof containing statement is returned """
        # Task 10.3

        statement = Formula.parse(statement) if type(statement) is str else statement
        exists_cond, cond_implies_statement = self.get_line_conclusion(line1), self.get_line_conclusion(line2)
        variable = exists_cond.variable
        step_UG = self.add_ug(Formula('A', variable, cond_implies_statement), line2)
        instantiation_map = {'R(v)': Prover.substitute_term_to_formal_param(exists_cond.predicate, variable),
                             'Q()': str(statement), 'x': variable}
        step_ES = self.add_instantiated_assumption(Prover.ES.instantiate(instantiation_map), Prover.ES,
                                                   instantiation_map)

        endl = self.add_tautological_inference(statement, [line1, step_UG, step_ES])
        return self.assert_end_proof(endl, statement)

    def add_flipped_equality(self, flipped, line_number):
        """ Add a sequence of validly justified lines to the proof being
            constructed, where the formula of the last line is flipped,
            which is an equality of the form 'c=d' (for some terms c, d) where
            the formula in line line_numer in this proof is 'd=c'. The number
            of the (new) line in this proof containing flipped is returned """
        # Task 10.6
        c_eq_d = self.proof.lines[line_number].formula
        assert is_equality(c_eq_d.root)
        c, d = str(c_eq_d.first), str(c_eq_d.second)

        end1 = self.apply_equality_axiom(Prover.ME, {'c': c, 'd': d, 'R(v)': 'v=' + c})
        end2 = self.apply_equality_axiom(Prover.RX, {'c': c})
        end2 = self.add_tautological_inference(d + '=' + c, [line_number, end1, end2])

        return self.assert_end_proof(end2, flipped)


    def add_free_instantiation(self, instantiation, line_number, substitution_map):
        """ Append a sequence of validly justified lines to the proof being
            constructed, where the formula of the last line is statement, which
            is an instantiation of the formula in line line_number in this
            proof, where the instantiation is simultaneously to the free
            variables appearing as keys in the substitution map. Example: if
            line line_number has the formula 'Az[f(x,y)=g(z,y)]', then when
            calling this method with the substitution map {'y':'h(w)'}, the
            instantiation should be 'Az[f(x,h(w))=g(z,h(w))]'. The number of the
            (new) line in this proof containing instantiation is returned """
        # Task 10.7
        instantiation_map_zi, substitution_map_with_zi = Prover.substitute_map(substitution_map)

        endl = self.substitute_origin(substitution_map, instantiation_map_zi, line_number)
        endl = self.substitute_origin(substitution_map_with_zi, substitution_map_with_zi, endl)

        return self.assert_end_proof(endl, instantiation)

    def substitute_origin(self, origin_map, substitute_map, line_number):
        """ substitute formula in line number given the maps """
        endl = line_number
        for origin in origin_map:
            substitute_var = Term.parse(substitute_map[origin]) if type(substitute_map[origin]) is str else \
                substitute_map[origin]
            formula = self.get_line_conclusion(endl)
            endl = self.add_ug('A' + str(origin) + '[' + str(formula) + ']', endl)
            endl = self.add_universal_instantiation(formula.substitute({origin: substitute_var}), endl, substitute_var)

        return endl

    @staticmethod
    def substitute_map(substitution_map):
        instantiation_map_zi, substitution_map_with_zi = {}, {}
        for y_i in substitution_map.keys():
            z_i = next(fresh_variable_name_generator)
            instantiation_map_zi[y_i] = z_i
            substitution_map_with_zi[z_i] = substitution_map[y_i]

        return instantiation_map_zi, substitution_map_with_zi

    def add_substituted_equality(self, substituted, line_number,
                                 term_with_free_v):
        """ Add a sequence of validly justified lines to the proof being
            constructed, where the formula of the last line is substituted,
            which is an equality of two terms, each of which is derived by
            substituting a term for the variable v in term_with_free_v. The
            two terms to be substituted for v are the two sides of the equality
            that is the formula in line line_number in this proof. Example: if
            line line_number has the formula 'g(x)=h(y)' and term_with_free_v
            is 'v+7', then substituted should be 'g(x)+7=h(y)+7'. The number of
            the (new) line in this proof containing substituted is returned """
        # Task 10.8
        formula = self.get_line_conclusion(line_number)
        phi, theta = formula.first, formula.second
        term_with_free_v = Term.parse(term_with_free_v) if type(term_with_free_v) is str else term_with_free_v
        t_phi, t_theta = str(term_with_free_v.substitute({'v': phi})), str(term_with_free_v.substitute({'v': theta}))

        phi, theta = str(formula.first), str(formula.second)
        end1 = self.apply_equality_axiom(Prover.ME, {'c': phi, 'd': theta, 'R(v)': t_phi + '=' + str(term_with_free_v)})
        end2 = self.apply_equality_axiom(Prover.RX, {'c': t_phi})

        endl = self.add_tautological_inference(substituted, [line_number, end1, end2])
        return self.assert_end_proof(endl, substituted)

    def _add_chained_two_equalities(self, line1, line2):
        """ Add a sequence of validly justified lines to the proof being
            constructed, where the formula of the last line is an equality of
            the form 'c=d' (for some terms c, d) where the formulae in lines
            line1 and line2 in this proof are respectively 'c=a' and 'a=d' (for
            some term a). Example: if Line 7 holds 'a=b', and Line 3 holds
            'b=f(b)', then if line1=7 and line2=3, then the formula of the last
            line added will be the chained equality 'a=f(b)'. The number of the
            (new) line in this proof containing the chained equality is
            returned """
        # Task 10.9.1
        a_eq_b = self.proof.lines[line1].formula
        b_eq_c = self.proof.lines[line2].formula

        a, b, c = str(a_eq_b.first), str(a_eq_b.second), str(b_eq_c.second)
        assert b == str(b_eq_c.first)

        flipped = self.add_flipped_equality(b + '=' + a, line1)
        endl = self.apply_equality_axiom(Prover.ME, {'c': b, 'd': a, 'R(v)': 'v=' + c})
        endl = self.add_tautological_inference(a + '=' + c, [flipped, line2, endl])

        return self.assert_end_proof(endl, a + '=' + c)

    def add_chained_equality(self, chained, line_numbers):
        """ Add a sequence of validly justified lines to the proof being
            constructed, where the formula of the last line is chained, which
            is an equality of the form 'c=d' (for some terms c, d) where the
            formulae in the lines in this proof whose numbers are given in the
            list line_numbers are of the form (in order) 'c=a1', 'a1=a2', ...,
            'an=d' (for some n and some terms a1,a2,...,an). Example: if Line 7
            holds 'a=b', Line 3 holds 'b=f(b)' and Line 9 holds 'f(b)=0', then
            if line_numbers=[7,3,9], then chained should be 'a=0'. The number of
            the (new) line in this proof containing substituted is returned """
        # Task 10.9.2
        endl = line_numbers[0]
        for line in line_numbers[1:]:
            endl = self._add_chained_two_equalities(endl, line)

        return self.assert_end_proof(endl, chained)

    def apply_equality_axiom(self, axiom, instantiation_map):
        return self.add_instantiated_assumption(axiom.instantiate(instantiation_map), axiom, instantiation_map)
