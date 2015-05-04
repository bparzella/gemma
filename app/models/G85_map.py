#####################################################################
# G85_map.py
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

import logging

from xml.etree import ElementTree

def int16(value):
	return int(value, 16)

class G85Object(object):
	def __repr__(self):
		return self.__class__.__name__ + ": " + str(self.__dict__)

	def propertyFromMap(self, map, propertyName, converter, mandatory=True, default=None):
		if propertyName in map.attrib:
			setattr(self, propertyName, converter(map.attrib[propertyName]))
		else:
			if mandatory==True:
				logging.warning("{} is missing mandatory field {}".format(self.__class__.__name__, propertyName))

			setattr(self, propertyName, default)

	@staticmethod
	def elementName(name):
		return "{http://www.semi.org}" + name

class G85Row(G85Object):
	def __repr__(self):
		return self.__class__.__name__ + ": " + str(len(self.cols)) + "cols"

	@classmethod
	def fromXML(cls, row):
		newRow = cls()

		newRow.rowData = row.text

		return newRow

	def unpack(self, binType):
		if binType == "ASCII":
			self.cols = self.rowData
		elif binType == "Decimal":
			self.cols = [int(c) for c in self.rowData.split(" ")]
		elif binType == "HexaDecimal":
			self.cols = [int(c, 16) for c in [self.rowData[i:i+2] for i in range(0, len(self.rowData), 2)]]
		elif binType == "Integer2":
			self.cols = [int(c, 16) for c in [self.rowData[i:i+4] for i in range(0, len(self.rowData), 4)]]

class G85Data(G85Object):
	@classmethod
	def fromXML(cls, data):
		newData = cls()

		newData.propertyFromMap(data, "MapName", str, False, "")
		newData.propertyFromMap(data, "MapVersion", str, False, "")

		newData.rows = []

		for row in data.findall(newData.elementName("Row")):
			newData.rows.append(G85Row.fromXML(row))

		return newData

class G85ReferenceDevice(G85Object):
	@classmethod
	def fromXML(cls, referenceDevice):
		newReferenceDevice = cls()

		newReferenceDevice.propertyFromMap(referenceDevice, "ReferenceDeviceX", int, True)
		newReferenceDevice.propertyFromMap(referenceDevice, "ReferenceDeviceY", int, True)
		newReferenceDevice.propertyFromMap(referenceDevice, "RefDevicePosX", float, False, 0.0)
		newReferenceDevice.propertyFromMap(referenceDevice, "RefDevicePosY", float, False, 0.0)

		return newReferenceDevice

class G85Bin(G85Object):
	@classmethod
	def fromXML(cls, bin):
		newBin = cls()

		newBin.propertyFromMap(bin, "BinCode", int16, False, 0)
		newBin.propertyFromMap(bin, "BinCount", int, False, 0)
		newBin.propertyFromMap(bin, "BinQuality", str, False, "")
		newBin.propertyFromMap(bin, "BinDescription", str, False, "")

		return newBin

class G85Device(G85Object):
	@classmethod
	def fromXML(cls, device):
		newDevice = cls()

		newDevice.data = G85Data.fromXML(device.find(newDevice.elementName("Data")))

		newDevice.propertyFromMap(device, "BinType", str, True, "ASCII")
		newDevice.propertyFromMap(device, "OriginLocation", int, True, 0)

		for row in newDevice.data.rows:
			row.unpack(newDevice.BinType)

		newDevice.propertyFromMap(device, "ProductId", str, False, "")
		newDevice.propertyFromMap(device, "LotId", str, False, "")
		newDevice.propertyFromMap(device, "Orientation", int)
		newDevice.propertyFromMap(device, "WaferSize", int, False, 0)
		newDevice.propertyFromMap(device, "DeviceSizeX", float, False, 0.0)
		newDevice.propertyFromMap(device, "DeviceSizeY", float, False, 0.0)
		newDevice.propertyFromMap(device, "StepSizeX", float, False, 0.0)
		newDevice.propertyFromMap(device, "StepSizeY", float, False, 0.0)
		newDevice.propertyFromMap(device, "MagazineId", str, False, "")
		newDevice.propertyFromMap(device, "Rows", int, False, len(newDevice.data.rows))
		newDevice.propertyFromMap(device, "Columns", int, False, len(newDevice.data.rows[0].cols))
		newDevice.propertyFromMap(device, "FrameId", str, False, "")
		newDevice.propertyFromMap(device, "NullBin", int16)
		newDevice.propertyFromMap(device, "SupplierName", str, False, "")
		newDevice.propertyFromMap(device, "CreateData", str, False, "")
		newDevice.propertyFromMap(device, "LastModified", str, False, "")
		newDevice.propertyFromMap(device, "Status", str, False, "")
		newDevice.propertyFromMap(device, "SlotNumber", int, False, 0)
		newDevice.propertyFromMap(device, "SubstrateNumber", int, False, 0)
		newDevice.propertyFromMap(device, "GoodDevices", int, False, 0)

		newDevice.referenceDevices = []
		for referenceDevice in device.findall(newDevice.elementName("ReferenceDevice")):
			newDevice.referenceDevices.append(G85ReferenceDevice.fromXML(referenceDevice))

		newDevice.bins = []
		for bin in device.findall(newDevice.elementName("Bin")):
			newDevice.bins.append(G85Bin.fromXML(bin))

		return newDevice

class G85Map(G85Object):
	@classmethod
	def fromXML(cls, map):
		newMap = cls()

		newMap.device = G85Device.fromXML(map.find(newMap.elementName("Device")))

		newMap.propertyFromMap(map, "SubstrateType", str)
		newMap.propertyFromMap(map, "SubstrateId", str)
		newMap.propertyFromMap(map, "FormatRevision", str, False, "G85-0703")

		return newMap

	@classmethod
	def load(cls, filename, waferId):
		document = ElementTree.parse(filename)
		root = document.getroot()

		if root.tag == G85Object.elementName("Map"):
			if (root.attrib["SubstrateId"] == waferId):
				return cls.fromXML(root)
		elif root.tag == "Maps":
			for map in root.findall('Map'):
				if (map.attrib["SubstrateId"] == waferId):
					return cls.fromXML(map)

		logging.warning("Map {} not found in {}".format(waferId, filename))
		return None 
