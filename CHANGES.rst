**********
Change Log
**********

In development
==============

* Fix bug in worker.get_web_data() function that caused an infinite loop to
  start after a waited-for file was finally downloaded.

v1.1
====

* Eliminated lib module by refactoring command-line argument parseing
  functions into attr.s-decorated nemo_nowcast.cli.CommandLineInterface
  class that is available in the nemo_nowcat namespace.
* Refactored system config data structure and lib.load_config() into
  attr.s-decorated nemo_nowcast.config.Config class that is available
  in the nemo_nowcat namespace.
* Added worker and message classes & worker.get_web_data() function
  to nemo_nowcast namespace.
* Refactored message data structure, lib.serialize_message(),
  and lib.deserialize_message() functions into attr.s-decorated
  nemo_nowcast.message.Message class.
* Refactored nemo_nowcast.manager.NowcastManager and
  nemo_nowcast.worker.NowcastWorker into attr.s-decorated classes.
* Add nemo_nowcast.worker.NowcastWorker.get_web_data() function to
  robustly download content from URLs via retries with exponential backoff.
* Refactored nemo_nowcast.workers.NextWorker into attr.s-decorated class
  with launch method moved in from lib module.
* Added arrow and attrs packages as dependencies
  (available from gomss-nowcast channel on anaconda.org).
* Fix bugs that arise when scheduled workers config is missing or empty.


v1.0
====

* Add worker launch scheduler module.
* Add clear_checklist built-in worker.
* Add rotate_logs built-in worker.
* Add framework documentation.
* Add example next_workers module.
* Add ability to substitute environment variable values into nowcast
  system YAML configuration file.
* Add sleep & awaken example nowcast worker modules.


v0.3
====

* Add nowcast worker module.


v0.2
====

* Start API docs.
* Add nowcast manager module.
* Start unit test suite.
* Start Sphinx docs with package development section.
* Add message broker module.


v0.1
====

* Initial release for packaging testing.
