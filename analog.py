from gpiozero import MCP3008
from time import sleep

#create an object called pot that refers to MCP3008 channel 0
while True:
    pot = MCP3008(0)
    print(pot.value)
    sleep(0.1)