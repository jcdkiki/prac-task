class AVLTree:
    class Node:
        def __init__(
                self,
                val: int,
                left = None, 
                right = None,
                height: int = 0
            ):
            self.val = val
            self.left = left
            self.right = right
            self.height = height

        def update_height(self):
            self.height = 1 + max(AVLTree.Node.get_height(self.left), AVLTree.Node.get_height(self.right))

        def right_rotate(self):
            child = self.left
            mid = child.right

            child.right = self
            self.left = mid

            self.update_height()
            child.update_height()
            return child

        def left_rotate(self):
            child = self.right
            mid = child.left

            child.left = self
            self.right = mid

            self.update_height()
            child.update_height()
            return child

        @staticmethod
        def get_height(root): 
            return 0 if root is None else root.height

        @staticmethod
        def get_factor(root): 
            return 0 if root is None else AVLTree.Node.get_height(root.left) - AVLTree.Node.get_height(root.right)

        def rebalance(self):
            self.update_height()
            factor = self.get_factor(self)

            if factor == -2:
                if self.get_factor(self.right) > 0:
                    self.right = self.right.right_rotate()
                return self.left_rotate()
            if factor == 2:
                if self.get_factor(self.left) < 0:
                    self.left = self.left.left_rotate()
                return self.right_rotate()
            return self

        @staticmethod
        def insert(root, val: int): 
            if root is None:
                return AVLTree.Node(val), True

            res = False
            if val < root.val:
                root.left, res = AVLTree.Node.insert(root.left, val)
            elif val > root.val:
                root.right, res = AVLTree.Node.insert(root.right, val)
            else:
                return root, False

            return root.rebalance(), res

        def clear(self):
            if self.left is not None:
                self.left.clear()
            if self.right is not None:
                self.right.clear()

            del self

        @staticmethod
        def get_min_node(root):
            while root.left is not None:
                root = root.left
            
            return root

        def get_max_node(root):
            while root.right is not None:
                root = root.right

            return root

        def erase_min(self):
            if self.left is None:
                right = self.right
                result = self.val
                del self
                return right, result
            
            self.left, result = self.left.erase_min()
            return self.rebalance(), result

        def erase_max(self):
            if self.right is None:
                left = self.left
                result = self.val
                del self
                return left, result
            
            self.right, result = self.right.erase_max()
            return self.rebalance(), result

        @staticmethod
        def erase(root, val): 
            if root is None:
                return None, False

            res = False
            if val < root.val:
                root.left, res = AVLTree.Node.erase(root.left, val)
            elif val > root.val:
                root.right, res = AVLTree.Node.erase(root.right, val)
            else:
                res = True
                if root.right is None:
                    left = root.left
                    del root
                    return left, res

                root.right, new_val = root.right.erase_min()
                root.val = new_val

            return root.rebalance(), res

        @staticmethod
        def in_order(root, function):
            if root is None:
                return
             
            AVLTree.Node.in_order(root.left, function)
            function(root)
            AVLTree.Node.in_order(root.right, function)
        
        @staticmethod
        def pre_order(root, function):
            if root is None:
                return
             
            function(root)
            AVLTree.Node.pre_order(root.left, function)
            AVLTree.Node.pre_order(root.right, function)

        @staticmethod
        def post_order(root, function):
            if root is None:
                return
             
            AVLTree.Node.post_order(root.left, function)
            AVLTree.Node.post_order(root.right, function)
            function(root)

        @staticmethod
        def sorted_arr_to_avl(arr, start, end):
            if start > end:
                return None

            mid = start + (end - start) // 2
            root = AVLTree.Node(arr[mid])
            root.left = AVLTree.Node.sorted_arr_to_avl(arr, start, mid - 1)
            root.right = AVLTree.Node.sorted_arr_to_avl(arr, mid + 1, end)
            return root

        @staticmethod
        def join(t1, t2):
            arr1 = []
            AVLTree.Node.in_order(t1, lambda node: arr1.append(node.val))
            arr2 = []
            AVLTree.Node.in_order(t2, lambda node: arr2.append(node.val))

            arr = []
            i = 0
            j = 0
            while i < len(arr1) and j < len(arr2):
                if arr1[i] < arr2[j]:
                    arr.append(arr1[i])
                    i += 1
                else:
                    arr.append(arr2[j])
                    j += 1
            
            while i < len(arr1):
                arr.append(arr1[i])
                i += 1
            
            while j < len(arr2):
                arr.append(arr2[j])
                j += 1
            
            return AVLTree.Node.sorted_arr_to_avl(arr, 0, len(arr) - 1)

    def __init__(self):
        self.root = None
        self.len = 0

    def __len__(self) -> int:
        return self.len

    def insert(self, val: int):
        self.root, res = AVLTree.Node.insert(self.root, val)
        self.len += int(res)

    def erase(self, val: int):
        self.root, res = AVLTree.Node.erase(self.root, val)
        self.len -= int(res)

    def erase_min(self):
        if self.root is None:
            raise RuntimeError("Tree is empty")
        self.root, result = self.root.erase_min()
        return result

    def erase_max(self):
        if self.root is None:
            raise RuntimeError("Tree is empty")
        self.root, result = self.root.erase_max()
        return result

    def get_min(self):
        while self.left is not None:
            self = self.left
        return self
    
    def get_max(self):
        while self.right is not None:
            self = self.right
        return self

    def join(self, t):
        res = AVLTree.Node.join(self.root, t.root)
        AVLTree.Node.clear(self.root)
        self.root = res

    def split(self, x):
        def _split(node):
            if not node:
                return (None, None)
            
            if node.val <= x:
                left, right = _split(node.right)
                node.right = left
                AVLTree.Node.update_height(node)
                return (AVLTree.Node.rebalance(node), right)
            else:
                left, right = _split(node.left)
                node.left = right
                AVLTree.Node.update_height(node)
                return (left, AVLTree.Node.rebalance(node))

        left_tree = AVLTree()
        right_tree = AVLTree()
        left_tree.root, right_tree.root = _split(self.root)
        return left_tree, right_tree


    def __del__(self):
        if self.root is not None:
            self.root.clear()

    def __copy__(self):
        def copy_node(node):
            if node is None:
                return None
            return AVLTree.Node(node.val, copy_node(node.left), copy_node(node.right), node.height)

        new_tree = AVLTree()
        new_tree.root = copy_node(self.root)
        return new_tree

    def __deepcopy__(self):
        return self.__copy__()

    def __str__(self):
        def node_to_str(node):
            if node is None:
                return ""
            result = ""
            if node.left is not None:
                result += f"{node.val} -- {node.left.val} [label=L]\n"
                result += node_to_str(node.left)
            if node.right is not None:
                result += f"{node.val} -- {node.right.val} [label=R]\n"
                result += node_to_str(node.right)
            return result

        return f"strict graph {{\n{node_to_str(self.root)}}}"
