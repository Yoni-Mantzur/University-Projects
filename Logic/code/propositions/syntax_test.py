""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/propositions/syntax_test.py """

from code.propositions.syntax import Formula

def test_infix(debug=True):
    if debug:
        print("Testing infix of formula 'x12'")
    assert Formula('x12').infix() == 'x12'
    if debug:
        print("Testing infix of formula '(p|p)'")
    assert Formula('|',Formula('p'),Formula('p')).infix() == '(p|p)'
    if debug:
        print("Testing infix of formula '~(p&q7)'")
    assert Formula('~', Formula('&', Formula('p'), Formula('q7'))).infix() == '~(p&q7)'
                  
def test_from_infix(debug=True):
    for infix in ['p', '~x12', '(x&y)', '~~(x|~T)', '((x1&~x2)|F)']:
        if debug:
            print("Testing infix parsing of formula", infix)
        assert Formula.from_infix(infix).infix() == infix

def test_prefix(debug=True):
    if debug:
        print("Testing prefix of formula 'x12'")
    assert Formula('x12').prefix() == 'x12'
    if debug:
        print("Testing prefix of formula '|pp' (in infix: '(p|p)')")
    assert Formula('|',Formula('p'),Formula('p')).prefix() == '|pp'
    if debug:
        print("Testing prefix of formula '~&pq7' (in infix: '~(p&q7)')")
    assert Formula('~', Formula('&', Formula('p'), Formula('q7'))).prefix() == '~&pq7'

def test_from_prefix(debug=False):
    for prefix in ['p', '~x12', '&xy', '~~|x~T', '|&x1~x2F']:
        if debug:
            print("Testing prefix parsing of formula", prefix)
        assert Formula.from_prefix(prefix).prefix() == prefix

def test_variables(debug=False):
    for infix,variables in [['(x|(y70&~x))', {'x', 'y70'}],
                            ['((x|y)|z)', {'x', 'y', 'z'}],
                            ['~~(p11&~q11)', {'p11', 'q11'}],
                            ['(T|p)', {'p'}],
                            ['F', set()],
                            ['~(T|F)', set()]]:
        formula = Formula.from_infix(infix)
        if debug:
            print ("Testing variables of", formula)
        assert formula.variables() == variables

def test_infix_all_operators(debug=False):
    for binary_operator in ['->', '<->', '-&', '-|']:
        infix = '(p' + binary_operator + 'q)'
        if debug:
            print("Testing infix of formula '" + infix + "'")
        assert Formula(binary_operator, Formula('p'), Formula('q')).infix() == infix

    if debug:
        print("Testing infix of formula '(p?q:r)'")
    assert Formula('?:', Formula('p'), Formula('q'), Formula('r')).infix() == '(p?q:r)'


def test_from_infix_all_operators(debug=False):
    for infix in ['T', 'F', 'p', '~p', '(p&q)', '(p|q)', '(p->q)', '(p<->q)',
                  '(p-&q)', '(p-|q)', '(p?q:r)', '(F?F:F)', '(T->T)',
                  '(~(x->y)->z)', '~(T?T:T)', '((x<->x)?x:x)',
                  '(F?(y123-&F):(y123-|F))']:
        if debug:
            print("Testing infix parsing of formula", infix)
        assert Formula.from_infix(infix).infix() == infix

def test_prefix_all_operators(debug=False):
    for binary_operator in ['->', '<->', '-&', '-|']:
        infix = '(p' + binary_operator + 'q)'
        prefix = binary_operator + 'pq'
        if debug:
            print("Testing prefix of formula '" + prefix + "' (in infix: '" + infix + "')")
        assert Formula(binary_operator, Formula('p'), Formula('q')).prefix() == prefix

    if debug:
        print("Testing prefix of formula '?:pqr' (in infix: '(p?q:r)')")
    assert Formula('?:', Formula('p'), Formula('q'), Formula('r')).prefix() == '?:pqr'

def test_from_prefix_all_operators(debug=False):
    for prefix in ['T', 'F', 'p', '~p', '&pq', '|pq', '->pq', '<->pq', '-&pq',
                   '-|pq', '?:pqr', '?:FFF', '->TT', '->~->xyz', '~?:TTT',
                   '?:<->xxxx', '?:F-&y123F-|y123F']:
        if debug:
            print("Testing prefix parsing of formula", prefix)
        assert Formula.from_prefix(prefix).prefix() == prefix

def test_variables_all_operators(debug=False):
    for infix,variables in [['(x|(y70&~(p?y70:z)))', {'p', 'x', 'y70', 'z'}],
                            ['(((x1->x11)-|x111)-&(x1?x11:(x111<->x1111)))',
                             {'x1', 'x11', 'x111', 'x1111'}]]:
        formula = Formula.from_infix(infix)
        if debug:
            print ("Testing variables of", formula)
        assert formula.variables() == variables
