from enum import Enum

# 
class Idx(Enum):
    TITLE = 0
    FIELD_WFI = 1
    ON_STAIRS = 2
    ON_ITEM = 3
    GAME_OVER = 9
    ON_ENEMY = 10
    BATTLE_WFI = 11
    ATTACK = 12
    ENEMY_TURN = 13
    ESCAPE = 14
    LOSE = 15
    WIN = 16
    LEVEL_UP = 17
    POTION = 20
    BLAZE_GEM = 21
    BATTLE_END = 22

z = Idx.TITLE
print(z)
print(z == Idx.TITLE)

exit()

from random import random

def move_cars(car_positions):
    # return map(lambda x: x + 1 if random() > 0.3 else x,
    #            car_positions)
    return [x+1 if random()>0.3 else x for x in car_positions]

def output_car(car_position):
    return 'S:'+'-' * car_position

def run_step_of_race(state):
    return {'time': state['time'] - 1,
            'car_positions': move_cars(state['car_positions'])}

def draw(state):
    print('\nTime'+str(state['time']))
    print(state['car_positions'])
    print('\n'.join(map(output_car, state['car_positions'])))

def race(state):
    draw(state)
    if state['time']:
        race(run_step_of_race(state))

race({'time': 5,
      'car_positions': [1, 1, 1]})