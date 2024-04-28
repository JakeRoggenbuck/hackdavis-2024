const int speakerPin = 6;

const int redLeftPin = 5;
const int blueLeftPin = 4;
const int greenLeftPin = 3;

const int redRightPin = 11;
const int blueRightPin = 10;
const int greenRightPin = 9;

const int trigPin = 13;
const int echoPin = 12;

void setup() {
  Serial.begin(9600);
  pinMode(speakerPin, OUTPUT);
  pinMode(redLeftPin, OUTPUT);
  pinMode(blueLeftPin, OUTPUT);
  pinMode(greenLeftPin, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  digitalWrite(redLeftPin, HIGH);
  digitalWrite(redRightPin, HIGH);
  digitalWrite(greenLeftPin, HIGH);
  digitalWrite(greenRightPin, HIGH);
  digitalWrite(blueLeftPin, HIGH);
  digitalWrite(blueRightPin, HIGH);
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

float updateDistance() {
  // Read the echoPin, returns the sound wave travel time in microseconds
  long duration = pulseIn(echoPin, HIGH);
  // Convert the time into a distance (cm)
  float distance_m = (duration * 0.034 / 2) / 100;
  // Print distance to serial monitor
  Serial.print("Distance: ");
  Serial.print(distance_m);
  Serial.println(" m");

  return distance_m;
}

void checkSensor() {
  Serial.print("CHECKING BRAKE SENSOR\n");
  pingSensor();
  float distance = updateDistance();

  while (distance < 4.5) {
    pingSensor();
    distance = updateDistance();
    digitalWrite(speakerPin, HIGH);
    digitalWrite(redLeftPin, LOW);
    digitalWrite(redRightPin, LOW);
    delay(250);
    digitalWrite(speakerPin, LOW);
    digitalWrite(redLeftPin, HIGH);
    digitalWrite(redRightPin, HIGH);
    delay(250);
  }
  
  digitalWrite(speakerPin, LOW);
}

void blink_beep(int redPin, int greenPin, int bluePin) {
  digitalWrite(redPin, LOW);        
  digitalWrite(greenPin, LOW);
  digitalWrite(bluePin, LOW);
  digitalWrite(speakerPin, HIGH);
  delay(200);
  digitalWrite(redPin, HIGH);
  digitalWrite(greenPin, HIGH);
  digitalWrite(bluePin, HIGH);
  digitalWrite(speakerPin, LOW);
  delay(200);
}

void checkLane() {
  Serial.print("CHECKING LANE ASSIST\n");
  
  if (Serial.available() > 0) {
    String data = Serial.readString();
    while (data == "LANE_LEFT_SIG") {
      Serial.print("FLICKERING\n");
      blink_beep(redLeftPin, greenLeftPin, blueLeftPin);
      data = Serial.readString();
    }

    while (data == "LANE_RIGHT_SIG") {
      Serial.print("FLICKERING\n");
      blink_beep(redRightPin, greenRightPin, blueRightPin);
      data = Serial.readString();
    }
  }
}

void checkFace() {
  Serial.print("CHECKING FACE\n");
  if (Serial.available() > 0) {
    String data = Serial.readString();
    while (data == "FACE_SIG") {
      digitalWrite(speakerPin, HIGH);
      delay(250);
      digitalWrite(speakerPin, LOW);
      delay(250);
      data = Serial.readString();
    }
  }
}

void checkBSM() {
  Serial.print("CHECKING BLIND SPOT MONITOR\n");
  if (Serial.available() > 0) {
    String data = Serial.readString();
    while (data == "BSM_LEFT_SIG") {
      Serial.print("LEFT ON\n");
      digitalWrite(redLeftPin, LOW);        
      data = Serial.readString();
    }

    while (data == "BSM_RIGHT_SIG") {
      Serial.print("RIGHT ON\n");
      digitalWrite(redRightPin, LOW);        
      data = Serial.readString();
    }
  }
}

void loop() {
  checkSensor();
  checkLane();
  checkFace();
  checkBSM();
}
