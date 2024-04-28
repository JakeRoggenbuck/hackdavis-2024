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
    delay(250);
    digitalWrite(speakerPin, LOW);
    delay(250);
  }
  
  digitalWrite(speakerPin, LOW);
}

void checkLane() {
  Serial.print("CHECKING LANE ASSIST\n");
  if (Serial.available() > 0) {
    char data = Serial.read();
    if (data == "LANE_LEFT_SIG") {
      
    }
  }
}

void checkFace() {
  Serial.print("CHECKING FACE\n");
  if (Serial.available() > 0) {
    char data = Serial.read();
    if (data == "FACE_SIG") {
      Serial.print("TODO: FACE DETECTION");
    }
  }
}

void checkBSM() {
  Serial.print("CHECKING BLIND SPOT MONITOR\n");
  if (Serial.available() > 0) {
    char data = Serial.read();
    if (data == "BSM_SIG") {
      Serial.print("TODO: BSM BEHAVIOR");
    }
  }
}

void loop() {
  checkSensor();
  checkLane();
  checkFace();
  checkBSM();
}
