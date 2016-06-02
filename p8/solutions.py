# -*- coding: utf-8
"""
Solutions to technical interview questions.
"""


def question1(s, t):
    """
    Given two strings s and t, determine whether some anagram of
    t is a substring of s. For example: if s = “udacity” and t = “ad”,
    then the function returns True. Your function definition should
    look like: “question1(s, t)”, and return a boolean True or False.
    :param s: string to search in
    :param t: string to search for
    :return:
    """
    def freqs(word):
        result = {}
        for letter in word:
            result[letter] = result.get(letter, 0) + 1
        return result

    if s and t and len(t) <= len(s):
        head = 0
        tail = head + len(t) - 1
        freqs_t = freqs(t)
        freqs_s = freqs(s[head:tail + 1])
        while tail < len(s):
            if freqs_t == freqs_s:
                return True
            if freqs_s[s[head]] == 1:
                del freqs_s[s[head]]
            else:
                freqs_s[s[head]] -= 1
            head += 1
            tail += 1
            if tail < len(s):
                freqs_s[s[tail]] = freqs_s.get(s[tail], 0) + 1
    return False


def question2(a):
    """
    Given a string a, find the longest palindromic substring contained in a.
    Your function definition should look like "question2(a)", and return
    a string.
    :param a: string to search for palindrome in
    :return:
    """
    max_len = 0
    max_pal = None

    if a:
        l = len(a)
        npos = 2 * l + 1
        for i in range(npos):
            head = i / 2
            tail = head + i % 2
            while head > 0 and tail < l and a[head - 1] == a[tail]:
                head -= 1
                tail += 1

            current_len = tail - head
            if current_len > max_len:
                max_len = current_len
                max_pal = a[head:tail]

    return max_pal


class Graph(object):
    """
    Graph representation.
    Nodes is a set of all nodes.
    Edges is a dict of:
      node_from: set([(node_to, weight),
                      (node_to, weight), ...])
    """
    def __init__(self, nodes=None, edges=None):
        self.nodes = set(nodes) if nodes else set([])
        self.edges = edges or {}

    def has_node(self, n):
        return n in self.nodes

    def add_edge(self, n1, n2, w):
        self.nodes.add(n1)
        self.nodes.add(n2)
        if n1 not in self.edges:
            self.edges[n1] = set([])
        self.edges[n1].add((n2, w))

    def as_list(self):
        return {
            n: list(es)
            for n, es in self.edges.items()
        }


def question3(G):
    """
    Given an undirected graph G, find the minimum spanning tree within G.
    A minimum spanning tree connects all vertices in a graph with the smallest
    possible total weight of edges. Your function should take in and return
    an adjacency list structured like this:
    {'A':[('B',2)],'B':[('A',2),('C',5)],'C':[('B',5)]}.
    Vertices are represented as unique strings. The function definition
    should be "question3(G)"
    Uses Kruskal's greedy algorithm.
    :param G: adjacency list
    :type G: dict
    :return: adjacency list
    :rtype: dict
    """
    # Create a dictionary mapping every vertex to its own tree at first.
    trees = {node: node for node in G}
    # Sort all edges by weight.
    edges = sorted([(w, n1, n2) for n1, es in G.iteritems() for n2, w in es])
    mst = Graph()
    for w, n1, n2 in edges:
        # if n1 and n2 belong to different trees, add them to MST and combine them into same tree
        if trees[n1] != trees[n2]:
            trees[n2] = trees[n1]
            mst.add_edge(n1, n2, w)
    return mst.as_list()


def test_q3():
    g1 = {
        'A': [('B', 2)],
        'B': [('A', 2), ('C', 5)],
        'C': [('B', 5)]
    }
    a1 = {
        'A': [('B', 2)],
        'B': [('C', 5)]
    }
    assert question3(g1) == a1
    print('Q3: OK')


def test_q1():
    assert question1('udacity', 'ad') == True
    assert question1('udacity', 'boo') == False
    assert question1('', '') == False
    assert question1(None, None) == False
    print('Q1: OK')


def test_q2():
    assert question2('abababa') == 'abababa'
    assert question2('forgeeksskeegfor') == 'geeksskeeg'
    assert question2(None) is None
    print('Q2: OK')


def main():
    test_q1()
    test_q2()
    test_q3()


if __name__ == '__main__':
    main()
