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

    or from PyPI:

    ```bash
    pip install opensips
    ```

2. Import the package in your Python code:

    ```python
    from opensips.mi import OpenSIPSMI, OpenSIPSMIException
    from opensips.event import OpenSIPSEvent, OpenSIPSEventException, OpenSIPSEventHandler
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
    hdl = OpenSIPSEventHandler(mi_connector, 'datagram', ip='127.0.0.1', port=50012)

    def some_callback(message):
        # do something with the message (it is a JSON object)
        pass
    
    ev: OpenSIPSEvent = None
    try:
        event = hdl.subscribe('E_PIKE_BLOCKED', some_callback)
    except OpenSIPSEventException as e:
        # handle the exception

    try:
        ev.unsubscribe('E_PIKE_BLOCKED')
    except OpenSIPSEventException as e:
        # handle the exception
    ```

## Documentation

* [MI](docs/mi.md) - contains information about supported MI communication types and required parameters for each type.
* [Event Interface](docs/event.md) - lists the supported event transport protocols and provides information about the required parameters for each protocol.

## Scripts
### MI
After installing the package, you can use the provided [opensips-mi](opensips/mi/__main__.py) script to run MI commands. This script takes the following arguments:
- `-t` or `--type` - the type of the MI communication (`http`, `datagram` or `fifo`).
- `-i` or `--ip` - the IP address of the OpenSIPS server.
- `-p` or `--port` - the port of the OpenSIPS MI.
- `-f` or `--fifo-file` - the path to the FIFO file.
- `-fb` or `--fifo-fallback` - the path to the FIFO fallback file.
- `-fd` or `--fifo-reply-dir` - the directory where the FIFO reply files are stored.

#### Usage
```bash
# general usage
opensips-mi -t datagram -p 8080 command_name [command_args ...]

# this will execute get_statistics command
opensips-mi -t datagram -p 8080 -s core: shmem:

# you can pass json string as argument with -j flag for commands that require arrays as arguments
opensips-mi -t datagram -p 8080 get_statistics -j "{'statistics': ['core:', 'shmem:']}"
```

### Event
You can use the provided [opensips-event](opensips/event/__main__.py) script to subscribe for OpenSIPS events. This script takes the following arguments:
- all the above arguments for the MI communication
- `-T` or `--transport` - the transport protocol to use (`datagram`, `stream`).
- `-li` or `--listen-ip` - the IP address to listen on.
- `-lp` or `--listen-port` - the port to listen on.
- `-e` or `--expire` - the expiration time for the subscription.
- the event name to subscribe for.

#### Usage
```bash
opensips-event -t datagram -p 8080 -T datagram -lp 50012 -e 3600 E_PIKE_BLOCKED
```

## License

<!-- License source -->
[License-GPLv3]: https://www.gnu.org/licenses/gpl-3.0.en.html "GNU GPLv3"
[Logo-CC_BY]: https://i.creativecommons.org/l/by/4.0/88x31.png "Creative Common Logo"
[License-CC_BY]: https://creativecommons.org/licenses/by/4.0/legalcode "Creative Common License"

The `python-opensips` source code is licensed under the [GNU General Public License v3.0][License-GPLv3]

All documentation files (i.e. `.md` extension) are licensed under the [Creative Common License 4.0][License-CC_BY]

![Creative Common Logo][Logo-CC_BY]

© 2024 - OpenSIPS Solutions
