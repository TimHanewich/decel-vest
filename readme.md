# Deceleration Vest
Detecting deceleration while in/on a vehicle from wearing an MPU6050 accelerometer.

## Raspberry Pi Pico Tips
- Great youtube videos on getting started:
    - Getting started: https://www.youtube.com/watch?v=yzsEr2QCGPw
    - Using rShell: https://www.youtube.com/watch?v=IMZUZuytt7o&ab_channel=CoreElectronics
- Pico Datasheet: https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf
- Using **rshell**
    - To copy contents of a folder to another folder
        - `cp MyCodeFolder/* /pyboard/`
- Using I2C with Pico:  https://www.hackster.io/mr-alam/how-to-use-i2c-pins-in-raspberry-pi-pico-i2c-scanner-code-8f489f
- Using MPU6050 with Raspberry Pi Pico
    - https://peppe8o.com/using-gyroscope-and-accelerometer-with-mpu6050-raspberry-pi-pico-and-micropython/
    - The **imu** and **vector3d** class aparently will work with the MPU6050: https://github.com/micropython-IMU/micropython-mpu9x50
- Using the *machine* module in MicroPython: https://docs.micropython.org/en/latest/library/machine.html

## Example of using MPU6050 module with MicroPython (from peppe8o)
```
from imu import MPU6050
import time
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
imu = MPU6050(i2c)

while True:
    # Following print shows original data get from libary. You can uncomment to see raw data
    #print(imu.accel.xyz,imu.gyro.xyz,imu.temperature,end='\r')
    
    # Following rows round values get for a more pretty print:
    ax=round(imu.accel.x,2)
    ay=round(imu.accel.y,2)
    az=round(imu.accel.z,2)
    gx=round(imu.gyro.x)
    gy=round(imu.gyro.y)
    gz=round(imu.gyro.z)
    tem=round(imu.temperature,2)
    print(ax,"\t",ay,"\t",az,"\t",gx,"\t",gy,"\t",gz,"\t",tem,"        ",end="\r")
    
    # Following sleep statement makes values enought stable to be seen and
    # read by a human from shell
    time.sleep(0.2)
```

## Using NEO-6M GPS Module with Raspberry Pi Pico
- https://microcontrollerslab.com/neo-6m-gps-module-raspberry-pi-pico-micropython/
- NMEA Codes: http://aprs.gids.nl/nmea/

## The need for MicroPython Double Precision
By default, only single float precision is enabled in micropython. For the GPS-related calculations (distance between two points that uses sin, cos, acos, etc), we need to use double precision numbers. 

[MicroPython 1.19.1 with Double Precision floating point numbers enabled (not the default single precision)](micropython-1.19.1-double-precision.uf2)

This article describes how to do this. These are the steps I followed: https://community.element14.com/products/raspberry-pi/b/blog/posts/pi-pico-rp2040-micropython-double-precision
- Download MicroPython .zip file from: https://micropython.org/download/

## Using CSV files with MicroPython
For whatever reason, MicroPython reads the new lines in a CSV file that is generated by Excel as \r, not \n. So reading a single line with file.readline() doesn't work, it tries to read the whole file. To fix this, copy and paste the content from an Excel-saved CSV file into another CSV file (text editor). MicroPython will be able to read the new line in that file.


## The Transistor-boosted LED light current:
- With the landscape lighting LED bulb (12V):
    - Current draw from the battery is 0.15A using the DC-DC boost converter (~3.25V to 11.5V).
    - The LED bulb normally only draws 0.041A, but it draws more current due to the need to boost the voltage.
    - The current draw into the transistor base (from the GPIO pin) is < 0.001A, extremely small. But **NEEDS TO GO THROUGH A 10,000 OHM RESISTOR**!
- With the [red marine lights](https://www.amazon.com/dp/B081HD261N?psc=1&smid=A1J9BIVZ7I2UP0&ref_=chk_typ_imgToDp) (12V)
    - Current draw raw @ 12V: 0.07A
    - Current draw @ 3.5V going through MT3608 boost converter to 12V: 0.311A

## Searching for the right LED
- Circular, like [this](https://www.amazon.com/Landscape-Halogen-Equivalent-Daylight-Recessed/dp/B07N86919J/ref=sr_1_58?crid=2HQB8UFH497GN&keywords=BAOMING+G4+led+red&qid=1658066241&sprefix=baoming+g4+led+re%2Caps%2C72&sr=8-58), but needs to be red.

## Notable commits
- Works perfectly, with 1 LED: `0e79e44b835c4c671140007cf82c78b128e7ad99`