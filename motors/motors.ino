-//Land rover code for the arduino
//sets up the motors for movement and allows for pre-programmed paths to be made
//Created by Brandon
//Date: 06/12/2017

#include "pitches.h"

int melody[] = {
  NOTE_C5, NOTE_D5, NOTE_E5, NOTE_G5, NOTE_A5, NOTE_B5,NOTE_C6};
int duration = 500;

//initialise the buzzer
const int buzzer = 2;

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
const int speed1 = 40; //below 40 the robot either doesnt move or moves at an incredibly slow speed
const int speed2 = 70;
const int speed3 = 150;
const int speed4 = 255;

const int trigger = A0;
const int echo = 7;

const int LLED = 8;
const int RLED = 12;

#define LEFT LOW, HIGH
#define RIGHT HIGH, LOW
#define BOTH HIGH, HIGH
#define NONE LOW, LOW

//define 2 directions for the turns
#define FORWARD LOW
#define BACKWARD HIGH

const int w = 119;
const int a = 97;
const int s = 115;
const int d = 100;
const int q = 113;
const int e = 101;
const int x = 120;
const int b = 98;

void setup() {

  Serial.begin(115200);

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

  pinMode(buzzer, OUTPUT);
}


void loop() {

  while (true){
    if (Serial.available() > 0){
      int request = Serial.read();
      Serial.print(request);
      switch (request) {
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

void soundBuzzer(){
  tone(buzzer, NOTE_D5, duration);
}

void soundHorn(){
  for (int thisNote = 0; thisNote < 8; thisNote++){
    tone(buzzer, melody[thisNote], duration);
    delay(1);
  }
}

//creates a function to move the robot forward
//takes a variable speed to control how fast the movement goes
void forward(int speed) {
  analogWrite(frontMotor1, speed);
  digitalWrite(frontMotor2, LOW);
}

void stopMovement() {

  analogWrite(steering1, 0);
  digitalWrite(steering2, LOW);

  analogWrite(frontMotor1, 0);
  digitalWrite(frontMotor2, LOW);

  analogWrite(backMotor1, 0);
  digitalWrite(backMotor2, LOW);
}

//creates a function to turn
//takes value from 0-255 to move and a bool to go left LOW, right HIGH 
void steer(int value, bool turn) {
  
  analogWrite(steering1, value);
  digitalWrite(steering2, turn);

}


//creates a function to move backwards
//
void reverse(int speed) {

  analogWrite(frontMotor1, speed);
  digitalWrite(frontMotor2, HIGH);
}

