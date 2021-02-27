import socket
import os
import tqdm



server_host = "127.0.0.1"
server_port = 8888

buffer_size =  4096
separator = "<separator>"


s = socket.socket()
s.bind(("",server_port))

s.listen(5)
print(f"server is listening{server_host}{server_port}")

client_socket,address =s.accept()

print(f"client{address}connected")

received = client_socket.recv(buffer_size).decode()
file_name ,file_size  =  received.split(separator)
file_name = os.path.basename(file_name)
file_size = int(file_size)


progress = tqdm.tqdm(range(file_size),f"receiving{file_name}",unit="B",
                                    unit_divisor = 1024,unit_scale = True)

with open(file_name,"wb")as f:
    for _ in progress:
        bytes_read = client_socket.recv(buffer_size)
        if not bytes_read:
            break
        f.write(bytes_read)
        progress.update(len(bytes_read))
client_socket.close()
s.close()