#include <Adafruit_NeoPixel.h>
#define PIN            1
#define NUMPIXELS      2

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

int delayval = 500;

void setup() {
  pixels.begin();
}

void loop() {

 for(int i=0;i<NUMPIXELS;i++){
  //pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
    pixels.setPixelColor(i, pixels.Color(0,150,0)); // Moderately bright green color.

    pixels.show(); // This sends the updated pixel color to the hardware.

    delay(delayval); // Delay for a period of time (in milliseconds).

  }
}
