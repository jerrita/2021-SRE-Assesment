import socket
import os
import tqdm


separator = "<separator>"

host = "127.0.0.1"
port = 8888

buffer_size  = 16384

file_name = "1.jpg"

file_size = os.path.getsize(file_name)
#创建socket
s = socket.socket()
#连接服务器
print(f"connecting....{host}:{port}")
s.connect((host,port))
print("success!")
#发送文件名字大小 ,encode()
s.send(f"{file_name}{separator}{file_size}".encode())
#文件传输
progress = tqdm.tqdm(range(file_size),f"sending{file_name}",unit='B',unit_divisor= 1024)
with open(file_name,"rb") as f:
    for _ in progress:
        bytes_read = f.read(buffer_size)
        if not bytes_read:
            break
        s.sendall(bytes_read)
        progress.update(len(bytes_read))

s.close()