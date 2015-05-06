#####################################################################
# app/helpers/json_encoder.py
#
# (c) Copyright 2015, Benjamin Parzella. All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#####################################################################


def jsonEncoder(o):
    if isinstance(o, set):
        return list(o)

    if hasattr(o, "_serializeData") and callable(getattr(o, "_serializeData")):
        return getattr(o, "_serializeData")()
    else:
        return o.__dict__
