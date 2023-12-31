import pygame
import sys

def main():
    pygame.init()
    pygame.display.set_caption("初めてのPygame 画像表示")
    screen = pygame.display.set_mode((640, 360))
    clock = pygame.time.Clock()
    img_bg = pygame.image.load("Chapter10/pg_bg.png")
    img_chara = [
        pygame.image.load("Chapter10/pg_chara0.png"),
        pygame.image.load("Chapter10/pg_chara1.png")
    ]
    tmr = 0

    while True:
        tmr += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    screen = pygame.display.set_mode((640, 360), pygame.FULLSCREEN)
                if event.key == pygame.K_F2 or event.key == pygame.K_ESCAPE:
                    screen = pygame.display.set_mode((640, 360))
        x = tmr%160
        for i in range(5):
            screen.blit(img_bg, [i*160-x, 0])
        screen.blit(img_chara[tmr%2], [224, 160])
        pygame.display.update()
        clock.tick(5)

if __name__ == '__main__':
    main()

"""     ----画像を画面に描画する----
screen.blit(画像を読み込んだ変数, [x座標, y座標])
※ 座標は左上を指定する
"""

"""     ----画像操作関数----
1 : 拡大縮小
    img_s = pygame.transform.scale(img, [幅, 高さ])
2 : 回転
    img_r = pygame.transform.rotate(img, 回転角)
3 : 回転＋拡大縮小
    img_rz = pygame.transform.rotozoom(img, 回転角, 大きさの比率)
※ 回転角は度数法(degree)で指定する。
"""