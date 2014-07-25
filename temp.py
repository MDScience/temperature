#!/usr/bin/python3
 
import os
import glob
import time
import gspread
import sys
import datetime

 

 
#attempt to log in to your google account
try:
    gc = gspread.login('account@account.com','password') #put in your account and password for google drive
except:
    print('fail')
    sys.exit()
 
#open the spreadsheet
worksheet = gc.open('spreadsheet_name').sheet1 #put in the name of the spreadsheet
 
#initiate the temperature sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
#set up the location of the sensor in the system
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
print ('Code is running')
  
def read_temp_raw(): #a function that grabs the raw temperature data from the sensor
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines 
 
def read_temp(): #a function that checks that the connection was good and strips out the temperature
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos !=-1:
      temp_string = lines[1][equals_pos+2:]
      temp_c = float(temp_string)/1000.0
      temp_f = temp_c * 9.0/5.0 + 32.0
      return temp_c
 
while True: #infinite loop
    print('loop is running')
    tempin = read_temp() #get the temp
    values = [datetime.datetime.now(), tempin]
    worksheet.append_row(values)
    time.sleep(15) 
