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