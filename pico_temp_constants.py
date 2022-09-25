''' constants file for pico_temp_display_LCD.py
pico_temp_constants.py '''

''' LCD constants '''
I2C_ADDR     = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

''' character constants '''
CHAR_CELCIUS = 0
CHAR_ARROW_RIGHT = 1
CHAR_ARROW_LEFT = 2
CHAR_COPYRIGHT = 3
CHAR_OMEGA = 4
CHAR_FOX = 5
CHAR_BELL = 6
CHAR_PADLOCK = 7

''' File Constants '''
FILE_APPEND = "a"
FILE_READ = "r"
FILE_WRITE = "w"

''' Program Constants '''
UPDATE_INTERVAL = 60
FILE_HEADER = "Temperature logger (C) SGF 2022. Update Interval: "
