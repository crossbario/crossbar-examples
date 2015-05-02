// Turn on LED when pushing a button

// define pins as we are using on the Tinkerkit sensorshield
int ledPin = 11;    // this is O0 connected to a LED
int analogPin = 0;  // this is I0 connected to a push button

void setup()
{
    pinMode(ledPin, OUTPUT);
    pinMode(analogPin, INPUT);
}

void loop()
{
    int val = analogRead(analogPin);
    if (val > 512) {
        digitalWrite(ledPin, HIGH);
    } else {
        digitalWrite(ledPin, LOW);
    }
    delay(50);
}
