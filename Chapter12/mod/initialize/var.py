from . idx import Idx

class SceneVar():
    def __init__(self):
        self.idx = Idx.TITLE
        self.tmr = 0

sv = SceneVar()
tmr = 0
speed = 3

class Floor():
    from os.path import dirname
    import sys
    if __name__ == '__main__': sys.path.append(dirname(dirname(dirname(__file__))))
    now = 0
    max = 0
    welcome = 0

    def go_downstaris():
        Floor.now += 1
        if Floor.now > Floor.max:
            Floor.max = Floor.now
        Floor.welcome = 15

    def draw_reached_floor(screen, font, x, y):
        from mod.initialize.color import CYAN
        from mod.initialize.comdraw import draw_text
        if Floor.max < 1:return
        draw_text(screen, "You reached floor {}.".format(Floor.max), x, y, font, CYAN)

    def draw_welcome_newfloor(screen, font, x, y):
        from mod.initialize.color import CYAN
        from mod.initialize.comdraw import draw_text
        if Floor.welcome > 0:
            Floor.welcome -= 1
            draw_text(screen, "Welcome to floor {}.".format(Floor.now), 300, 180, font, CYAN)
    
    def enemy_type():
        from random import randint
        return randint(0, 9) if Floor.now >= 10 else randint(0, Floor.now)
    
    def enemy_level():
        from random import randint
        return randint(1, Floor.now)

pl_x = 0
pl_y = 0
pl_d = 0
pl_a = 0

class Unit():
    def __init__(self):
        self.lifemax = 0
        self.life = 0
        self.str = 0

pl = Unit()
emy = Unit()

pl_lifemax = 0
pl_life = 0
pl_str = 0
food = 0
potion = 0
blazegem = 0
treasure = 0

emy_name = ""
emy_lifemax = 0
emy_life = 0
emy_str = 0
emy_x = 0
emy_y = 0
emy_step = 0
emy_blink = 0

dmg_eff = 0
btl_cmd = 0

dmg = 0
lif_p = 0
str_p = 0
