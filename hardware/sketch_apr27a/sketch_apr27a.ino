const int speakerPin = 6;
const int redPin = 5;
const int bluePin = 4;
const int greenPin = 3;

const int trigPin = 13;
const int echoPin = 12;

void checkSensor() {

}

void checkLane() {

}

void checkFace() {

}

void checkBSM() {

}

void setup() {
  // put your setup code here, to run once:
  serial.begin(9600);
  pinMode(6, OUTPUT);
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
