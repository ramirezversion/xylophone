import os
import time
from gpiozero import MCP3008
from time import sleep
import threading
import soundfile as sf
import sounddevice as sd

#
# Global variables
#
sounds_path = "/home/pi/xylophone" + "/sounds/"
global_volume = 20
sensitivity = [25,25,25,25,25,25,15,15]
wait_time = 0.05
chromatic = []
diatonic = []
media = {}

#
# Play one sound with volume setted by 'volume' global variable, sending all outputs to dev null from os execution
#
def play_sound(sound):
    #os.system("aplay " + sounds_path + sound + " -M -N > /dev/null 2>&1 &")
    sd.play(sound[0],sound[1])



#
# Read sensor and play sound
#
def read_and_play_sound(i, sound):
    global wait_time
    while True:
        try:
            press = MCP3008(i)
            if int(press.value * 100.00) > int(sensitivity[i]):
                print("playing sound: " + sound + " - " + str(press.value*100) + "%")
                play_sound(media[sound])
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
    
    for file in sorted(files):
        media[file] = sf.read(path + file)
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