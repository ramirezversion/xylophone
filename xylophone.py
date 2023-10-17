import os
import time
from gpiozero import MCP3008
from time import sleep


#
# Global variables
#
sounds_path = "/home/pi/xylophone" + "/sounds/"
volume = 20
chromatic = []
diatonic = []


#
# Play one sound with volume setted by 'volume' global variable, sending all outputs to dev null from os execution
#
def play_sound(sound, volume):
    os.system("amixer -M sset PCM " + str(volume) + "% > /dev/null 2>&1")
    os.system("aplay " + sounds_path + sound + " > /dev/null 2>&1 &")


#
# Play sounds list (only for testing)
#
def play_sounds_list(sounds_list):
    for sound in sounds_list:
        play_sound(sound, volume)
        time.sleep(0.3)


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

    # Never ending loop
    while True:
        # Read value from volume potentiometer and assign to global variable
        pot = MCP3008(0)
        volume = int(pot.value * 100)
        print("- Volume: " + str(volume))

        # Reproduce a sound to test volume potentiometer
        #play_sounds_list(chromatic)
        play_sound(chromatic[0], volume)
        time.sleep(0.3)
    

#
# Main function
#
if __name__ == '__main__':
    main()