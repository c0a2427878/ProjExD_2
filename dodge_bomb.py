import os
import random
import time
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数が：こうかとんRectまたは爆弾Rect
    戻り値：判定結果タプル（横,縦）
    画面外ならTrue、外ならFalues
    """
    yoko,tate = True,True
    if rct.left <0 or WIDTH < rct.right:
        yoko = False
    if rct.top <0 or HEIGHT < rct.bottom:
        tate = False

    return yoko,tate

def gameover(screen: pg.Surface) -> None:
    blackout = pg.Surface((WIDTH, HEIGHT))  
    blackout.fill((0,0,0))  #塗りつぶし
    blackout.set_alpha(150) #透明度
    screen.blit(blackout, (0,0))

    kk_cry = pg.image.load("fig/8.png")
    kk_cry1_rect = kk_cry.get_rect(center = (WIDTH//3, HEIGHT//2)) #画像配置
    kk_cry2_rect = kk_cry.get_rect(center = (2*WIDTH//3, HEIGHT//2))
    screen.blit(kk_cry,kk_cry1_rect)
    screen.blit(kk_cry,kk_cry2_rect)

    fonto = pg.font.Font(None,80) #フォントとサイズ
    txt = fonto.render("Game Over", True, (255,255,255)) 
    txt_rect = txt.get_rect(center=(WIDTH//2,HEIGHT//2))  #位置調整

    screen.blit(txt,txt_rect)

    pg.display.update()

    time.sleep(5)

def create_bomb_data() -> list[tuple[int, pg.Surface]]:
    bomb_data = []
    for r in range(1, 11):
        acc = r  # 加速度
        size = 20 * r  # 爆弾のサイズ
        bb_img = pg.Surface((size, size), pg.SRCALPHA)
        pg.draw.circle(bb_img, (255, 0, 0), (size // 2, size // 2), 10 * r)
        bomb_data.append((acc, bb_img))
    return bomb_data





def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg") 

    #爆弾データを作る
    bomb_data = create_bomb_data()
    bb_accs = [acc for acc, img in bomb_data]
    bb_imgs = [img for acc, img in bomb_data]
   
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255,0,0),(10,10), 10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH), random.randint(0,HEIGHT)
    vx ,vy = +5 , +5
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    tmr = 0
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            gameover(screen)

        if kk_rct.colliderect(bb_rct):
            print("Game Over")
            return

            
        
        

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #左右方向
                sum_mv[1] += mv[1] #上下方向
            

        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        bb_rct.move_ip(vx,vy)

        #時間に応じた爆弾設定
        idx = min(tmr // 75, 9)
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_img = bb_imgs[idx]

        bb_rct.move_ip(avx, avy)

        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
