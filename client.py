"""Red-Black Tree Ordered Index Engine.
100% Python Standard Library.
"""

from typing import Dict, List, Any, Optional, Tuple

RED = True
BLACK = False

class RBNode:
    def __init__(self, key, value, color=RED, parent=None, left=None, right=None):
        self.key = key
        self.value = value
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right

class RedBlackTreeIndex:
    """Self-balancing Red-Black Tree providing guaranteed O(log N) search, insertion, and range queries."""

    def __init__(self):
        self.NIL = RBNode(key=None, value=None, color=BLACK)
        self.root = self.NIL
        self.size = 0

    def _left_rotate(self, x):
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

    def _right_rotate(self, y):
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

    def insert(self, key, value):
        node = RBNode(key=key, value=value, color=RED, parent=None, left=self.NIL, right=self.NIL)
        y = None
        x = self.root
        while x != self.NIL:
            y = x
            if node.key < x.key:
                x = x.left
            elif node.key > x.key:
                x = x.right
            else:
                x.value = value
                return
        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
        self.size += 1
        self._insert_fixup(node)

    def _insert_fixup(self, z):
        while z.parent and z.parent.color == RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == RED:
                    z.parent.color = BLACK
                    y.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._left_rotate(z.parent.parent)
        self.root.color = BLACK

    def search(self, key):
        curr = self.root
        while curr != self.NIL:
            if key == curr.key:
                return curr.value
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return None

    def range_query(self, min_key, max_key) -> List[Tuple[Any, Any]]:
        results = []
        def in_order(node):
            if node == self.NIL:
                return
            if node.key > min_key:
                in_order(node.left)
            if min_key <= node.key <= max_key:
                results.append((node.key, node.value))
            if node.key < max_key:
                in_order(node.right)
        in_order(self.root)
        return results

    def verify_invariants(self) -> Dict[str, Any]:
        if self.root == self.NIL:
            return {"valid": True, "black_height": 0, "size": 0}
        if self.root.color != BLACK:
            return {"valid": False, "error": "Root is not black"}

        black_height_set = set()

        def dfs(node, black_count):
            if node == self.NIL:
                black_height_set.add(black_count + 1)
                return True
            if node.color == RED:
                if node.left.color == RED or node.right.color == RED:
                    return False
            curr_black = black_count + (1 if node.color == BLACK else 0)
            return dfs(node.left, curr_black) and dfs(node.right, curr_black)

        is_valid = dfs(self.root, 0) and len(black_height_set) == 1
        return {
            "valid": is_valid,
            "black_height": list(black_height_set)[0] if black_height_set else 0,
            "size": self.size
        }
