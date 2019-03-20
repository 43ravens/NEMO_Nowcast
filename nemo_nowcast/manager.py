# Copyright 2016-2019 Doug Latornell, 43ravens

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""NEMO_Nowcast manager.
"""
import argparse
import importlib
import logging
import logging.config
import os
import pprint
import signal
import time

import attr
import requests
import yaml
import zmq
import zmq.log.handlers

from nemo_nowcast import CommandLineInterface, Config, Message


def main():
    """
    Setup and run the nowcast system manager.

    See :command:`python -m nemo_nowcast.manager --help`
    for details of the command-line interface.
    """
    mgr = NowcastManager()
    mgr.setup()
    mgr.run()


@attr.s
class NowcastManager:
    """Construct a :py:class:`nemo_nowcast.manager.NowcastManager` instance.
    """

    #: The name of the manager instance.
    #: Used in the nowcast messaging system and for logging.
    name = attr.ib(default="manager")
    #: :py:class:`nemo_nowcast.config.Config` object that holds
    #: the nowcast system configuration that is loaded from the configuration
    #: file in the :py:meth:`~nemo_nowcast.manager.NowcastManager.setup` method.
    config = attr.ib(default=attr.Factory(Config))
    #: Logger for the manager.
    #: Configured from the :kbd:`logging` section of the configuration file
    #: in the :py:meth:`~nemo_nowcast.manager.NowcastManager.setup` method .
    logger = attr.ib(default=None)
    #: Nowcast system checklist: :py:class:`dict` containing the present
    #: state of the nowcast system.
    checklist = attr.ib(default=attr.Factory(dict))
    #: :py:class:`argparse.Namespace` instance containing the arguments
    #: and option flags and values parsed from the command-line when the
    #: :py:meth:`~nemo_nowcast.manager.NowcastManager.setup` method is called.
    _parsed_args = attr.ib(default=None)
    #: The :kbd:`message registry` section of
    #: :py:attr:`~nemo_nowcast.manager.config`.
    _msg_registry = attr.ib(default=None)
    #: Worker race condition management data structure: :py:class:`dict`
    #: containing collections of workers that must all finish before
    #: another collection of workers are launched
    _race_condition_mgmt = attr.ib(default=attr.Factory(dict))
    #: Name of the Python module that contains functions to calculate
    #: lists of workers to launch after previous workers end their work.
    #: Set from the :kbd:`message registry` section of
    #: :py:attr:`~nemo_nowcast.manager.config` in the
    #: py:meth:`~nemo_nowcast.manager.NowcastManager.setup` method.
    _next_workers_module = attr.ib(default=None)
    #: :py:class:`zmq.Context` instance that provides the basis for the
    #: nowcast messaging system.
    _context = attr.ib(default=attr.Factory(zmq.Context))
    #: :py:class:`zmq.Context.socket` instance that is connected to the
    #: message broker to enable nowcast system messages to be exchanged
    #: with worker processes.
    #: Created when the
    #: py:meth:`~nemo_nowcast.manager.NowcastManager.run` method is called.
    _socket = attr.ib(default=None)

    def setup(self):
        """Set up the nowcast system manager process including:

        * Building the command-line parser, and parsing the command-line used
          to launch the manager
        * Reading and parsing the configuration file given on the command-line
        * Configuring the logging system as specified in the configuration file
        * Logging the manager's PID, and the file path/name that was used to
          configure it.
        * Importing the :py:mod:`next_workers` module specified in the
          configuration file.

        The set-up is repeated if the manager process receives a HUP signal
        so that the configuration can be re-loaded without having to stop and
        re-start the manager.
        """
        self._parsed_args = self._cli()
        self.config.load(self._parsed_args.config_file)
        self._msg_registry = self.config["message registry"]
        msg = self._configure_logging()
        self.logger.info("running in process {}".format(os.getpid()))
        self.logger.info("read config from {.file}".format(self.config))
        self.logger.info(msg)
        try:
            self._next_workers_module = importlib.import_module(
                self._msg_registry["next workers module"]
            )
        except ImportError:
            self.logger.critical(
                "could not find next workers module: {[next workers module]}".format(
                    self._msg_registry
                ),
                exc_info=True,
            )
            raise
        self.logger.info(
            "next workers module loaded from {[next workers module]}".format(
                self._msg_registry
            )
        )

    def _cli(self, args=None):
        """Configure command-line argument parser and return parsed arguments
        object.
        """
        cli = CommandLineInterface(
            self.name, package="nemo_nowcast", description=__doc__
        )
        cli.build_parser(add_help=False)
        parser = argparse.ArgumentParser(
            prog=cli.parser.prog,
            description=cli.parser.description,
            parents=[cli.parser],
        )
        parser.add_argument(
            "--ignore-checklist",
            action="store_true",
            help="""
            Don't load the serialized checklist left by a previously
            running manager instance.
            """,
        )
        return parser.parse_args(args)

    def _configure_logging(self):
        """Configure the manager's logging system interface.
        """
        self.logger = logging.getLogger(self.name)
        if "publisher" in self.config["logging"]:
            # Publish log messages to distributed logging aggregator
            logging_config = self.config["logging"]["publisher"]
            logging_config["handlers"]["zmq_pub"]["context"] = self._context
            port = self.config["zmq"]["ports"]["logging"][self.name]
            addr = "tcp://*:{port}".format(port=port)
            logging_config["handlers"]["zmq_pub"]["interface_or_socket"] = addr
            logging.config.dictConfig(logging_config)
            for handler in self.logger.root.handlers:
                if isinstance(handler, zmq.log.handlers.PUBHandler):
                    handler.root_topic = self.name
                    handler.formatters = {
                        logging.DEBUG: logging.Formatter("%(message)s\n"),
                        logging.INFO: logging.Formatter("%(message)s\n"),
                        logging.WARNING: logging.Formatter("%(message)s\n"),
                        logging.ERROR: logging.Formatter("%(message)s\n"),
                        logging.CRITICAL: logging.Formatter("%(message)s\n"),
                    }
            # Not sure why, but we need a brief pause before we start logging
            # messages
            time.sleep(1)
            msg = "publishing logging messages to {addr}".format(addr=addr)
        else:
            # Write log messages to local file system
            #
            # Replace logging RotatingFileHandlers with WatchedFileHandlers so
            # that we notice when log files are rotated and switch to writing
            # to the new ones
            logging_config = self.config["logging"]
            logging_handlers = logging_config["handlers"]
            rotating_handler = "logging.handlers.RotatingFileHandler"
            watched_handler = "logging.handlers.WatchedFileHandler"
            for handler in logging_handlers:
                if logging_handlers[handler]["class"] == rotating_handler:
                    logging_handlers[handler]["class"] = watched_handler
                    del logging_handlers[handler]["backupCount"]
            logging.config.dictConfig(logging_config)
            msg = "writing logging messages to local file system"
        return msg

    def run(self):
        """Run the nowcast system manager:

        * Create the :py:class:`zmq.Context.socket` for communication with the
          worker processes and connect it to the message broker.
        * Install signal handlers for hangup, interrupt, and kill signals.
        * Launch the manager's message processing loop
        """
        self._socket = self._context.socket(zmq.REP)
        zmq_host = self.config["zmq"]["host"]
        zmq_port = self.config["zmq"]["ports"]["manager"]
        self._socket.connect("tcp://{host}:{port}".format(host=zmq_host, port=zmq_port))
        self.logger.info(
            "connected to {host} port {port}".format(host=zmq_host, port=zmq_port)
        )
        self._install_signal_handlers(zmq_host, zmq_port)
        if not self._parsed_args.ignore_checklist:
            self._load_checklist()
        self._process_messages()

    def _install_signal_handlers(self, zmq_host, zmq_port):
        """Set up hangup, interrupt, and kill signal handlers.
        """

        def sighup_handler(signal, frame):
            self.logger.info("hangup signal (SIGHUP) received; reloading configuration")
            self._socket.disconnect(
                "tcp://{host}:{port}".format(host=zmq_host, port=zmq_port)
            )
            self.setup()
            self.run()

        signal.signal(signal.SIGHUP, sighup_handler)

        def sigint_handler(signal, frame):
            self.logger.info(
                "interrupt signal (SIGINT or Ctrl-C) received; shutting down"
            )
            self._socket.close()
            raise SystemExit

        signal.signal(signal.SIGINT, sigint_handler)

        def sigterm_handler(signal, frame):
            self.logger.info("termination signal (SIGTERM) received; shutting down")
            self._socket.close()
            raise SystemExit

        signal.signal(signal.SIGTERM, sigterm_handler)

    def _load_checklist(self):
        """Load the serialized checklist left on disk by a previously
        running manager instance.
        """
        checklist_file = self.config["checklist file"]
        try:
            with open(checklist_file, "rt") as f:
                self.checklist = yaml.safe_load(f)
                self.logger.info("checklist read from {}".format(checklist_file))
                self.logger.info(
                    "checklist:\n{}".format(pprint.pformat(self.checklist))
                )
        except FileNotFoundError:
            self.logger.warning("checklist load failed:", exc_info=True)
            self.logger.warning("running with empty checklist")

    def _process_messages(self):
        """Process messages from workers.
        """
        while True:
            self.logger.debug("listening...")
            try:
                self._try_messages()
            except zmq.ZMQError as e:
                # Fatal ZeroMQ problem
                self.logger.critical("ZMQError:", exc_info=e)
                self.logger.critical("shutting down")
                break
            except SystemExit:
                # Termination by signal
                break
            except Exception as e:
                self.logger.critical("unhandled exception:", exc_info=e)
                self.logger.critical("shutting down")

    def _try_messages(self):
        """Try to process messages.

        Extracted from the :kbd:`try:` block in :py:meth:`_process_messages`
        so that it can be tested outside of the :kbd:`while True:` loop.
        """
        message = self._socket.recv_string()
        reply, next_workers = self._message_handler(message)
        self._socket.send_string(reply)
        for worker in next_workers:
            worker.launch(self.config, self.name)

    def _message_handler(self, message):
        """Handle message from worker.
        """
        msg = Message.deserialize(message)
        if msg.source not in self._msg_registry["workers"]:
            reply = self._handle_unregistered_worker_msg(msg)
            return reply, []
        if msg.type not in self._msg_registry["workers"][msg.source]:
            reply = self._handle_unregistered_msg_type(msg)
            return reply, []
        self._log_received_msg(msg)
        if msg.type == "clear checklist":
            reply = self._clear_checklist()
            return reply, []
        if msg.type == "need":
            reply = self._handle_need_msg(msg)
            return reply, []
        reply, next_workers = self._handle_continue_msg(msg)
        return reply, next_workers

    def _handle_unregistered_worker_msg(self, msg):
        """Emit error message to log about a message received from a worker
        that is not included in the message registry.
        """
        self.logger.error(
            "message received from unregistered worker: {.source}".format(msg),
            extra={"worker_msg": msg},
        )
        reply = Message(self.name, "unregistered worker").serialize()
        return reply

    def _handle_unregistered_msg_type(self, msg):
        """Emit error message to log about a message type received from a worker
        that is not included in the message registry.
        """
        self.logger.error(
            "unregistered message type received from "
            "{0.source} worker: {0.type}".format(msg),
            extra={"worker_msg": msg},
        )
        reply = Message(self.name, "unregistered message type").serialize()
        return reply

    def _log_received_msg(self, msg):
        """Emit debug message about message received from worker.
        """
        self.logger.debug(
            "received message from {0.source}: ({0.type}) {msg_words}".format(
                msg, msg_words=self._msg_registry["workers"][msg.source][msg.type]
            ),
            extra={"worker_msg": msg},
        )

    def _handle_need_msg(self, msg):
        """Handle request for checklist section message from worker.
        """
        reply = Message(
            self.name, "ack", payload=self.checklist[msg.payload]
        ).serialize()
        return reply

    def _handle_continue_msg(self, msg):
        """Handle success, failure, or crash message from worker by generating
        list of subsequent workers to launch.
        """
        if msg.payload is not None:
            self._update_checklist(msg)
        self._slack_notification(msg)
        importlib.reload(self._next_workers_module)
        try:
            after_func = getattr(
                self._next_workers_module, "after_{worker}".format(worker=msg.source)
            )
        except AttributeError:
            self.logger.critical(
                "could not find after_{worker} in {next_workers} module".format(
                    worker=msg.source,
                    next_workers=self._msg_registry["next workers module"],
                ),
                exc_info=True,
            )
            reply = Message(self.name, "no after_worker function").serialize()
            return reply, []
        next_workers = after_func(msg, self.config, self.checklist)
        if len(next_workers) > 1 and isinstance(next_workers[-1], set):
            next_workers, self._race_condition_mgmt["must finish"] = next_workers
            self._race_condition_mgmt["then launch"] = []
            self.logger.debug(
                "race condition management activated: {._race_condition_mgmt}".format(
                    self
                )
            )
        try:
            self._race_condition_mgmt["must finish"].remove(msg.source)
            self._race_condition_mgmt["then launch"].extend(next_workers)
            next_workers.clear()
            self.logger.debug(
                "{worker} finished and race condition management updated: {race_condition_mgmt}".format(
                    worker=msg.source, race_condition_mgmt=self._race_condition_mgmt
                )
            )
        except (KeyError, ValueError):
            # No race condition management in effect, or worker not in "must finish" list
            pass
        try:
            if not self._race_condition_mgmt["must finish"]:
                next_workers = self._race_condition_mgmt["then launch"]
                self._race_condition_mgmt = {}
                self.logger.debug(
                    "race condition management ended; "
                    "next workers released: {next_workers}".format(
                        next_workers=next_workers
                    )
                )
        except KeyError:
            # No race condition management in effect
            pass
        reply = Message(self.name, "ack").serialize()
        return reply, next_workers

    def _update_checklist(self, msg):
        """Update the checklist value at worker's key with the items passed from
        the worker.

        If key is not present in the checklist, add it with the worker
        items as its value.

        Write the checklist to disk as a YAML file so that it can be
        inspected and/or recovered if the manager instance is restarted.
        """
        try:
            key = self._msg_registry["workers"][msg.source]["checklist key"]
        except KeyError:
            raise KeyError("checklist key not found for {.source} worker".format(msg))
        try:
            self.checklist[key].update(msg.payload)
        except (KeyError, AttributeError):
            self.checklist[key] = msg.payload
        self.logger.info(
            "checklist updated with [{0}] items from {1.source} worker".format(
                key, msg
            ),
            extra={"worker_msg": msg},
        )
        self._write_checklist_to_disk()

    def _write_checklist_to_disk(self):
        """Write the checklist to disk as a YAML file so that it can be
        inspected and/or recovered if the manager instance is restarted.
        """
        with open(self.config["checklist file"], "wt") as f:
            yaml.dump(self.checklist, f)

    def _slack_notification(self, msg):
        try:
            slack_notifications = self.config["slack notifications"]
        except KeyError:
            # No slack notification section in config, and that's okay!
            return
        slack_msg = {
            "text": "{worker}: {msg_type}".format(worker=msg.source, msg_type=msg.type)
        }
        try:
            slack_msg["text"] = "\n".join(
                (
                    slack_msg["text"],
                    "Log: {}".format(slack_notifications["website log url"]),
                )
            )
        except KeyError:
            # Not everyone publishes their logs and/or checklist to the web...
            pass
        try:
            slack_msg["text"] = "\n".join(
                (
                    slack_msg["text"],
                    "Checklist: {}".format(
                        slack_notifications["website checklist url"]
                    ),
                )
            )
        except KeyError:
            # Not everyone publishes their logs and/or checklist to the web...
            pass
        for key, workers in slack_notifications.items():
            if not key.startswith("SLACK"):
                continue
            slack_url_envvar = key
            try:
                slack_url = os.environ[slack_url_envvar]
            except KeyError:
                # No value found in environment
                self.logger.debug(
                    "slack notification environment variable not found: {}".format(
                        slack_url_envvar
                    )
                )
                continue
            if msg.source in workers:
                requests.post(slack_url, json=slack_msg)

    def _clear_checklist(self):
        """Write the checklist to a log file, then clear it.

        This method is called in response to a "clear checklist" message from
        the :py:mod:`nemo_nowcast.workers.clear_checklist` worker.
        That worker is typically run once per nowcast cycle (e.g. daily) at the
        end of processing, just before rotating the log files via the
        :py:mod:`nemo_nowcast.workers.rotate_logs` worker.
        """
        checklist_logger = logging.getLogger("checklist")
        if checklist_logger.handlers:
            self.logger.info("writing checklist to log file")
            for handler in checklist_logger.handlers:
                checklist_logger.log(
                    handler.level,
                    "checklist:\n{}".format(pprint.pformat(self.checklist)),
                )
                handler.close()
        self.checklist.clear()
        self._write_checklist_to_disk()
        self.logger.info("checklist cleared")
        reply = Message(self.name, "checklist cleared").serialize()
        return reply


if __name__ == "__main__":
    main()  # pragma: no cover
