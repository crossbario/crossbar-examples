// hardware pins
static const int PIN_LED1 = 11;

void setup() {
    // setup hardware pin modes
    pinMode(PIN_LED1, OUTPUT);
}

void loop() {
    // toggle LED every 500ms
    digitalWrite(PIN_LED1, HIGH);
    delay(500);
    digitalWrite(PIN_LED1, LOW);
    delay(500);
}
