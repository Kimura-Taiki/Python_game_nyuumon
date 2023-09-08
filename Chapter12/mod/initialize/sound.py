import pygame

se = [ 
    pygame.mixer.Sound("Chapter12/sound/ohd_se_attack.ogg"),
    pygame.mixer.Sound("Chapter12/sound/ohd_se_blaze.ogg"),
    pygame.mixer.Sound("Chapter12/sound/ohd_se_potion.ogg"),
    pygame.mixer.Sound("Chapter12/sound/ohd_jin_gameover.ogg"),
    pygame.mixer.Sound("Chapter12/sound/ohd_jin_levup.ogg"),
    pygame.mixer.Sound("Chapter12/sound/ohd_jin_win.ogg")
]
for sound in se:
    sound.set_volume(0.1)
pygame.mixer.music.set_volume(0.1)
