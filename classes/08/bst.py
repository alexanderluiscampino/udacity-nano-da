class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST(object):
    def __init__(self, root):
        self.root = Node(root)

    def insert(self, new_val):
        if self.root:
            self.add_child(self.root, new_val)
        else:
            self.root = Node(new_val)

    def search(self, find_val):
        return self.find_child(self.root, find_val)

    def add_child(self, start, value):
        if value > start.value:
            if start.right:
                self.add_child(start.right, value)
            else:
                start.right = Node(value)
        else:
            if start.left:
                self.add_child(start.left, value)
            else:
                start.left = Node(value)

    def find_child(self, start, value):
        if not start:
            return False
        if start.value == value:
            return True
        if value > start.value:
            return self.find_child(start.right, value)
        else:
            return self.find_child(start.left, value)

# Set up tree
tree = BST(4)

# Insert elements
tree.insert(2)
tree.insert(1)
tree.insert(3)
tree.insert(5)

# Check search
# Should be True
print tree.search(4)
# Should be False
print tree.search(6)
