def mineAssocRules(isets, n, min_support=2, min_confidence=0.5):
    rules = []
    visited = set()
    for key in sorted(isets, key=lambda k: len(k), reverse=True):
        support = isets[key]
        if support < min_support or len(key) < 2:
            continue

        for item in key:
            left = key.difference([item])
            right = frozenset([item])
            _mineAssocRules(
                left, right, support, visited, isets,
                min_support, min_confidence, rules, n)

    return rules


def _mineAssocRules(
        left, right, rule_support, visited, isets, min_support,
        min_confidence, rules, n):
    if (left, right) in visited or len(left) < 1:
        return
    else:
        visited.add((left, right))

    #antecedent (left) => consequent (right)
    support_a = isets[left]
    support_b = isets[right]

    confidence = float(rule_support) / float(support_a)
    lift = ( float(rule_support) / n ) / ( float(support_a) / n*float(support_b) / n )
    cosine = ( float(support_a) + float(support_b) ) / float(support_a) * float(support_b)
    
    if confidence >= min_confidence:
        rules.append((left, right, rule_support, confidence, lift, cosine))
        # We can try to increase right!
        for item in left:
            new_left = left.difference([item])
            new_right = right.union([item])
            _mineAssocRules(
                new_left, new_right, rule_support, visited, isets,
min_support, min_confidence, rules, n)