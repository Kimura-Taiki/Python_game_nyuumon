from functools import reduce
# from .pginit import screen, fontS
from .var import sv

def pipeline_each(data, fns):
    return reduce(lambda a, x: x(a), fns, data)

scene_steps = 0

def scene_change(enum):
    global sv
    sv.idx = enum
    sv.tmr = 0

def step_by_step(steps, resolved, spd=1):
    global sv
    now = sv.tmr*spd
    acc = 0
    for i, step in enumerate(steps):
        # print("now={}, acc={}, i={}, step={}".format(now, acc, i, step))
        acc += step[1]
        if (now < acc) or (i >= resolved):
            past_idx = sv.idx
            step[0]()
            if sv.idx != past_idx:
                return 0
            return ((resolved+1)%len(steps)) if i >= resolved else resolved

def pass_method():
    return

# def scene_by_schedule(schedule): # step_by_stepによる処理を一本化
#     global scene_steps
#     scene_steps = step_by_step(schedule, scene_steps, speed)

# def scene_in_battle(schedule): # バトル中のstep_by_step系シーンを一本化
#     draw_battle(screen, fontS)
#     scene_by_schedule(schedule)
