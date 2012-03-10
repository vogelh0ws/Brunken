#!/usr/bin/python -tt

import xmlrpclib, time

TCP_IP = '127.0.0.1'
TCP_PORT = 29478

def show_state(client):
	print 'Light 1: '+client.get_light_state(0)
	print 'Light 2: '+client.get_light_state(1)

cli = xmlrpclib.ServerProxy('http://'+TCP_IP+':'+str(TCP_PORT))

print cli.system.listMethods()

while(1):
	print cli.set_light_state(0,False)
	print cli.set_light_state(1,True)
	time.sleep(1)
	print cli.set_light_state(0,True)
	print cli.set_light_state(1,False)
	time.sleep(1)

