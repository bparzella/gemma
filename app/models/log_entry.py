#####################################################################
# app/models/log_entry.py
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

from app import db

#class LogEntry(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    tool_id = db.Column(db.Integer, db.ForeignKey('tool.id'), nullable=False)
#    timestamp = db.Column(db.DateTime())
#    severity = db.Column(db.Integer)
#    group = db.Column(db.String(20))
#    data = db.Column(db.Text())
#
#    def __repr__(self):
#        return str(self.id)
