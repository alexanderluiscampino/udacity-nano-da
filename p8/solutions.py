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

    # Can't search for a substring within None
    if s is None:
        return False

    # Empty string is a substring of any string
    if t == '':
        return True

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
    # No palindromes in None
    if a is None:
        return None

    # Longest palindrome in empty string is empty string
    if a == '':
        return ''

    max_len = 0
    max_pal = None
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
    if not G:
        return None

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


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def add_child(self, other):
        if other.value > self.value:
            self.right = other
        else:
            self.left = other

    def __repr__(self):
        return '{}'.format(self.value)


class BST(object):
    def __init__(self, root):
        self.root = root

    @classmethod
    def from_matrix(cls, m, r):
        nodes = {}
        # Collect all nodes in a dictionary by value
        for node_value in range(len(m[0])):
            nodes[node_value] = TreeNode(node_value)

        # Go through the dictionary and assign node children
        for node_value in nodes:
            for other_value, is_link in enumerate(m[node_value]):
                if is_link:
                    nodes[node_value].add_child(nodes[other_value])

        return BST(nodes[r])

    def lca(self, root, v1, v2):
        """Find lowest common ancestor node for values v1 and v2.
        :param root: TreeNode
        :param v1: int node value
        :param v2: int node value
        """
        if root is None:
            return None

        if v1 < root.value and v2 < root.value:
            return self.lca(root.left, v1, v2)

        if v1 > root.value and v2 > root.value:
            return self.lca(root.right, v1, v2)
        return root

    def __repr__(self):
        return self.format_tree(self.root)

    def format_node(self, node):
        return '{}: ({}, {})'.format(node.value, node.left, node.right)

    def format_tree(self, root):
        if root:
            return '{}\n{}\n{}'.format(
                self.format_node(root),
                self.format_node(root.left),
                self.format_node(root.right))


def question4(T, r, n1, n2):
    """
    Find the least common ancestor between two nodes on a binary search tree.
    The least common ancestor is the farthest node from the root that is an
    ancestor of both nodes. For example, the root is a common ancestor of
    all nodes on the tree, but if both nodes are descendants of the root's
    left child, then that left child might be the lowest common ancestor.
    You can assume that both nodes are in the tree, and the tree itself
    adheres to all BST properties. The function definition should look like
    "question4(T, r, n1, n2)", where T is the tree represented as a matrix,
    where the index of the list is equal to the integer stored in that node
    and a 1 represents a child node, r is a non-negative integer representing
    the root, and n1 and n2 are non-negative integers representing the two
    nodes in no particular order.
    :param T: Tree as 2d array
    :param r: root node value
    :param n1: first node to search for
    :param n2: second node to search for
    :return: int
    """
    if not T or r is None or n1 is None or n2 is None:
        return None

    tree = BST.from_matrix(T, r)
    result = tree.lca(tree.root, n1, n2)
    return result.value


class Node(object):
    """Linked list node."""
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        values = [self.data]
        current = self.next
        while current:
            values.append(current.data)
            current = current.next
        return ' -> '.join(['{}'.format(v) for v in values])


def create_ll(values):
    """Convenience method for testing linked list."""
    head = None
    if values:
        head = Node(values[0])
        current = head
        if len(values) > 1:
            for v in values[1:]:
                current.next = Node(v)
                current = current.next
    return head


def question5(ll, m):
    """
    Find the element in a singly linked list that's m elements from the end.
    For example, if a linked list has 5 elements, the 3rd element from the end is
    the 3rd element. The function definition should look like "question5(ll, m)",
    where ll is the first node of a linked list and m is the "mth number from the end".
    Return the value of the node at that position.
    :param ll: Node root
    :param m: int number of steps from end
    :return: int node value
    """
    slow = ll
    fast = ll

    # Move fast pointer forward m - 1 times
    for i in range(m - 1):
        fast = fast.next
        if fast is None:
            # Our list is shorter than the range asked.
            return None

    # Now move both fast and slow pointers until end of list.
    while True:
        if fast.next is None:
            return slow.data
        if slow.next is None:
            return None
        fast = fast.next
        slow = slow.next


def test_q1():
    assert question1('udacity', 'ad') == True
    assert question1('udacity', 'boo') == False
    assert question1('', '') == True
    assert question1('foo', '') == True
    assert question1(None, 'ab') == False
    assert question1(None, None) == False
    print('Q1: OK')


def test_q2():
    assert question2('abababa') == 'abababa'
    assert question2('forgeeksskeegfor') == 'geeksskeeg'
    assert question2('') == ''
    assert question2(None) is None
    print('Q2: OK')


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
    g2 = {
        'A': [('B', 1), ('C', 2)],
        'B': [('D', 3)],
        'C': [('D', 4)],
        'D': []
    }
    a2 = {
        'A': [('B', 1), ('C', 2)],
        'B': [('D', 3)]
    }
    assert question3(g1) == a1
    assert question3(g2) == a2
    assert question3(None) is None
    assert question3({}) is None

    print('Q3: OK')


def test_q4():
    assert question4(
        [[0, 1, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [1, 0, 0, 0, 1],
         [0, 0, 0, 0, 0]], 3, 1, 4) == 3
    assert question4([[0, 0, 0],
                      [1, 0, 1],
                      [0, 0, 0]], 1, 0, 2) == 1
    assert question4([], None, None, None) is None
    assert question4(None, None, None, None) is None
    print('Q4: OK')


def test_q5():
    l1 = create_ll([1, 2, 3, 4, 5])
    assert question5(l1, 3) == 3
    assert question5(l1, 4) == 2
    assert question5(l1, 5) == 1
    assert question5(l1, 6) is None
    print('Q5: OK')


def main():
    test_q1()
    test_q2()
    test_q3()
    test_q4()
    test_q5()


if __name__ == '__main__':
    main()
