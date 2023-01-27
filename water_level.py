import RPi.GPIO as GPIO
import os
import glob
import time
import math
from getmac import get_mac_address as gma
from datetime import datetime
from gpiozero import CPUTemperature
#import mysql.connector as mysql

GPIO.setmode(GPIO.BCM)

# Get MAC Address
print (gma())

# Temperature Sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
    
def read_temp():
    lines = read_temp_raw()
    while lines [0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
#        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c
        
# Air Temp function saved as variable for future calculations.
air_temp = read_temp()

# Level Sensor Pinout
TRIG = 23
ECHO = 24

# Datetime object containing current date and time.
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

# CPU temperature object containing current CPU temp.
cpu = CPUTemperature()

# Calculate speed of sound based on temperature.
speed_sound = (346 + 0.606 * air_temp) * 100 / 2

# Server IP address/domain name
#HOST = "ENTER HOST NAME"
# Database name, if you want to just connect to MySql server, leave this blank.
#DATABASE = "ENTER DATABASE NAME"
# This is the user you create.
#USER = "ENTER USER NAME"
# User password
#PASSWORD = "ENTER PASSWORD"
# Connect to MySQL Server
#db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
#print("Connected to:", db_connection.get_server_info())

print ("CPU temp is",cpu.temperature,"Degrees C")
print ("Air temp is",air_temp, "Degrees C")
print (dt_string)
print ("Distance Measurement In Progress")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print ("Waiting For Sensor To Settle")
time.sleep(2)

GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

while GPIO.input(ECHO)==0:
    pulse_start = time.time()
    
while GPIO.input(ECHO)==1:
    pulse_end = time.time()
    
pulse_duration = pulse_end - pulse_start
distance = pulse_duration * speed_sound
distance = round(distance, 2)
distance_inches = round(distance * 0.3937, 2)

# Print calculated Distance.
print ("Distance:",distance_inches,"in")

# If there is a warning.
GPIO.cleanup()
