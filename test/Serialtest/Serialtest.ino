//Land rover code for the arduino
//sets up the motors for movement and allows for pre-programmed paths to be made
//Created by Brandon
//Date: 06/12/2017


//initialize the steering
const int steering1 = 3;
const int steering2 = 5;

//initialize the front motor
const int frontMotor1 = 6;
const int frontMotor2 = 9;

//intitialize the back motor
const int backMotor1 = 10;
const int backMotor2 = 11;

//create 4 different speeds
const int speed1 = 40; //below 40 the robot either doesnt move or moves at an incredibly small speed
const int speed2 = 70;
const int speed3 = 150;
const int speed4 = 255;

const int trigger = A0;
const int echo = 7;

const int LLED = 8;
const int RLED = 12;

unsigned long previousMillis = 0;

#define LIMIT 30
#define LEFT LOW, HIGH
#define RIGHT HIGH, LOW
#define BOTH HIGH, HIGH
#define NONE LOW, LOW

//define 2 directions for the turns
#define FORWARD LOW
#define BACKWARD HIGH

void setup() {
  //sets up serial port
  Serial.begin(9600);

  //define pinModes for the motors
  pinMode(steering1, OUTPUT);
  pinMode(steering2, OUTPUT);

  pinMode(frontMotor1, OUTPUT);
  pinMode(frontMotor2, OUTPUT);

  pinMode(backMotor1, OUTPUT);
  pinMode(backMotor2, OUTPUT);

  pinMode(trigger, OUTPUT);
  pinMode(echo, INPUT);

  pinMode(LLED, OUTPUT);
  pinMode(RLED, OUTPUT);
}


void loop() {
  //test for serial
  delay(2000);
  while(true){

    int distance = detect();

    if (distance <= LIMIT){
      String direction = avoid();

      if (direction == "left"){
        left(speed3, 255, FORWARD);
        delay(1000);
      }
      else if (direction == "right"){
        right(speed3, 0, FORWARD);
        delay(1000);
      }
      else {
        reverse(speed3);
        delay(1000);
      }
    }

    else{
      forward(speed3);
      lightLED(BOTH);
    }
  }
}


void lightLED(int right, int left) {
  digitalWrite(RLED, right);
  digitalWrite(LLED, left);
}
int detect() {
  digitalWrite(trigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger, LOW);
  int time = pulseIn(echo, HIGH);
  int distance = (1.595744680851064 * time) / 100;
  return distance;
}

//creates a function to move the robot forward
//takes a variable speed to control how fast the movement goes
void forward(int speed) {

  analogWrite(steering1, 0);
  digitalWrite(steering2, LOW);

  analogWrite(frontMotor1, speed);
  digitalWrite(frontMotor2, LOW);

  analogWrite(backMotor1, speed);
  digitalWrite(backMotor2, LOW);
}

//creates a function to move right
//takes 3 variables the speed, the angle you want the wheels at up to 20,
//and the direction you want the robot to go
void right(int speed, int angle, int direction) {

  analogWrite(steering1, angle);
  digitalWrite(steering2, HIGH);

  analogWrite(frontMotor1, speed);
  digitalWrite(frontMotor2, direction);
}

//creates a funciton to move left
//takes 3 variables the speed, the angle you want the wheels at up to 20,
//and the direction you want the robot to go
void left(int speed, int angle, int direction) {

  analogWrite(steering1, angle);
  digitalWrite(steering2, LOW);

  analogWrite(frontMotor1, speed);
  digitalWrite(frontMotor2, direction);
}

//creates a function to move backwards
//takes a variable speed, and the default is to move straight
void reverse(int speed) {

  analogWrite(steering1, 0);
  digitalWrite(steering2, HIGH);

  analogWrite(frontMotor1, speed);
  digitalWrite(frontMotor2, HIGH);
}

void stop(){

  analogWrite(steering1, 0);
  digitalWrite(steering2, HIGH);

  analogWrite(frontMotor1, 0);
  digitalWrite(frontMotor2, LOW);

  analogWrite(backMotor1, 0);
  digitalWrite(backMotor2, LOW);
}

String avoid(){

  stop();
  left(speed2, 255, FORWARD);
  delay(800);
  stop();
  int reading1 = detect();
  left(speed2, 255, BACKWARD);
  delay(800);
  stop();
  delay(100);
  right(speed2, 0, FORWARD);
  delay(800);
  stop();
  int reading2 = detect();
  right(speed2, 0, BACKWARD);
  delay(800);
  stop();
  if (reading1 > reading2){
    return "left";
  }
  else if (reading1 < reading2){
    return "right";
  }
  else{
    break;
  }
}
