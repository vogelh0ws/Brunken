/* Alle Zeichen zwischen Schrägstrich-Stern 
   und Stern-Schrägstrich sind Kommentare */

// Zeilenkommentare sind ebenfalls möglich
// alle auf die beiden Schrägstriche folgenden
// Zeichen einer Zeile sind Kommentar

#include <avr/io.h>		// (1)
#include <util/delay.h>

#include "uart.h"

int main (void)
{
	int i;
	char msg[2];

	DDRB = 0xFF;			// (3)
	PORTB = 0x00;			// (4)

	DDRD = 0x7C;

	uart_init();

	_delay_ms (1000);

	PORTB = 0x03;

	PORTD = 0x20;

	while (1)
	{
		// receive UART message
		for ( i = 0; i < 2; i++ )	
		{
			while( !(UCSRA & (1 << RXC)) );
			msg[i] = UDR;
		}

		// handle message
		if ( msg[1] )
		{
			PORTB &= ~(1 << msg[0]);
		}
		else
		{
			PORTB |=  (1 << msg[0]);
		}
	}				

	/* wird nie erreicht */
	return 0;			// (8)
}

