
import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPackBase

class ZenPack(ZenPackBase):
    """ DellMon loader
    """
    packZProperties = [
            ('zDellExpansionCardMapIgnorePci', False, 'boolean'),
            ]

    def install(self, app):
	
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
            rClass = devReports.getReportClass()
	    if not hasattr(devReports, 'Dell PowerEdge Reports'):
                dc = rClass('Dell PowerEdge Reports', None)
                devReports._setObject('Dell PowerEdge Reports', dc)
        ZenPackBase.install(self, app)
	self.setupZProperties(app)

    def upgrade(self, app):
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
            rClass = devReports.getReportClass()
	    if not hasattr(devReports, 'Dell PowerEdge Reports'):
                dc = rClass('Dell PowerEdge Reports', None)
                devReports._setObject('Dell PowerEdge Reports', dc)
        ZenPackBase.upgrade(self, app)

    def remove(self, app, junk):
        ZenPackBase.remove(self, app, junk)
        if hasattr(self.dmd.Reports, 'Device Reports'):
            devReports = self.dmd.Reports['Device Reports']
	    if hasattr(devReports, 'Dell PowerEdge Reports'):
                devReports._delObject('Dell PowerEdge Reports')
    
    def setupZProperties(self, app):
	x = self.dmd.Devices.getSubDevicesGen()
	for d in x:
	    if d.getHWManufacturerName() == 'Dell' and d.getHWSerialNumber()[-1]  == '1':
		#dollar = "$"
        	    #print "%s YES " % d.getId()
	        dell_link = '<a href= http://support.dell.com/support/topics/global.aspx/support/my_systems_info/details?c=us&l=en&s=gen&ServiceTag=%s target="_">DELL_SUPPORT_LINK</a>' %  d.getHWSerialNumber()
		orig_zlinks = d.zLinks
		if orig_zlinks.find('DELL_SUPPORT_LINK') >= 0: return#print "noop return"
	        if d.hasProperty('zLinks'):
		    d.zLinks = d.zLinks + ' | ' + dell_link
		else:
		    d._setProperty('zLinks', dell_link)
