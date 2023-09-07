import socket
import random

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("localhost", 5000))
    y=80 # must be at least 2

    with open('server_data/file.txt', "wb") as file:
        expected_packet = 1
        while True: # constantly listen for incoming packets
            packet, client_address = sock.recvfrom(y)
            if random.randint(1, 10) < 4: # random chance of packet loss
                continue
            seq_num = int.from_bytes(packet[:2], byteorder="big") # seq_num is first 2 bytes of packet
            print("Got PKT{}, expected {}".format(seq_num, expected_packet))
            if seq_num == expected_packet:
                if packet[2:] == b"EOF": # end of file reached: file received
                    break
                file.write(packet[2:]) # append the payload to the file
                expected_packet += 1
            ack_packet = seq_num.to_bytes(2, byteorder="big") + b"ACK"
            sock.sendto(ack_packet, client_address) # send back acknowledgement
            print('ACK{} sent'.format(seq_num))
    print("file.txt successfully received")

if __name__ == "__main__":
    main()
