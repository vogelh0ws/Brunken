#include <avr/io.h>
#include <util/delay.h>

#define BAUD 4800
#include <util/setbaud.h>
#include "uart.h"

void uart_init(void)   
{
	UBRRH = UBRRH_VALUE;
	UBRRL = UBRRL_VALUE;

#if USE_2X
	/* U2X-Modus erforderlich */
	UCSRA |= (1 << U2X);
#else
	/* U2X-Modus nicht erforderlich */
	UCSRA &= ~(1 << U2X);
#endif

	// hier weitere Initialisierungen (TX und/oder RX aktivieren, Modus setzen 
	UCSRB |= (1<<TXEN)|(1<<RXEN);                            // UART TX einschalten
	UCSRC  = (1 << UCSZ1)|(1 << UCSZ0); // Asynchron 8N1 
}

void uart_putc( unsigned char c )
{
	PORTB &= ~0x02; // enable led
	while (!(UCSRA & (1<<UDRE)))  /* warten bis Senden moeglich */
	{
	}                             

	UDR = c;                      /* sende Zeichen */
	PORTB |= 0x02; // disable led
}


/* puts ist unabhaengig vom Controllertyp */
void uart_puts( char *s )
{
	while (*s)
	{   /* so lange *s != '\0' also ungleich dem "String-Endezeichen(Terminator)" */
		uart_putc(*s);
		s++;
	}
}

unsigned char uart_getc( void )
{
	while ( !(UCSRA & (1 << RXC)) );

	return UDR;
}

void uart_echo( void )
{
	char buf;

	buf = uart_getc();

	PORTB &= ~0x02; // enable led

	uart_putc( buf );

	PORTB |= 0x02; // disable led
}


void uart_test( unsigned char tx )
{
	unsigned char rx;

	while ( !(UCSRA & (1<<UDRE)) ) // wait for empty data register
	{
	}

	UDR = tx; // send

	while ( !(UCSRA & (1 << RXC)) ) // wait for data
	{
	}

	rx = UDR; // receive

	if ( rx == tx )
		PORTB &= ~0x01;
	else 
		PORTB &= ~0x02;
	
	_delay_ms(200);
	PORTB |= 0x03;
	_delay_ms(200);
}
