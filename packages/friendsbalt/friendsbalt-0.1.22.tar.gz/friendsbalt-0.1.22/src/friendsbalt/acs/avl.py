from bst import BSTNode, BST

class AVLNode(BSTNode):
    def __init__(self, key, value):
        super().__init__(key, value)
        self.height = 1


def __str__(self, level=0, prefix="Root: "):
        ret = " " * (level * 4) + prefix + str(self.key) + " (Height: " + str(self.height) + ")\n"
        if self.left is not None:
            ret += self.left.__str__(level + 1, "L--- ")
        else:
            ret += " " * ((level + 1) * 4) + "L--- None\n"
        if self.right is not None:
            ret += self.right.__str__(level + 1, "R--- ")
        else:
            ret += " " * ((level + 1) * 4) + "R--- None\n"
        return ret

class AVLTree(BST):
    """
    AVLTree is a subclass of BST (Binary Search Tree) that implements a self-balancing binary search tree.
    It ensures that the tree remains balanced after every insertion and deletion operation.
    """
    def _height(self, node):
        return 0 if node is None else node.height
    
    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)
    
    def _update(self, node):
        node.height = max(self._height(node.left), self._height(node.right)) + 1
        self._update(node)

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update(y)
        self._update(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update(x)
        self._update(y)
        return y

    def _balance(self, node):
        if self._balance_factor(node) > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if self._balance_factor(node) < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node
    
    def _create_node(self, key, value):
        return AVLNode(key, value)
    
    def _put(self, key, value, node):
        node = super()._put(key, value, node)
        return self._balance(node)
    
    def _delete(self, key, node):
        node = super()._delete(key, node)
        if node is None:
            return node
        self._update(node)
        return self._balance(node)