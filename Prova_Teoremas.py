# Implementação de Tableau Analítico para fórmulas proposicionais simples.

import re
from copy import deepcopy

# ----- Parser simples -----
# Tokens: ->, ~, &, |, (, ), atom (A..Z)
TOKEN_RE = re.compile(r'\s*(->|~|&|\||\(|\)|[A-Z])')

def tokenize(s):
    tokens = TOKEN_RE.findall(s)
    return [t for t in tokens if t.strip()]

# Gramática:
# F -> A | (F & F) | (F | F) | (F -> F) | ~F
# Usamos parser recursivo simples tratando prioridade por parênteses.

class Formula:
    def __repr__(self):
        return self.__str__()

class Atom(Formula):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

class Not(Formula):
    def __init__(self, f):
        self.f = f
    def __str__(self):
        return f"~{self.f}"

class And(Formula):
    def __init__(self, left, right):
        self.l = left; self.r = right
    def __str__(self):
        return f"({self.l}&{self.r})"

class Or(Formula):
    def __init__(self, left, right):
        self.l = left; self.r = right
    def __str__(self):
        return f"({self.l}|{self.r})"

class Imp(Formula):
    def __init__(self, left, right):
        self.l = left; self.r = right
    def __str__(self):
        return f"({self.l}->{self.r})"

# Parser recursivo simples que exige parênteses para binárias
def parse(tokens):
    # We'll parse using a stack-based approach that handles parentheses
    def parse_expr(i):
        if i >= len(tokens):
            raise ValueError("Unexpected end")
        tok = tokens[i]
        if tok == '~':
            node, j = parse_expr(i+1)
            return Not(node), j
        if re.fullmatch(r'[A-Z]', tok):
            return Atom(tok), i+1
        if tok == '(':
            left, j = parse_expr(i+1)
            op = tokens[j]
            if op not in ['&','|','->']:
                raise ValueError("Operator expected, got " + op)
            right, k = parse_expr(j+1)
            if tokens[k] != ')':
                raise ValueError("Missing )")
            if op == '&':
                return And(left, right), k+1
            if op == '|':
                return Or(left, right), k+1
            if op == '->':
                return Imp(left, right), k+1
        raise ValueError("Invalid token " + tok)

    node, pos = parse_expr(0)
    if pos != len(tokens):
        raise ValueError("Extra tokens")
    return node

def parse_formula(s):
    tokens = tokenize(s)
    return parse(tokens)

# ----- Tableau -----
# Representamos um ramo como lista de fórmulas (instâncias de Formula)

def is_literal(f):
    return isinstance(f, Atom) or (isinstance(f, Not) and isinstance(f.f, Atom))

def formula_to_str(f):
    return str(f)

def contains_contradiction(branch):
    # procura A e ~A na mesma branch
    atoms = set()
    neg_atoms = set()
    for f in branch:
        if isinstance(f, Atom):
            atoms.add(f.name)
        elif isinstance(f, Not) and isinstance(f.f, Atom):
            neg_atoms.add(f.f.name)
    return len(atoms.intersection(neg_atoms)) > 0

def expand_branch(branch):
    # retorna lista de branches resultantes (cada branch é lista de fórmulas)
    # Se branch contém contradicao -> é fechado, representado por []
    if contains_contradiction(branch):
        return []
    # procura primeira fórmula não literal
    for i, f in enumerate(branch):
        if not is_literal(f):

            rest = branch[:i] + branch[i+1:]
            if isinstance(f, Not):
                inner = f.f
                # ~~A -> A
                if isinstance(inner, Not):
                    new_branch = rest + [inner.f]
                    return [new_branch]
                # ~(A & B) -> (~A) | (~B)
                if isinstance(inner, And):
                    b1 = rest + [Not(inner.l)]
                    b2 = rest + [Not(inner.r)]
                    return [b1, b2]
                # ~(A | B) -> (~A) & (~B)
                if isinstance(inner, Or):
                    new_branch = rest + [Not(inner.l), Not(inner.r)]
                    return [new_branch]
                # ~(A -> B) -> A & ~B
                if isinstance(inner, Imp):
                    new_branch = rest + [inner.l, Not(inner.r)]
                    return [new_branch]
            # f é And/Or/Imp
            if isinstance(f, And):
                new_branch = rest + [f.l, f.r]
                return [new_branch]
            if isinstance(f, Or):
                b1 = rest + [f.l]
                b2 = rest + [f.r]
                return [b1, b2]
            if isinstance(f, Imp):
                # A -> B equivale a (~A) | B ; tabela: bifurca em ~A e B
                b1 = rest + [Not(f.l)]
                b2 = rest + [f.r]
                return [b1, b2]
    # só houver literais e sem contradição, ramo aberto
    return [branch]

def branch_closed(branch):
    return contains_contradiction(branch)

def is_unsatisfiable(formulas):
    # constrói tableau para a conjunção das formulas (que representam um ramo inicial)
    branches = [list(formulas)]
    while True:
        new_branches = []
        progressed = False
        for br in branches:
            if branch_closed(br):
                # ramo fechado -> não entra nas novas
                continue
            # procura fórmula não literal
            non_literals = [x for x in br if not is_literal(x)]
            if not non_literals:
                # ramo aberto -> mantém
                new_branches.append(br)
            else:
                progressed = True
                expanded = expand_branch(br)
                for nb in expanded:
                    new_branches.append(nb)
        branches = new_branches
        if not progressed:
            break
    # se todos ramos fechados -> insatisfatível
    return all(branch_closed(b) for b in branches)

def is_tautology(formula_str):
    # testa se formula é tautologia verificando insatisfatibilidade de ~φ
    phi = parse_formula(formula_str)
    neg_phi = Not(phi)
    return is_unsatisfiable([neg_phi])

# ----- Exemplos de uso -----
if __name__ == "__main__":
    examples = [
        ("(~(~P))", True),
        ("(P->(Q|~P))", True),
        ("(P&~P)", False),
        ("((P->Q)&P)->Q", True)  # modus ponens
    ]
    for s, expected in examples:
        try:
            res = is_tautology(s)
            print(f"{s} -> tautologia? {res} (esperado {expected})")
        except Exception as e:
            print(f"Erro ao analisar {s}: {e}")