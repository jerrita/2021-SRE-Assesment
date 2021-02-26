import socket
import select
import time
import logging
from _thread import start_new_thread
import models

class ClientWorker:
    host: str
    port: int
    remote_port: int
    mode: int
    domain: str
    bufsize: int
    conn: socket.socket
    local_conn_map: "dict"
    local_conn_id_map: "dict"

    def __init__(self, host: str, port: int, remote_port: int, mode: int, domain: str='', bufsize: int=1024):
        self.host = host
        self.port = port
        self.remote_port = remote_port
        self.mode = mode
        self.domain = '' if domain is None else domain
        self.bufsize = bufsize
        self.local_conn_map = {}
        self.local_conn_id_map = {}

    def login(self, host: str, port: int, token: bytes):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.conn.connect((host, port))
        login_raw = models.LoginStruct(mode=self.mode, remote_port=self.remote_port, token=token, domain=self.domain).serialize()
        self.conn.sendall(login_raw)
        buf = b''
        while True:
            rl, _, _ = select.select([self.conn], [], [], 0.5)
            if not rl:
                continue

            got_len = len(buf)
            buf += self.conn.recv(models.LoginReplyStruct._length - got_len)
            if len(buf) >= models.LoginReplyStruct._length:
                break
        
        reply = models.LoginReplyStruct()

        reply.fill(buf[:models.LoginReplyStruct._length])

        return reply.errno

    def run(self):
        logging.debug('ClientWorker: I am running')
        start_new_thread(self.write_to_local, (), {})
        start_new_thread(self.read_from_local, (), {})

    def write_to_local(self):
        logging.debug('ClientWorker: write_to_local thread started')
        buf = b''
        local_conn = None
        while True:
            try:
                rl, wl, _ = select.select([self.conn], [], [], 0.5)
                if not rl:
                    continue

                buf += self.conn.recv(self.bufsize + models.ConnHeaderStruct._length)
                
                if buf == b'':
                    continue

                logging.debug('ClientWorker got:\n' + str(buf))
                conn_header = models.ConnHeaderStruct()
                logging.debug('ClientWorker got conn_header buffer length %d, should be %d' % (len(buf[:models.ConnHeaderStruct._length]), models.ConnHeaderStruct._length))
                conn_header.fill(buf[:models.ConnHeaderStruct._length])

                buf = buf[models.ConnHeaderStruct._length:]

                conn_id = conn_header.conn_id
                chunksize = conn_header.chunksize

                if conn_id in self.local_conn_map:
                    local_conn = self.local_conn_map[conn_id]
                else:
                    local_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    local_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
                    local_conn.connect((self.host, self.port))
                    self.local_conn_map[conn_id] = local_conn
                    self.local_conn_id_map[id(local_conn)] = conn_id
                local_conn.sendall(buf[:chunksize])

                buf = buf[chunksize:]
            except select.error:
                if local_conn is not None:
                    conn_id = self.local_conn_id_map[id(local_conn)]
                    del self.local_conn_id_map[id(local_conn)]
                    del self.local_conn_map[conn_id]
                    local_conn.shutdown(socket.SHUT_RDWR)
                    local_conn.close()
                self.conn.shutdown(socket.SHUT_RDWR)
                self.conn.close()

    def read_from_local(self):
        logging.debug('ClientWorker: read_from_local thread started')
        buf = b''
        while True:
            if not self.local_conn_map:
                time.sleep(0.5)
                continue

            rl, _, _ = select.select(list(self.local_conn_map.values()), [], [], 0.5)

            for sock in rl:
                sock: socket.socket
                buf += sock.recv(self.bufsize)

                if buf == b'':
                    continue

                logging.debug('ClientWorker read:\n' + str(buf))

                conn_id = self.local_conn_id_map[id(sock)]
                chunksize = len(buf)
                logging.debug('ClientWorker got conn_header buffer length %d, should be %d' % (len(buf[:models.ConnHeaderStruct._length]), models.ConnHeaderStruct._length))
                conn_header_raw = models.ConnHeaderStruct(conn_id, chunksize).serialize()
                self.conn.sendall(conn_header_raw + buf)

                buf = b''
                