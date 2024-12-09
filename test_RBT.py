import pytest
from RedBlackTree import RedBlackTree, Node, Color

@pytest.mark.parametrize("test_input,expected", [
    ([1, 2, 3], [(2, Color.BLACK), (1, Color.RED), (3, Color.RED)]),
    ([15], [(15, Color.BLACK)]),
    ([32, 18, 36, 20], [(32, Color.BLACK), (18, Color.BLACK), (36, Color.BLACK), (20, Color.RED)]),
    ([32, 18, 36, 34], [(32, Color.BLACK), (18, Color.BLACK), (36, Color.BLACK),(34, Color.RED)])
])
def test_rbt_insertion(test_input, expected):
    rbt = RedBlackTree(test_input)
    vals_expected = []
    for element in rbt.arr_rep:
        vals_expected.append((element.value, element.color))
    assert vals_expected == expected

@pytest.mark.parametrize("test_input,expected,v1,v2", [
    ([15, 12, 19, 13, 23], [15, 13, 19, 23], 12, 13),
    ([15, 12, 19, 8, 23], [15, 12, 23, 8], 19, 23),
    ([15, 12, 19, 9, 13, 23], [19, 23], 15, 19)
])
def test_rbt_transplant(test_input, expected, v1, v2):
    rbt = RedBlackTree(test_input)
    rbt.transplant(rbt.search_value(v1), rbt.search_value(v2))
    vals_expected = []
    for element in rbt.arr_rep:
        vals_expected.append(element.value)
    assert vals_expected == expected

@pytest.mark.parametrize("test_input,expected,start_tree", [
    (15, True, [15, 12, 19, 13, 23]),
    (23, True, [15, 12, 19, 13, 23]),
    (1, False, [15, 12, 19, 13, 23]),
])
def test_rbt_search(test_input, expected, start_tree):
    rbt = RedBlackTree(start_tree)
    search_success = (rbt.search_value(test_input).value == test_input)
    assert search_success == expected

@pytest.mark.parametrize("test_input,expected,start_tree", [
    (19, [(12, Color.BLACK), (8, Color.RED), (15, Color.RED), (5, Color.BLACK), (9, Color.BLACK), (13, Color.BLACK), (23, Color.BLACK), (10, Color.RED),], [12, 8, 15, 5, 9, 13, 19, 10, 23]),
    (5, [(12, Color.BLACK), (8, Color.RED), (15, Color.BLACK), (1, Color.BLACK), (9, Color.BLACK), (13, Color.RED), (23, Color.RED), (10, Color.RED),], [12, 8, 15, 5, 9, 13, 23, 1, 10]),
    (12, [(13, Color.BLACK), (8, Color.RED), (15, Color.BLACK), (1, Color.BLACK), (9, Color.BLACK), (23, Color.RED), (10, Color.RED),], [12, 8, 15, 1, 9, 13, 23, 10]),
    (15, [], [15]),
])
def test_rbt_delete(test_input, expected, start_tree):
    rbt = RedBlackTree(start_tree)
    rbt.delete(test_input)
    vals_expected = []
    for element in rbt.arr_rep:
        vals_expected.append((element.value, element.color))
    assert vals_expected == expected