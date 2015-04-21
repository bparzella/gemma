#####################################################################
# app/models/tool.py
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

class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    type = db.Column(db.String(80))
    passive = db.Column(db.Boolean)
    address = db.Column(db.String(80))
    port = db.Column(db.Integer)
    device_id = db.Column(db.Integer)
    enabled = db.Column(db.Boolean)
    collection_events = db.relationship('CollectionEvent', backref='tool', lazy='dynamic', cascade="all, delete, delete-orphan")
#    log_entries = db.relationship('LogEntry', backref='tool', lazy='dynamic', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return self.name

    def store(self):
        db.session.commit()
