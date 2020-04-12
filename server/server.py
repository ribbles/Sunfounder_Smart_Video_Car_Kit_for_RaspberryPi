#!/usr/bin/env python2
import RPi.GPIO as GPIO
import video_dir
import car_dir
import motor
from socket import *
import argparse
# https://docs.python.org/2.7/library/socketserver.html
from SocketServer import TCPServer, UDPServer, BaseRequestHandler
from time import ctime 

ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']

busnum = 1          # Edit busnum to 0, if you uses Raspberry Pi 1 or 0

HOST = ''           # The variable of HOST is null, so the function bind( ) can be bound to all valid addresses.
PORT = 21567
BUFSIZ = 1024       # Size of the buffer
ADDR = (HOST, PORT)

video_dir.setup(busnum=busnum)
car_dir.setup(busnum=busnum)
motor.setup(busnum=busnum)     # Initialize the Raspberry Pi GPIO connected to the DC motor. 
video_dir.home_x_y()
car_dir.home()



def process_request(data):
	# Analyze the command received and control the car accordingly.
	if not data:
		return "cmd not understood"
	if data == ctrl_cmd[0]:
		print 'motor moving forward'
		motor.forward()
	elif data == ctrl_cmd[1]:
		print 'recv backward cmd'
		motor.backward()
	elif data == ctrl_cmd[2]:
		print 'recv left cmd'
		car_dir.turn_left()
	elif data == ctrl_cmd[3]:
		print 'recv right cmd'
		car_dir.turn_right()
	elif data == ctrl_cmd[6]:
		print 'recv home cmd'
		car_dir.home()
	elif data == ctrl_cmd[4]:
		print 'recv stop cmd'
		motor.ctrl(0)
	elif data == ctrl_cmd[5]:
		print 'read cpu temp...'
		temp = cpu_temp.read()
		tcpCliSock.send('[%s] %0.2f' % (ctime(), temp))
	elif data == ctrl_cmd[8]:
		print 'recv x+ cmd'
		video_dir.move_increase_x()
	elif data == ctrl_cmd[9]:
		print 'recv x- cmd'
		video_dir.move_decrease_x()
	elif data == ctrl_cmd[10]:
		print 'recv y+ cmd'
		video_dir.move_increase_y()
	elif data == ctrl_cmd[11]:
		print 'recv y- cmd'
		video_dir.move_decrease_y()
	elif data == ctrl_cmd[12]:
		print 'home_x_y'
		video_dir.home_x_y()
	elif data[0:5] == 'speed':     # Change the speed
		print data
		numLen = len(data) - len('speed')
		if numLen == 1 or numLen == 2 or numLen == 3:
			tmp = data[-numLen:]
			print 'tmp(str) = %s' % tmp
			spd = int(tmp)
			print 'spd(int) = %d' % spd
			if spd < 24:
				spd = 24
			motor.setSpeed(spd)
	elif data[0:5] == 'turn=':	#Turning Angle
		print 'data =', data
		angle = data.split('=')[1]
		try:
			angle = int(angle)
			car_dir.turn(angle)
		except:
			print 'Error: angle =', angle
	elif data[0:8] == 'forward=':
		print 'data =', data
		spd = data[8:]
		try:
			spd = int(spd)
			motor.forward(spd)
		except:
			print 'Error speed =', spd
	elif data[0:9] == 'backward=':
		print 'data =', data
		spd = data.split('=')[1]
		try:
			spd = int(spd)
			motor.backward(spd)
		except:
			print 'ERROR, speed =', spd
	else:
		print 'Command Error! Cannot recognize command: ' + data



class RobotHandler(BaseRequestHandler):

	def handle(self):
		print "Client {} connected....".format(self.client_address)
		try:
			while True:
				data = self.request.recv(BUFSIZ).strip()
				print "{} wrote: {}".format(self.client_address[0], data)
				self.request.sendall(process_request(data) or 'OK')
				#self.request.sendall(self.data.upper())
		except Exception as e:
			print "Connection closed from {} ({})".format(self.client_address, str(e))
			pass


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Start robot command server to listen and obey.')
	parser.add_argument('--udp', dest='udp', action='store_const', const=True, default=False, help='Listen on UDP (default TCP)')
	args = parser.parse_args()

	if args.udp:
		server = UDPServer((HOST, PORT), RobotHandler)
	else:
		server = TCPServer((HOST, PORT), RobotHandler)
	server.serve_forever()
