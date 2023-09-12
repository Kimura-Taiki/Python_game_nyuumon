from functools import reduce, partial
import pygame
import sys
import random
from pygame.locals import *

# 色々な宣言をまとめてモジュール化
from mod.initializer import *

COMMAND = ["[A]ttack", "[P]otion", "[B]laze gem", "[R]un"]
TRE_NAME = ["Potion", "Blaze gem", "Food spoiled.", "Food +20", "Food +100"]
EMY_NAME = [
    "Green slime", "Red slime", "Axe beast", "Ogre", "Sword man",
    "Death hornet", "Signal slime", "Devil plant", "Twin killer", "Hell"
    ]

MAZE_W = 11
MAZE_H = 9

DUNGEON_W = MAZE_W*3
DUNGEON_H = MAZE_H*3

def pipeline_each(data, fns):
    return reduce(lambda a, x: x(a), fns, data)

def make_maze(maze_w, maze_h): # ダンジョンの元となる迷路の自動生成
    def set_wall(mz, x, y): #壁を作る
        mz[y][x] = 1
        return mz
    def set_random_room(mz, x, y): #20%の確率で部屋を作る
        if mz[y][x] == 0 and random.randint(0, 99) < 20:
            mz[y][x] = 2
        return mz
    XP = [ 0, 1, 0,-1]
    YP = [-1, 0, 1, 0]
    def set_pillar_wall(mz, x, y): #柱の隣に壁を作る
        r = random.randint(0, 3) if x==2 else random.randint(0, 2)# １列目は四方に、２列目以降は左以外に壁を作る
        mz[y+YP[r]][x+XP[r]] = 1
        return mz
    return pipeline_each([[0]*maze_w for i in range(maze_h)], 
                         [partial(set_wall, x=0, y=i) for i in range(maze_h)]+  #左外郭
                         [partial(set_wall, x=maze_w-1, y=i) for i in range(maze_h)]+ #右外郭
                         [partial(set_wall, x=i, y=0) for i in range(maze_w)]+ #上外郭
                         [partial(set_wall, x=i, y=maze_h-1) for i in range(maze_w)]+ #下外郭
                         [partial(set_wall, x=i, y=j) for j in range(2, maze_h-2, 2) for i in range(2, maze_w-2, 2)]+ #柱
                         [partial(set_pillar_wall, x=i, y=j) for j in range(2, maze_h-2, 2) for i in range(2, maze_w-2, 2)]+ #柱から上下左右の壁
                         [partial(set_random_room, x=i, y=j) for j in range(1, maze_h-1) for i in range(1, maze_w-1)]) #部屋

def make_dungeon(maze_w, maze_h): # ダンジョンの自動生成
    maze = make_maze(maze_w, maze_h) # 元となる迷路を作る
    # 迷路からダンジョンを作る
    def dig_tunnel(dgn, x, y, dx, dy):
        if (maze[y][x] == 0 or maze[y][x] == 2) and (maze[y+dy][x+dx] == 0 or maze[y+dy][x+dx] == 2):
            dgn[y*3+1+dy][x*3+1+dx] = 0
        return dgn
    def dig_dot(dgn, x, y):
        dgn[y][x] = 0
        return dgn
    def dig_room(dgn, x, y):
        return pipeline_each(dgn, [partial(dig_dot, x=i, y=j) for j in range(y*3, y*3+3) for i in range(x*3, x*3+3)])
    return pipeline_each([[9]*DUNGEON_W for j in range(DUNGEON_H)], 
                         [partial(dig_tunnel, x=i, y=j, dx=0, dy=0) for j in range(1, maze_h-1) for i in range(1, maze_w-1)]+
                         [partial(dig_tunnel, x=i, y=j, dx=0, dy=-1) for j in range(1, maze_h-1) for i in range(1, maze_w-1)]+
                         [partial(dig_tunnel, x=i, y=j, dx=0, dy=1) for j in range(1, maze_h-1) for i in range(1, maze_w-1)]+
                         [partial(dig_tunnel, x=i, y=j, dx=-1, dy=0) for j in range(1, maze_h-1) for i in range(1, maze_w-1)]+
                         [partial(dig_tunnel, x=i, y=j, dx=1, dy=0) for j in range(1, maze_h-1) for i in range(1, maze_w-1)]+
                         [partial(dig_room, x=i, y=j) for j in range(1, maze_h-1) for i in range(1, maze_w-1) if maze[j][i] == 2])

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

def move_player(key): # 主人公の移動
    global idx, tmr, pl_x, pl_y, pl_d, pl_a, pl_life, food, potion, blazegem, treasure

    if dungeon[pl_y][pl_x] == 1: # 宝箱に載った
        dungeon[pl_y][pl_x] = 0
        treasure = random.choice([0,0,0,1,1,1,1,1,1,2])
        if treasure == 0:
            potion += 1
        if treasure == 1:
            blazegem += 1
        if treasure == 2:
            food = int(food/2)
        idx = Idx.ON_ITEM
        tmr = 0
        return
    if dungeon[pl_y][pl_x] == 2: # 繭に載った
        dungeon[pl_y][pl_x] = 0
        r = random.randint(0, 99)
        if r < 40: # 食料
            treasure = random.choice([3,3,3,4])
            if treasure == 3: food += 20
            if treasure == 4: food += 100
            idx = Idx.ON_ITEM
            tmr = 0
        else: # 敵出現
            idx = Idx.ON_ENEMY
            tmr = 0
            return
    if dungeon[pl_y][pl_x] == 3: # 階段に載った
        idx = Idx.ON_STAIRS
        tmr = 0
        return
    
    # 方向キーで上下左右に移動
    x = pl_x
    y = pl_y
    if key[K_UP] == 1:
        pl_d = 0
        if dungeon[pl_y-1][pl_x] != 9:
            pl_y -= 1
    if key[K_DOWN] == 1:
        pl_d = 1
        if dungeon[pl_y+1][pl_x] != 9:
            pl_y += 1
    if key[K_LEFT] == 1:
        pl_d = 2
        if dungeon[pl_y][pl_x-1] != 9:
            pl_x -= 1
    if key[K_RIGHT] == 1:
        pl_d = 3
        if dungeon[pl_y][pl_x+1] != 9:
            pl_x += 1
    pl_a = pl_d*2
    if pl_x != x or pl_y != y: # 移動したら食料の量と体力を計算
        pl_a += tmr%2 # 移動したら足踏みのアニメーション
        if food > 0:
            food -= 1
            if pl_life < pl_lifemax:
                pl_life += 1
        else:
            pl_life -= 5
            if pl_life <= 0:
                pl_life = 0
                pygame.mixer.music.stop()
                idx = Idx.GAME_OVER
                tmr = 0

def draw_text(bg, txt, x, y, fnt, col): # 影付き文字の表示
    sur = fnt.render(txt, True, BLACK)
    bg.blit(sur, [x+1, y+2])
    sur = fnt.render(txt, True, col)
    bg.blit(sur, [x, y])

def draw_para(bg, fnt): # 主人公の能力を表示
    X = 30
    Y = 600
    bg.blit(imgPara, [X, Y])
    col = WHITE
    if pl_life < 10 and tmr%2 ==0: col = RED
    draw_text(bg, "{}/{}".format(pl_life, pl_lifemax), X+128, Y+6, fnt, col)
    draw_text(bg, str(pl_str), X+128, Y+33, fnt, WHITE)
    col = WHITE
    if food == 0 and tmr%2 == 0: col = RED
    draw_text(bg, str(food), X+128, Y+60, fnt, col)
    draw_text(bg, str(potion), X+266, Y+6, fnt, WHITE)
    draw_text(bg, str(blazegem), X+266, Y+33, fnt, WHITE)

def init_battle(): # 戦闘に入る準備をする
    global imgEnemy, emy_name, emy_lifemax, emy_life, emy_step, emy_x, emy_y
    typ = random.randint(0, floor)
    if floor >= 10:
        typ = random.randint(0, 9)
    lev = random.randint(1, floor)
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

def battle_command(bg, fnt, key): # コマンドの入力と表示
    global btl_cmd
    ent = False
    if key[K_a]: # Aキー
        btl_cmd = 0
        ent = True
    if key[K_p]: # Pキー
        btl_cmd = 1
        ent = True
    if key[K_b]: # Bキー
        btl_cmd = 2
        ent = True
    if key[K_r]: # Rキー
        btl_cmd = 3
        ent = True
    if key[K_UP] and btl_cmd > 0: # ↑キー
        btl_cmd -= 1
    if key[K_DOWN] and btl_cmd < 3: # Aキー
        btl_cmd += 1
    if key[K_SPACE] or key[K_RETURN]:
        ent = True
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

def scene_title(): # タイトル画面
    global screen, font, fontS, key
    global idx, tmr
    global floor, welcome, pl_lifemax, pl_life, pl_str, food, potion, blazegem
    global dungeon
    if tmr == 1:
        pygame.mixer.music.load("Chapter12/sound/ohd_bgm_title.ogg")
        pygame.mixer.music.play(-1)
    screen.fill(BLACK)
    screen.blit(imgTitle, [40, 60])
    if fl_max  >= 2:
        draw_text(screen, "You reached floor {}.".format(fl_max), 300, 460, font, CYAN)
    draw_text(screen, "Press space key", 320, 560, font, BLINK[tmr%6])
    if key[K_SPACE] == 1:
        dungeon = put_event(make_dungeon(MAZE_W, MAZE_H))
        put_protag(dungeon)
        floor = 1
        welcome = 15
        pl_lifemax = 300
        pl_life = pl_lifemax
        pl_str = 100
        food = 300
        potion = 0
        blazegem = 0
        idx = Idx.FIELD_WFI
        tmr = 0
        pygame.mixer.music.load("Chapter12/sound/ohd_bgm_field.ogg")
        pygame.mixer_music.play(-1)

def scene_field_wfi(): # プレイヤーの移動
    global welcome
    move_player(key)
    draw_dungeon(screen, fontS)
    draw_text(screen, "floor {} ({},{})".format(floor, pl_x, pl_y), 60, 40, fontS, WHITE)
    if welcome > 0:
        welcome -= 1
        draw_text(screen, "Welcome to floor {}.".format(floor), 300, 180, font, CYAN)

def scene_on_stairs(): # 画面切り替え
    global idx, floor, fl_max, welcome
    global dungeon
    draw_dungeon(screen, fontS)
    if 1 <= tmr and tmr <= 5:
        h = 80*tmr
        pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
        pygame.draw.rect(screen, BLACK, [0, 720-h, 880, h])
    if tmr == 5:
        floor += 1
        if floor > fl_max:
            fl_max = floor
        welcome = 15
        dungeon = put_event(make_dungeon(MAZE_W, MAZE_H))
        put_protag(dungeon)
    if 6 <= tmr and tmr <= 9:
        h = 80*(10-tmr)
        pygame.draw.rect(screen, BLACK, [0, 0, 880, h])
        pygame.draw.rect(screen, BLACK, [0, 720-h, 880, h])
    if tmr == 10:
        idx = Idx.FIELD_WFI

def scene_on_item(): # アイテム入手もしくはトラップ
    global idx
    draw_dungeon(screen, fontS)
    screen.blit(imgItem[treasure], [320, 220])
    draw_text(screen, TRE_NAME[treasure], 380, 240, font, WHITE)
    if tmr == 10:
        idx = Idx.FIELD_WFI

def scene_game_over(): # ゲームオーバー
    global idx, tmr, pl_a
    if tmr <= 30:
        PL_TURN = [2, 4, 0, 6]
        pl_a = PL_TURN[tmr%4]
        if tmr == 30: pl_a = 8 # 倒れた絵
        draw_dungeon(screen, fontS)
    elif tmr == 31:
        se[3].play()
        draw_text(screen, "You died.", 360, 240, font, RED)
        draw_text(screen, "Game over.", 360, 380, font, RED)
    elif tmr == 100:
        idx = Idx.TITLE
        tmr = 0

def scene_on_enemy(): # 戦闘準備
    global idx, tmr
    if tmr == 1:
        pygame.mixer.music.load("Chapter12/sound/ohd_bgm_battle.ogg")
        pygame.mixer.music.play(-1)
        init_battle()
        init_message()
    elif tmr <= 4:
        bx = (4-tmr)*220
        by = 0
        screen.blit(imgBtlBG, [bx, by])
        draw_text(screen, "Encounter!", 350, 200, font, WHITE)
    elif tmr <= 16:
        draw_battle(screen, fontS)
        draw_text(screen, emy_name+" appear!", 300, 200, font, WHITE)
    else:
        idx = Idx.BATTLE_WFI
        tmr = 0

def scene_battle_wfi(): # プレイヤーのターン(入力待ち)
    global idx, tmr
    draw_battle(screen, fontS)
    if tmr == 1: set_message("Your turn.")
    if battle_command(screen, font, key) == True:
        if btl_cmd == 0:
            idx = Idx.ATTACK
            tmr = 0
        if btl_cmd == 1 and potion > 0:
            idx = Idx.POTION
            tmr = 0
        if btl_cmd == 2 and blazegem > 0:
            idx = Idx.BLAZE_GEM
            tmr = 0
        if btl_cmd == 3:
            idx = Idx.ESCAPE
            tmr = 0

def scene_attack(): # プレイヤーの攻撃
    global idx, tmr, dmg, emy_blink, emy_life
    draw_battle(screen, fontS)
    if tmr == 1:
        set_message("You attack!")
        se[0].play()
        dmg = pl_str + random.randint(0, 9)
    if 2 <= tmr and tmr <= 4:
        screen.blit(imgEffect[0], [700-tmr*120, -100+tmr*120])
    if tmr == 5:
        emy_blink = 5
        set_message(str(dmg)+"pts of damage!")
    if tmr == 11:
        emy_life -= dmg
        if emy_life <= 0:
            emy_life = 0
            idx = Idx.WIN
            tmr = 0
    if tmr == 16:
        idx = Idx.ENEMY_TURN
        tmr = 0

def scene_enemy_turn(): # 敵のターン、敵の攻撃
    global idx, tmr, emy_step, dmg, dmg_eff, pl_life
    draw_battle(screen, fontS)
    if tmr == 1:
        set_message("Enemy turn.")
    if tmr == 5:
        set_message(emy_name + " attack!")
        se[0].play()
        emy_step = 30
    if tmr == 9:
        dmg = emy_str + random.randint(0, 9)
        set_message(str(dmg)+"pts of damage!")
        dmg_eff = 5
        emy_step = 0
    if tmr == 15:
        pl_life -= dmg
        if pl_life < 0:
            pl_life = 0
            idx = Idx.LOSE
            tmr = 0
    if tmr == 20:
        idx = Idx.BATTLE_WFI
        tmr = 0

def scene_escape(): # 逃げられる？
    global idx, tmr
    draw_battle(screen, fontS)
    if tmr == 1: set_message("…")
    if tmr == 2: set_message("……")
    if tmr == 3: set_message("………")
    if tmr == 4: set_message("…………")
    if tmr == 5:
        if random.randint(0, 99) < 60:
            idx = Idx.BATTLE_END
        else:
            set_message("You failed to flee.")
    if tmr == 10:
        idx = Idx.ENEMY_TURN
        tmr = 0

def scene_lose(): # 敗北
    global idx, tmr
    draw_battle(screen, fontS)
    if tmr == 1:
        pygame.mixer.music.stop()
        set_message("You lose.")
    if tmr == 11:
        idx = Idx.GAME_OVER
        tmr = 29

def scene_win(): # 勝利
    global idx, tmr
    draw_battle(screen, fontS)
    if tmr == 1:
        set_message("you win!")
        pygame.mixer.music.stop()
        se[5].play()
    if tmr == 28:
        idx = Idx.BATTLE_END
        if random.randint(0, emy_lifemax) > random.randint(0, pl_lifemax):
            idx = Idx.LEVEL_UP
            tmr = 0

def scene_level_up(): # レベルアップ
    global idx, tmr, pl_lifemax, pl_str
    draw_battle(screen, fontS)
    if tmr == 1:
        set_message("Level up!")
        se[4].play()
    if tmr == 21:
        lif_p = random.randint(10, 20)
        set_message("Max life + "+str(lif_p))
        pl_lifemax += lif_p
    if tmr == 26:
        str_p = random.randint(5, 10)
        set_message("Str + "+str(str_p))
        pl_str += str_p
    if tmr == 50:
        idx = Idx.BATTLE_END

def scene_potion(): # Potion
    global idx, tmr, pl_life, potion
    draw_battle(screen, fontS)
    if tmr == 1:
        set_message("Potion!")
        se[2].play()
    if tmr == 6:
        pl_life = pl_lifemax
        potion -= 1
    if tmr == 11:
        idx = Idx.ENEMY_TURN
        tmr = 0

def scene_blaze_gem(): # Blaze gem
    global idx, tmr, blazegem, dmg
    draw_battle(screen, fontS)
    img_rz = pygame.transform.rotozoom(imgEffect[1], 30*tmr, (12-tmr)/8)
    X = 440-img_rz.get_width()/2
    Y = 360-img_rz.get_height()/2
    screen.blit(img_rz, [X, Y])
    if tmr == 1:
        set_message("Blaze gem!")
        se[1].play()
    if tmr == 6:
        blazegem -= 1
    if tmr == 11:
        dmg = 1000
        idx = Idx.ATTACK
        tmr = 4

def scene_battle_end(): # 戦闘終了
    global idx, tmr
    pygame.mixer.music.load("Chapter12/sound/ohd_bgm_field.ogg")
    pygame.mixer.music.play(-1)
    idx = Idx.FIELD_WFI

scenes = {}
scenes[Idx.TITLE] = scene_title
scenes[Idx.FIELD_WFI] = scene_field_wfi
scenes[Idx.ON_STAIRS] = scene_on_stairs
scenes[Idx.ON_ITEM] = scene_on_item
scenes[Idx.GAME_OVER] = scene_game_over
scenes[Idx.ON_ENEMY] = scene_on_enemy
scenes[Idx.BATTLE_WFI] = scene_battle_wfi
scenes[Idx.ATTACK] = scene_attack
scenes[Idx.ENEMY_TURN] = scene_enemy_turn
scenes[Idx.ESCAPE] = scene_escape
scenes[Idx.LOSE] = scene_lose
scenes[Idx.WIN] = scene_win
scenes[Idx.LEVEL_UP] = scene_level_up
scenes[Idx.POTION] = scene_potion
scenes[Idx.BLAZE_GEM] = scene_blaze_gem
scenes[Idx.BATTLE_END] = scene_battle_end

def main(): # メイン処理
    global key, tmr, speed

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_s:
                    speed += 1
                    if speed == 4:
                        speed = 1
        
        tmr += 1
        key = pygame.key.get_pressed()

        for i, scene in scenes.items():
            if idx == i:
                scene()
                break
                
        draw_text(screen, "[S]peed "+str(speed), 740, 40, fontS, WHITE)

        pygame.display.update()
        clock.tick(4+2*speed)

if __name__ == '__main__':
    main()