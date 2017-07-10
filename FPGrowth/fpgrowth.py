# -*- coding: utf-8 -*-


from collections import defaultdict, deque, OrderedDict

def _sortTransactionsByFreq(
        transactions, key_func, reverse_int=False,
        reverse_ext=False, sort_ext=True):
    key_seqs = [{key_func(i) for i in sequence} for sequence in transactions]
    frequencies = getFrequencies(key_seqs)

    asorted_seqs = []
    for key_seq in key_seqs:
        if not key_seq:
            continue
        # Sort each transaction (infrequent key first)
        l = [(frequencies[i], i) for i in key_seq]
        l.sort(reverse=reverse_int)
        asorted_seqs.append(tuple(l))
    # Sort all transactions. Those with infrequent key first, first
    if sort_ext:
        asorted_seqs.sort(reverse=reverse_ext)

    return (asorted_seqs, frequencies)


def getFrequencies(transactions):
    '''Computes a dictionary, {key:frequencies} containing the frequency of
       each key in all transactions. Duplicate keys in a transaction are
       counted twice.
       :param transactions: a sequence of sequences. [ [transaction items...]]
    '''
    frequencies = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            frequencies[item] += 1
    return frequencies



class FPNode(object):

    root_key = object()

    def __init__(self, key, parent):
        self.children = {}
        self.parent = parent
        self.key = key
        self.count = 0
        self.next_node = None

    def add_path(self, path, index, length, heads, last_insert):
        if index >= length:
            return

        child_key = path[index]
        index += 1

        try:
            child = self.children[child_key]
        except Exception:
            child = self._create_child(child_key, heads, last_insert)
        child.count += 1
        heads[child_key][1] += 1

        child.add_path(path, index, length, heads, last_insert)

    def _create_child(self, child_key, heads, last_insert):
        child = FPNode(child_key, self)
        self.children[child_key] = child
        try:
            last_child = last_insert[child_key]
            last_child.next_node = child
        except Exception:
            heads[child_key] = [child, 0]
        last_insert[child_key] = child

        return child

    def get_cond_tree(
            self, child, count, visited, heads, last_insert,
            dont_create=False):

        key = self.key

        if dont_create:
            # This is a head, we don't want to copy it.
            cond_node = None
        else:
            try:
                cond_node = visited[self]
            except Exception:
                cond_node = self._create_cond_child(
                    visited, heads, last_insert)

        if self.parent is not None:
            # Recursion
            parent_node = self.parent.get_cond_tree(
                cond_node, count, visited, heads, last_insert, False)
            if cond_node is not None:
                cond_node.count += count
                heads[key][1] += count
                cond_node.parent = parent_node

        return cond_node

    def _create_cond_child(self, visited, heads, last_insert):
        key = self.key
        cond_node = FPNode(key, None)
        visited[self] = cond_node
        try:
            last_cond_node = last_insert[key]
            last_cond_node.next_node = cond_node
        except Exception:
            # Don't add root!
            if self.parent is not None:
                heads[key] = [cond_node, 0]
        last_insert[key] = cond_node

        return cond_node

    def _find_ancestor(self, heads, min_support):
        ancestor = self.parent
        while ancestor.key != FPNode.root_key:
            support = heads[ancestor.key][1]
            if support >= min_support:
                break
            else:
                ancestor = ancestor.parent
        return ancestor

    def prune_me(
            self, from_head_list, visited_parents, merged_before,
            merged_now, heads, min_support):
        try:
            # Parent was merged
            new_parent = merged_before[self.parent]
            self.parent = new_parent
        except KeyError:
            # Ok, no need to change parent
            pass

        ancestor = self._find_ancestor(heads, min_support)
        self.parent = ancestor

        try:
            # Oh, we visited another child of this parent!
            other_node = visited_parents[ancestor]
            merged_now[self] = other_node
            other_node.count += self.count
            # Remove yourself from the list
            if from_head_list is not None:
                from_head_list.next_node = self.next_node
            self.next_node = None
        except KeyError:
            # We are a new child!
            visited_parents[ancestor] = self

    def __str__(self):
        child_str = ','.join([str(key) for key in self.children])
        return '{0} ({1})  [{2}]  {3}'.format(
            self.key, self.count, child_str,
            self.next_node is not None)

    def __repr__(self):
        return self.__str__()


def get_fptree(transactions, key_func=None, min_support=2):
    '''Given a list of transactions and a key function, returns a data
       structure used as the input of the relim algorithm.
       :param transactions: a sequence of sequences. [ [transaction items...]]
       :param key_func: a function that returns a comparable key for a
        transaction item.
       :param min_support: minimum support.
    '''

    if key_func is None:
        def key_func(e):
            return e

    asorted_seqs, frequencies = _sortTransactionsByFreq(
        transactions, key_func, True, False, False)
    transactions = [
        [item[1] for item in aseq if item[0] >= min_support] for
        aseq in asorted_seqs]

    root = FPNode(FPNode.root_key, None)
    heads = {}
    last_insert = {}
    for transaction in transactions:
        root.add_path(transaction, 0, len(transaction), heads, last_insert)

    # Here, v[1] is = to the frequency
    sorted_heads = sorted(heads.values(), key=lambda v: (v[1], v[0].key))
    new_heads = OrderedDict()
    for (head, head_support) in sorted_heads:
        new_heads[head.key] = (head, head_support)

    return (root, new_heads)


def _init_heads(orig_heads):
    new_heads = OrderedDict()
    for key in orig_heads:
        new_heads[key] = (None, 0)
    return new_heads


def _create_cond_tree(head_node, new_heads, pruning):
    visited = {}
    last_insert = {}
    while head_node is not None:
        head_node.get_cond_tree(
            None, head_node.count, visited, new_heads,
            last_insert, True)
        head_node = head_node.next_node
    return new_heads


def _prune_cond_tree(heads, min_support):
    merged_before = {}
    merged_now = {}
    for key in reversed(heads):
        (node, head_support) = heads[key]
        if head_support > 0:
            visited_parents = {}
            previous_node = None
            while node is not None:
                # If the node is merged, we lose the next_node
                next_node = node.next_node
                node.prune_me(
                    previous_node, visited_parents, merged_before,
                    merged_now, heads, min_support)
                if node.next_node is not None:
                    # Only change the previous node if it wasn't merged.
                    previous_node = node
                node = next_node
        merged_before = merged_now
        merged_now = {}


def fpgrowth(fptree, min_support=2, pruning=False):
    '''Finds frequent item sets of items appearing in a list of transactions
       based on FP-Growth by Han et al.
       :param fptree: The input of the algorithm. Must come from
        `get_fptree`.
       :param min_support: The minimal support of a set.
       :param pruning: Perform a pruning operation. Default to False.
       :rtype: A set containing the frequent item sets and their support.
    '''
    fis = set()
    report = {}
    _fpgrowth(fptree, fis, report, min_support, pruning)
    return report


def _fpgrowth(fptree, fis, report, min_support=2, pruning=True):
    (_, heads) = fptree
    n = 0
    for (head_node, head_support) in heads.values():
        if head_support < min_support:
            continue

        fis.add(head_node.key)
        report[frozenset(fis)] = head_support
        new_heads = _init_heads(heads)
        _create_cond_tree(head_node, new_heads, pruning)
        if pruning:
            _prune_cond_tree(new_heads, min_support)
        n = n + 1 + _fpgrowth(
            (None, new_heads), fis, report, min_support, pruning)
        fis.remove(head_node.key)
    return n
