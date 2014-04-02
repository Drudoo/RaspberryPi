#include "ofMain.h"
#include "testApp.h"

int main() {

	ofSetupOpenGL(1920,880,OF_WINDOW);
	ofRunApp(new testApp());

}