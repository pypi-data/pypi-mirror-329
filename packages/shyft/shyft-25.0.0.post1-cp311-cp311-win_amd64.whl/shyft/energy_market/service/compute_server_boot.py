from shyft.energy_market import stm
import logging
import time
from shyft.energy_market.service.boot import _configure_logger, Exit

def create_server(port_num: int,
                  api_port_num: int):
    srv = stm.compute.Server()
    srv.set_listening_port(port_num)
    srv.start_server()
    return srv


def start_server(port_num: int,
                 dstm_port_num: int):
    log = logging.getLogger('')

    srv = create_server(port_num, dstm_port_num)
    log.info(f'Starting server on port {port_num}.')

    ex = Exit()

    def assoc():

        dstm_client = stm.DStmClient(f'localhost:{dstm_port_num}', 1000)
        try:
            dstm_client.add_compute_server(f'localhost:{port_num}')
            dstm_client.close()
        except Exception as e:
            log.error(f'{e}')
        del dstm_client

    while True:
        assoc()
        time.sleep(5)
        if ex.now:
            break

    log.info(f'terminating services')
    srv.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("host_port", type=int)
    parser.add_argument("dstm_port", type=int)
    args = parser.parse_args()
    start_server(args.host_port, args.dstm_port)
