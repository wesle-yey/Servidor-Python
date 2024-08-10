from socket import *
import sys

def get_local_ip():
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error:
        return None

serverPort = 5050
SERVER = get_local_ip()
if SERVER:
    print("Endereço IP local:", SERVER)

ADDR = (SERVER, serverPort)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(ADDR)
serverSocket.listen(1)

print('Hosteando...')

while True:
    connectionSocket, addr = serverSocket.accept()
    print('CONECTADO')
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        with open(filename[1:], 'rb') as f:
            outputdata = f.read()

        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        connectionSocket.sendall(outputdata)
        connectionSocket.close()

    except IOError:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())

        connectionSocket.close()

serverSocket.close()
