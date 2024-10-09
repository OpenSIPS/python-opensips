# OpenSIPS Python Packages - MI

This package can be used to execute OpenSIPS Management Interface (MI) commands.

## Supported Communication Types

The following communication types are supported:
* `http` - uses the HTTP protocol to communicate with the MI interface. Requires the `url` parameter to be set.
* `datagram` - uses the UDP protocol to communicate with the MI interface. Requires the `ip` and `port` parameters to be set.
* `fifo` - uses a FIFO file to communicate with the MI interface. Requires 3 parameters: `fifo_file`, `fifo_file_fallback` and `fifo_reply_dir`.

To instantiate the `OpenSIPSMI` class, you need to provide the communication type and the required parameters in a key-value format. For example:

```python
mi = OpenSIPSMI('http', url='http://localhost:8888/mi')

# or
mi = OpenSIPSMI('datagram', ip='127.0.0.1', port=8080)

# or
mi = OpenSIPSMI('fifo', fifo_file='/tmp/opensips_fifo', fifo_file_fallback='/tmp/opensips_fifo_fallback', fifo_reply_dir='/tmp/opensips/')
```

## Methods

The `OpenSIPSMI` class provides the following methods:
* `execute` - to run an MI command and get the response. If an error occurs, an `OpenSIPSMIException` is raised.
* `valid` - to check if the MI connection is valid. Returns a tuple with a boolean value and a list of error messages.
