"""Subclass of PexViewerMainFrame, which is generated by wxFormBuilder."""

import wx
import GeneratedGUI as gg #import generated GUI
from ConfigReader import *
import sqlitepersist as sqp
from PersistClasses import *

# Implementing PexViewerMainFrame
class PexViewerMain( gg.PexViewerMainFrame ):
	def __init__(self, parent ):
		#gg.PexViewerMainFrame.__init__( self, parent )
		super().__init__(parent)
		self.init_prog()
		self.init_db()
        #self.ShowMembers()

	def init_prog(self):
		self._configuration = ConfigReader("./PexDb.conf")

	def init_db(self):
		dbfilename = self._configuration.get_value("database", "filename")
		self._fact = sqp.SQFactory("PexDb", dbfilename)
		doinits = self._configuration.get_value("database", "tryinits")
		if doinits:
			self._initandseeddb()

	def _initandseeddb(self):
		pclasses = [sqp.PCatalog, Unit, Experiment, Printer, Extruder, Parameter, Setting]
		createds = []
		for pclass in pclasses:
			done = self._fact.try_createtable(pclass)
			if done:
				createds.append(pclass)

		if sqp.PCatalog in createds:
			sdr = sqp.SQPSeeder(self._fact, "./PexSeeds/catalogs.json")
			sdr.create_seeddata()

		if Unit in createds:
			sdr = sqp.SQPSeeder(self._fact, "./PexSeeds/units.json")
			sdr.create_seeddata()

		if Parameter in createds:
			sdr = sqp.SQPSeeder(self._fact, "./PexSeeds/parameters.json")
			sdr.create_seeddata()

	
	# Handlers for PexViewerMainFrame events.
	def quit_PexViewer( self, event ):
		# TODO: Implement quit_PexViewer
		pass

if __name__ == '__main__':
	app = wx.App()
	frm = PexViewerMain(None)
	frm.Show()
	app.MainLoop()
	


