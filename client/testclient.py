#!/usr/bin/python -tt

import xmlrpclib

TCP_IP = '127.0.0.1'
TCP_PORT = 29478

cli = xmlrpclib.ServerProxy('http://'+TCP_IP+':'+str(TCP_PORT))

print cli.system.listMethods()

print cli.get_number_of_lights()
print cli.get_light_state(0)
print cli.get_light_state(1)
print cli.set_light_state(1,True)
print cli.get_light_state(0)
print cli.get_light_state(1)
