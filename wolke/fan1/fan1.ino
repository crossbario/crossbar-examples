// Frequency Measurement on multiple PINs using counting

#define FAN_COUNT 1
#define ITER_DELAY 200
#define REPORT_EVERY_ITERS 8000

unsigned long time_started;
int iterations;
int state[FAN_COUNT];
int counter[FAN_COUNT];

void reset_counters () {
    for (int i = 0; i < FAN_COUNT; ++i) {
        state[i] = 0;
        counter[i] = 0;
    }
    time_started = micros();
    iterations = 0;
}

void process_counters () {
    for (int i = 0; i < FAN_COUNT; ++i) {
        int current = digitalRead(22 + i);
        if (current != state[i]) {
            counter[i] += 1;
        }
        state[i] = current;
    }
    iterations += 1;
}

void report_counters () {
    unsigned long time_ended = micros();
    unsigned long elapsed = 0;

    if (time_ended > time_started) {
        elapsed = time_ended - time_started;
    } else {
        elapsed = time_ended + ((unsigned long)(-1) - time_started);
    }



    Serial.print(elapsed);
    Serial.print(",");
    for (int i = 0; i < FAN_COUNT; ++i) {
        double rpm = (60. * (double)(counter[i]) / (((double)(elapsed)) / 1000000.)) / 4.;
        Serial.print(counter[i]);
        Serial.print(",");
        Serial.print(rpm);
        Serial.print(",");
        Serial.println();
    }

    reset_counters();
}

void setup () {
    // setup serial communication
    Serial.begin(115200);

    pinMode(13, OUTPUT);
    pinMode(22, INPUT_PULLUP);

    reset_counters();
}

void loop () {
    process_counters();
    
    if (iterations > REPORT_EVERY_ITERS) {
        report_counters();
    }

    delayMicroseconds(ITER_DELAY);
}
