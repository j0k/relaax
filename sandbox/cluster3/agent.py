from __future__ import print_function

import sys
sys.path.append('../../pkg')
sys.path.append('../../server')

import argparse
import logging
import ruamel.yaml

import algorithms.a3c.agent
import algorithms.a3c.bridge
import algorithms.a3c.params
import loop.socket_loop


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--params', type=str, default=None, help='parameters YAML file')
    parser.add_argument('--bind', type=str, default=None, help='address to serve (host:port)')
    parser.add_argument('--master', type=str, default=None, help='master address (host:port)')
    parser.add_argument('--log-dir', type=str, default=None, help='TensorBoard log directory')
    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(message)s',
        level=logging.INFO
    )

    with open(args.params, 'r') as f:
        yaml = ruamel.yaml.load(f, Loader=ruamel.yaml.Loader)

    params = algorithms.a3c.params.Params(yaml)

    loop.socket_loop.run_agents(
        args.bind,
        _get_factory(
            params=params,
            master=args.master,
            log_dir=args.log_dir
        )
    )


def _get_factory(params, master, log_dir):
    return lambda n_agent: algorithms.a3c.agent.Agent(
        params=params,
        master=algorithms.a3c.bridge.MasterStub(master),
        log_dir='%s/worker_%d' % (log_dir, n_agent)
    )


if __name__ == '__main__':
    main()
