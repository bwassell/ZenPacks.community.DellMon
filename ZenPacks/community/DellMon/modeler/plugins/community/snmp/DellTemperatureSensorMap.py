################################################################################
#
# This program is part of the DellMon Zenpack for Zenoss.
# Copyright (C) 2009, 2010, 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""DellTemperatureSensorMap

DellTemperatureSensorMap maps the cpqHeTemperatureTable table to temperaturesensors objects

$Id: DellTemperatureSensorMap.py,v 1.2 2011/09/21 22:25:55 egor Exp $"""

__version__ = '$Revision: 1.2 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap

class DellTemperatureSensorMap(SnmpPlugin):
    """Map Dell System Management Temperature Sensors table to model."""

    maptype = "TemperatureSensorMap"
    modname = "ZenPacks.community.DellMon.DellTemperatureSensor"
    relname = "temperaturesensors"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('temperatureProbeTable',
                    '.1.3.6.1.4.1.674.10892.1.700.20.1',
                    {
                        '.5': 'status',
                        '.7': '_type',
                        '.8': 'id',
                        '.10': 'threshold',
                    }
        ),
    )

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        tsensorstable = tabledata.get("temperatureProbeTable")
        rm = self.relMap()
        for oid,tsensor in tabledata.get("temperatureProbeTable",{}).iteritems():
            try:
                om = self.objectMap(tsensor)
                if om.status < 3: continue
                om.id = self.prepId(getattr(om, 'id', 'Unknown'))
                om.snmpindex = oid.strip('.')
                if om._type == 16:
                    om.modname = "ZenPacks.community.DellMon.DellDiscreteTemperatureSensor"
                    om.threshold = 1
            except AttributeError:
                continue
            rm.append(om)
        return rm
