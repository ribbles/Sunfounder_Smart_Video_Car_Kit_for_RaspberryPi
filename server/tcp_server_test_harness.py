#!/usr/bin/env python
from socket import *
from time import ctime          # Import necessary modules

ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop',
            'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']

busnum = 1          # Edit busnum to 0, if you uses Raspberry Pi 1 or 0

# The variable of HOST is null, so the function bind( ) can be bound to all valid addresses.
HOST = '127.0.0.1'
PORT = 21567
BUFSIZ = 1500       # Size of the buffer
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)    # Create a socket.
tcpSerSock.bind(ADDR)    # Bind the IP address and port number of the server.
# The parameter of listen() defines the number of connections permitted at one time. Once the
tcpSerSock.listen(5)
# connections are full, others will be rejected.


while True:
    print('Waiting for connection on', HOST, PORT)
    # Waiting for connection. Once receiving a connection, the function accept() returns a separate
    # client socket for the subsequent communication. By default, the function accept() is a blocking
    # one, which means it is suspended before the connection comes.
    tcpCliSock, addr = tcpSerSock.accept()
    # print(the IP address of the client connected with the server.
    print('...connected from :', addr)

    while True:
        # Receive data sent from the client.
        data = tcpCliSock.recv(BUFSIZ).strip()
        # Analyze the command received and control the car accordingly.
        if not data:
            break
        if data == ctrl_cmd[0]:
            print('motor moving forward')
        elif data == ctrl_cmd[1]:
            print('recv backward cmd')
        elif data == ctrl_cmd[2]:
            print('recv left cmd')
        elif data == ctrl_cmd[3]:
            print('recv right cmd')
        elif data == ctrl_cmd[6]:
            print('recv home cmd')
        elif data == ctrl_cmd[4]:
            print('recv stop cmd')
        elif data == ctrl_cmd[5]:
            print('read cpu temp...')
            temp = 32
            tcpCliSock.send('[%s] %0.2f' % (ctime(), temp))
        elif data == ctrl_cmd[8]:
            print('recv x+ cmd')
        elif data == ctrl_cmd[9]:
            print('recv x- cmd')
        elif data == ctrl_cmd[10]:
            print('recv y+ cmd')
        elif data == ctrl_cmd[11]:
            print('recv y- cmd')
        elif data == ctrl_cmd[12]:
            print('home_x_y')
        elif data[0:5] == 'speed':     # Change the speed
            print(data)
            numLen = len(data) - len('speed')
            if numLen == 1 or numLen == 2 or numLen == 3:
                tmp = data[-numLen:]
                print('tmp(str) = %s' % tmp)
                spd = int(tmp)
                print('spd(int) = %d' % spd)
                if spd < 24:
                    spd = 24
        elif data[0:5] == 'turn=':  # Turning Angle
            print('data =', data)
            angle = data.split('=')[1]
            try:
                angle = int(angle)
            except:
                print('Error: angle =', angle)
        elif data[0:8] == 'forward=':
            print('data =', data)
            spd = data[8:]
            try:
                spd = int(spd)
            except:
                print('Error speed =', spd)
        elif data[0:9] == 'backward=':
            print('data =', data
            spd = data.split('=')[1]
            try:
                spd = int(spd)
            except:
                print('ERROR, speed =', spd)

        else:
            print('Command Error! Cannot recognize command: ' + data)

tcpSerSock.close()
