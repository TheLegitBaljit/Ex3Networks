import socket
import time
import os

ID1 = 7421
ID2 = 5669

time_pt1 = []
time_pt2 = []

file_size = os.path.getsize("text.txt")
part_size = file_size // 2 if file_size % 2 == 0 else file_size // 2 + 1


def receive_file(filename, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        while True:
            with open(filename, 'wb') as f:
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, "cubic".encode())
                # Receive first half of file
                start_time = time.time()
                data = b""
                while len(data.decode()) < part_size - 4:
                    chunk = conn.recv(2048)
                    if not chunk:
                        break
                    data += chunk
                f.write(data)
                end_time = time.time()
                print(f'Received first half in {end_time - start_time} seconds')
                time_pt1.append(end_time - start_time)

                # Send authentication:
                auth_msg = str(ID1 ^ ID2).encode()
                conn.sendall(auth_msg)

                # Receive second half of file
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, "reno".encode())
                start_time = time.time()
                data = b""
                while len(data.decode()) < part_size - 4:
                    chunk = conn.recv(2048)
                    if not chunk:
                        break
                    data += chunk
                f.write(data)
                end_time = time.time()
                print(f'Received second half in {end_time - start_time} seconds')
                time_pt2.append(end_time - start_time)

                conn.sendall("again".encode())

                is_done = conn.recv(18).decode()
                if is_done == "_done_sending_all_":
                    conn.close()
                    break

    print(time_pt1)
    print("Avg time for part 1 is: ", sum(time_pt1) / len(time_pt1))
    print(time_pt2)
    print("Avg time for part 2 is: ", sum(time_pt2) / len(time_pt2))


receive_file('received.txt', 'localhost', 9000)
