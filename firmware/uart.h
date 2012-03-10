#ifndef _UART_H
#define _UART_H

void uart_init( void );

void uart_putc( unsigned char c );

void uart_puts( char *s );

unsigned char uart_getc( void );

void uart_echo( void );

void uart_test(unsigned char tx);

#endif /* !_UART_H */
