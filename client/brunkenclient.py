#!/usr/bin/python -tt

# where to make connection between lightbutton and light
# how to implement tcp messages/protocol 
#	-> twisted, struct, protobuf


from gi.repository import GdkX11, Gtk, Gdk
import gst, socket, xmlrpclib

TCP_IP = "localhost"
TCP_PORT =  29478

class BrunkenClient:
	def __init__(self, nroflights):
		self.connected = False
		self.lights = []
		for i in range(nroflights):
			self.lights.append(Light(i))

	def connect(self):
		self.cli = xmlrpclib.ServerProxy('http://'+TCP_IP+':'+str(TCP_PORT))
		
		# send status request
		# receive status request
		# set light status
		for light in self.lights:
			self.set_light_state(light.get_number(), self.cli.get_light_state(light.get_number()))

	def set_light_state(self, nr, state):
		self.lights[nr].set_state(self.cli.set_light_state(nr, state))
	def get_light_state(self, nr):
		return self.lights[nr].get_state()
	def toggle_light(self, nr):
		if self.lights[nr].get_state() == True:
			self.set_light_state(nr, False)
		else:
			self.set_light_state(nr, True)

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


class LogWindow(Gtk.ScrolledWindow):

	def __init__(self):
		Gtk.ScrolledWindow.__init__(self)
		self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.ALWAYS)
		
		self.logtext = Gtk.TextView(editable=False)
		self.add(self.logtext)

	def print_(self, text):
		print "Log:	", text,
		textbuffer = self.logtext.get_buffer()
		textbuffer.insert(textbuffer.get_end_iter(), text)
		self.scroll_to_end()

	# don't know if this is a good way
	def scroll_to_end(self): 
		textbuffer = self.logtext.get_buffer()
		insert_mark = textbuffer.get_insert()
		textbuffer.place_cursor(textbuffer.get_end_iter())
		self.logtext.scroll_to_mark(insert_mark , 0.0, True, 0.0, 1.0)


class MyWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Brunken")
		self.set_default_size(640,480)
		self.set_border_width(20)

		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		self.add(vbox)

		hbox = Gtk.Box(spacing=10)
		vbox.pack_start(hbox, True, True, 0)

		# box containing toggle switches
		togglebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
		hbox.pack_start(togglebox, False, False, 0)

		self.light1 = Gtk.ToggleButton("Licht 1")
		self.light1.connect("toggled", self.on_light_toggled )
		togglebox.pack_start(self.light1, False, False, 0)
	
		self.light2 = Gtk.ToggleButton("Licht 2")
		self.light2.connect("toggled", self.on_light_toggled )
		togglebox.pack_start(self.light2, False, False, 0)

		# video
		self.videow = Gtk.DrawingArea()
		hbox.pack_start(self.videow, True, True, 0)

		# box containing main control 
		sysbox = Gtk.Box(spacing=10)
		vbox.pack_start(sysbox, False, False, 0)
		
		# log window
		self.log = LogWindow()
		sysbox.pack_start(self.log, True, True, 0)
		self.log.print_("Brunken up and running...\n")


		# control buttons
		controlbut = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=5)
		sysbox.pack_start(controlbut, False, False, 0)

		quitb = Gtk.Button("Quit")
		quitb.connect("clicked", Gtk.main_quit)
		controlbut.pack_end(quitb, False, False, 0)
		
		connectbutton = Gtk.Button(label="Connect")
		connectbutton.set_property("width-request", 100)
		connectbutton.connect("clicked", self.on_connect_disconnect)
		controlbut.pack_end(connectbutton, False, False, 0)

		# gstreamer business
		self.player = gst.element_factory_make("playbin2", "player")
		#self.player = gst.parse_launch ("tcpclientsrc host=127.0.0.1 port=8080 ! autovideosink")
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)

	def on_light_toggled(self, button):
		if self.brunken.connected:
			if button.get_label() == "Licht 1":
				self.brunken.toggle_light(0)
			elif button.get_label() == "Licht 2":
				self.brunken.toggle_light(1)

	def on_connect_disconnect(self, button):
		if button.get_label() == "Connect":
			button.set_label("Disconnect")

			self.brunken = BrunkenClient(2)
			self.brunken.connect()
			self.light1.set_active(self.brunken.get_light_state(0))
			self.light2.set_active(self.brunken.get_light_state(1))
			self.brunken.connected = True

			self.player.set_property("uri", "http://127.0.0.1:29479")
			self.player.set_state(gst.STATE_PLAYING)
		else:
			self.player.set_state(gst.STATE_NULL)
			button.set_label("Connect")

	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_ERROR:
			self.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
		
	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
			
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", True)
			Gdk.threads_enter()
			imagesink.set_xwindow_id(self.videow.get_property('window').get_xid())
			Gdk.threads_leave()
	
win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gdk.threads_init()
Gtk.main()
