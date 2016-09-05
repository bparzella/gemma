#####################################################################
# app/controllers/tool_ec.py
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
from flask import request
from secsgem.secs.variables import SecsVarU4, SecsVarString


@app.route("/tools/<toolname>/ec/<ecid>", methods=['POST', 'GET'])
def tool_ec(toolname, ecid):
    handler = helpers.connectionManager[toolname]
    if request.method == 'POST':
        if helpers.is_int(ecid):
            result = handler.request_ec(SecsVarU4(int(ecid))).data[0].value
        else:
            result = handler.request_ec(SecsVarString(ecid)).data[0].value
        result.set(request.form["value"])

        if helpers.is_int(ecid):
            result = handler.set_ec(SecsVarU4(int(ecid)), result)
        else:
            result = handler.set_ec(SecsVarString(ecid), result)

        return str(result)
    else:
        if helpers.is_int(ecid):
            result = handler.request_ec(SecsVarU4(int(ecid)))[0].get()
        else:
            result = handler.request_ec(SecsVarString(ecid))[0].get()

        return str(result)
