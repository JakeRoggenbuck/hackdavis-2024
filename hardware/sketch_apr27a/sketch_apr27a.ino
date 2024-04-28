const int speakerPin = 6;
const int redPin = 5;
const int bluePin = 4;
const int greenPin = 3;

const int trigPin = 13;
const int echoPin = 12;

void setup() {
  // put your setup code here, to run once:
  serial.begin(9600);
  pinMode(speakerPin, OUTPUT);
  pinMode(redPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void pingSensor() {
  // Clear the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Set the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
}

void checkSensor() {
  Serial.print("CHECKING BRAKE SENSOR");
  pingSensor();
  // Read the echoPin, returns the sound wave travel time in microseconds
  long duration = pulseIn(echoPin, HIGH);
  // Convert the time into a distance (cm)
  float distance_cm = duration * 0.034 / 2;
  // Print distance to serial monitor
  Serial.print("Distance: ");
  Serial.print(distance_cm);
  Serial.println(" cm");

  while (distance < 100) {
    digitalWrite(speakerPin, HIGH);
    delay(500)
  }
  
  digitalWrite(speakerPin, LOW);
}

void checkLane() {
  Serial.print("CHECKING LANE ASSIST")
  if (Serial.available() > 0) {
    char data = Serial.read();
    if (data == "BRAKE_SIG") {
      Serial.print("TODO: BRAKING BEHAVIOR")
    }
  }
}

void checkFace() {
  Serial.print("CHECKING FACE")
  if (Serial.available() > 0) {
    char data = Serial.read();
    if (data == "FACE_SIG") {
      Serial.print("TODO: FACE DETECTION")
    }
  }
}

void checkBSM() {
  Serial.print("CHECKING BLIND SPOT MONITOR")
  if (Serial.available() > 0) {
    char data = Serial.read();
    if (data == "BSM_SIG") {
      Serial.print("TODO: BSM BEHAVIOR")
    }
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(6, HIGH);
  delay(1000);
  digitalWrite(6, LOW);
  delay(1000); 

  checkSensor();
  checkLane();
  checkFace();
  checkBSM();
}
