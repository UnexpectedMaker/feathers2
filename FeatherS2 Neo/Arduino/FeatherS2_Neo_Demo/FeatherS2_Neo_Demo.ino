// Unexpected Maker FeatherS2 Neo Example code
//
// Requires the following Adafruit libraries to be installed
#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>
//
#include <Fonts/TomThumb.h>

#define PIN 21
#define LED_EN 4

Adafruit_NeoMatrix matrix = Adafruit_NeoMatrix(5, 5, PIN,
  NEO_MATRIX_TOP     + NEO_MATRIX_LEFT +
  NEO_MATRIX_COLUMNS + NEO_MATRIX_PROGRESSIVE,
  NEO_GRB            + NEO_KHZ800);

const uint16_t colors[] = {
  matrix.Color(255, 0, 0), matrix.Color(0, 255, 0), matrix.Color(0, 0, 255) };

bool output = true; 
int update_period = 100;
unsigned long time_now = 0;

void setup() {

  Serial.begin(115200);

  // Set the LED POWER PIN - LDO2
  // Without this, the LEDs wil have no power.
  pinMode(LED_EN, OUTPUT);
  digitalWrite(LED_EN, output);
  
  matrix.begin();
  matrix.setTextWrap(false);
  matrix.setBrightness(20);
  matrix.setTextColor(colors[0]);
  matrix.setFont(&TomThumb);  
}

int x    = matrix.width();
int pass = 0;

void loop() {

  if(millis() - time_now > update_period)
  {
    time_now = millis();  

    matrix.fillScreen(0);
    matrix.setCursor(x, 5);
    matrix.print(F("G-DAY MATES!"));
    if(--x < -36) {
      x = matrix.width();
      if(++pass >= 3) pass = 0;
      matrix.setTextColor(colors[pass]);
    }
    matrix.show();
  }
}
