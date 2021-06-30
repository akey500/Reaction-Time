#sudo nano /etc/rc.local
import RPi.GPIO as GPIO
from time import sleep
import random
from oledU import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

oled = oledU(128,32)

nswitches= 6
gpiosLights=[5,6,19,7,16,20] #out
gpioSwitch= [11,13,26,8,12,21]#in
gpiobuttons= [17,27,22]

nLights = len(gpiosLights)

for i in gpiosLights:
    GPIO.setup(i, GPIO.OUT, initial=GPIO.LOW)
    
for i in gpioSwitch:
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
for i in gpiobuttons:
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
#functions   
def off(n):
    GPIO.output(n, GPIO.LOW)
    
def alloff():
    for i in gpiosLights:
      off(i)  
           
def on(n):
    GPIO.output(n, GPIO.HIGH)



def rungame(runtime):
    i = random.randint(0, nLights-1)
    i_on= i
    on(gpiosLights[i])

    flags=[]
    for i in range (nswitches):
        flags.append(False)
    flags[i_on]= True


    #sleep(2)
    #off(40)
    dt= 0.2
    nsteps= int(runtime/dt)

    count= 0
    
    

    for x in range (nsteps):
        sleep(dt)
        
        inputValue = GPIO.input(gpioSwitch[i_on])
        if (inputValue == False):
            i = random.randint(0, nLights-1)
            print("Button press 1:", i+1)
            off(gpiosLights[i_on])
            on(gpiosLights[i])
            flags[i_on]= False
            i_on= i
            flags[i_on]= True
            count+= 1
            oled.write("Score:"+str(count))

    print (count)
    
    alloff()
    
    
    
while True:
    sleep(0.1)
    
    inputValue = GPIO.input(gpiobuttons[0])
    if (inputValue == False):
        print("30 SEC:")
        rungame(30)
        
    inputValue = GPIO.input(gpiobuttons[1])
    if (inputValue == False):
        print("60 SEC:")
        rungame(60)
        
    inputValue = GPIO.input(gpiobuttons[2])
    if (inputValue == False):
        print("90 SEC:")
        rungame(90)
    
