import os
import random
import pytest
from avl_map import AVLTreeMap

N_ELEMENTS = 30

@pytest.fixture
def avl_map_and_dict():
    os.makedirs("draw/erase", exist_ok=True)
    
    avl = AVLTreeMap()
    ref_dict = {}
    for i in range(N_ELEMENTS):
        avl.insert(i, hex(i))
        ref_dict[i] = hex(i)
    return avl, ref_dict

def is_avl(node: AVLTreeMap.Node | None) -> None:
    if node is None:
        return

    balance_factor = abs(get_height(node.left) - get_height(node.right))
    assert balance_factor < 2, f"Node {node.key} is not balanced (balance factor: {balance_factor})"

    if node.left is not None:
        assert node.left.key < node.key, f"Left child {node.left.key} >= parent {node.key}"
        is_avl(node.left)

    if node.right is not None:
        assert node.right.key > node.key, f"Right child {node.right.key} <= parent {node.key}"
        is_avl(node.right)

def get_height(node: AVLTreeMap.Node | None) -> int:
    if node is None:
        return 0
    return node.height

def check_elements(avl: AVLTreeMap, ref_dict: dict) -> None:
    size = 0
    stack = [avl.root]
    while stack:
        node = stack.pop()
        if node is None:
            continue

        size += 1
        assert node.key in ref_dict
        assert node.value == ref_dict[node.key]

        stack.append(node.left)
        stack.append(node.right)

    assert size == len(ref_dict)

def draw_tree(avl: AVLTreeMap, filename: str) -> None:
    with open(f"{filename}.dot", "w") as f:
        f.write(str(avl))
    os.system(f"dot -Tpng {filename}.dot > {filename}.png")

def test_default(avl_map_and_dict):
    avl, ref_dict = avl_map_and_dict
    is_avl(avl.root)
    check_elements(avl, ref_dict)
    draw_tree(avl, "draw/before")

def test_insert(avl_map_and_dict):
    avl, ref_dict = avl_map_and_dict
    new_keys = [N_ELEMENTS, N_ELEMENTS + 1]
    for key in new_keys:
        avl.insert(key, hex(key))
        ref_dict[key] = hex(key)
    
    is_avl(avl.root)
    check_elements(avl, ref_dict)
    draw_tree(avl, "draw/insert")

def test_get_minmax(avl_map_and_dict):
    avl, ref_dict = avl_map_and_dict

    dict_min_key = min(ref_dict)
    dict_max_key = max(ref_dict)
    dict_min_value = ref_dict[dict_min_key]
    dict_max_value = ref_dict[dict_max_key]
    avl_min_key, avl_min_value = avl.get_min()
    avl_max_key, avl_max_value = avl.get_max()

    assert avl_min_key == dict_min_key
    assert avl_max_key == dict_max_key
    assert avl_min_value == dict_min_value
    assert avl_max_value == dict_max_value    

def test_erase_many(avl_map_and_dict):
    avl, ref_dict = avl_map_and_dict
    order = list(ref_dict.keys())
    random.shuffle(order)

    for i, key in enumerate(order, start=1):
        avl.erase(key)
        ref_dict.pop(key)
        
        is_avl(avl.root)
        check_elements(avl, ref_dict)

        draw_tree(avl, f"draw/erase/{i}-{key}")

def test_get_minmax_empty():
    tree = AVLTreeMap()
    with pytest.raises(RuntimeError):
        tree.get_min()
    with pytest.raises(RuntimeError):
        tree.get_max()

def test_erase_empty():
    tree = AVLTreeMap()
    assert tree.erase(42) is None, "Erasing from empty tree should return None"

def test_join():
    s = dict()
    t1 = AVLTreeMap()
    t2 = AVLTreeMap()

    for i in range(N_ELEMENTS):
        key_even = i * 2
        key_odd = i * 2 + 1
        s[key_even] = f"value_{key_even}"
        s[key_odd] = f"value_{key_odd}"
        t1.insert(key_even, f"value_{key_even}")
        t2.insert(key_odd, f"value_{key_odd}")
    
    t1.join(t2)
    arr = []
    is_avl(t1.root)
    check_elements(t1, s)
    draw_tree(t1, "draw/join")
    
def test_len():
    s = dict()
    avl = AVLTreeMap()
    for _ in range(1000):
        key = random.randint(0, 30)
        s[key] = f"value_{key}"
        avl.insert(key, f"value_{key}")
    
    assert len(s) == len(avl)
    check_elements(avl, s)
    
def test_split():
    avl = AVLTreeMap()
    for i in range(N_ELEMENTS):
        avl.insert(i, f"value_{i}")

    split_key = N_ELEMENTS // 3
    avl1, avl2 = avl.split(split_key)

    draw_tree(avl1, "draw/split1")
    draw_tree(avl2, "draw/split2")

if __name__ == "__main__":
    pytest.main()
