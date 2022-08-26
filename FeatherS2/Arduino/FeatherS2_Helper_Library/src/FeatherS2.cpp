// ---------------------------------------------------------------------------
// FeatherS2 Helper Library - v1.4 - 18/10/2019
//
// Created by Seon Rozenblum - seon@unexpectedmaker.com
//
// See "FeatherS2.h" for purpose, syntax, version history, links, and more.
//
// v1.0 - Initial Release
// ---------------------------------------------------------------------------

#include "FeatherS2.h"
#include <SPI.h>
#include "driver/adc.h"
#include "esp_adc_cal.h"


FeatherS2::FeatherS2()
{
    pinMode( DOTSTAR_PWR, OUTPUT );
    DotStar_SetPower( false );

    for (int i = 0; i < 3; i++ )
        pixel[i] = 0;

    isInit = false;
    brightness = 128;
    colorRotation = 0;
    nextRotation = 0;
}

FeatherS2::~FeatherS2()
{
    isInit = false;
    DotStar_SetPower( false );
}

void FeatherS2::DotStar_SetBrightness(uint8_t b)
{
    // Stored brightness value is different than what's passed.  This
    // optimizes the actual scaling math later, allowing a fast 8x8-bit
    // multiply and taking the MSB.  'brightness' is a uint8_t, adding 1
    // here may (intentionally) roll over...so 0 = max brightness (color
    // values are interpreted literally; no scaling), 1 = min brightness
    // (off), 255 = just below max brightness.
    brightness = b + 1;
}

// Convert separate R,G,B to packed value
uint32_t FeatherS2::Color(uint8_t r, uint8_t g, uint8_t b)
{
    return ((uint32_t)r << 16) | ((uint32_t)g << 8) | b;
}

void FeatherS2::DotStar_Show(void)
{
    if ( !isInit )
    {
        isInit = true;
        swspi_init();
        delay(10);
    }
    
    uint16_t b16 = (uint16_t)brightness; // Type-convert for fixed-point math

    // Start-frame marker
    for( int i=0; i<4; i++) swspi_out(0x00);    
    
    // Pixel start
    swspi_out(0xFF);     
    
    for( int i=0; i<3; i++)
    {
        if( brightness > 0)
            swspi_out((pixel[i] * b16) >> 8); // Scale, write - Scaling pixel brightness on output
        else
            swspi_out(pixel[i]); // R,G,B @Full brightness (no scaling) 
    }             

    // // End frame marker
    swspi_out(0xFF);  
}


void FeatherS2::swspi_out(uint8_t n)
{
    for(uint8_t i=8; i--; n <<= 1)
    {
        if (n & 0x80)
            digitalWrite(DOTSTAR_DATA, HIGH);
        else
            digitalWrite(DOTSTAR_DATA, LOW);
        digitalWrite(DOTSTAR_CLK, HIGH);
        digitalWrite(DOTSTAR_CLK, LOW);
    }
    delay(1);
}

void FeatherS2::DotStar_Clear() { // Write 0s (off) to full pixel buffer
    for (int i = 0; i < 3; i++ )
        pixel[i] = 0;

    DotStar_Show();
}

// Set pixel color, separate R,G,B values (0-255 ea.)
void FeatherS2::DotStar_SetPixelColor(uint8_t r, uint8_t g, uint8_t b)
{
    pixel[0] = b;
    pixel[1] = g;
    pixel[2] = r;

    DotStar_Show();
}

// Set pixel color, 'packed' RGB value (0x000000 - 0xFFFFFF)
void FeatherS2::DotStar_SetPixelColor(uint32_t c)
{
    pixel[0] = (uint8_t)c;
    pixel[1] = (uint8_t)(c >>  8);
    pixel[2] = (uint8_t)(c >> 16);

    DotStar_Show();
}

void FeatherS2::swspi_init(void)
{
    DotStar_SetPower( true );
    digitalWrite(DOTSTAR_DATA , LOW);
    digitalWrite(DOTSTAR_CLK, LOW);
}

void FeatherS2::swspi_end()
{
    DotStar_SetPower( false );
}

// Switch the DotStar power
void FeatherS2::DotStar_SetPower( bool state )
{
	digitalWrite( DOTSTAR_PWR, !state );
	pinMode( DOTSTAR_DATA, state ? OUTPUT : INPUT_PULLDOWN );
	pinMode( DOTSTAR_CLK, state ? OUTPUT : INPUT_PULLDOWN );
}

void FeatherS2::DotStar_CycleColor()
{
    DotStar_CycleColor(0);
}

void FeatherS2::DotStar_CycleColor( unsigned long wait = 0 )
{
    if ( millis() > nextRotation + wait )
    {
        nextRotation = millis();

        colorRotation++;
        byte WheelPos = 255 - colorRotation;
        if(WheelPos < 85)
        {
            DotStar_SetPixelColor(255 - WheelPos * 3, 0, WheelPos * 3);
        }
        else if(WheelPos < 170)
        {
            WheelPos -= 85;
            DotStar_SetPixelColor(0, WheelPos * 3, 255 - WheelPos * 3);
        }
        else
        {
            WheelPos -= 170;
            DotStar_SetPixelColor(WheelPos * 3, 255 - WheelPos * 3, 0);
        }
        DotStar_Show();
    }
}

// Tone - Sound wrapper
void FeatherS2::Tone( uint8_t pin, uint32_t freq )
{
    if ( !isToneInit )
    {
        pinMode( pin, OUTPUT);
        ledcSetup(0, freq, 8); // Channel 0, resolution 8
        ledcAttachPin( pin , 0 );
        isToneInit = true;
    }

    ledcWriteTone( 0, freq );
}

void FeatherS2::NoTone( uint8_t pin )
{
    if ( isToneInit )
    {
        ledcWriteTone(0, 0);
        pinMode( pin, INPUT_PULLDOWN);
        isToneInit = false;
    }
}
