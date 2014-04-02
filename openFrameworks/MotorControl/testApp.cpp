#include "testApp.h"

#define ENA1 0
#define ENA2 3
#define IN1 1
#define IN2 2
#define IN3 4
#define IN4 5

void testApp::setup() {
	if (wiringPiSetup() == -1) {
		cout << "Error on wiringPi setup" << endl;
	} else {
		pinMode(ENA1, OUTPUT);
		pinMode(ENA2, OUTPUT);
		pinMode(IN1, OUTPUT);
		pinMode(IN2, OUTPUT);
		pinMode(IN3, OUTPUT);
		pinMode(IN4, OUTPUT);
	}
}

void testApp::update() {
	if (keyIsDown[356]) { //LEFT KEY
		digitalWrite(ENA1,HIGH);
		digitalWrite(IN1,HIGH);
		digitalWrite(IN2,LOW);

		digitalWrite(ENA2,HIGH);
		digitalWrite(IN3,LOW);
		digitalWrite(IN4,HIGH);
	} else if (keyIsDown[357]) { //UP KEY
		digitalWrite(ENA1,HIGH);
		digitalWrite(IN1,HIGH);
		digitalWrite(IN2,LOW);

		digitalWrite(ENA2,HIGH);
		digitalWrite(IN3,HIGH);
		digitalWrite(IN4,LOW);
	} else if (keyIsDown[358]) { //RIGHT KEY
		digitalWrite(ENA1,HIGH);
		digitalWrite(IN1,LOW);
		digitalWrite(IN2,HIGH);

		digitalWrite(ENA2,HIGH);
		digitalWrite(IN3,HIGH);
		digitalWrite(IN4,LOW);
	} else if (keyIsDown[359]) { //DOWN KEY
		digitalWrite(ENA1,HIGH);
		digitalWrite(IN1,LOW);
		digitalWrite(IN2,HIGH);

		digitalWrite(ENA2,HIGH);
		digitalWrite(IN3,LOW);
		digitalWrite(IN4,HIGH);
	} else {
		digitalWrite(ENA1,LOW);
		digitalWrite(IN1,LOW);
		digitalWrite(IN2,LOW);

		digitalWrite(ENA2,LOW);
		digitalWrite(IN3, LOW);
		digitalWrite(IN4,LOW);
	}
}

void testApp::draw() {

}

void testApp::keyPressed(int key) {
	if (key==356||key==357||key==358||key==359) {
		keyIsDown[key] = true;
	}
}

void testApp::keyReleased(int key) {
	if (key==356||key==357||key==358||key==359) {
		keyIsDown[key] = false;
	}
}