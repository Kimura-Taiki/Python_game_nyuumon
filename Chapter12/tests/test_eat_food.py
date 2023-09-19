import sys
import os
import pytest

# これ結構重要じゃない？
if __name__ == '__main__': sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from mod.scenes.field_wfi import eat_food
# print(sys.path)

def walk(n):
    food = 10
    pl_life = 10
    pl_lifemax = 12
    for i in range(n):
        food, pl_life = eat_food(food=food, pl_life=pl_life, pl_lifemax=pl_lifemax)
    return food, pl_life

# 特定のテストを割愛
# 参考 https://note.com/npaka/n/n84de488ba011
@pytest.mark.skip
def test_false():
    assert False

@pytest.mark.parametrize(('n', 'food', 'pl_life'), [
    ( 0, 10, 10),
    ( 2,  8, 12),
    ( 6,  4, 12),
    (10,  0, 12),
    (12,  0,  2),
    (13,  0,  0),
    (20,  0,  0)
])
def test_eat_food(n, food, pl_life):
    assert walk(n) == (food, pl_life)