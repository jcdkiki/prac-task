class AVLTreeMap:
    class Node:
        def __init__(self, key, value, left=None, right=None, height=0):
            self.key = key
            self.value = value
            self.left = left
            self.right = right
            self.height = height

        def update_height(self):
            self.height = 1 + max(AVLTreeMap.Node.get_height(self.left), AVLTreeMap.Node.get_height(self.right))

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
        def get_balance_factor(root):
            return 0 if root is None else AVLTreeMap.Node.get_height(root.left) - AVLTreeMap.Node.get_height(root.right)

        def rebalance(self):
            self.update_height()
            factor = AVLTreeMap.Node.get_balance_factor(self)

            if factor == -2:
                if AVLTreeMap.Node.get_balance_factor(self.right) > 0:
                    self.right = self.right.right_rotate()
                return self.left_rotate()
            if factor == 2:
                if AVLTreeMap.Node.get_balance_factor(self.left) < 0:
                    self.left = self.left.left_rotate()
                return self.right_rotate()
            return self

        @staticmethod
        def insert(root, key, value):
            if root is None:
                return AVLTreeMap.Node(key, value), True

            res = False
            if key < root.key:
                root.left, res = AVLTreeMap.Node.insert(root.left, key, value)
            elif key > root.key:
                root.right, res = AVLTreeMap.Node.insert(root.right, key, value)
            else:
                root.value = value
                return root, False

            return root.rebalance(), res

        def clear(self):
            if self.left:
                self.left.clear()
            if self.right:
                self.right.clear()

        @staticmethod
        def erase_min(node):
            if node.left is None:
                return node.right, (node.key, node.value)
            node.left, (min_key, min_value) = AVLTreeMap.Node.erase_min(node.left)
            return node.rebalance(), (min_key, min_value)

        @staticmethod
        def erase_max(node):
            if node.right is None:
                return node.left, (node.key, node.value)
            node.right, (max_key, max_value) = AVLTreeMap.Node.erase_max(node.right)
            return node.rebalance(), (max_key, max_value)

        @staticmethod
        def erase(root, key):
            if root is None:
                return None, False

            res = False
            if key < root.key:
                root.left, res = AVLTreeMap.Node.erase(root.left, key)
            elif key > root.key:
                root.right, res = AVLTreeMap.Node.erase(root.right, key)
            else:
                res = True
                if root.right is None:
                    left = root.left
                    root.left = None
                    root.clear()
                    return left, res

                root.right, (min_key, min_value) = AVLTreeMap.Node.erase_min(root.right)
                root.key, root.value = min_key, min_value

            return root.rebalance(), res

        @staticmethod
        def in_order(root, func):
            if root:
                AVLTreeMap.Node.in_order(root.left, func)
                func(root)
                AVLTreeMap.Node.in_order(root.right, func)

        @staticmethod
        def sorted_arr_to_avl(arr, start, end):
            if start > end:
                return None

            mid = start + (end - start) // 2
            root = AVLTreeMap.Node(arr[mid][0], arr[mid][1])
            root.left = AVLTreeMap.Node.sorted_arr_to_avl(arr, start, mid - 1)
            root.right = AVLTreeMap.Node.sorted_arr_to_avl(arr, mid + 1, end)
            return root

        @staticmethod
        def join(t1, t2):
            arr1 = []
            AVLTreeMap.Node.in_order(t1, lambda node: arr1.append((node.key, node.value)))
            arr2 = []
            AVLTreeMap.Node.in_order(t2, lambda node: arr2.append((node.key, node.value)))

            arr = []
            i = 0
            j = 0
            while i < len(arr1) and j < len(arr2):
                if arr1[i][0] < arr2[j][0]:
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
            
            return AVLTreeMap.Node.sorted_arr_to_avl(arr, 0, len(arr) - 1)
        
    def __init__(self):
        self.root = None
        self.len = 0

    def __len__(self):
        return self.len

    def insert(self, key, value):
        self.root, res = self.Node.insert(self.root, key, value)
        self.len += int(res)

    def erase(self, key):
        self.root, res = self.Node.erase(self.root, key)
        self.len -= int(res)

    def get(self, key):
        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node.value
        raise KeyError(f"Key {key} not found")

    def __contains__(self, key):
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def get_min(self):
        if self.root is None:
            raise RuntimeError("Tree is empty")
        node = self.root
        while node.left is not None: node = node.left
        return node.key, node.value

    def get_max(self):
        if self.root is None:
            raise RuntimeError("Tree is empty")
        node = self.root
        while node.right is not None: node = node.right
        return node.key, node.value

    def get_max(self):
        if self.root is None:
            raise RuntimeError("Tree is empty")
        self.root, (key, value) = self.Node.erase_max(self.root)
        self.len -= 1
        return (key, value)

    def split(self, x):
        def _split(node):
            if node is None:
                return (None, None)
            if node.key <= x:
                left, right = _split(node.right)
                node.right = left
                node.update_height()
                return (node.rebalance(), right)
            else:
                left, right = _split(node.left)
                node.left = right
                node.update_height()
                return (left, node.rebalance())

        left_tree = AVLTreeMap()
        right_tree = AVLTreeMap()
        left_tree.root, right_tree.root = _split(self.root)
        left_tree.len = AVLTreeMap._count_nodes(left_tree.root)
        right_tree.len = AVLTreeMap._count_nodes(right_tree.root)
        return left_tree, right_tree

    @staticmethod
    def _count_nodes(root):
        if root is None:
            return 0
        return 1 + AVLTreeMap._count_nodes(root.left) + AVLTreeMap._count_nodes(root.right)

    def join(self, other):
        new_root = self.Node.join(self.root, other.root)
        self.root = new_root
        self.len = self._count_nodes(new_root)
        other.root = None
        other.len = 0

    def __del__(self):
        if self.root:
            self.root.clear()

    def __str__(self):
        def node_to_str(node):
            if node is None:
                return ""
            result = ""
            if node.left is not None:
                result += f"{node.key} -- {node.left.key} [label=L]\n"
                result += node_to_str(node.left)
            if node.right is not None:
                result += f"{node.key} -- {node.right.key} [label=R]\n"
                result += node_to_str(node.right)
            return result

        return f"strict graph {{\n{node_to_str(self.root)}}}"
