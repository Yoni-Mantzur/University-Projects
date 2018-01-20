""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/predicates/proofs_test.py """

from code.predicates.syntax import *
from code.predicates.proofs import *

def test_instantiate_formula(debug=True):
    for formula_str,templates,constant_and_variable_instantiation_map,relations_instantiation_map,instance in [
            ('R(c)', {'c'}, {'c': Term('9')}, {},  'R(9)'),
            ('(R(0)->R(x))', {'R'}, {}, {'R': (['v'], Formula.parse('v=1'))},
             '(0=1->x=1)'),
            ('(Ax[R(x)]->R(c))', {'c', 'R'}, {'c': Term('9')},
             {'R': (['v'], Formula.parse('(Q(y)|v=0)'))},
             '(Ax[(Q(y)|x=0)]->(Q(y)|9=0))'),
            ('((R(0)&Az[(R(z)->R(s(z)))])->Az[R(z)])', {'R'}, {},
             {'R': (['v'], Formula.parse('plus(x,v)=plus(v,x)'))},
             '((plus(x,0)=plus(0,x)&Az[(plus(x,z)=plus(z,x)->plus(x,s(z))=plus(s(z),x))])->Az[plus(x,z)=plus(z,x)])'),
            ('Ax[R(x)]', {'R'}, {}, {'R':(['v'],Formula.parse('v=1'))},
             'Ax[x=1]'),
            ('Ax[R(x)]', {'R', 'x'}, {'x': Term('z')},
             {'R':(['v'],Formula.parse('v=x'))}, 'Az[z=x]')]:
        schema = Schema(formula_str, templates)
        if debug:
            print('Substituting constant and variable instantiation map',
                  constant_and_variable_instantiation_map,
                  'and relations instantiation map',
                  relations_instantiation_map,
                  'in schema', schema, '...')
        result = schema.instantiate_formula(
            Formula.parse(formula_str), constant_and_variable_instantiation_map,
            relations_instantiation_map, set())
        if debug:
            print('... yields', result)
        assert str(result) == instance

    for formula_str,templates,constant_and_variable_instantiation_map,relations_instantiation_map in [
            ('Ax[R(0)]', {'R'}, {}, {'R':(['v'],Formula.parse('x=1'))}),
            ('Ax[R(0)]', {'R', 'x'}, {'x': Term('z')},
             {'R':(['v'],Formula.parse('z=1'))})]:
        schema = Schema(formula_str, templates)
        if debug:
            print('Substituting constant and variable instantiation map',
                  constant_and_variable_instantiation_map,
                  'and relations instantiation map',
                  relations_instantiation_map,
                  'in schema', schema, '...')
        try:
            result = schema.instantiate_formula(
                Formula.parse(formula_str),
                constant_and_variable_instantiation_map,
                relations_instantiation_map, set())
            assert False
        except Schema.BoundVariableError:
            if debug:
                print('Threw a BoundVariableException as expected')

def test_instantiate(debug=True):
    for formula,templates,instantiation_map,instance in [
            ('R(c)', {'c'}, {'c':'9'}, 'R(9)'),
            ('(R(0)->R(x))', {'R'}, {'R(v)':'v=1'}, '(0=1->x=1)'),
            ('(Ax[R(x)]->R(c))', {'c', 'R'}, {'R(v)':'(Q(y)|v=0)', 'c':'9'},
             '(Ax[(Q(y)|x=0)]->(Q(y)|9=0))'),
            ('((R(0)&Az[(R(z)->R(s(z)))])->Az[R(z)])', {'R'},
             {'R(v)':'plus(x,v)=plus(v,x)'},
             '((plus(x,0)=plus(0,x)&Az[(plus(x,z)=plus(z,x)->plus(x,s(z))=plus(s(z),x))])->Az[plus(x,z)=plus(z,x)])'),
            ('(Ax[R(x)]->R(c))', {'c', 'x', 'R'},
             {'c':'0', 'x':'y', 'R(v)':'Q(v)'}, '(Ay[Q(y)]->Q(0))'),
            ('(Ax[R(x)]->R(c))', {'c', 'x', 'R'},
             {'c':'0', 'x':'y', 'R(x)':'Q(x)'}, '(Ay[Q(y)]->Q(0))'),
            ('(Ax[R(x)]->R(c))', {'c', 'x', 'R'},
             {'c':'0', 'x':'y', 'R(xyz)':'Q(xyz)'}, '(Ay[Q(y)]->Q(0))'),
            ('(Ax[R(x)]->R(c))', {'c', 'x', 'R'},
             {'c':'0', 'x':'y', 'R(xyz)':'Q(v)'}, '(Ay[Q(v)]->Q(v))'),
            ('(Ax[R(x)]->R(c))', {'c', 'x', 'R'},
             {'c':'f(g(a),g(a))', 'x':'x', 'R(vvv)':'(vvv=0|R(vvv,z))'},
             '(Ax[(x=0|R(x,z))]->(f(g(a),g(a))=0|R(f(g(a),g(a)),z)))'),
            ('(Ax[R(x)]->R(c))', {'c', 'x', 'R'}, {}, '(Ax[R(x)]->R(c))'),
            ('(Ax[R(x)]->R(c))', {'c', 'x', 'R'}, {'Q(v)':'v=0'}, None),
            ('(Ax[R(x)]->R(c))', {'c', 'x', 'R'}, {'R(z)':'Q(0)', 'a':'b'},
             None),
            ('(Ax[R(x)]->R(c))', {'c', 'x', 'R'}, {'c':'f(x)'},
             '(Ax[R(x)]->R(f(x)))'),
            ('(Ax[R(x)]->R(c))', {'c', 'x', 'R'}, {'c':'x', 'x':'z'},
             '(Az[R(z)]->R(x))'),
            ('(Ax[R(x)]->R(c))', {'c', 'x', 'R'},{'R(v)':'Q(v,z)'},
             '(Ax[Q(x,z)]->Q(c,z))'),
            ('(Ax[R(x)]->R(c))', {'c', 'x', 'R'},{'R(v)':'Q(v,x)'}, None),
            ('(Ax[R(x)]->R(c))', {'c', 'x', 'R'},{'x':'z', 'R(v)':'Q(v,x)'},
             '(Az[Q(z,x)]->Q(c,x))'),
            ('(Ax[R(x)]->R(c))', {'c', 'x', 'R'}, {'c':'z', 'R(v)':'Q(v,z)'},
             '(Ax[Q(x,z)]->Q(z,z))'),
            ('(c1=c2->(R(c1)->R(c2)))', {'c1', 'c2', 'R'},
             {'c1':'f(x)', 'R(v)':'v=c'}, '(f(x)=c2->(f(x)=c->c2=c))'),
            ('(c1=c2->(R(c1)->R(c2)))', {'c1', 'c2', 'R'},
             {'c2':'c1', 'c1':'c2'}, '(c2=c1->(R(c2)->R(c1)))'),
            ('(c1=c2->(R(c1)->R(c2)))', {'c1', 'c2', 'R'},
             {'R(v)':'R(c1,c2,v)'}, '(c1=c2->(R(c1,c2,c1)->R(c1,c2,c2)))'),
            ('(c1=c2->(R(c1)->R(c2)))', {'c1', 'c2', 'R'},
             {'c1':'c2', 'c2':'c1', 'R(v)':'R(c1,c2,v)'},
             '(c2=c1->(R(c1,c2,c2)->R(c1,c2,c1)))'),
            ('(c1=c2->(R(c1)->R(c2)))', {'c1', 'c2', 'R'},
             {'R(v)':'(Q(v)&Av[S(v)])'},
             '(c1=c2->((Q(c1)&Av[S(v)])->(Q(c2)&Av[S(v)])))'),
            ('(Ax[(Q()->R(x))]->(Q()->Ax[R(x)]))', {'R', 'Q', 'x'},
             {'Q()':'v=0', 'R(v)':'S(v)'},
             '(Ax[(v=0->S(x))]->(v=0->Ax[S(x)]))'),
            ('(Ax[(Q()->R(x))]->(Q()->Ax[R(x)]))', {'R', 'Q', 'x'},
             {'Q()':'v=0', 'R(v)':'S(v)', 'x':'z'},
             '(Az[(v=0->S(z))]->(v=0->Az[S(z)]))'),
            ('(Ax[(Q()->R(x))]->(Q()->Ax[R(x)]))', {'R', 'Q', 'x'},
             {'Q()':'z=0'},
             '(Ax[(z=0->R(x))]->(z=0->Ax[R(x)]))'),
            ('(Ax[(Q()->R(x))]->(Q()->Ax[R(x)]))', {'R', 'Q', 'x'},
             {'Q()':'x=0'}, None),
            ('(Ax[(Q()->R(x))]->(Q()->Ax[R(x)]))', {'R', 'Q', 'x'},
             {'Q()':'x=0', 'x':'z'}, '(Az[(x=0->R(z))]->(x=0->Az[R(z)]))'),
            ('(Ax[(Q()->R(x))]->(Q()->Ax[R(x)]))', {'R', 'Q', 'x'},
             {'Q()':'z=0', 'x':'z'}, None),
            ('(Axxx[RRR(xxx)]->Eyyy[QQQ(yyy)])', {'RRR', 'yyy'},
             {'RRR(zzz)':'zzz=yyy', 'yyy':'xxx'},
             '(Axxx[xxx=yyy]->Exxx[QQQ(xxx)])'),
            ('(Axxx[RRR(xxx)]->Eyyy[QQQ(yyy)])', {'RRR', 'yyy'},
             {'QQQ(v)':'v=0'}, None),
            ('(Axxx[RRR(xxx)]->Eyyy[QQQ(yyy)])', {'RRR', 'yyy'},
             {'QQQ(v)':'RRR(v)'}, None),
            ('(Axxx[RRR(xxx)]->Eyyy[QQQ(yyy)])', {'RRR', 'yyy'}, {'xxx':'z'},
             None)]:
        schema = Schema(formula, templates)
        if debug:
            print('Substituting instantiation map', instantiation_map,
                  'in schema', schema, '...')
        result = schema.instantiate(instantiation_map)
        if debug:
            print('... yields', result)
        if instance is None:
            assert result is None
        else:
            assert str(result) == instance

def test_verify_a_justification(debug=True):
    for assumption_str,templates,instantiation_map,conclusion_str,validity in [
            ('u=0', {'u'}, {'u': 'x'}, 'x=0', True),
            ('(u=0->v=1)', {'u', 'v'}, {'u': 'x', 'v': 'y'}, '(x=0->y=1)', True),
            ('Ev[u=f(v)]', {'v'}, {'v': 'x'}, 'Ex[u=f(x)]', True),
            ('u=0', {'u'}, {'u': 'x'}, 'y=0', False),
            ('Av[u=v]', {'u'}, {'u': 'x'}, 'Av[u=v]', False),
            ('Av[u=v]', {'u'}, {'u': 'x'}, 'Ax[u=x]', False),
            ('Ax[(Q(z)->R(x))]', {'Q'}, {'Q(v)': 'x=v'}, 'Ax[(x=z->R(x))]', False)]:

        assumptions = [Schema(assumption_str, templates)]
        conclusion = Formula.parse(conclusion_str)
        lines = [Proof.Line(Formula.parse(conclusion_str), ('A', 0, instantiation_map))]
        proof = Proof(assumptions, conclusion, lines)
        checked_line = 0
        if debug:
            print('Verifying A justification of line ' + str(checked_line) +
                  ' in proof:\n' + str(proof))
        result = proof.verify_a_justification(checked_line)
        if debug:
            print('... yields', result)
        assert result == validity

def test_verify_t_justification(debug=True):
    for conclusion_str,validity in [
            ('(R(c)|~R(c))', True),
            ('(x=0->x=0)', True),
            ('(((R(x)->Q(y))&(Q(y)->S(z)))->(R(x)->S(z)))', True),
            ('(Ex[x=0]->Ex[x=0])', True),
            ('x=0', False),
            ('x=x', False),
            ('Ax[(R(0)|~R(0))]', False)]:
        conclusion = Formula.parse(conclusion_str)
        lines = [Proof.Line(Formula.parse(conclusion_str), ('T',))]
        proof = Proof([], conclusion, lines)
        checked_line = 0
        if debug:
            print('Verifying T justification of line ' + str(checked_line) +
                  ' in proof:\n' + str(proof))
        result = proof.verify_t_justification(checked_line)
        if debug:
            print('... yields', result)
        assert result == validity

def test_verify_mp_justification(debug=True):
    # Test valid line
    assumptions = [Schema('u=0', {'u'}),
                   Schema('(u=0->v=1)', {'u', 'v'})]
    conclusion = Formula.parse('v=1')
    lines = [Proof.Line(Formula.parse('x=0'), ('A', 0, {'u': 'x'})),
             Proof.Line(Formula.parse('(x=0->y=1)'), ('A', 1, {'u': 'x', 'v': 'y'})),
             Proof.Line(Formula.parse('y=1'), ('MP', 0, 1))]
    proof = Proof(assumptions, conclusion, lines)
    checked_line = 2
    if debug:
        print('Verifying MP justification of line ' + str(checked_line) +
              ' in proof:\n' + str(proof))
    result = proof.verify_mp_justification(checked_line)
    if debug:
        print('... yields', result)
    assert result

    # Test valid line reversed order assumption
    assumptions = [Schema('(u=0->v=1)', {'u', 'v'}),
                   Schema('u=0', {'u'})]
    conclusion = Formula.parse('v=1')
    lines = [Proof.Line(Formula.parse('(f(x)=0->g(y)=1)'),
                        ('A', 0, {'u': 'f(x)', 'v': 'g(y)'})),
             Proof.Line(Formula.parse('f(x)=0'), ('A', 1, {'u': 'f(x)'})),
             Proof.Line(Formula.parse('g(y)=1'), ('MP', 1, 0))]
    proof = Proof(assumptions, conclusion, lines)
    checked_line = 2
    if debug:
        print('Verifying MP justification of line ' + str(checked_line) +
              ' in proof:\n' + str(proof))
    result = proof.verify_mp_justification(checked_line)
    if debug:
        print('... yields', result)
    assert result

    # Test valid line with quantifier
    assumptions = [Schema('(u=0->v=1)', {'u', 'v'}),
                   Schema('u=0', {'u'})]
    conclusion = Formula.parse('v=1')
    lines = [Proof.Line(Formula.parse('(Ax[f(x)=0]->Ey[f(y)=1])'),
                        ('A', 0, {'u': 'Ax[f(x)=0]', 'v': 'Ey[f(y)=1]'})),
             Proof.Line(Formula.parse('Ax[f(x)=0]'),
                        ('A', 1, {'u': 'Ax[f(x)=0]'})),
             Proof.Line(Formula.parse('Ey[f(y)=1]'), ('MP', 1, 0))]
    proof = Proof(assumptions, conclusion, lines)
    checked_line = 2
    if debug:
        print('Verifying MP justification of line ' + str(checked_line) +
              ' in proof:\n' + str(proof))
    result = proof.verify_mp_justification(checked_line)
    if debug:
        print('... yields', result)
    assert result

    # Test invalid line - type 1
    assumptions = [Schema('u=0', {'u'}),
                   Schema('(u=1->v=1)', {'u', 'v'})]
    conclusion = Formula.parse('v=1')
    lines = [Proof.Line(Formula.parse('x=0'), ('A', 0, {'u': 'x'})),
             Proof.Line(Formula.parse('(x=1->y=1)'),
                        ('A', 1, {'u': 'x', 'v': 'y'})),
             Proof.Line(Formula.parse('y=1'), ('MP', 0, 1))]
    proof = Proof(assumptions, conclusion, lines)
    checked_line = 2
    if debug:
        print('Verifying MP justification of line ' + str(checked_line) +
              ' in proof:\n' + str(proof))
    result = proof.verify_mp_justification(checked_line)
    if debug:
        print('... yields', result)
    assert not result

    # Test invalid line - type 2
    assumptions = [Schema('u=0', {'u'}),
                   Schema('(u=0->v=1)', {'u', 'v'})]
    conclusion = Formula.parse('v=0')
    lines = [Proof.Line(Formula.parse('x=0'), ('A', 0, {'u': 'x'})),
             Proof.Line(Formula.parse('(x=0->y=1)'),
                        ('A', 1, {'u': 'x', 'v': 'y'})),
             Proof.Line(Formula.parse('y=0'), ('MP', 0, 1))]
    proof = Proof(assumptions, conclusion, lines)
    checked_line = 2
    if debug:
        print('Verifying MP justification of line ' + str(checked_line) +
              ' in proof:\n' + str(proof))
    result = proof.verify_mp_justification(checked_line)
    if debug:
        print('... yields', result)
    assert not result

    # Test pointing to lines that appear after the conclusion
    assumptions = [Schema('u=0', {'u'}),
                   Schema('(u=0->v=1)', {'u', 'v'})]
    conclusion = Formula.parse('v=1')
    lines = [Proof.Line(Formula.parse('x=0'), ('A', 0, {'u': 'x'})),
             Proof.Line(Formula.parse('y=1'), ('MP', 0, 2)),
             Proof.Line(Formula.parse('(x=0->y=1)'),
                        ('A', 1, {'u': 'x', 'v': 'y'}))]
    proof = Proof(assumptions, conclusion, lines)
    checked_line = 1
    if debug:
        print('Verifying MP justification of line ' + str(checked_line) +
              ' in proof:\n' + str(proof))
    result = proof.verify_mp_justification(checked_line)
    if debug:
        print('... yields', result)
    assert not result

def test_verify_ug_justification(debug=True):
    for assumption_str, templates, conclusion_str, validity in [
            ('x=0', {'x'}, 'Ax[x=0]', True),
            ('x=0', {'x'}, 'Ay[x=0]', True),
            ('Ax[x=0]', set(), 'Ax[Ax[x=0]]', True),
            ('(x=0&y=0)', {'x', 'y'}, 'Ax[(x=0&y=0)]', True),
            ('R(c)', {'c'}, 'Axyz[R(c)]', True),
            ('x=0', {'x'}, 'Ex[x=0]', False),
            ('x=0', {'x'}, 'Ax[z=0]', False),
            ('(x=0&y=0)', {'x', 'y'}, '(Ax[x=0]&y=0)', False)]:
        assumptions = [Schema(assumption_str, templates)]
        conclusion = Formula.parse(conclusion_str)
        lines = [Proof.Line(Formula.parse(assumption_str), ('A', 0, {})),
                 Proof.Line(Formula.parse(conclusion_str), ('UG', 0))]
        proof = Proof(assumptions, conclusion, lines)
        checked_line = 1
        if debug:
            print('Verifying UG justification of line ' + str(checked_line) +
                  ' in proof:\n' + str(proof))
        result = proof.verify_ug_justification(checked_line)
        if debug:
            print('... yields', result)
        assert result == validity

        # Test pointing to lines that appear after the conclusion
        assumptions = [Schema('x=0', {'x'})]
        conclusion = Formula.parse('Ax[x=0]')
        lines = [Proof.Line(Formula.parse('Ax[x=0]'), ('UG', 1)),
                 Proof.Line(Formula.parse('x=0'), ('A', 0, {}))]
        proof = Proof(assumptions, conclusion, lines)
        checked_line = 0
        if debug:
            print('Verifying UG justification of line ' + str(checked_line) +
                  ' in proof:\n' + str(proof))
        result = proof.verify_ug_justification(checked_line)
        if debug:
            print('... yields', result)
        assert not result

def test_is_valid(debug=True):
    assumptions = []
    conclusion=Formula.parse('(R(0)|~R(0))')
    proof = Proof(assumptions,conclusion, [])
    if debug:
        print('\n*************\nCreated a Proof:', proof)
    proof.lines.append(Proof.Line(Formula.parse('(R(0)|R(0))'), ('T',)))
    assert not proof.verify_t_justification(0)
    proof.lines[0] = Proof.Line(Formula.parse('(R(0)->R(0))'), ('T',))
    assert proof.verify_t_justification(0)
    assert not proof.is_valid()
    proof.lines[0] = Proof.Line(conclusion, ('T',))
    assert proof.verify_t_justification(0)
    if debug:
        print('Added a line and got:', proof)
    assert proof.is_valid()

    assumptions = [Schema('R(0)'), Schema('(R(0)->Q(1))')]
    conclusion = Formula.parse('Q(1)')
    lines = [Proof.Line(assumptions[0].formula,('A',0,{})),
             Proof.Line(assumptions[1].formula,('A',1,{})),
             Proof.Line(conclusion, ('MP',0,1))]
    proof = Proof(assumptions, conclusion, lines)
    if debug:
        print('\n*************\nCreated a Proof:', proof)
    assert proof.is_valid()


    assumptions = [Schema('R(x)')]
    conclusion = Formula.parse('Ax[R(x)]')
    lines = [Proof.Line(assumptions[0].formula, ('A',0,{})),
             Proof.Line(conclusion, ('UG',0))]
    proof = Proof(assumptions, conclusion, lines)
    if debug:
        print('\n*************\nCreated a Proof:', proof)
    assert proof.is_valid()
