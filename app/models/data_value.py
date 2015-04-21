#####################################################################
# app/models/data_value.py
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

class DataValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ce_id = db.Column(db.Integer, db.ForeignKey('collection_event.id'), nullable=False)
    dvid = db.Column(db.Integer)

    def __repr__(self):
        return str(self.dvid)

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
