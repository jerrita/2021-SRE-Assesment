import multiprocessing
import time
import logging
import utils
from _thread import start_new_thread
from client.static import static_http_server
from client.worker import ClientWorker

def mainloop(server: str, port: int, token: bytes, worker_args: dict):
    if worker_args['static']:
        worker_args['host'] = '127.0.0.1'
        worker_args['port'] = utils.get_free_port()
        start_new_thread(static_http_server, (str(worker_args['static']), worker_args['port'], worker_args['host']))
    worker = ClientWorker(host=worker_args.get('host'), port=worker_args.get('port'), remote_port=worker_args.get('remote_port'), mode=worker_args.get('mode'), domain=worker_args.get('domain', ''), bufsize=worker_args.get('bufsize', 1024))
    for i in range(0, 3):
        errno = worker.login(server, port, token)
        logging.debug('mainloop login, errno ' + str(errno))
        if errno != 0:
            if i == 2:
                logging.error('login failure times exceeded!')
                return
            else:
                logging.warn("login failure: %d, retrying..." % errno)
                time.sleep(3)
        else:
            break
    worker.run()
    while True:
        pass

def new_proc(server: str, port: int, token: bytes, args: dict, ):
    p = multiprocessing.Process(target=mainloop,args=(server, port, token, args))
    p.start()
    return p