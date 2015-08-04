// hardware pins
static const int PIN_LED1 = 11;
static const int PIN_BTN1 = A0;
static const int PIN_POT1 = A1;


void setup() {
    // setup hardware pin modes
    pinMode(PIN_LED1, OUTPUT);
    pinMode(PIN_BTN1, INPUT);
    pinMode(PIN_POT1, INPUT);
}

void loop() {
    // read sensors values ..
    int btn1 = digitalRead(PIN_BTN1);
    int pot1 = analogRead(PIN_POT1);

    // .. and turn on/off LED based on button/analog values
    if (btn1 || pot1 > 400) {
        digitalWrite(PIN_LED1, HIGH);
    } else {
        digitalWrite(PIN_LED1, LOW);
    }

    // rate limiting
    delay(20);
}
