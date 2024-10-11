#!/usr/bin/env python
##
## This file is part of the OpenSIPS Python Package
## (see https://github.com/OpenSIPS/python-opensips).
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.
##

""" OpenSIPS Event script """

import sys
import json
import time
import signal
import argparse
from opensips.mi import OpenSIPSMI
from opensips.event import OpenSIPSEvent, OpenSIPSEventException

parser = argparse.ArgumentParser()

communication = parser.add_argument_group('communication')

communication.add_argument('-t', '--type',
                    type=str,
                    default='fifo',
                    choices=['fifo', 'http', 'datagram'],
                    help='OpenSIPS MI Communication Type')
communication.add_argument('-i', '--ip',
                    type=str,
                    help='OpenSIPS MI IP Address',
                    default='127.0.0.1')
communication.add_argument('-p', '--port',
                    type=int,
                    help='OpenSIPS MI Port',
                    default=8888)
communication.add_argument('-f', '--fifo-file',
                    metavar='FIFO_FILE',
                    type=str,
                    help='OpenSIPS MI FIFO File')
communication.add_argument('-fb', '--fifo-fallback',
                    metavar='FIFO_FALLBACK_FILE',
                    type=str,
                    help='OpenSIPS MI Fallback FIFO File')
communication.add_argument('-fd', '--fifo-reply-dir',
                    metavar='FIFO_DIR',
                    type=str,
                    help='OpenSIPS MI FIFO Reply Directory')

event = parser.add_argument_group('event')

event.add_argument('event',
                    type=str,
                    help='OpenSIPS Event Name')

event.add_argument('-T', '--transport',
                    type=str,
                    choices=['datagram', 'stream'],
                    help='OpenSIPS Event Transport',
                    default='datagram')
event.add_argument('-li', '--listen-ip',
                    type=str,
                    help='OpenSIPS Event Listen IP Address',
                    default='0.0.0.0')
event.add_argument('-lp', '--listen-port',
                    type=int,
                    help='OpenSIPS Event Listen Port',
                    default=0)
event.add_argument('-e', '--expire',
                    type=int,
                    help='OpenSIPS Event Expire Time',
                    default=None)

def main():
    """ Main function of the opensips-event script """

    args = parser.parse_args()

    if args.type == 'fifo':
        fifo_args = {}
        if args.fifo_file:
            fifo_args['fifo_file'] = args.fifo_file
        if args.fifo_fallback:
            fifo_args['fifo_file_fallback'] = args.fifo_fallback
        if args.fifo_reply_dir:
            fifo_args['fifo_reply_dir'] = args.fifo_reply_dir
        mi = OpenSIPSMI('fifo', **fifo_args)
    elif args.type == 'http':
        mi = OpenSIPSMI('http', url=f'http://{args.ip}:{args.port}/mi')
    elif args.type == 'datagram':
        mi = OpenSIPSMI('datagram', datagram_ip=args.ip, datagram_port=args.port)
    else:
        print(f'Unknownt type: {args.type}')
        sys.exit(1)

    ev = OpenSIPSEvent(mi, args.transport, ip=args.listen_ip, port=args.listen_port)

    def event_handler(message):
        """ Event handler callback """
        try:
            message_json = json.loads(message.decode('utf-8'))
            print(json.dumps(message_json, indent=4))
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")

    def timer(*_):
        """ Timer to notify when the event expires """
        ev.unsubscribe(args.event)
        sys.exit(0) # successful

    if args.expire:
        signal.signal(signal.SIGALRM, timer)
        signal.alarm(args.expire)

    signal.signal(signal.SIGINT, timer)
    signal.signal(signal.SIGTERM, timer)

    try:
        ev.subscribe(args.event, event_handler, expire=args.expire)
    except OpenSIPSEventException as e:
        print(e)
        sys.exit(1)

    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
