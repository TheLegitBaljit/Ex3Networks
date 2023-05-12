import socket
import os

ID1 = 7421
ID2 = 5669

def send_file(filename, host, port):
    file_size = os.path.getsize(filename)
    part_size = file_size // 2 if file_size % 2 == 0 else file_size // 2 + 1
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    with open(filename, 'rb') as f:
        data = f.read()
    while True:
        print("Changing CC algorithm to cubic")
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, "cubic".encode())
        # Send first half of file
        print("Sending the first half")
        s.sendall(data[:part_size])  # Changed from s.send() to s.sendall()
        print("First half size" , part_size)  # Changed from temp to part_size
        print("Waiting for authentication")
        # Receive the authentication from the server
        auth = s.recv(5)
        if auth.decode() == str(ID1 ^ ID2):
            # Send second half of file
            print("Changing CC algorithm to Reno")
            s.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, "reno".encode())
            print("Sending the second half")
            s.sendall(data[part_size:])  # Changed from s.send() to s.sendall()
            print("Second half size", len(data[part_size:]))  # Changed from temp to len(data[part_size:])
        else:
            print("Connection was cut")
            s.close()
            break

        print("File sent.")
        # Ask user if they want to send the file again
        check = s.recv(50).decode()
        if check == "again":
            send_again = input('Send file again? (y/n): ')
            if send_again.lower() != 'y':
                s.send("_done_sending_all_".encode())
                s.close()
                break
            else:
                s.send("_keep_sending_".encode())

send_file('text.txt', 'localhost', 9000)

