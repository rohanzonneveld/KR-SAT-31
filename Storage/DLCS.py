from collections import Counter

def dlcs(symbols, clauses):
    """
    DLCS (Dynamic Largest Combined Sum) heuristic
    Cp the number of clauses containing literal x
    Cn the number of clauses containing literal -x
    Here we select the variable maximizing Cp + Cn
    Returns x if Cp >= Cn otherwise -x
    """
    scores = Counter(l for c in clauses for l in disjuncts(c))
    CP_CN = sorted(symbols, key=lambda symbol: scores[symbol] + scores[~symbol])
    return P if scores[P] >= scores[~P] else -P