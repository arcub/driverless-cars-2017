#include <Servo.h>

Servo servo;

int pos = 90;
const int defPos = 90;

const int rled = 2;
const int bled = 3;
const int gled = 4;
const int yled = 5;

const int w = 119;
const int a = 97;
const int s = 115;
const int d = 100;
const int l = 108;
const int c = 99;
const int m = 109;
const int left = 44;
const int right = 46;
const int returnPosition = 47;

int count = 0;

bool lightRed = false;
bool lightBlue = false;
bool lightGreen = false;
bool lightYellow = false;

#define RED HIGH, LOW, LOW, LOW
#define BLUE LOW, HIGH, LOW, LOW
#define GREEN LOW, LOW, HIGH, LOW
#define YELLOW LOW, LOW, LOW, HIGH
#define RB HIGH, HIGH, LOW, LOW
#define RG HIGH, LOW, HIGH, LOW
#define RY HIGH, LOW, LOW, HIGH
#define BG LOW, HIGH, HIGH, LOW
#define BY LOW, HIGH, LOW, HIGH
#define GY LOW, LOW, HIGH, HIGH
#define NONE LOW, LOW, LOW, LOW

unsigned long previousMillis = 0;
const int interval = 500;

void setup() {
  Serial.begin(115200);
  pinMode(rled, OUTPUT);
  pinMode(bled, OUTPUT);
  pinMode(gled, OUTPUT);
  pinMode(yled, OUTPUT);
  
  servo.attach(22);
  servo.write(defPos);
}

void loop() {
  while(true){
    unsigned long currentMillis = millis();
    if (Serial.available() > 0){
      int request = Serial.read();
      if (request != l){
        if (request != m){
          if(request == w){
            lightLED(RED);
          }
          else if (request == a){
            lightLED(BLUE);
          }
          else if (request == s){
            lightLED(GREEN);
          }
          else if (request == d){
            lightLED(YELLOW);
          }
          else if (request == left){
            count ++;
            if (count == 5){
              count = 0;
              moveServo(true);
            }
          }
          else if (request == right){
            count ++;
            if (count == 5){
              count = 0;
              moveServo(false);
            }
          }
          else if (request == returnPosition){
            returnServo();
          }
        }
      }
    }
    lightLED(NONE);
  }
}

void moveServo(bool movement){
  if (movement == true){
    if (pos < 160){
      pos += 1;
    }
    else {
      pos = 160;
    }
    servo.write(pos);
  }
  else {
    if (pos > 20){
      pos -= 1;
    }
    else {
      pos = 20;
    }
    servo.write(pos);
  }
  delay(10);
}

void returnServo(){
  if (pos < defPos){
    for (pos; pos <= defPos; pos++){
      servo.write(pos);
    }
  }
  else {
    for (pos; pos >= defPos; pos--){
      servo.write(pos);
    }
  }
}

void lightLED(int red, int blue, int green, int yellow){
  digitalWrite(rled, red);
  digitalWrite(bled, blue);
  digitalWrite(gled, green);
  digitalWrite(yled, yellow);
}

