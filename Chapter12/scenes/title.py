def scene_title():
    global screen, font, fontS, key
    global idx, tmr
    global floor, welcome, pl_lifemax, pl_life, pl_str, food, potion, blazegem
    if tmr == 1:
        pygame.mixer.music.load("Chapter12/sound/ohd_bgm_title.ogg")
        pygame.mixer.music.play(-1)
    screen.fill(BLACK)
    screen.blit(imgTitle, [40, 60])
    if fl_max  >= 2:
        draw_text(screen, "You reached floor {}.".format(fl_max), 300, 460, font, CYAN)
    draw_text(screen, "Press space key", 320, 560, font, BLINK[tmr%6])
    if key[K_SPACE] == 1:
        make_dungeon()
        put_event()
        floor = 1
        welcome = 15
        pl_lifemax = 300
        pl_life = pl_lifemax
        pl_str = 100
        food = 300
        potion = 0
        blazegem = 0
        idx = Idx.FIELD_WFI
        pygame.mixer.music.load("Chapter12/sound/ohd_bgm_field.ogg")
        pygame.mixer_music.play(-1)
