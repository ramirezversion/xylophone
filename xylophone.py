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
max_play_time = [100,100,100,100,100,100,100,100]
active_pad = [0,0,0,0,0,0,0,0]
pad_play_time = [0,0,0,0,0,0,0,0]
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
# Read sensors and play sounds
#
def read_and_play_sounds(sounds_list):
    global max_play_time
    while True:
        try:
            #for sound in sounds_list:
            #    global global_volume
            #    play_sound(sound)
            #    time.sleep(0.3)
            for i in range(6,8):
                press = MCP3008(i)
                if int(press.value * 100) > sensitivity[i] and active_pad[i] == 0:
                    active_pad[i] = 1
                    print("playing sound: " + str(press.value*100))
                    play_sound(sounds_list[i-6])
                    time.sleep(0.1)                    
                elif active_pad[i] == 1:
                    pad_play_time[i] += 1
                    if pad_play_time[i] > max_play_time[i]:
                        active_pad[i] = 0
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
    for tone in chromatic:
        if not "#" in tone:
            diatonic.append(tone)
    print("- diatonic loaded!")
    print(diatonic)
    print()

    t1 = threading.Thread(target=set_volume, args=())
    t2 = threading.Thread(target=read_and_play_sounds, args=(chromatic,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


#
# Main function
#
if __name__ == '__main__':
    main()