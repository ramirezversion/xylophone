import pygame as pg
import time

pg.mixer.init()
pg.init()

a1Note = pg.mixer.Sound("F:\Project Harpsichord\The wavs\A1.wav")
a2Note = pg.mixer.Sound("F:\Project Harpsichord\The wavs\A0.wav")

pg.mixer.set_num_channels(50)

for i in range(25):
    a1Note.play()
    time.sleep(0.3)
    a2Note.play()
    time.sleep(0.3)







    https://classes.engineering.wustl.edu/ese205/core/index.php?title=Playing_multiple_sounds_at_once

#this is code from the final version of code used to program the Laser Harp. This is saying that if lasers 1 and/or 2 are broken, the wav file associated with that file will be played. 
import pygame
pygame.mixer.pre_init()
pygame.mixer.init()
pygame.init()
while true
if(light_level > 800):  # state 1
  pygame.mixer.Channel(0).play(pygame.mixer.Sound('/home/pi/laserharp-sounds/1.wav'))
if (light_level2 > 800):  # state 2
  pygame.mixer.Channel(1).play(pygame.mixer.Sound('/home/pi/laserharp-sounds/2.wav'))