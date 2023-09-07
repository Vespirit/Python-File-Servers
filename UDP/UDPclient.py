import socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (input("IP the server is on: "), 5000)
    y=80 # must be at least 2
    window_size = 4

    with open("client_data/file.txt", "rb") as file:
        packets = []
        chunk = file.read(y-2)
        packet_num = 0
        while chunk: # Create the packets from the file
            packets.append(packet_num.to_bytes(2, byteorder="big") + chunk)
            chunk = file.read(y-2)
            packet_num += 1
        packets.append(packet_num.to_bytes(2, byteorder="big") + b"EOF") # end of file packet
        window_start = 0
        window_end = window_start + window_size
        while window_start < len(packets): # exit loop after final packet
            for i in range(window_start, min(window_end+1, len(packets))):
                sock.sendto(packets[i], server_addr) # send packets in window
                print('PKT{} sent'.format(i))
            expected_ack = window_start # first expected ack is beginning of window
            for i in range(window_start, min(window_end+1, len(packets))): # receive acks
                try:
                    sock.settimeout(1)
                    ack_packet, _ = sock.recvfrom(y)
                    seq_num = int.from_bytes(ack_packet[:2], byteorder="big")
                    print('ACK{} received'.format(seq_num))
                    if seq_num == expected_ack+1: # correct ack returned
                        expected_ack += 1
                    if expected_ack == len(packets): # file is finished sending
                        print("file.txt successfully sent")
                        return
                except socket.timeout: # packet loss occurred
                    print('PKT{} Request Timed Out'.format(i))
                    break
            window_start = expected_ack
            window_end = min(expected_ack + window_size, len(packets))
            print('start {} end {}'.format(window_start, window_end))

if __name__ == "__main__":
    main()
