// Frequency Measurement on 1 PIN using hardware interrupts
// and measuring actual duratations (period lengths)

// http://www.atmel.com/Images/Atmel-2549-8-bit-AVR-Microcontroller-ATmega640-1280-1281-2560-2561_datasheet.pdf
// https://www.arduino.cc/en/Hacking/PinMapping2560

/*
82  PK7 ( ADC15/PCINT23 )   Analog pin 15
83  PK6 ( ADC14/PCINT22 )   Analog pin 14
84  PK5 ( ADC13/PCINT21 )   Analog pin 13
85  PK4 ( ADC12/PCINT20 )   Analog pin 12
86  PK3 ( ADC11/PCINT19 )   Analog pin 11
87  PK2 ( ADC10/PCINT18 )   Analog pin 10
88  PK1 ( ADC9/PCINT17 )    Analog pin 9
89  PK0 ( ADC8/PCINT16 )    Analog pin 8

Vector No.  Program Address Source  Interrupt Definition
12          $0016           PCINT2  Pin Change Interrupt Request 2
*/

#define PIN_COUNT 8
static const int PINS[PIN_COUNT] = {A8, A9, A10, A11, A12, A13, A14, A15};

void enable_pci () {
    cli();        // switch interrupts off while messing with their settings  
    PCICR = 0x04; // Enable Pin-Change Interrupts on Block 3
    PCMSK2 = 0b11111111;
    sei();        // turn interrupts back on    

    for (int i = 0; i < PIN_COUNT; ++i) {
        pinMode(PINS[i], INPUT_PULLUP);
    }
}

void setup () {
    Serial.begin(115200);

    // enable pin change mode interrupts on A8-A15
    enable_pci();
}

int counter = 0;

void loop () {
    Serial.print(counter);
    Serial.println();
    counter += 1;

    delay(500);
}

ISR(PCINT2_vect) {
    // Interrupt service routine. Every single PCINT16..23 (= A8..A15) change
    // will generate an interrupt: but this will always be the same interrupt routine
    Serial.print("hello");
    Serial.println();
}
