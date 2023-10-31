import os
import time
from gpiozero import MCP3008
from time import sleep
import threading


#
# Global variables
#
sounds_path = "/home/pi/xylophone" + "/sounds/"
global_volume = 20
sensitivity = [25,25,25,25,25,25,85,25]
max_play_time = 0.075
chromatic = []
diatonic = []


#
# Play one sound with volume setted by 'volume' global variable, sending all outputs to dev null from os execution
#
def play_sound(sound):
    global global_volume
    os.system("amixer -M sset PCM " + str(global_volume) + "% > /dev/null 2>&1")
    os.system("aplay " + sounds_path + sound + " > /dev/null 2>&1 &")


#
# Read sensor and play sound
#
def read_and_play_sound(i, sound):
    global max_play_time
    while True:
        try:
            #for sound in sounds_list:
            #    global global_volume
            #    play_sound(sound)
            #    time.sleep(0.3)
            press = MCP3008(i)
            if int(press.value * 100.00) > int(sensitivity[i]):
                print("playing sound: " + sound + " - " + str(press.value*100) + "%")
                play_sound(sound)
                time.sleep(max_play_time)                    
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
            global_volume = int(pot.value * 100)
            #print("- Volume: " + str(global_volume))
        except KeyboardInterrupt:
            break
        except:
            continue


#
# Read and load sounds from sounds folder path
#
def load_sounds(path):
    files = []
    # Iterate directory
    for file_path in os.listdir(path):
        # check if current file_path is a file
        if os.path.isfile(os.path.join(path, file_path)):
            # add filename to list
            files.append(file_path)
    return sorted(files)


#
# Print header, include some ascii art better
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

    # volume thread
    t1 = threading.Thread(target=set_volume, args=())
    t1.start()
    # threads for read values and play sounds
    threads = []

    #for sounds in chromatic:
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