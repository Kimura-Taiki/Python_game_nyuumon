import pygame
import sys
import random
from pygame.locals import * # pygame.QUITやpygame.KEYDOWNなどの定数を略記可能にする

WHITE = (255,255,255)
BLACK = (  0,  0,  0)

imgBtlBG = pygame.image.load("Chapter11/btlbg.png")
imgEffect = pygame.image.load("Chapter11/effect_a.png")
imgEnemy = pygame.image.load("Chapter11/enemy4.png")
emy_x = 440-imgEnemy.get_width()/2
emy_y = 560-imgEnemy.get_height()
emy_step = 0
emy_blink = 0
dmg_eff = 0
COMMAND = ["[A]ttack", "[P]otion", "[B]laze gem", "[R]un"]

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

def draw_text(bg, txt, x, y, fnt, col):
    sur = fnt.render(txt, True, BLACK)
    bg.blit(sur, [x+1, y+2])
    sur = fnt.render(txt, True, col)
    bg.blit(sur, [x, y])

def draw_battle(bg, fnt):
    global emy_blink, dmg_eff
    bx = 0
    by = 0
    if dmg_eff > 0:
        dmg_eff -= 1
        bx = random.randint(-20, 20)
        by = random.randint(-10, 10)
    bg.blit(imgBtlBG, [bx, by])
    if emy_blink%2 == 0:
        bg.blit(imgEnemy, [emy_x, emy_y])
    if emy_blink > 0:
        emy_blink -= 1
    for i in range(10):
        draw_text(bg, message[i], 600, 100+i*50, fnt, WHITE)

def battle_command(bg, fnt):
    for i in range(4):
        draw_text(bg, COMMAND[i], 20, 360+60*i, fnt, WHITE)

def main():
    global emy_step, emy_blink, dmg_eff
    idx = 10
    tmr = 0

    pygame.init()
    pygame.display.set_caption("ターン制の処理")
    screen = pygame.display.set_mode((880, 720))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)

    init_message()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        draw_battle(screen, font)
        tmr += 1
        key = pygame.key.get_pressed()

        if idx == 10: # 戦闘開始
            if tmr == 1: set_message("Encounter!")
            if tmr == 6:
                idx = 11
                tmr = 0

        elif idx == 11: # プレイヤー入力待ち
            if tmr == 1: set_message("Your turn.")
            battle_command(screen, font)
            if key[K_a] == 1 or key[K_SPACE] == 1:
                idx = 12
                tmr = 0
            
        elif idx == 12: # プレイヤーの攻撃
            if tmr == 1: set_message("Your attack!")
            if 2 <= tmr and tmr <= 4:
                screen.blit(imgEffect, [700-tmr*120, -100+tmr*120])
            if tmr == 5:
                emy_blink = 5
                set_message("***pts of damage!")
            if tmr == 16:
                idx = 13
                tmr = 0
        
        elif idx == 13: # 敵のターン、敵の攻撃
            if tmr == 1:set_message("Enemy turn.")
            if tmr == 5:
                set_message("Enemy attack!")
                emy_step = 30
            if tmr == 9:
                set_message("***pts of damage!")
                dmg_eff = 5
                emy_step = 0
            if tmr == 20:
                idx = 11
                tmr = 0
        
        pygame.display.update()
        clock.tick(5)

if __name__ == '__main__':
    main()



""" ----インデックスの値と処理
10: 戦闘に入る準備を行う。
    idxの値を11にし、プレイヤーの入力待ちに移る。
11: プレイヤーの入力を待つ。「戦う」「逃げる」などのコマンドを選ぶ。
    「戦う」を選ぶとidx12に、「逃げる」を選ぶとidx14に移る。
12: 主人公『プレイヤー』が敵を攻撃する処理。
    敵のライフを減らし、０以下になったらidx16の戦闘勝利へ移る。
    そうでなければidx13の敵のターンに移る。
13: 敵が主人公を攻撃する処理。
    主人公ライフを減らし、０以下になったらidx15の戦闘敗北へ移る。
    そうでなければidx11のプレイヤーの入力待ちに移る。
14: 敵から逃げられるかを乱数などで決める。
    逃げられるなら移動画面に戻る。
    逃げられないならidx13の敵の攻撃に移る。
15: 戦闘敗北の処理。
16: 戦闘勝利の処理。
"""