//Code to control the LEDs on the land rover
//Created by Brandon
//Date: 06/12/2017

//sets up the LED pins
const byte LLED = 8;
const byte RLED = 12;

//defines 4 different states for the LEDs
#define LEFT LOW, HIGH
#define RIGHT HIGH, LOW
#define BOTH HIGH, HIGH
#define NONE LOW, LOW

void setup() {
  //initializes the pin Modes
  pinMode(LLED, OUTPUT);
  pinMode(RLED, OUTPUT);
}

//example code for displaying the LEDS
void loop() {
  lightLED(LEFT);
  delay(100);
  lightLED(RIGHT);
  delay(100);
  lightLED(BOTH);
  delay(100);
  lightLED(NONE);
  delay(100);
}

//creates function to light the LEDs
void lightLED(int right, int left){
  digitalWrite(RLED, right);
  digitalWrite(LLED, left);
}

