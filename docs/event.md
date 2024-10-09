# OpenSIPS Python Packages - Event Interface

This package can be used to subscribe to OpenSIPS Event Interface events.

## Supported backend protocols

The following event transport protocols are supported:
* `datagram` - uses either UDP or UNIX datagram to receive notifications for subscribed events. If using UDP, the `ip` and `port` parameters are required. If using UNIX datagram, the `socket_path` parameter is required.
* `stream` - uses TCP to communicate with the Event Interface. Requires the `ip` and `port` parameters to be set.

## How to use

To instantiate the `OpenSIPSEvent` class, you need to provide a MI connector, the backend protocol and the required parameters in a key-value format. Then `subscribe` and `unsubscribe` methods can be used to manage the subscriptions.

```python
mi_connector = OpenSIPSMI('http', url='http://localhost:8888/mi')
event = OpenSIPSEvent(mi_connector, 'datagram', ip='127.0.0.1', port=50012)

try:
    event.subscribe('E_PIKE_BLOCKED', some_callback)
except OpenSIPSEventException as e:
    # handle the exception

try:
    event.unsubscribe('E_PIKE_BLOCKED')
except OpenSIPSEventException as e:
    # handle the exception
```

## Subscribing

By default, the subscription will be permanent. If you want to set a timeout, you can use the `expires` parameter. The value should be an integer representing the number of seconds the subscription will be active.

## How it works

When subscribing to an event, a new thread is created to listen for notifications. The thread will call the callback function provided when an event is received. When unsubscribing, the thread will be stopped and the socket will be closed if no exceptions occur. You can also use `stop` method to stop the thread and close the socket manually.
