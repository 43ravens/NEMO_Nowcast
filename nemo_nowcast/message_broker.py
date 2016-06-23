# Copyright 2016 Doug Latornell, 43ravens

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""NEMO_Nowcast ZeroMQ message broker.

This broker provides the static point in the nowcast messaging framework,
allowing the nowcast manager to be restarted more or less at will.
"""
import logging
import logging.config
import os
import signal

import zmq

from nemo_nowcast import lib


NAME = 'message_broker'

logger = logging.getLogger(NAME)

context = zmq.Context()


def main():
    """
    Set up and run the nowcast system messgae broker.

    Set-up includes:

    * Building the command-line parser, and parsing the command-line used
      to launch the message broker
    * Reading and parsing the configuration file given on the command-line
    * Configuring the logging system as specified in the configuration file
    * Logging the message broker's PID, and the file path/name that was used to
      configure it.

    The set-up is repeated if the message broker process receives a HUP signal
    so that the configuration can be re-loaded without having to stop and
    re-start the message broker.

    After the set-up is complete, launch the broker message queuing process.

    See :command:`python -m nowcast.message_broker -help`
    for details of the command-line interface.
    """
    parser = lib.base_arg_parser(NAME, package='nemo_nowcast',
        description=__doc__)
    parsed_args = parser.parse_args()
    config = lib.load_config(parsed_args.config_file)
    logging.config.dictConfig(config['logging'])
    logger.info('running in process {}'.format(os.getpid()))
    logger.info('read config from {.config_file}'.format(parsed_args))
    run(config)


def run(config):
    """Run the nowcast system message broker:

    * Create and bind the :py:class:`zmq.Context.socket` instances for
      communication with the manager and worker processes.
    * Install signal handlers for hangup, interrupt, and kill signals.
    * Launch the brokers message queuing process.
    """
    frontend, backend = _bind_zmq_sockets(config)
    _install_signal_handlers(frontend, backend)
    # Broker messages between workers on frontend and manager on backend
    try:
        zmq.device(zmq.QUEUE, frontend, backend)
    except zmq.ZMQError as e:
        # Fatal ZeroMQ problem
        logger.critical('ZMQError: {}'.format(e))
        logger.critical('shutting down')
    except SystemExit:
        # Termination by signal
        pass
    except Exception as e:
        logger.critical('unhandled exception:', exc_info=e)
        logger.critical('shutting down')


def _bind_zmq_sockets(config):
    """Create 0mq sockets and bind them to ports.
    """
    frontend = context.socket(zmq.ROUTER)
    backend = context.socket(zmq.DEALER)
    frontend_port = config['zmq']['ports']['frontend']
    frontend.bind('tcp://*:{}'.format(frontend_port))
    logger.info('frontend bound to port {}'.format(frontend_port))
    backend_port = config['zmq']['ports']['backend']
    backend.bind('tcp://*:{}'.format(backend_port))
    logger.info('backend bound to port {}'.format(backend_port))
    return backend, frontend


def _install_signal_handlers(frontend, backend):
    """Set up hangup, interrupt, and kill signal handlers.
    """
    def sighup_handler(signal, frame):
        logger.info(
            'hangup signal (SIGHUP) received; reloading configuration')
        frontend.close()
        backend.close()
        main()
    signal.signal(signal.SIGHUP, sighup_handler)

    def cleanup():
        frontend.close()
        backend.close()
        context.destroy()

    def sigint_handler(signal, frame):
        logger.info(
            'interrupt signal (SIGINT or Ctrl-C) received; shutting down')
        cleanup()
        raise SystemExit
    signal.signal(signal.SIGINT, sigint_handler)

    def sigterm_handler(signal, frame):
        logger.info(
            'termination signal (SIGTERM) received; shutting down')
        cleanup()
        raise SystemExit
    signal.signal(signal.SIGTERM, sigterm_handler)


if __name__ == '__main__':
    main()
