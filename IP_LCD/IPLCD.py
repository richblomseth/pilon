#!/usr/bin/python3

# Periodically get and display the IP address and CPU temperature;
# repeat until the Select button is pressed

import sys
sys.path.append('/usr/share/adafruit/webide/repositories/my-pi-projects/Char_LCD')
sys.path.append('/usr/share/adafruit/webide/repositories/my-pi-projects/WiFi_Radio')

import os
import subprocess
import sys
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

# Get the hostname
def get_hostname():
    p = subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE)
    data = p.communicate()
    split_data = data[0].split()
    hostname = split_data[0]
    return hostname

# Get the default IP address
def get_ipaddress():
    arg = 'ip route list'
    p = subprocess.Popen(arg, shell=True, stdout=subprocess.PIPE)
    data = p.communicate()
    split_data = data[0].split()
    ipaddr = "Test" # TBD split_data[split_data.index('src')+1]
    return ipaddr

# Get the R-Pi temperature
def get_temperature():
    try:
        s = subprocess.check_output(["/opt/vc/bin/vcgencmd", "measure_temp"])
        return int(round(float(s.split('=')[1][:-3])*1.8 + 32))
    except:
        return 0

# Initialize the LCD
lcd = Adafruit_CharLCDPlate()
lcd.begin(16, 2)
lcd.clear()
lcd.backlight(lcd.ON)

# Main loop
done = False
while not done:
    lcd.message((get_hostname())) # TBD + ": " + str(get_temperature()) + str(chr(0xDF)) + "F").center(16))
    lcd.setCursor(0, 1)
    lcd.message(str(get_ipaddress()).center(16))
    # print get_ipaddress()

# TBD -- was xrange
    for i in range(100):
        if lcd.buttonPressed(lcd.SELECT):
            # Select button pressed--clear display and terminate
            lcd.clear()
            lcd.backlight(lcd.OFF)
            done = True
            subprocess.call("/usr/share/adafruit/webide/repositories/my-pi-projects/WiFi_Radio/PiPhi.py", shell=True)
            break
        sleep(0.1)
            
