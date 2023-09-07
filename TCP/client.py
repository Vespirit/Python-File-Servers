import socket
import os

buffer = 1024

def c_list(sock):
    # Look for the response
    ret = sock.recv(buffer).decode()
    print(ret)

def c_push(sock, filename):
    # Check if file exists
    if not os.path.isfile(filename):
        print('Error: file does not exist.')
        return
    # Find size of the file and send it, so server knows how many times to recv
    filesize = os.stat(filename).st_size
    sock.sendall(str(filesize).encode())
    # Send the file
    with open(filename, 'rb') as file:
        data = file.read()
    sock.sendall(data)
    # Look for confirmation
    confirm = sock.recv(buffer).decode()
    print(confirm)

def c_delete(sock):
    # Look for the response
    ret = sock.recv(buffer).decode()
    print(ret)

def c_overwrite(sock):
    # Look for the response
    ret = sock.recv(buffer).decode()
    print(ret)

def main():

    host = input("IP of the host you wish to connect to: ")
    port = 5000
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (host, port)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    command = ''
    while (command != 'EXIT'):
        # Input and send commands, deal with them as necessary
        command = input("Enter a command: ")
        sock.sendall(command.encode())
        args = command.split(' ')
        if (args[0] == 'LIST'):
            c_list(sock)
        elif (args[0] == 'PUSH'):
            if (len(args) != 2):
                print('Error: incorrect usage of PUSH.')
                continue
            c_push(sock, args[1])
        elif (args[0] == 'DELETE'):
            if (len(args) != 2):
                print('Error: incorrect usage of DELETE.')
                continue
            c_delete(sock)
        elif (args[0] == 'OVERWRITE'):
            if (len(args) != 2):
                print('Error: incorrect usage of OVERWRITE.')
                continue
            c_overwrite(sock)
    # On EXIT command, break the loop and close connection
    print('Disconnected from the server!')
    sock.close()

if __name__ == '__main__':
    main()