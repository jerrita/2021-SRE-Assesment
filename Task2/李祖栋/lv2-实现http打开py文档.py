# 实现简单的http的服务器
import socket
import re

# 解析用户的请求
def tackle_request(request_info):
    request_lines = request_info.splitlines()
    print(">>"*20)
    print(request_lines)
    print(">>"*20)
    # GET /index.html HTTP/1.1
    if request_lines:
        ret = re.match(r"[^/]+([^ ]*)",request_lines[0])
        if ret:
            file_name = ret.group(1)
            print("***"*20,file_name)
            return file_name
    return ""

def server_service(client_socket,client_addr):
    # 接受客户端发送过来的请求
    # GET /index.html HTTP/1.1......
    request_info = client_socket.recv(1024).decode("utf-8")
#    print(">>>"*50)
#    print(request_info)
#    print(">>>"*50)
    file_name = tackle_request(request_info)

    # 发送对应的数据
    try:
        f = open("./python-3.6.12-docs-html"+file_name,"rb")
    except:
        respond_info = "HTTP/1.1 404 NOT FOUND \r\n"
        respond_info += "\r\n"
        respond_info += "----------file not found------------"
        # 发送数据
        client_socket.send(respond_info.encode("utf-8"))
    # 准备发送数据
    else:
        html_content = f.read()
        f.close()
        respond_info = "HTTP/1.1 200 OK\r\n"
        respond_info += "\r\n"
        # 将内容发送给浏览器
        client_socket.send(respond_info.encode("utf-8"))
        client_socket.send(html_content)


def main():
    # 创建套接字
    tcp_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
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
