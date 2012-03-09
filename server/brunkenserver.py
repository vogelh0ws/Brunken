#!/usr/bin/python -tt

from SimpleXMLRPCServer import SimpleXMLRPCServer as Server

class Brunken:
	def __init__(self, nroflights):
		self.lights = []
		for i in range(nroflights):
			self.lights.append(Light(i))
	def set_light_state(self, nr, state):
		self.lights[nr].set_state(state)
		return self.lights[nr].get_state()
	def get_light_state(self, nr):
		return self.lights[nr].get_state()
	def get_number_of_lights(self):
		return len(self.lights)
class Light:
	def __init__(self, number):
		self.number = number
		self.state  = False
	def get_number(self):
		return self.number
	def set_state(self, state):
		self.state = state
	def get_state(self):
		return self.state

#def _dispatch(self, method, params):
#	try:
#		return getattr(self, method)(*params) 
#	except (AttributeError, TypeError):
#		return None

TCP_IP = '127.0.0.1'
TCP_PORT = 29478

srv = Server((TCP_IP, TCP_PORT))

brunken = Brunken(2)

srv.register_instance(brunken)

srv.register_introspection_functions()

srv.serve_forever()
