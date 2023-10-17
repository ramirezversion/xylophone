import os
import time
from gpiozero import MCP3008
from time import sleep


sounds_path = "/home/pi/xylophone" + "/sounds/"
volume = 80
chromatic = []
diatonic = []


#
#
#
def play_sound(sound, volume):
    os.system("amixer -M sset PCM " + str(volume) + "%")
    os.system("aplay " + sounds_path + sound + "&")


#
#
#
def play_sounds_list(sounds_list):
    for sound in sounds_list:
        play_sound(sound, volume)
        time.sleep(0.3)


#
#
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
#
#
def print_header():
    print()
    print("----------------------")
    print("- Starting Xylophone -")
    print("----------------------")
    print()

#
#
#
def main():
    # Your program goes here
    print_header()
    print("... loading sounds")
    print()
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

    #play sounds
    while True:
        #play_sounds_list(chromatic)
        pot = MCP3008(0)
        print(pot.value)
        if pot.value > 0.5:
            play_sound(chromatic[0], volume)
        sleep(0.1)

    

#
#
#
if __name__ == '__main__':
    main()