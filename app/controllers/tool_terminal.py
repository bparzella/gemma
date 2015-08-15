#####################################################################
# app/controllers/tool_terminal.py
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

from app import app, helpers
from flask import request, abort


@app.route("/tools/<toolname>/terminal/<TID>", methods=['POST', 'GET'])
def tool_terminal(toolname, TID):
    handler = helpers.connectionManager[toolname]

    if handler is None:
        abort(404)

    if request.method == 'POST':
        handler.send_equipment_terminal(int(TID), request.form["text"].encode('ascii','replace'))

    return "OK"
