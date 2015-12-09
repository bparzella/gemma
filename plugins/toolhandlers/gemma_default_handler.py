#####################################################################
# gemma_default_handler.py
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

from secsgem import GemHostHandler

from app import helpers, models


class gemma_default_handler(GemHostHandler):
    def __init__(self, address, port, active, sessionID, name, eventHandler=None, customConnectionHandler=None):
        GemHostHandler.__init__(self, address, port, active, sessionID, name, eventHandler, customConnectionHandler)

        self.register_callback(7, 3, self.S7F3Handler)
        self.register_callback(7, 5, self.S7F5Handler)

        self.register_callback(12, 1, self.S12F1Handler)
        self.register_callback(12, 3, self.S12F3Handler)
        self.register_callback(12, 5, self.S12F5Handler)
        self.register_callback(12, 9, self.S12F9Handler)
        self.register_callback(12, 15, self.S12F15Handler)

    def S7F3Handler(self, connection, packet):
        """Callback handler for Stream 7, Function 3, Process Program Send - Request.

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        message = self.secs_decode(packet)

        tool = models.Tool.query.filter(models.Tool.name == self.name).first()

        helpers.storeProcessProgram(tool.process_program_scope, message.PPID, message.PPBODY)
        connection.sendResponse(self.stream_function(7, 4)(0), packet.header.system)

        data = {"processProgramScope": tool.process_program_scope, "processProgramID": message.PPID, "connection": self.connection, 'handler': self}
        self.fire_event("ProcessProgramStored", data)

    def S7F5Handler(self, connection, packet):
        """Callback handler for Stream 7, Function 5, Process Program Send - Request.

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        message = self.secs_decode(packet)

        tool = models.Tool.query.filter(models.Tool.name == self.name).first()

        data = helpers.getProcessProgram(tool.process_program_scope, message.get())
        
        if data:
            connection.sendResponse(self.stream_function(7, 6)({"PPID": message.get(), "PPBODY": data}), packet.header.system)

        data = {"processProgramScope": tool.process_program_scope, "processProgramID": message.get(), "connection": self.connection, 'handler': self}
        self.fire_event("ProcessProgramRetrieved", data)

    def S12F1Handler(self, connection, packet):
        """Callback handler for Stream 12, Function 1, map setup data - send

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        message = self.secs_decode(packet)

        print message

        s12f02 = self.stream_function(12, 2)(value=0)

        print s12f02

        connection.sendResponse(s12f02, packet.header.system)

    def S12F3Handler(self, connection, packet):
        """Callback handler for Stream 12, Function 3, map setup data - request

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        message = self.secs_decode(packet)

        print message

        map = models.G85Map.load("data/map/"+message.MID+".xml", message.MID)

        s12f04 = self.stream_function(12, 4)()
        s12f04.MID = message.MID
        s12f04.IDTYP = message.IDTYP
        s12f04.FNLOC = message.FNLOC
        s12f04.ORLOC = message.ORLOC
        s12f04.RPSEL = 0
        for referenceDevice in map.device.referenceDevices:
            s12f04.REF.append([referenceDevice.ReferenceDeviceX, referenceDevice.ReferenceDeviceY])
        s12f04.DUTMS = "um"
        s12f04.XDIES = map.device.DeviceSizeX
        s12f04.YDIES = map.device.DeviceSizeY
        s12f04.ROWCT = map.device.Rows
        s12f04.COLCT = map.device.Columns
        s12f04.PRDCT = 1024
        s12f04.BCEQU = [20, 21, 22]
        s12f04.NULBC = [map.device.NullBin]
        s12f04.MLCL = 1024

        print s12f04

        connection.sendResponse(s12f04, packet.header.system)

    def S12F5Handler(self, connection, packet):
        """Callback handler for Stream 12, Function 5, map transmit inquire

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        message = self.secs_decode(packet)

        print message

        s12f06 = self.stream_function(12, 6)(value=0)

        print s12f06

        connection.sendResponse(s12f06, packet.header.system)

    def S12F9Handler(self, connection, packet):
        """Callback handler for Stream 12, Function 9, map data type 2 - send

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        message = self.secs_decode(packet)

        print message

        s12f10 = self.stream_function(12, 10)(value=0)

        print s12f10

        connection.sendResponse(s12f10, packet.header.system)

    def S12F15Handler(self, connection, packet):
        """Callback handler for Stream 12, Function 15, map data type 2 - request

        .. seealso:: :func:`secsgem.hsmsConnections.hsmsConnection.registerCallback`

        :param connection: connection the message was received on
        :type connection: :class:`secsgem.hsmsConnections.hsmsConnection`
        :param packet: complete message received
        :type packet: :class:`secsgem.hsmsPackets.hsmsPacket`
        """
        message = self.secs_decode(packet)

        map = models.G85Map.load("data/map/"+message.MID+".xml", message.MID)

        s12f16 = self.stream_function(12, 16)()
        s12f16.MID = message.MID
        s12f16.IDTYP = message.IDTYP
        s12f16.STRP = [0, 0]

        binlt = []

        for row in map.device.data.rows:
            for col in row.cols:
                binlt.append(col)

        s12f16.BINLT = binlt

        connection.sendResponse(s12f16, packet.header.system)
