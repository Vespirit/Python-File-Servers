import socket
import os
import threading

buffer = 1024

def s_list(conn):
    # Get directory listing
    lst = '\n'.join(os.listdir('server_data'))
    # Send response
    if not lst:
        conn.sendall(b'Server directory is empty!')
    else:
        conn.sendall(lst.encode())

def s_push(conn, filename):
    # Receive filesize
    filesize = int(conn.recv(buffer).decode())
    data = b''
    # Compile file data over the necessary amount of buffers
    for _ in range(filesize//buffer + 1):
        data += conn.recv(buffer)
    filename = filename[filename.find('/')+1:] # remove directory from filename
    # Write to the server directory
    with open('server_data/' + filename, 'wb') as file:
        file.write(data)
    # Send confirmation
    conn.sendall(('Received the file ' + filename + '!').encode())

def s_overwrite(conn, filename):
    # Get server directory listing
    files = os.listdir('server_data')
    if (filename not in files): # Specified file not in server directory
        conn.sendall(b'File not found!')
        return
    # Overwrite text contents of the file
    with open('server_data/' + filename, 'w') as file:
        file.write("Why do they call it oven when you of in the cold food of out hot eat the food")
    # Send confirmation
    conn.sendall(('The file ' + filename + ' overwritten!').encode())

def s_delete(conn, filename):
    # Get server directory listing
    files = os.listdir('server_data')
    if (len(files) == 0): # Nothing in the server directory
        conn.sendall(b'Server directory is empty!')
        return
    if (filename not in files): # Specified file not in server directory
        conn.sendall(b'File not found!')
        return
    # Delete the file
    os.remove('server_data/' + filename)
    # Send confirmation
    conn.sendall(('The file ' + filename + ' deleted!').encode())

def handle_client(conn, addr):
    command = ''
    while (command != 'EXIT'):
        # Read the command sent by client
        command = conn.recv(buffer).decode()
        args = command.split(' ')
        # Deal with it as necessary
        if (args[0] == 'LIST'):
            s_list(conn)
        elif (args[0] == 'PUSH'):
            if (len(args) != 2):
                continue
            s_push(conn, args[1])
        elif (args[0] == 'DELETE'):
            if (len(args) != 2):
                continue
            s_delete(conn, args[1])
        elif (args[0] == 'OVERWRITE'):
            if (len(args) != 2):
                continue
            s_overwrite(conn, args[1])

    conn.close()

def main():
    host = ''
    port = 5000
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to the port
    sock.bind((host, port))
    # Listen for incoming connections
    sock.listen(5)

    while True:
        # Wait for a connection
        print('[LISTENING] Server is listening...')
        conn, addr = sock.accept()
        print('[NEW CONNECTION]', addr)
        # Designate connection to a thread
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == '__main__':
    print('[STARTING] Server is starting...')
    main()
