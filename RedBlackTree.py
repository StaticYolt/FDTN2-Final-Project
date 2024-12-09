from collections import deque
from enum import Enum


class Color(Enum):
    BLACK = 0
    RED = 1


class Node:
    def __init__(self, value, color=Color.RED):
        self.value = value
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

    def __str__(self):
        return f"{self.value} ({self.color.name})"

    def sibling(self):
        if not self.parent:
            return None
        if self == self.parent.left:
            return self.parent.right
        else:
            return self.parent.left


class RedBlackTree:
    def __init__(self, inp_arr=[]):
        self.NIL = Node(None, color=Color.BLACK)  #How to ensure all the Nil Nodes will be Black
        self.root = self.NIL
        self.arr_rep = []
        for element in inp_arr:
            self.insert(element)

    def __str__(self):
        return ", ".join(str(node) for node in self.arr_rep)
    #Runtime: O(1)
    def left_rotate(self, x: Node):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # Runtime: O(1)
    def right_rotate(self, y: Node):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    # Runtime: O(n)
    def insert(self, val: int):
        node = Node(val)
        node.left = self.NIL
        node.right = self.NIL

        parent = None
        current = self.root
        while current is not self.NIL:
            parent = current
            if node.value < current.value:
                current = current.left
            else:
                current = current.right

        node.parent = parent
        if parent is None:
            self.root = node
        elif node.value < parent.value:
            parent.left = node
        else:
            parent.right = node

        node.color = Color.RED
        self.insert_fixup(node)
        self.update_arr_rep()

    # Runtime: O(log(n))
    def insert_fixup(self, z: Node):
        while z.parent and z.parent.color == Color.RED:  # While parent is red
            if z.parent == z.parent.parent.left:  # Parent is a left child
                y = z.parent.sibling()  # Get the sibling of the parent (another term could be uncle)
                if y and y.color == Color.RED:  # Case 1: Uncle is red
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:  # Case 2: z is a right child
                        z = z.parent
                        self.left_rotate(z)
                    # Case 3: z is a left child
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self.right_rotate(z.parent.parent)
            else:  # Parent is a right child
                y = z.parent.sibling()  # Get the sibling of the parent
                if y and y.color == Color.RED:  # Case 1: Uncle is red
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:  # Case 2: z is a left child
                        z = z.parent
                        self.right_rotate(z)
                    # Case 3: z is a right child
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self.left_rotate(z.parent.parent)
        self.root.color = Color.BLACK  # Ensure the root is always black

    # Runtime: O(n)
    def search_value(self, value: int) -> Node:
        for node in self.arr_rep:
            if node.value == value:
                return node
        return self.NIL

    # Runtime: O(n)
    def inorder_traversal(self, node: Node = None):
        if node is None:
            node = self.root
        if node != self.NIL:
            self.inorder_traversal(node.left)
            print(f"{node.value} ({node.color.name})", end=" ")
            self.inorder_traversal(node.right)

    #Runtime: O(n)
    def update_arr_rep(self):
        self.arr_rep = []
        if self.root == self.NIL:
            return
        queue = deque([self.root])
        while queue:
            current = queue.popleft()
            if current != self.NIL:
                self.arr_rep.append(current)
                queue.append(current.left)
                queue.append(current.right)
    #Runtime: O(1)
    def transplant(self, x: Node, y: Node):
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.parent = x.parent
        self.update_arr_rep()
    #Runtime: O(n)
    def delete(self, val: int):
        z = self.search_value(val)
        if z == self.NIL:
            print("NO NULL FOUND")
            return None
        y = z
        y_c_original = y.color

        if z.left == self.NIL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_c_original = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_c_original == Color.BLACK:
            self.delete_fixup(x)
        self.update_arr_rep()

    # Runtime: O(log(n))
    def delete_fixup(self, x: Node):
        while x != self.root and x.color == Color.BLACK:
            if x == x.parent.left:
                y = x.parent.right
                if y.color == Color.RED:
                    y.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.left_rotate(x.parent)
                    y = x.parent.right
                if y.left.color == Color.BLACK and y.right.color == Color.BLACK:
                    y.color = Color.RED
                    x = x.parent
                else:
                    if y.right.color == Color.BLACK:
                        y.left.color = Color.BLACK
                        y.color = Color.RED
                        self.right_rotate(y)
                        y = x.parent.right
                    y.color = x.parent.color
                    x.parent.color = Color.BLACK
                    y.right.color = Color.BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                y = x.parent.left
                if y.color == Color.RED:
                    y.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.right_rotate(x.parent)
                    y = x.parent.left
                if y.right.color == Color.BLACK and y.left.color == Color.BLACK:
                    y.color = Color.RED
                    x = x.parent
                else:
                    if y.left.color == Color.BLACK:
                        y.right.color = Color.BLACK
                        y.color = Color.RED
                        self.left_rotate(y)
                        y = x.parent.left
                    y.color = x.parent.color
                    x.parent.color = Color.BLACK
                    y.left.color = Color.BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = Color.BLACK
    #Runtime: log(n)
    def minimum(self, x) -> Node:
        while x.left != self.NIL:
            x = x.left
        return x
