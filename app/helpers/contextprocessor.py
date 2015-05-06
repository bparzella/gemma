#####################################################################
# app/helpers/contextprocessor.py
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

from app import app


@app.context_processor
def utility_processor():
    def handlebar_tag(tag):
        return '{{' + tag + '}}'

    def handlebar_tag_raw(tag):
        return '{{{' + tag + '}}}'
    return dict(handlebar_tag=handlebar_tag, handlebar_tag_raw=handlebar_tag_raw)
