// hardware pins
static const int PIN_LED1 = 11;
static const int PIN_BTN1 = A0;


void setup() {
    // setup hardware pin modes
    pinMode(PIN_LED1, OUTPUT);
    pinMode(PIN_BTN1, INPUT);
}

void loop() {
    // read button and turn on/off LED accordingly
    int btn1 = digitalRead(PIN_BTN1);
    if (btn1) {
        digitalWrite(PIN_LED1, HIGH);
    } else {
        digitalWrite(PIN_LED1, LOW);
    }

    // rate limiting
    delay(20);
}
