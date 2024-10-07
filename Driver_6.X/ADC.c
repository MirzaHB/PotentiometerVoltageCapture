// Author: hassanbaig, Armin Sandhu, Kaylyn Tanton

#include "xc.h"
#include "ADC.h"

uint16_t do_ADC(void)
{
    uint16_t ADCvalue; // Variable to hold the ADC converted value from the buffer ADC1BUF0.

    AD1CON1bits.ADON = 1;   // Turn ON the ADC module.
    AD1CON1bits.FORM = 0;
    AD1CON1bits.SSRC = 7;
    AD1CON1bits.ASAM = 0;

    AD1CON2bits.VCFG = 0;
    AD1CON2bits.CSCNA = 0;
    AD1CON2bits.BUFM = 0;
    AD1CON2bits.ALTS = 0;

    AD1CON3bits.ADRC = 0;
    AD1CON3bits.SAMC = 15;

    AD1CHSbits.CH0NA = 0;
    AD1CHSbits.CH0SA = 5;
    AD1PCFG = 0;

    AD1CON1bits.SAMP = 1;   // Start sampling.

    while (AD1CON1bits.DONE == 0){} //Wait for the conversion to complete.
    ADCvalue = ADC1BUF0;  // Read the converted value from the buffer register
    AD1CON1bits.SAMP = 0; // Stop sampling
    AD1CON1bits.ADON = 0; // Turn off the ADC module 
    return (ADCvalue);    // Return the ADC result to the calling function.
}



