void setup() {
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);
  pinMode(A6, INPUT);
  pinMode(A7, INPUT);
  Serial.begin(115200);
}

void loop() {
  int sensor0 = analogRead(A0);
  int sensor1 = analogRead(A1);
  int sensor2 = analogRead(A2);
  int sensor3 = analogRead(A3);
  int sensor4 = analogRead(A4);
  int sensor5 = analogRead(A5);
  int sensor6 = analogRead(A6);
  int sensor7 = analogRead(A7);

  Serial.print(sensor0);

  Serial.print(",");
  Serial.print(sensor1);

  Serial.print(",");
  Serial.print(sensor2);

  Serial.print(",");
  Serial.print(sensor3);

  Serial.print(",");
  Serial.print(sensor4);

  Serial.print(",");
  Serial.print(sensor5);

  Serial.print(",");
  Serial.print(sensor6);

  Serial.print(",");
  Serial.print(sensor7);

  Serial.println();

  delay(10);
}
