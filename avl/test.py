import os
import random
import pytest
from avl_tree import AVLTree

N_ELEMENTS = 30

@pytest.fixture
def avl_tree_and_set():
    avl = AVLTree()
    ref_set = set()
    for i in range(N_ELEMENTS):
        avl.insert(i)
        ref_set.add(i)
    return avl, ref_set

def is_avl(node: AVLTree.Node | None) -> None:
    if node is None:
        return

    balance_factor = abs(get_height(node.left) - get_height(node.right))
    assert balance_factor < 2, f"Node {node.val} is not balanced (balance factor: {balance_factor})"

    if node.left is not None:
        assert node.left.val < node.val, f"Left child {node.left.val} >= parent {node.val}"
        is_avl(node.left)

    if node.right is not None:
        assert node.right.val > node.val, f"Right child {node.right.val} <= parent {node.val}"
        is_avl(node.right)

def get_height(node: AVLTree.Node | None) -> int:
    if node is None:
        return 0
    return node.height

def check_elements(avl: AVLTree, ref_set: set) -> None:
    size = 0
    stack = [avl.root]
    while stack:
        node = stack.pop()
        if node is None:
            continue

        size += 1
        assert node.val in ref_set, f"Value {node.val} not found in the reference set"

        stack.append(node.left)
        stack.append(node.right)

    assert size == len(ref_set), "Tree size does not match the reference set size"

def draw_tree(avl: AVLTree, filename: str) -> None:
    with open(f"{filename}.dot", "w") as f:
        f.write(str(avl))
    os.system(f"dot -Tpng {filename}.dot > {filename}.png")

def test_default(avl_tree_and_set):
    avl, ref_set = avl_tree_and_set
    is_avl(avl.root)
    check_elements(avl, ref_set)
    draw_tree(avl, "draw/before")

def test_insert(avl_tree_and_set):
    avl, ref_set = avl_tree_and_set
    ref_set.add(N_ELEMENTS)
    ref_set.add(N_ELEMENTS + 1)
    avl.insert(N_ELEMENTS)
    avl.insert(N_ELEMENTS + 1)

    is_avl(avl.root)
    check_elements(avl, ref_set)
    draw_tree(avl, "draw/insert")

def test_erase_min(avl_tree_and_set):
    avl, ref_set = avl_tree_and_set
    result = avl.erase_min()
    ref_set.remove(min(ref_set))

    is_avl(avl.root)
    check_elements(avl, ref_set)
    assert result == 0
    draw_tree(avl, "draw/erase-min")

def test_erase_max(avl_tree_and_set):
    avl, ref_set = avl_tree_and_set
    result = avl.erase_max()
    ref_set.remove(max(ref_set))

    is_avl(avl.root)
    check_elements(avl, ref_set)
    assert result == N_ELEMENTS - 1
    draw_tree(avl, "draw/erase-max")

def test_erase_many(avl_tree_and_set):
    avl, ref_set = avl_tree_and_set
    order = list(ref_set)
    random.shuffle(order)

    for i, x in enumerate(order, start=1):
        avl.erase(x)
        ref_set.remove(x)

        is_avl(avl.root)
        check_elements(avl, ref_set)

        filename = f"draw/erase/{i}-{x}"
        draw_tree(avl, filename)
        os.system(f"cp {filename}.png draw/frames/{i}.png")

    os.system("ffmpeg -framerate 10 -i draw/frames/%d.png draw/erase.mp4 2> /dev/null")

def test_erase_minmax_empty():
    tree = AVLTree()
    with pytest.raises(RuntimeError):
        tree.erase_min()
    with pytest.raises(RuntimeError):
        tree.erase_max()

def test_erase_empty():
    tree = AVLTree()
    assert tree.erase(42) is None

def test_join():
    s = set()
    t1 = AVLTree()
    t2 = AVLTree()

    for i in range(N_ELEMENTS):
        s.add(i*2)
        s.add(i*2 + 1)
        t1.insert(i*2)
        t2.insert(i*2 + 1)
    
    
    t1.join(t2)
    arr = []
    AVLTree.Node.in_order(t1.root, lambda node: arr.append(node.val))
    assert arr == list(s)

    draw_tree(t1, "draw/join")

def test_len():
    s = set()
    avl = AVLTree()
    for i in range(1000):
        x = random.randint(0, 30)
        s.add(x)
        avl.insert(x)
    
    assert len(s) == len(avl)

    arr = []
    AVLTree.Node.in_order(avl.root, lambda node: arr.append(node.val))
    assert arr == list(s)

def test_split():
    avl = AVLTree()
    for i in range(N_ELEMENTS):
        avl.insert(i)

    avl1, avl2 = avl.split(N_ELEMENTS // 3)

    draw_tree(avl1, "draw/split1")
    draw_tree(avl2, "draw/split2")

if __name__ == "__main__":
    os.makedirs("draw/erase", exist_ok=True)
    os.makedirs("draw/frames", exist_ok=True)

    pytest.main()

    os.system("rm -rf draw/*.dot draw/erase/*.dot draw/frames")
