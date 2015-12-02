#include <stdlib.h> // for abs()

// hardware pins
static const int PIN_LED1 = 11;
static const int PIN_BTN1 = A0;
static const int PIN_POT1 = A1;

// For the Yun, you have to choose which
// serial port to connect to.
// Uncomment the line below to use 
// serial-over-USB to your computer
// #define USE_SERIAL_OVER_USB 1

#ifdef USE_SERIAL_OVER_USB
    // Serial connects to USB-over-Serial
    Serial_* serial = &Serial;
#else
    // Serial1 connects to the MCU with the CPU ..
    HardwareSerial* serial = &Serial1;
#endif


void setup() {
    // setup hardware pin modes
    pinMode(PIN_LED1, OUTPUT);
    pinMode(PIN_BTN1, INPUT);
    pinMode(PIN_POT1, INPUT);

    // setup serial communication
    serial->begin(115200);
}

int last_btn1 = -1;
int last_pot1 = -1;

void loop() {
    // read sensors values
    int btn1 = digitalRead(PIN_BTN1);
    int pot1 = analogRead(PIN_POT1);

    // check for changed values
    bool changed = false;

    if (last_btn1 < 0 || btn1 != last_btn1) {
        last_btn1 = btn1;
        changed = true;
    }

    if (last_pot1 < 0 || abs(pot1 - last_pot1) > 1) {
        last_pot1 = pot1;
        changed = true;
    }

    // forward changed values over serial
    if (changed) {
        serial->print(btn1);
        serial->print(",");
        serial->print(pot1);
        serial->println();        
    }

    // read commands from serial ..
    while (serial->available()) {

        // .. and turn on/off LED based on command received
        int value = serial->read();
        if (value == '0') {
            digitalWrite(PIN_LED1, LOW);
        } else if (value == '1') {
            digitalWrite(PIN_LED1, HIGH);
        }
    }

    // rate limiting
    delay(20);
}
