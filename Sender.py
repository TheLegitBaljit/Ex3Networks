import socket
import os

ID1 = 7421
ID2 = 5669


def send_file(filename, host, port):
    file_size = os.path.getsize(filename)
    part_size = file_size // 2
    with open(filename, 'rb') as f:
        data = f.read()
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, "cubic".encode())
        # Send first half of file
        s.sendall(data[:part_size])
        s.close()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        # Receive the authentication from the server
        auth = s.recv(5)
        if auth.decode() == str(ID1 ^ ID2):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            # Send second half of file
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, "reno".encode())
            s.sendall(data[part_size:])
            s.close()
        else:
            s.close()
            print("Connection was cut")
            break
        # Ask user if they want to send the file again
        send_again = input('Send file again? (y/n): ')
        if send_again.lower() != 'y':
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.sendall("_done_sending_all_".encode())
            s.close()
            break
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.sendall("_keep_sending_".encode())
            s.close()


send_file('text.txt', 'localhost', 8000)
