""" (c) This file is part of the course
    Mathematical Logic through Programming
    by Gonczarowski and Nisan.
    File name: code/propositions/syntax.py """


def is_variable(s):
    """ Is s an atomic proposition?  """
    return 'p' <= s[0] <= 'z' and (len(s) == 1 or s[1:].isdigit())

def is_letter(s_i):
    return 'p' <= s_i <= 'z'

def is_unary(s):
    """ Is s a unary operator? """
    return s == '~'


def is_binary(s):
    """ Is s a binary operator? """
    return s == '&' or s == '|' or (len(s) == 2 and (s[0] == '-' and (s[1] == '>' or s[1] == '&' or s[1] == '|'))) \
           or (len(s) == 3 and (s[0] == '<' and s[1] == '-' and s[2] == '>'))


def is_constant(s):
    """ Is s a constant? """
    return s == 'T' or s == 'F'


def is_ternary(s):
    return len(s) == 2 and s[0] == '?' and s[1] == ':'


def get_root(root):
    if root[0] == '&' or root[0] == '|':
        return root[0], 1

    if root[0] == '-':
        return root[:2], 2

    if root[0] == '<':
        return root[:3], 3

    if root[0] == '?':
        return root[0], 0  # means ternary

    return '', -1


class Formula:
    """ A Propositional Formula """

    def __init__(self, root, first=None, second=None, third=None):
        """ Create a new formula from its root (a string) and, when needed, the
        first and second operands (each of them a Formula)."""
        if is_constant(root) or is_variable(root):
            assert first is None and second is None
            self.root = root
        elif is_unary(root):
            assert type(first) is Formula and second is None
            self.root, self.first = root, first
        elif is_binary(root):
            assert type(first) is Formula and type(second) is Formula
            self.root, self.first, self.second = root, first, second
        else:
            assert is_ternary(root) and type(first) is Formula and type(second) is Formula and type(third) is Formula
            self.root, self.first, self.second, self.third = root, first, second, third

    def __repr__(self):
        return self.infix()

    def __eq__(self, other):
        return self.infix() == other.infix()

    def __ne__(self, other):
        return not self == other

    def infix(self):
        """ Return an infix representation of self """

        def _infix_helper(f, infix_str):
            if f is None:
                return infix_str

            if is_constant(f.root) or is_variable(f.root):
                infix_str += f.root

            elif is_unary(f.root):
                infix_str += f.root + _infix_helper(f.first, infix_str)

            elif is_binary(f.root):
                infix_str += '(' + _infix_helper(f.first, infix_str) + f.root + _infix_helper(f.second, infix_str) + ')'

            else:
                infix_str += '(' + _infix_helper(f.first, infix_str) + f.root[0] + _infix_helper(f.second, infix_str) \
                             + f.root[1] + _infix_helper(f.third, infix_str) + ')'
            return infix_str

        return _infix_helper(self, "")

    @staticmethod
    def from_infix(s):
        """ Return a propositional formula whose infix representation is s """
        def _from_infix_helper(idx):
            if is_unary(s[idx]):
                first, new_idx = _from_infix_helper(idx+1)
                return Formula(s[idx], first), new_idx

            if s[idx] == '(':
                first, new_idx = _from_infix_helper(idx+1)
                root, gap_idx = get_root(s[new_idx:])
                if gap_idx > 0:
                    second, new_idx = _from_infix_helper(new_idx+gap_idx)
                    return Formula(root, first, second), new_idx + 1  # The new_idx + 1 is for the ')'

                second, new_idx = _from_infix_helper(new_idx+1)
                root2 = s[new_idx]
                third, new_idx = _from_infix_helper(new_idx + 1)
                return Formula(root + root2, first, second, third), new_idx + 1  # The new_idx + 1 is for the ')'
            if is_constant(s[idx]):
                return Formula(s[idx]), idx+1

            var_idx = Formula.get_variable_index(s, idx)
            if var_idx > 0:
                return Formula(s[idx:var_idx]), var_idx

            return None

        return _from_infix_helper(0)[0]

    @staticmethod
    def get_variable_index(s, ptr):
        idx = ptr
        if is_letter(s[idx]):
            idx += 1

        while idx < len(s) and s[idx].isdigit():
            idx += 1

        return idx

    def prefix(self):
        """ Return a prefix representation of self """
        # Task 1.3
        def _prefix_helper(f, prefix_str):
            if f is None:
                return prefix_str

            if is_constant(f.root) or is_variable(f.root):
                prefix_str += f.root

            elif is_unary(f.root):
                prefix_str += f.root + _prefix_helper(f.first, prefix_str)

            elif is_binary(f.root):
                prefix_str += f.root + _prefix_helper(f.first, prefix_str) + _prefix_helper(f.second, prefix_str)

            else:
                prefix_str += f.root + _prefix_helper(f.first, prefix_str) + _prefix_helper(f.second, prefix_str) + \
                              _prefix_helper(f.third, prefix_str)

            return prefix_str

        return _prefix_helper(self, "")

    @staticmethod
    def from_prefix(s):
        """ Return a propositional formula whose prefix representation is s """

        def _from_prefix_helper(idx):
            if is_unary(s[idx]):
                first, new_idx = _from_prefix_helper(idx+1)
                return Formula(s[idx], first), new_idx

            if is_constant(s[idx]):
                return Formula(s[idx]), idx+1

            root, gap_idx = get_root(s[idx:])
            if gap_idx >= 0:
                first, new_idx = _from_prefix_helper(idx+(gap_idx if gap_idx > 0 else 2))
                second, new_idx = _from_prefix_helper(new_idx)
                if gap_idx > 0:
                    return Formula(root, first, second), new_idx

                third, new_idx = _from_prefix_helper(new_idx)
                return Formula(s[idx:idx+2], first, second, third), new_idx

            var_idx = Formula.get_variable_index(s, idx)
            if var_idx > 0:
                return Formula(s[idx:var_idx]), var_idx
            return None

        return _from_prefix_helper(0)[0]

    def variables(self):
        """ Return the set of atomic propositions (variables) used in self """
        set_vars = set()

        def _variables_helper(f):

            if is_constant(f.root):
                return

            if is_variable(f.root):
                set_vars.add(f.root)
                return

            _variables_helper(f.first)

            if is_binary(f.root):
                _variables_helper(f.second)

            if is_ternary(f.root):
                _variables_helper(f.second)
                _variables_helper(f.third)

        _variables_helper(self)
        return set_vars


