# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## v2.1.0

* Add trajectory flag

## v2.0.0

* add Odrive PRO support

## v1.4.0

* add `set_rate_of_change` to mock.

## v1.3.0

* add function to get dbc path

## v1.2.0

* add `axis_id` property

## v1.1.1

* fix inspector


## v1.1.0

* add `UDP_DATA_DEST` environment variable for configuring `UDP_Client`.


## v1.0.0

* refactor can interface creation to environment variables.
    - `CAN_CHANNEL=vcan0`
    - `CAN_INTERFACE=socketcan`
* Classes now accept an instance of `can.Bus`

## v0.12.2

* avoid repeated warnings
* let can thread crash on exceptions
* switch to `pyproject.toml`

## v0.11.0


* refactor position demo.
* replace `--debug` option in cli by `LOGLEVEL=debug`  env variable.

## v0.10.0

* add `watchdog` demo.
* change linting to `ruff`
* add timeout for `set_axis_state` and `wait_for_heartbeat`
* add `wait_for_heartbeat()` - used used to get status before checking for errors.


## v0.9.2

* cancel task on stop
* add `roc` parameter to `mock`

## v0.8.0

* add `set_axis_state_no_wait`


## v0.7.0

* add amplitude parameter to `demo` code
* split udp feedback per axis
* remove polling example
* add refererence to `ODriveCAN` in `.feedback_callback`
* rename `.position_callback` to `.feedback_callback`


## v0.6.1

* Beta release
* Updated examples and docs
* Major refactoring
* Made `OdriveMock` behave realistically.



## v0.5.0

* implemented full dbc interface
* ramp velocity control demo
* position control demo with different input modes

