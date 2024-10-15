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

import json
from collections import OrderedDict
from typing import Tuple

def extract_json(json_acc: list, data: bytes) -> Tuple[list, bytes]:

    """ Extracts JSON data from a byte stream """

    while data:
        try:
            json_obj, idx = json.JSONDecoder(object_pairs_hook=OrderedDict).raw_decode(data.decode("utf-8"))
            json_acc.append(json_obj)
            data = data[idx:]
        except json.JSONDecodeError as e:
            break
    return json_acc, data
