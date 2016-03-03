#####################################################################
# app/controllers/tool_sv.py
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
from secsgem.secs.variables import SecsVarU4, SecsVarString


@app.route("/tools/<toolname>/sv/<svid>")
def tool_sv(toolname, svid):
    handler = helpers.connectionManager[toolname]
    if helpers.is_int(svid):
        result = handler.request_sv(SecsVarU4(value=int(svid)))
    else:
        result = handler.request_sv(SecsVarString(value=svid))

    if isinstance(result, list):
        return str(result)

    return str(result)
