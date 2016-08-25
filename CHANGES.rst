**********
Change Log
**********

In development
==============

* Add lib.get_web_data() function to robustly download content from URLs
  via retries with exponential backoff.
* Refactored workers.NextWorker into attrs-decorated package with launch
  method moved in from lib module.
* Added arrow and attrs as dependencies (available from gomss-nowcast
  channel on anaconda.org).
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
