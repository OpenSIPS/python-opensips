# OpenSIPS Python Packages - Event Interface

This package can be used to subscribe to OpenSIPS events.

## Supported backend protocols

The following event transport protocols are supported:
* `datagram` (Default) - uses either UDP or UNIX datagram to receive notifications for subscribed events. By default, the UDP protocol is used with the `ip` and `port` parameters set to `0.0.0.0` and `0` (any available port) respectively, but you can tune them to your needs.
To use the UNIX datagram, set the `socket_path` parameter.
* `stream` - uses TCP to communicate with the Event Interface. Default values for `ip` and `port` are `0.0.0.0` and `0` (any available port) respectively, but you can change them as needed.

## How to use

To subscribe to events, you must instantiate an `OpenSIPSEventHandler`. This class can be used to subscribe and unsubscribe from events. It uses an `OpenSIPSMI` object to communicate with the OpenSIPS MI interface. By default, a MI connector is created with the `fifo` type, but you can set it as a parameter in the constructor. As said before, the default transport protocol is `datagram`, but you can change it by setting the `_type` parameter.

Next step is to create an `OpenSIPSEvent` object. This can be done by calling the `subscribe` method of the `OpenSIPSEventHandler` object or by creating an `OpenSIPSEvent` object directly. The `subscribe` method will return an `OpenSIPSEvent` object.

To unsubscribe from an event, you can call the `unsubscribe` method of the `OpenSIPSEvent` object or the `unsubscribe` method of the `OpenSIPSEventHandler` object.

```python
from opensips.mi import OpenSIPSMI, OpenSIPSMIException
from opensips.event import OpenSIPSEvent, OpenSIPSEventException

# simple way
hdl = OpenSIPSEventHandler()

# tuned way
mi_connector = OpenSIPSMI('http', url='http://localhost:8888/mi')
hdl = OpenSIPSEventHandler(mi_connector, 'datagram', ip='127.0.0.1', port=50012)

try:
    ev = hdl.subscribe('E_PIKE_BLOCKED', some_callback)
except OpenSIPSEventException as e:
    # handle the exception

# or create an OpenSIPSEvent object directly
ev = OpenSIPSEvent(hdl, 'E_PIKE_BLOCKED', some_callback)

try:
    ev.unsubscribe()
    # or
    hdl.unsubscribe('E_PIKE_BLOCKED')
except OpenSIPSEventException as e:
    # handle the exception
```

If `callback` function is called with `None` as a parameter, it means that there was an error while receiving the event and no JSON object could be parsed from the received data after 10 retries.

## Subscribing

By default, the subscription will be permanent. If you want to set a timeout, you can use the `expires` parameter. The value should be an integer representing the number of seconds the subscription will be active.

## How it works

When subscribing to an event, a new thread is created to listen for notifications. The thread will call the callback function provided when an event is received. When unsubscribing, the thread will be stopped and the socket will be closed if no exceptions occur. You can also use `stop` method to stop the thread and close the socket manually.
