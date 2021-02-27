# 实现简单的http的服务器
import socket

def server_service(client_socket,client_addr):
    # 接受客户端发送过来的请求
    # GET / HTTP/1.1......
    request_info = client_socket.recv(1024).decode("utf-8")
    print("客户端的请求:"+request_info)
    # 准备发送数据
    respond_info = "HTTP/1.1/ 200 OK\r\n"
    respond_info += "\r\n"
    # 模拟服务器发送的数据
    respond_info += "hahahha"
    # 发送数据
    client_socket.send(respond_info.encode("utf-8"))
def main():
    # 创建套接字
    tcp_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # 绑定本地ip
    tcp_server.bind(("",7890))
    # 设置为被动模式(listen)
    tcp_server.listen(128)  # 128代表

    while True:
        # 等待连接(accept),这里会堵塞直到有第一个客户端连接
        print("----waiting for connect----")
        client_socket,client_addr = tcp_server.accept()
        print("----finish connect----")
        # print(client_addr)
        # 发送数据给客户端
        server_service(client_socket,client_addr)  # 发送套接字
        # 关闭套接字
        client_socket.close()
    tcp_server.close()

if __name__ == "__main__":
    main()
