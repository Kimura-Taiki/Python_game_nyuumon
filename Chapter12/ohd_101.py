from functools import reduce, partial
import pygame
import sys
import random
from pygame.locals import *

# 色々な宣言をまとめてモジュール化
from mod.initializer import *
# from mod.scenes import field_wfi
from mod.scenes.field_wfi import eat_food, make_maze, make_dungeon

COMMAND = ["[A]ttack", "[P]otion", "[B]laze gem", "[R]un"]
TRE_NAME = ["Potion", "Blaze gem", "Food spoiled.", "Food +20", "Food +100"]
EMY_NAME = [
    "Green slime", "Red slime", "Axe beast", "Ogre", "Sword man",
    "Death hornet", "Signal slime", "Devil plant", "Twin killer", "Hell"
    ]

# -------------------------------- 共用メソッド --------------------------------

def scene_by_schedule(schedule): # step_by_stepによる処理を一本化
    global scene_steps
    scene_steps = step_by_step(schedule, scene_steps, speed)

def scene_in_battle(schedule): # バトル中のstep_by_step系シーンを一本化
    draw_battle(screen, fontS)
    scene_by_schedule(schedule)

# -------------------------------- 部分メソッド --------------------------------

def draw_dungeon(bg, fnt): # ダンジョンを描画する
    bg.fill(BLACK)
    for y in range(-4, 6):
        for x in range(-5, 6):
            X = (x+5)*80
            Y = (y+4)*80
            dx = pl_x + x
            dy = pl_y + y
            if 0 <= dx and dx < DUNGEON_W and 0 <= dy and dy < DUNGEON_H:
                if dungeon[dy][dx] <= 3:
                    bg.blit(imgFloor[dungeon[dy][dx]], [X, Y])
                if dungeon[dy][dx] == 9:
                    bg.blit(imgWall, [X, Y-40])
                    if dy >= 1 and dungeon[dy-1][dx] == 9:
                        bg.blit(imgWall2, [X, Y-80])
            if x == 0 and y == 0: # 主人公キャラの表示
                bg.blit(imgPlayer[pl_a], [X, Y-40])
    bg.blit(imgDark, [0, 0]) # 四隅が暗闇の画像を重ねる
    draw_para(bg, fnt) # 主人公の能力を表示

def space(dgn): # (x, y)のタプル型としてダンジョン上の空白地を返す
    while True:
        x = random.randint(3, DUNGEON_W-4)
        y = random.randint(3, DUNGEON_H-4)
        if dgn[y][x] == 0:
            return x, y

def put_event(dungeon): # 床にイベントを配置する
    def set_dot(dgn, x, y, n):
        dgn[y][x] = n
        return dgn
    def dig_3x3(dgn, x, y, n):
        return pipeline_each(dgn, 
                             [partial(set_dot, x=i, y=j, n=0) for j in range(y-1, y+2) for i in range(x-1, x+2)]+
                             [partial(set_dot, x=x, y=y, n=n)])
    return pipeline_each(dungeon,
                            [partial(dig_3x3, x=x, y=y, n=3) for x, y in [space(dungeon)]]+ # 階段の配置
                            [partial(set_dot, x=x, y=y, n=random.choice([1,2,2,2,2])) for x, y in [list(space(dungeon)) for i in range(15)]]) # 宝箱と繭の配置

def put_protag(dgn): # 主人公をダンジョン上の空白地にランダムに投下
    global pl_x, pl_y, pl_d, pl_a
    pl_x, pl_y = space(dgn)
    pl_d = 1
    pl_a = 2
    # 以下はアイテム処理を見る為の追記
    global dungeon
    dungeon[pl_y-3][pl_x] = 2
    dungeon[pl_y-2][pl_x] = 2
    dungeon[pl_y-1][pl_x] = 2
    dungeon[pl_y][pl_x-1] = 1
    dungeon[pl_y][pl_x+1] = 1
    dungeon[pl_y+1][pl_x] = 3

def move_player(key): # 主人公の移動
    global sv, pl_x, pl_y, pl_d, pl_a, food, potion, blazegem, treasure
    def on_event(bool, chip, i, func):
        global dungeon, pl_x, pl_y, sv
        if dungeon[pl_y][pl_x] != chip: return bool
        dungeon[pl_y][pl_x] = 0
        func()
        scene_change(i)
        return True
    def on_treasure():
        global treasure, potion, blazegem, food
        treasure = random.choice([0,0,0,1,1,1,1,1,1,2])
        if treasure == 0:
            potion += 1
        if treasure == 1:
            blazegem += 1
        if treasure == 2:
            food = int(food/2)
    def on_food():
        global treasure, food
        treasure = random.choice([3,3,3,4])
        if treasure == 3: food += 20
        if treasure == 4: food += 100
    def shift_scene_only():
        pass
    pipeline_each(False, [partial(on_event, chip=1,                                         i=Idx.ON_ITEM,  func=on_treasure),
                          partial(on_event, chip=(2 if random.randint(0, 99) < 40 else -1), i=Idx.ON_ITEM,  func=on_food),
                          partial(on_event, chip=2,                                         i=Idx.ON_ENEMY, func=shift_scene_only),
                          partial(on_event, chip=3,                                         i=Idx.ON_STAIRS,func=shift_scene_only)])

    # 方向キーで上下左右に移動
    def move(bool, k_code, dir, dx, dy):
        global pl_x, pl_y, pl_d
        if key[k_code] != 1: return bool or False
        pl_d = dir
        if dungeon[pl_y+dy][pl_x+dx] == 9: return bool or False
        pl_x += dx
        pl_y += dy
        return True
    is_move = pipeline_each(False,
                            [partial(move, k_code=K_UP,   dir=0, dx= 0, dy=-1),
                             partial(move, k_code=K_DOWN, dir=1, dx= 0, dy= 1),
                             partial(move, k_code=K_LEFT, dir=2, dx=-1, dy= 0),
                             partial(move, k_code=K_RIGHT,dir=3, dx= 1, dy= 0)])
    pl_a = pl_d*2
    if is_move == True: # 移動したら食料の量と体力を計算
        pl_a += tmr%2 # 移動したら足踏みのアニメーション
        food, pl.life = eat_food(food, pl.life, pl.lifemax)
        if pl.life <= 0:
            pygame.mixer.music.stop()
            scene_change(Idx.FALLEN)

def draw_para(bg, fnt): # 主人公の能力を表示
    X = 30
    Y = 600
    bg.blit(imgPara, [X, Y])
    col = WHITE
    if pl.life < 10 and tmr%2 ==0: col = RED
    draw_text(bg, "{}/{}".format(pl.life, pl.lifemax), X+128, Y+6, fnt, col)
    draw_text(bg, str(pl.str), X+128, Y+33, fnt, WHITE)
    col = WHITE
    if food == 0 and tmr%2 == 0: col = RED
    draw_text(bg, str(food), X+128, Y+60, fnt, col)
    draw_text(bg, str(potion), X+266, Y+6, fnt, WHITE)
    draw_text(bg, str(blazegem), X+266, Y+33, fnt, WHITE)

def init_battle(): # 戦闘に入る準備をする
    global imgEnemy, emy_name, emy_lifemax, emy_life, emy_step, emy_x, emy_y
    typ = Floor.enemy_type()
    lev = Floor.enemy_level()
    imgEnemy = pygame.image.load("Chapter12/image/enemy"+str(typ)+".png")
    emy_name = EMY_NAME[typ] + " LV" + str(lev)
    emy_lifemax = 60*(typ+1) + (lev-1)*10
    emy_life = emy_lifemax
    myst     = int(emy_lifemax/8)
    emy_x = 440-imgEnemy.get_width()/2
    emy_y = 560-imgEnemy.get_height()

def draw_bar(bg, x, y, w, h, val, max): # 敵の体力を表示するバー
    pygame.draw.rect(bg, WHITE, [x-2, y-2, w+4, h+4])
    pygame.draw.rect(bg, BLACK, [x, y, w, h])
    if val > 0:
        pygame.draw.rect(bg, (0,128,255), [x, y, w*val/max, h])

def draw_battle(bg, fnt): # 戦闘画面の描画
    global emy_blink, dmg_eff
    bx = 0
    by = 0
    if dmg_eff > 0:
        dmg_eff -= 1
        bx = random.randint(-20, 20)
        by = random.randint(-10, 10)
    bg.blit(imgBtlBG, [bx, by])
    if emy_life > 0 and emy_blink%2 == 0:
        bg.blit(imgEnemy, [emy_x, emy_y+emy_step])
    draw_bar(bg, 340, 580, 100, 10, emy_life, emy_lifemax)
    if emy_blink > 0:
        emy_blink -= 1
    for i in range(10): # 戦闘メッセージの表示
        draw_text(bg, message[i], 600, 100+i*50, fnt, WHITE)
    draw_para(bg, fnt) # 主人公の能力を表示

once_juuji = True
def battle_command(bg, fnt, key): # コマンドの入力と表示
    global btl_cmd, once_juuji
    def assign_cmd(b_e, k_code, cmd):
        return (cmd, True) if key[k_code] else b_e
    def shift_cmd(b_e, k_code, shift, mod, oj):
        return ((b_e[0]+shift+mod)%mod, False) if key[k_code] and oj else b_e
    def decide_cmd(b_e, k_code):
        return (b_e[0], True) if key[k_code] else b_e
    btl_cmd, ent = pipeline_each((btl_cmd, False), [
        partial(assign_cmd, k_code=K_a, cmd=0), # Aキー
        partial(assign_cmd, k_code=K_p, cmd=1), # Pキー
        partial(assign_cmd, k_code=K_b, cmd=2), # Bキー
        partial(assign_cmd, k_code=K_r, cmd=3), # Rキー
        partial(shift_cmd, k_code=K_UP, shift=-1, mod=4, oj=once_juuji), # ↑キー
        partial(shift_cmd, k_code=K_DOWN, shift=1, mod=4, oj=once_juuji), # ↓キー
        partial(decide_cmd, k_code=K_SPACE), # 空白キー
        partial(decide_cmd, k_code=K_RETURN) # 改行キー
        ])
    once_juuji = not (key[K_UP] or key[K_DOWN])
    for i in range(4):
        c = WHITE
        if btl_cmd == i: c = BLINK[tmr%6]
        draw_text(bg, COMMAND[i], 20, 360+i*60, fnt, c)
    return ent

# 戦闘メッセージの表示処理
message = [""]*10
def init_message():
    for i in range(10):
        message[i] = ""

def set_message(msg):
    for i in range(10):
        if message[i] == "":
            message[i] = msg
            return
    for i in range(9):
        message[i] = message[i+1]
    message[9] = msg

def make_new_dungeon():
    global dungeon
    pygame.draw.rect(screen, BLACK, [0, 0, 880, 720])
    Floor.go_downstaris()
    dungeon = put_event(make_dungeon(MAZE_W, MAZE_H))
    put_protag(dungeon)

def scene_title(): # タイトル画面
    global screen, font, fontS, key
    global sv
    global food, potion, blazegem
    global dungeon
    if sv.tmr == 1:
        pygame.mixer.music.load("Chapter12/sound/ohd_bgm_title.ogg")
        pygame.mixer.music.play(-1)
    screen.fill(BLACK)
    screen.blit(imgTitle, [40, 60])
    Floor.draw_reached_floor(screen=screen, font=font, x=300, y=460)
    draw_text(screen, "Press space key", 320, 560, font, BLINK[tmr%6])
    if key[K_SPACE] == 1:
        Floor.now = 0
        make_new_dungeon()
        pl.lifemax = 300
        pl.life = pl.lifemax
        pl.str = 100
        food = 300
        potion = 0
        blazegem = 0
        scene_change(Idx.FIELD_WFI)
        pygame.mixer.music.load("Chapter12/sound/ohd_bgm_field.ogg")
        pygame.mixer_music.play(-1)

def scene_field_wfi(): # プレイヤーの移動
    move_player(key)
    draw_dungeon(screen, fontS)
    draw_text(screen, "floor {} ({},{})".format(Floor.now, pl_x, pl_y), 60, 40, fontS, WHITE)
    Floor.draw_welcome_newfloor(screen=screen, font=font, x=300, y=180)

# Idx.ON_STAIRS系統(画面切り替え)の工程メソッド
def close_curtain():
    global tmr, screen
    draw_dungeon(screen, fontS)
    h = 80*tmr
    pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
    pygame.draw.rect(screen, BLACK, [0, 720-h, 880, h])
def open_curtain():
    global tmr, screen
    draw_dungeon(screen, fontS)
    h = 80*(10-tmr)
    pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
    pygame.draw.rect(screen, BLACK, [0, 720-h, 880, h])
on_stairs_schedule = [[close_curtain, 5],
                      [make_new_dungeon, 0],
                      [open_curtain, 5],
                      [partial(scene_change, enum=Idx.FIELD_WFI), 0]]

# Idx.ON_ITEM系統(アイテム入手もしくはトラップ)の工程メソッド
def draw_get_item():
    draw_dungeon(screen, fontS)
    screen.blit(imgItem[treasure], [320, 220])
    draw_text(screen, TRE_NAME[treasure], 380, 240, font, WHITE)
on_item_schedule = [[draw_get_item, 10],
                    [partial(scene_change, enum=Idx.FIELD_WFI), 0]]

# Idx.ON_ENEMY系統(戦闘準備)の工程メソッド
def battle_start():
    pygame.mixer.music.load("Chapter12/sound/ohd_bgm_battle.ogg")
    pygame.mixer.music.play(-1)
    init_battle()
    init_message()
def encounter():
    bx = (4-tmr)*220
    by = 0
    screen.blit(imgBtlBG, [bx, by])
    draw_text(screen, "Encounter!", 350, 200, font, WHITE)
def enemy_appear():
    draw_battle(screen, fontS)
    draw_text(screen, emy_name+" appear!", 300, 200, font, WHITE)
on_enemy_schedule = [[battle_start, 0],
                     [encounter, 4],
                     [enemy_appear, 12],
                     [partial(scene_change, enum=Idx.BATTLE_WFI), 0]]

def scene_battle_wfi(): # プレイヤーのターン(入力待ち)
    global sv
    draw_battle(screen, fontS)
    if sv.tmr == 1: set_message("Your turn.")
    if battle_command(screen, font, key) == True:
        cmd_list = [[0, partial(scene_change, enum=Idx.ATTACK)],
                    [1, partial(scene_change, enum=Idx.POTION)],
                    [2, partial(scene_change, enum=Idx.BLAZE_GEM)],
                    [3, partial(scene_change, enum=Idx.ESCAPE)]]
        for cmd in cmd_list:
            if btl_cmd == cmd[0]:
                cmd[1]()

# Idx.ENEMY_TURN系統(敵のターン、敵の攻撃)の工程メソッド
def enter_enemy():
    global emy_step
    set_message(emy_name + " attack!")
    se[0].play()
    emy_step = 30
def shake_protag():
    global dmg, dmg_eff, emy_step
    dmg = emy_str + random.randint(0, 9)
    set_message(str(dmg)+"pts of damage!")
    dmg_eff = 5
    emy_step = 0
def settle_damage():
    pl.life -= dmg
    if pl.life < 0:
        pl.life = 0
        scene_change(Idx.LOSE)
enemy_turn_schedule = [[partial(set_message,msg="Enemy turn."), 0],
                       [pass_method, 5],
                       [enter_enemy, 0],
                       [pass_method, 4],
                       [shake_protag, 0],
                       [pass_method, 6],
                       [settle_damage, 0],
                       [pass_method, 5],
                       [partial(scene_change, enum=Idx.BATTLE_WFI), 0]]

# Idx.ESCAPE系統(逃げられる？)の工程メソッド
def escape_judgement():
    if random.randint(0, 99) < 60:
        scene_change(Idx.BATTLE_END)
    else:
        set_message("You failed to flee.")
escape_schedule = [[partial(set_message, msg="…"), 1],
                   [partial(set_message, msg="……"), 1],
                   [partial(set_message, msg="………"), 1],
                   [partial(set_message, msg="…………"), 1],
                   [escape_judgement, 0],
                   [pass_method, 6],
                   [partial(scene_change, enum=Idx.ENEMY_TURN), 0]]

# Idx.LOSE系統(敗北)の工程メソッド
def you_lose():
    pygame.mixer.music.stop()
    set_message("You lose.")
lose_schedule = [[you_lose, 0],
                 [pass_method, 12],
                 [partial(scene_change, enum=Idx.GAME_OVER), 0]]

# Idx.WIN系統(勝利)の工程メソッド
def you_win():
    set_message("you win!")
    pygame.mixer.music.stop()
    se[5].play()
def win_end():
    if random.randint(0, emy_lifemax) > random.randint(0, pl.lifemax):
        scene_change(Idx.LEVEL_UP)
    else:
        scene_change(Idx.BATTLE_END)
win_schedule = [[you_win, 0],
                [pass_method, 28],
                [win_end, 0]]

# Idx.LEVEL_UP系統(レベルアップ)の工程メソッド
def level_up():
    set_message("Level up!")
    se[4].play()
def max_life_plus():
    lif_p = random.randint(10, 20)
    set_message("Max life + "+str(lif_p))
    pl.lifemax += lif_p
def str_plus():
    str_p = random.randint(5, 10)
    set_message("Str + "+str(str_p))
    pl.str += str_p
level_up_schedule = [[level_up, 0],
                     [pass_method, 20],
                     [max_life_plus, 0],
                     [pass_method, 5],
                     [str_plus, 0],
                     [pass_method, 25],
                     [partial(scene_change, enum=Idx.BATTLE_END), 0]]

# Idx.POTION系統(Potion)の工程メソッド
def has_potion():
    global potion
    if potion == 999: #改変中-----------------------------------------------------------------------------------------------------
        set_message("No Potion.")
        scene_change(enum=Idx.BATTLE_WFI)
        return
    set_message("Potion!")
    se[2].play()
def full_recovery():
    global potion
    pl.life = pl.lifemax
    potion -= 1
potion_schedule = [[has_potion, 0],
                   [pass_method, 6],
                   [full_recovery, 0],
                   [pass_method, 5],
                   [partial(scene_change, enum=Idx.ENEMY_TURN), 0]]

# Idx.BLAZE_GEM系統(Blaze gem)の工程メソッド
def has_blaze_gem():
    global blazegem, dmg
    if blazegem == 999: #改変中-----------------------------------------------------------------------------------------------------
        set_message("No Blaze Gem.")
        scene_change(enum=Idx.BATTLE_WFI)
        return
    set_message("Blaze gem!")
    se[1].play()
    draw_blaze()
    blazegem -= 1
    dmg = 1000
def draw_blaze():
    img_rz = pygame.transform.rotozoom(imgEffect[1], 30*tmr, (12-tmr)/8)
    X = 440-img_rz.get_width()/2
    Y = 360-img_rz.get_height()/2
    screen.blit(img_rz, [X, Y])
blaze_gem_schedule = [[has_blaze_gem, 0],
                      [draw_blaze, 11],
                      [partial(scene_change, enum=Idx.DAMAGED_ENEMY), 0]]

def scene_battle_end(): # 戦闘終了
    global sv
    pygame.mixer.music.load("Chapter12/sound/ohd_bgm_field.ogg")
    pygame.mixer.music.play(-1)
    scene_change(Idx.FIELD_WFI)

# Idx.FALLEN系統(フィールド上でよろめいて倒れる)の工程メソッド
def staggered():
    global pl_a
    PL_TURN = [2, 4, 0, 6]
    pl_a = PL_TURN[tmr%4]
    draw_dungeon(screen, fontS)
def fallen():
    global pl_a
    pl_a = 8
    draw_dungeon(screen, fontS)
fallen_schedule = [[staggered, 28],
                   [fallen, 0],
                   [partial(scene_change, enum=Idx.GAME_OVER), 0]]

# Idx.GAME_OVER系統(ゲームオーバー)の工程メソッド
def you_died():
    se[3].play()
    draw_text(screen, "You died.", 360, 240, font, RED)
    draw_text(screen, "Game over.", 360, 380, font, RED)
game_over_schedule = [[you_died, 0],
                      [pass_method, 70],
                      [partial(scene_change, enum=Idx.TITLE), 0]]

# Idx.ATTACK系統(プレイヤーの攻撃)の工程メソッド
def protag_slash():
    global dmg
    set_message("You attack!")
    se[0].play()
    dmg = pl.str + random.randint(0, 9)
def shake_bg():
    screen.blit(imgEffect[0], [700-tmr*120, -100+tmr*120])
attack_schedule = [[protag_slash, 0],
                   [shake_bg, 5],
                   [partial(scene_change, enum=Idx.DAMAGED_ENEMY), 0]]

# Idx.DAMAGED_ENEMY系統(敵の被弾)の工程メソッド
def shake_enemy():
    global emy_blink
    emy_blink = 5
    set_message(str(dmg)+"pts of damage!")
def settle_damage():
    global emy_life
    emy_life -= dmg
    if emy_life <= 0:
        emy_life = 0
        scene_change(Idx.WIN)
damaged_enemy_schedule = [[shake_enemy, 0],
                          [pass_method, 5],
                          [settle_damage, 0],
                          [pass_method, 5],
                          [partial(scene_change, enum=Idx.ENEMY_TURN), 0]]

scenes = {}
scenes[Idx.TITLE] = scene_title
scenes[Idx.FIELD_WFI] = scene_field_wfi
scenes[Idx.ON_STAIRS] = partial(scene_by_schedule, schedule=on_stairs_schedule)
scenes[Idx.ON_ITEM] = partial(scene_by_schedule, schedule=on_item_schedule)
scenes[Idx.GAME_OVER] = partial(scene_by_schedule, schedule=game_over_schedule)
scenes[Idx.ON_ENEMY] = partial(scene_by_schedule, schedule=on_enemy_schedule)
scenes[Idx.BATTLE_WFI] = scene_battle_wfi
scenes[Idx.ATTACK] = partial(scene_in_battle, schedule=attack_schedule)
scenes[Idx.ENEMY_TURN] = partial(scene_in_battle, schedule=enemy_turn_schedule)
scenes[Idx.ESCAPE] = partial(scene_in_battle, schedule=escape_schedule)
scenes[Idx.LOSE] = partial(scene_in_battle, schedule=lose_schedule)
scenes[Idx.WIN] = partial(scene_in_battle, schedule=win_schedule)
scenes[Idx.LEVEL_UP] = partial(scene_in_battle, schedule=level_up_schedule)
scenes[Idx.POTION] = partial(scene_in_battle, schedule=potion_schedule)
scenes[Idx.BLAZE_GEM] = partial(scene_in_battle, schedule=blaze_gem_schedule)
scenes[Idx.BATTLE_END] = scene_battle_end
scenes[Idx.FALLEN] = partial(scene_by_schedule, schedule=fallen_schedule)
scenes[Idx.DAMAGED_ENEMY] = partial(scene_in_battle, schedule=damaged_enemy_schedule)

def main(): # メイン処理
    global key, sv, speed

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_s:
                    speed = speed%3+1
        
        sv.tmr += 1
        key = pygame.key.get_pressed()

        for i, scene in scenes.items():
            if sv.idx == i:
                scene()
                break
                
        draw_text(screen, "[S]peed "+str(speed), 740, 40, fontS, WHITE)

        pygame.display.update()
        # clock.tick(4+2*speed)
        clock.tick(10)

if __name__ == '__main__':
    main()