//Code uses the ultrasonic to determine distance
//Created by Brandon
//Date: 06/12/2017

//defines the pins
const byte trigger = A0;
const byte echo = 7;

//sets up serial communications and sets up the pins as input and output
void setup() {
  Serial.begin(115200);
  pinMode(trigger, OUTPUT);
  pinMode(echo, INPUT); 
}

//code to get the distance and print it to the screen, will eventually be made into a function
void loop() {
  digitalWrite(trigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger, LOW);
  int time = pulseIn(echo, HIGH);
  int distance = (1.595744680851064 * time) / 100;
  Serial.print("Time = ");
  Serial.print(time);
  Serial.print(" Distance = ");
  Serial.println(distance);
}
