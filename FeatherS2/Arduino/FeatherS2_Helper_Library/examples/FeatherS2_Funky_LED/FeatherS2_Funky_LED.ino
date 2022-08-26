#include <FeatherS2.h>

// Initialise the FeatherS2 library
FeatherS2 fs2 = FeatherS2();

void setup()
{
  // Not used
}

void loop()
{
  // Cycle the DotStar colour every 25 milliseconds
  fs2.DotStar_CycleColor(25);

  // You can set the DotStar colour directly using r,g,b values
  // fs2.DotStar_SetPixelColor( 255, 128, 0 );

  // You can set the DotStar colour directly using a uint32_t value
  // fs2.DotStar_SetPixelColor( 0xFFC900 );

  // You can clear the DotStar too
  // fs2.DotStar_Clear();

  // To power down the DotStar for deep sleep you call this
  // fs2.DotStar_SetPower( false );
}
