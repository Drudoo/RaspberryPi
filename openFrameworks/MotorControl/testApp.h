#pragma once

#include "ofMain.h"
#include "wiringPi.h"

class testApp : public ofBaseApp {
public:
	void setup();
	void update();
	void draw();

	void keyPressed(int key);
	void keyReleased(int key);

private:
	bool keyIsDown[255];
};