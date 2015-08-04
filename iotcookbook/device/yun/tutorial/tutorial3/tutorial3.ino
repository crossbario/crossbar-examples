// hardware pins
static const int PIN_LED1 = 11;
static const int PIN_BTN1 = A0;
static const int PIN_POT1 = A1;

// on the Yun, Serial1 connects to the MCU with the CPU ..
HardwareSerial* serial = &Serial1;

// .. and Serial connects to USB-over-Serial
//HardwareSerial* serial = &Serial;


void setup() {
    // setup hardware pin modes
    pinMode(PIN_LED1, OUTPUT);
    pinMode(PIN_BTN1, INPUT);
    pinMode(PIN_POT1, INPUT);

    // setup serial communication
    serial->begin(115200);
}


void loop() {
    // read sensors values ..
    int btn1 = digitalRead(PIN_BTN1);
    int pot1 = analogRead(PIN_POT1);

    // .. and forward the values over serial
    serial->print(btn1);
    serial->print(",");
    serial->print(pot1);
    serial->println();

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
