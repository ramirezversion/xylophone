import os
import time
from gpiozero import MCP3008
from time import sleep
import threading
import pygame as pg

#
# Global variables
#
sounds_path = "/home/pi/xylophone" + "/sounds/"
global_volume = 20
sensitivity = [25,25,25,25,25,25,15,15]
wait_time = 0.1
chromatic = []
diatonic = []
media = {}
pg.mixer.pre_init()
pg.init()


#
# Play each sound in its own channel
#
def play_sound(sound, channel):
    global pg
    pg.mixer.Channel(channel).play(sound)


#
# Read sensor and play sound
#
def read_and_play_sound(i, sound):
    global wait_time
    global global_volume
    while True:
        try:
            press = MCP3008(i)
            if int(press.value * 100.00) > int(sensitivity[i]):
                print("playing sound: " + sound + " - " + str(int(press.value*100)) + "%")
                play_sound(media[sound],i)
                time.sleep(wait_time)                    
        except KeyboardInterrupt:
            break
        except:
            continue


#
# Modify volume
#
def set_volume():
    global global_volume
    while True:
        try:
            pot = MCP3008(0)
            # +1 and -1 values because reading value is so sensitive. in this way it is reduced the number of system call to modify the volume
            if (int(pot.value * 100) > global_volume + 1) or (int(pot.value * 100) < global_volume - 1):
                global_volume = int(pot.value * 100)
                os.system("amixer -M sset PCM " + str(global_volume) + "% > /dev/null 2>&1")
                print("volume set: " + str(global_volume))
        except KeyboardInterrupt:
            break
        except:
            continue


#
# Read and load sounds from sounds folder path
#
def load_sounds(path):
    global media
    files = []
    # Iterate directory
    for file_path in os.listdir(path):
        # check if current file_path is a file
        if os.path.isfile(os.path.join(path, file_path)):
            # add filename to list
            files.append(file_path)
    
    # Load sounds into memory for fast playing without disk reading delay
    for file in sorted(files):
        media[file] = pg.mixer.Sound(path + file)
    return sorted(files)


#
# Print header
#
def print_header():
    print()
    print("----------------------")
    print("- Starting Xylophone -")
    print("----------------------")
    print()


#
# Main
#
def main():
    global pg
    # Print header
    print_header()
    print("... loading sounds")
    print()
    # Load sounds and print output
    chromatic = load_sounds(sounds_path)
    print("- chromatic loaded!")
    print(chromatic)
    print()
    #for tone in chromatic:
    #    if not "#" in tone:
    #        diatonic.append(tone)
    #print("- diatonic loaded!")
    #print(diatonic)
    #print()

    # Volume thread
    t1 = threading.Thread(target=set_volume, args=())
    t1.start()
    # Threads for read values and play sounds
    threads = []

    # Create a channel for each note
    pg.mixer.set_num_channels(len(chromatic))

    #for sound in chromatic: - temporary set to value 6 and 7 because pin 6 and 7 are used for testing
    for i in range(6,8):
        t = threading.Thread(target=read_and_play_sound, args=(i,chromatic[i],))
        t.start()
    
    for t in threads:
        t.join()

    t1.join()

#
# Main function
#
if __name__ == '__main__':
    main()