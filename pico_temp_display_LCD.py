'''
read and display the temperature
and output the results to temp_log.txt
(C)SGF2022
'''

''' Python supplied libraries '''
import utime
from machine import I2C, Pin

''' Programmer supplied libraries '''
''' These are stored in /lib folder '''
from lcd_api import LcdApi             #to control the LCD
from pico_i2c_lcd import I2cLcd        #to control the LCD
import csv_functions_api as csv        #read and write to a text file
import pico_temp_constants as con      #program constants stored here

''' Possible libraries to include in the future'''
#from char_api import custom_character as char
#import char_api

''' Setup OnBoard LED Variable (This is for Pico and Pico H) '''
LED = Pin(25, Pin.OUT)

''' set variables for comms and LCD '''
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, con.I2C_ADDR, con.I2C_NUM_ROWS, con.I2C_NUM_COLS)


''' set up the file header string '''
#file_header = "Temperature logger (C) SGF 2022. Update Interval: "

''' function to handle the greeting '''
def greeting():
    
    lcd.clear()
    lcd.move_to(4,0)
    lcd.putstr("Welcome")
    lcd.move_to(2,1)
    lcd.putstr("To NerdCave")
    
    lcd.move_to(0,0)
    lcd.putchar(chr(con.CHAR_BELL))
    lcd.move_to(15,0)
    lcd.putchar(chr(con.CHAR_OMEGA))
    
    lcd.move_to(0,1)
    lcd.putchar(chr(con.CHAR_PADLOCK))
    lcd.move_to(15,1)
    lcd.putchar(chr(con.CHAR_FOX))   
    
    utime.sleep(3)

def update_time(UPDATE_TIME):
    
    lcd.clear()
    lcd.move_to(0,0)
    lcd.putstr("Please enter an")
    lcd.move_to(0,1)
    lcd.putstr("interval in secs")
    
    while True:
        try:
            UPDATE_TIME = int(input("Enter an update interval in seconds: "))
            break
        except ValueError:
            print ("Please enter a whole number.")
            
    lcd.clear()
    return UPDATE_TIME
    
''' function to read the time from the Pico' real time closk RTC '''
def read_time():
    
    rtc=machine.RTC()
    timestamp = rtc.datetime()
    time_stamp_string="%02d.%02d.%02d-%02d.%02d.%02d"%(timestamp[0:3] + timestamp[4:7])
    datestring = time_stamp_string.rsplit("-",2)

    return ("Time:" + datestring[1])

def read_date():

    rtc=machine.RTC()
    timestamp = rtc.datetime()
    time_stamp_string="%02d.%02d.%02d-%02d.%02d.%02d"%(timestamp[0:3] + timestamp[4:7])
    datestring = time_stamp_string.rsplit("-",2)
    
    return ("Date:" + datestring[0])
    

''' function to read the ambient temperature from the Pico's semsor '''
def read_temp():
    
    sensor_temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    formatted_temperature = "{:.2f}".format(temperature)
    string_temperature = str("Temp:" + formatted_temperature + " C")
    
    return string_temperature

''' functon to define characters
go to https://maxpromer.github.io/LCD-Character-Creator/
copy the hex values into a new custom_char '''
def customcharacter():
    
    #celcius
  lcd.custom_char(con.CHAR_CELCIUS, bytearray([
  0x07,
  0x05,
  0x07,
  0x00,
  0x00,
  0x00,
  0x00,
  0x00
        
        ]))

    #arrow right
  lcd.custom_char(con.CHAR_ARROW_RIGHT, bytearray([
  0x00,
  0x04,
  0x02,
  0x1F,
  0x02,
  0x04,
  0x00,
  0x00
        ]))
  
    # arrow left
  lcd.custom_char(con.CHAR_ARROW_LEFT, bytearray([
  0x00,
  0x04,
  0x08,
  0x1F,
  0x08,
  0x04,
  0x00,
  0x00
        ]))
  
    #(c)
  lcd.custom_char(con.CHAR_COPYRIGHT, bytearray([
  0x0E,
  0x11,
  0x17,
  0x19,
  0x19,
  0x17,
  0x11,
  0x0E
        ]))
  
    #Ohm
  lcd.custom_char(con.CHAR_OMEGA, bytearray([
  0x00,
  0x0E,
  0x11,
  0x11,
  0x0A,
  0x0A,
  0x1B,
  0x00
        ]))

    #Fox
  lcd.custom_char(con.CHAR_FOX, bytearray([
  0x0A,
  0x1B,
  0x1F,
  0x15,
  0x1F,
  0x0E,
  0x04,
  0x00
        ]))
  
    #Bell
  lcd.custom_char(con.CHAR_BELL, bytearray([
  0x00,
  0x04,
  0x0E,
  0x0E,
  0x0E,
  0x1F,
  0x04,
  0x00
        ]))

    #Padlock
  lcd.custom_char(con.CHAR_PADLOCK, bytearray([
  0x0E,
  0x11,
  0x11,
  0x1F,
  0x1B,
  0x1B,
  0x1F,
  0x00
        ]))


'''
Main Program starts here
'''

LED.on()
customcharacter() 
greeting()
lcd.clear()
UPDATE_INTERVAL = update_time(0)

''' write the file header '''
header = con.FILE_HEADER + str(UPDATE_INTERVAL) + "seconds" + "\n"
csv.write_string("" + "\n",con.FILE_APPEND)
csv.write_string(header,con.FILE_APPEND)
csv.write_string("-" * 60 + "\n",con.FILE_APPEND)

try:
    
    while True:
       
        ''' display time on LCD '''
        lcd.move_to(0,1)
        lcd.putstr(read_time())
       
        ''' display temp on LCD '''
        lcd.move_to(0,0)
        lcd.putstr(read_temp())
        lcd.move_to(10,0)
        lcd.putchar(chr(con.CHAR_CELCIUS))
        
        ''' write results to a text file '''
        csv.write_string(str(read_date()) + " - " + str(read_time()) + " - " + str(read_temp()) + "\n",con.FILE_APPEND)
        
        print(str(read_date()) + " - " + str(read_time()) + " - " + str(read_temp()))
        
        ''' to show user that code is running
        flash the LED at the update interval rate '''
        LED.toggle()
        
        utime.sleep(UPDATE_INTERVAL)
        
except KeyboardInterrupt:
    
    ''' A managed way of handling Ctrl-C '''
    print ("Ctrl-C Pressed")
    LED.off()
    lcd.hal_backlight_off()
    
finally:
    
    LED.off()
    lcd.hal_backlight_off()
