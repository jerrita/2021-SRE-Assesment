import hashlib
import logging
import argparse
from _thread import start_new_thread
import server
import utils
import models

CRITICAL_KEYS = {
    "port": int,
}

parser = argparse.ArgumentParser(description="netfwd client")
parser.add_argument('-c', '--config', help='specify config path', default='config.yml')

def main(args):
    logging.basicConfig(level=logging.INFO)

    config = utils.parse_yaml(args.config)
    assert config, 'without config I cannot do anything!'

    if config.get('debug'):
        logging.basicConfig(level=logging.DEBUG)

    port = int(config['port'])
    assert port > 0 and port < 65536, 'port must be in range (0, 65535]'

    host = config.get('host', '0.0.0.0')

    tokens = config.get('tokens', [])

    valid_tokens = []
    for token in tokens:
        data = hashlib.md5(token.encode('utf-8')).digest()
        valid_tokens.append(data)

    loopserver = server.LoopServer(port, host, valid_tokens=valid_tokens, bufsize=config.get('bufsize', 1024))
    loopserver.run()

if __name__ == "__main__":
    main(parser.parse_args())