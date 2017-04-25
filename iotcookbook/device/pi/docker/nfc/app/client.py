from Adafruit_GPIO import I2C

# https://github.com/adafruit/Adafruit_Python_GPIO/blob/master/Adafruit_GPIO/I2C.py
# https://github.com/adafruit/Adafruit_Python_GPIO/blob/master/tests/test_I2C.py

device = I2C.get_i2c_device(0x2d)
print(device)
print(dir(device))
