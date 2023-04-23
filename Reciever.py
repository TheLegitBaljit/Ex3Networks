import socket
import time

ID1 = 7421
ID2 = 5669

time_pt1 = []
time_pt2 = []


def receive_file(filename, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            with open(filename, 'wb') as f:
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, "cubic".encode())
                # Receive first half of file
                start_time = time.time()
                data = ""
                while True:
                    chunk = conn.recv(2000000).decode()
                    print(chunk.__sizeof__())
                    if len(chunk) <= 0:
                        break
                    data += chunk
                f.write(data.encode())
                end_time = time.time()
                print(f'Received first half in {end_time - start_time} seconds')
                time_pt1.append(end_time - start_time)

                conn, addr = s.accept()

                # Send authentication:
                conn.sendall(str(ID1 ^ ID2).encode())

                conn.close()

                conn, addr = s.accept()

                # Receive second half of file
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, "reno".encode())
                start_time = time.time()
                data = ""
                while True:
                    chunk = conn.recv(2000000).decode()
                    print(chunk.__sizeof__())
                    if len(chunk) <= 0:
                        break
                    data += chunk
                f.write(data.encode())
                end_time = time.time()
                print(f'Received second half in {end_time - start_time} seconds')
                time_pt2.append(end_time - start_time)

                conn, addr = s.accept()
                is_done = conn.recv(50).decode()
                if is_done == "_done_sending_all_":
                    break
                else:
                    conn.close()

    print(time_pt1)
    print("Avg time for part 1 is: ", sum(time_pt1) / len(time_pt1))
    print(time_pt2)
    print("Avg time for part 2 is: ", sum(time_pt2) / len(time_pt2))


receive_file('received.txt', 'localhost', 8000)
