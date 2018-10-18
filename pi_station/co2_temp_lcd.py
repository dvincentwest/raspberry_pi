from __future__ import print_function
import serial
import time
import traceback
import csv
from RPLCD.i2c import CharLCD
from Adafruit_DHT import read_retry

LCD_ADDRESS = 0x27
LCD_I2C_PORT_EXPANDER = 'PCF8574'
lcd = CharLCD(LCD_I2C_PORT_EXPANDER, LCD_ADDRESS)

co2_sensor = serial.Serial(
        '/dev/ttyS0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1.0)

def read_CO2():  #mh_z19():
    """read CO2 levels from the MH-Z19 sensor"""
    try:
        while 1:
            result=co2_sensor.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
            s=co2_sensor.read(9)
            # python2 code
            # if len(s) >= 4 and s[0] == b"\xff" and s[1] == b"\x86":
                # return {'CO2': ord(s[2])*256 + ord(s[3])}
            # python3 code
            if len(s) >= 4 and s[0] == 255 and s[1] == 134:
                return {'CO2': (s[2])*256 + (s[3])}
            break
    except:
        traceback.print_exc()

if __name__ == '__main__':

    blanks = " " * 16
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('CO2: ')
    lcd.cursor_pos = (1, 0)
    lcd.write_string('T: ')
    beginning_time = time.time()


    with open('record.csv', 'w') as f:
        fw = csv.writer(f)
        fw.writerow(('time', 'CO2-PPM', 'Temp-C', 'Humidity-PCT'))

        while True:
            thetime = time.time()
            co2 = read_CO2()['CO2']
            humidity, temperature = read_retry(11, 17)
            lcd.cursor_pos = (0, 5)
            lcd.write_string((str(co2) + ' PPM' + blanks)[:16-5])
            lcd.cursor_pos = (1, 3)
            t_string = '%d' % temperature + 'C'
            h_string = '%d' % humidity + '%'
            lcd.write_string((t_string + '  H:' + h_string + blanks)[:16-6])
            print('CO2:', co2, 'T:', temperature, 'H:', humidity)
            fw.writerow((thetime, co2, temperature, humidity))

            time.sleep(1)
