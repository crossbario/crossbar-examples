//int led = 13;
int led = 11;

HardwareSerial *port;

void setup() {                
    pinMode(led, OUTPUT);    

#ifdef __AVR_ATmega32U4__
    port = &Serial1; // Arduino Yun
#else
    port = &Serial;  // Arduino Mega and others
#endif
    port->begin(9600);
}

#define SERIAL_BUFFER_LEN 64

int delay_ms = 200;
char serial_buffer[SERIAL_BUFFER_LEN];
int serial_buffer_len = 0;

void loop() {
    digitalWrite(led, HIGH);
    port->println("HIGH");
    delay(delay_ms);

    digitalWrite(led, LOW);
    port->println("LOW");
    delay(delay_ms);


    while (port->available() && serial_buffer_len < SERIAL_BUFFER_LEN) {

        char c = port->read();

        if (c == '\n') {
            serial_buffer[serial_buffer_len] = 0;
            delay_ms = atoi(serial_buffer);
            serial_buffer_len = 0;
        } else {
            serial_buffer[serial_buffer_len] = c;
            serial_buffer_len += 1;
        }
    }
}
