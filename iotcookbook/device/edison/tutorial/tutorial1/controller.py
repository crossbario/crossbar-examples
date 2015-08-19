import mraa
import time

# O0 (used as digital) on Arduino Tinkershield
led1 = mraa.Gpio(11)
led1.dir(mraa.DIR_OUT)

# I0 (used as digital) on Arduino Tinkershield
btn1 = mraa.Gpio(14)
btn1.dir(mraa.DIR_IN)

# I1 (used as analog) on Arduino Tinkershield
pot1 = mraa.Aio(1)

while True:
    pot1_val = pot1.read()
    btn1_val = btn1.read()
    if btn1_val or pot1_val > 400:
        led1.write(1)
    else:
        led1.write(0)

    time.sleep(0.02)
