// Frequency Measurement on 1 PIN using hardware interrupts
// and measuring actual duratations (period lengths)

static const int PIN_FAN1 = 2; // D3 (Yun) = Interrupt 0 / O5 (Tinkershield)

unsigned long last_time = 0;
unsigned long last_period = 0;

void handler () {
    unsigned long current_time = micros();

    if (last_time == 0) {
        last_time = micros();
        return;
    }

    last_period = current_time - last_time;
    last_time = current_time;
}

void setup () {
    Serial.begin(115200);
    pinMode(PIN_FAN1, INPUT_PULLUP);

    // https://www.arduino.cc/en/Reference/AttachInterrupt
    attachInterrupt(0, handler, RISING);
}

void loop () {

    int rpm = 0;

    if (last_period != 0) {
        rpm = (int) round(60. * (1000000. / ((double)(last_period))) / 2.);
    }

    Serial.print(rpm);
    Serial.println();

    delay(500);
}
