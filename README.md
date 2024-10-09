# OpenSIPS Python Packages

This repository contains a collection of Python packages for OpenSIPS. These modules are designed to be as lightweight as possible and provide a simple interface for interacting with OpenSIPS.

## Features

Currently, the following packages are available:
- `mi` - can be used to execute OpenSIPS Management Interface (MI) commands.
- `event` - allows you to use OpenSIPS Event Interface subscriptions.

## Usage

1. Install the package from source code:
    
    ```bash
    git clone
    cd python-opebsips
    pip install .
    ```

2. Import the package in your Python code:

    ```python
    from opensips.mi import OpenSIPSMI, OpenSIPSMIException
    from opensips.event import OpenSIPSEvent, OpenSIPSEventException
    ```

3. Use the methods provided by the modules:

    ```python
    mi = OpenSIPSMI('http', url='http://localhost:8888/mi')
    try:
        response = mi.execute('ps')
        # do something with the response
    except OpenSIPSMIException as e:
        # handle the exception
    ```

    ```python
    mi_connector = OpenSIPSMI('http', url='http://localhost:8888/mi')
    event = OpenSIPSEvent(mi_connector, 'datagram', ip='127.0.0.1', port=50012)

    def some_callback(message):
        # do something with the message
        pass

    try:
        event.subscribe('E_PIKE_BLOCKED', some_callback)
    except OpenSIPSEventException as e:
        # handle the exception

    try:
        event.unsubscribe('E_PIKE_BLOCKED')
    except OpenSIPSEventException as e:
        # handle the exception
    ```

## Documentation

* [MI](docs/mi.md) - contains information about supported MI communication types and required parameters for each type.
* [Event Interface](docs/event.md) - lists the supported event transport protocols and provides information about the required parameters for each protocol.

## License

<!-- License source -->
[License-GPLv3]: https://www.gnu.org/licenses/gpl-3.0.en.html "GNU GPLv3"
[Logo-CC_BY]: https://i.creativecommons.org/l/by/4.0/88x31.png "Creative Common Logo"
[License-CC_BY]: https://creativecommons.org/licenses/by/4.0/legalcode "Creative Common License"

The `python-opensips` source code is licensed under the [GNU General Public License v3.0][License-GPLv3]

All documentation files (i.e. `.md` extension) are licensed under the [Creative Common License 4.0][License-CC_BY]

![Creative Common Logo][Logo-CC_BY]

© 2024 - OpenSIPS Solutions
