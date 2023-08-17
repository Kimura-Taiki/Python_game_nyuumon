import pygame   # pygameモジュールをインポート
import sys  # sysモジュールをインポート

WHITE = (255, 255, 255) # 色の定義　白
BLACK = (  0,   0,   0) # 色の定義　黒

def main(): # メイン処理を行う関数の定義
    pygame.init()   # pygameモジュールの初期化
    pygame.display.set_caption("初めてのPygame")    # ウィンドウに表示されるタイトルを指定
    screen = pygame.display.set_mode((800, 600))    # 描画面(スクリーン)を初期化する
    clock = pygame.time.Clock() # clockオブジェクトを作成
    font = pygame.font.Font(None, 80)   # フォントオブジェクトを作成
    tmr = 0 # 時間を管理する定数tmrの宣言

    while True: # 無限ループ
        tmr += 1    # tmrの値を1増やす
        for event in pygame.event.get():    # pygameのイベントを繰り返しで処理する
            if event.type == pygame.QUIT:   # ウィンドウのXボタンをクリックした時
                pygame.quit()   # pygameモジュールの初期化を解除
                sys.exit()  # プログラムを終了する

        txt = font.render(str(tmr), True, WHITE)    # Surfaceに文字列を描く
        screen.fill(BLACK)  # 指定した色でスクリーンをクリアする
        screen.blit(txt, [300, 200])    # 文字列を描いたSurfaceをスクリーンに転送
        pygame.display.update() # 画面を更新する
        clock.tick(10)  # フレームレートを指定

if __name__ == '__main__':  # このプログラムが直接実行されたときに
    main()  # main関数を呼び出す

"""     ----Pygameでの文字列描画----
1 : フォントと文字サイズを指定(12行目)
    font = pygame.font.Font(None, 80)   # フォントオブジェクトを作成
    # pygameのフォント指定。
    # tkinterのフォント指定とは違います。
2 : 文字列をSurfaceに描く(22行目)
    txt = font.render(str(tmr), True, WHITE)    # Surfaceに文字列を描く
    # render()命令で文字列と色を指定し、文字列を描いたSurfaceを作ります。
    # ２つ目の引数をTrueにすると文字の縁が滑らかになります。
3 : 上述のSurfaceをウィンドウに貼り付ける(24行目)
    screen.blit(txt, [300, 200])    # 文字列を描いたSurfaceをスクリーンに転送
    # blit()命令で画面に貼り付けます。
"""

"""     ----if __name__ == '__main__':の意味
他のPythonのプログラムにimportされた際に勝手に起動する事を防ぐ。
"""