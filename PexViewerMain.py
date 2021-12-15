"""Subclass of PexViewerMainFrame, which is generated by wxFormBuilder."""

from datetime import datetime
import wx
import wx.propgrid as pg
import GeneratedGUI as gg #import generated GUI
from ConfigReader import *
from WxGuiMapper import WxGuiMapperExperiment
import sqlitepersist as sqp
from PersistClasses import *

# Implementing PexViewerMainFrame
class PexViewerMain( gg.PexViewerMainFrame ):
	def __init__(self, parent ):
		#gg.PexViewerMainFrame.__init__( self, parent )
		super().__init__(parent)
		self.init_prog()
		self.init_db()
		self.init_gui()

	def init_prog(self):
		self._configuration = ConfigReader("./PexDb.conf")

	def init_db(self):
		dbfilename = self._configuration.get_value("database", "filename")
		self._fact = sqp.SQFactory("PexDb", dbfilename)
		doinits = self._configuration.get_value("database", "tryinits")
		self._fact.set_db_dbglevel(self._configuration.get_value("database", "dbgfilename"),
			self._configuration.get_value("database", "dbglevel"))
		if doinits:
			self._initandseeddb()


	# def repair_exp_properties(self):
	# 	"""repair things for the property items that were not generated sufficiently"""
	# 	#repair the names
	# 	self.m_carriedoutdtPGI.SetName("carriedoutdt")
	# 	self.m_carriedoutdtPGI.SetAttribute("DateFormat", "%Y.%d.%m %H:%M:%S")

	# 	self.m_descriptionPGI.SetName("description")
	# 	self.m_printerPGI.SetName("printerused")
	# 	self.m_extruderPGI.SetName("extruderused")

	# 	#fill the choices
	# 	prchoices = []
	# 	for pr in self._printers:
	# 		prchoices.append(str(pr))

	# 	prprop = self.m_experimentPG.GetProperty("printerused")
	# 	prprop.SetChoices(pg.PGChoices(prchoices))

	# 	extchoices = []
	# 	for pr in self._extruders:
	# 		extchoices.append(str(pr))

	# 	prprop = self.m_experimentPG.GetProperty("extruderused")
	# 	prprop.SetChoices(pg.PGChoices(extchoices))
		
	def create_exp_gui(self):
		self._expgui = WxGuiMapperExperiment(self._fact, self.m_experimentPG)
	
		
	def init_gui(self):
		self._printers = self._get_all_printers()
		self._extruders = self._get_all_extruders()

		self._prefprinter = self._get_preferred_printer()
		self._prefextruder = self._get_preferred_extruder()

		self.create_exp_gui()
		self._experiments = self.get_experiments()
		self.refresh_dash()

	
	def _get_all_printers(self):
		q = sqp.SQQuery(self._fact, Printer)
		answ = list(q)

		return answ

	def _get_all_extruders(self):
		q = sqp.SQQuery(self._fact, Extruder)
		answ = list(q)

		return answ

	def _get_preferred_printer(self):
		abbr = self._configuration.get_value("preferences", "stdprinter")
		answ = sqp.SQQuery(self._fact, Printer).where(Printer.Abbreviation==abbr).first_or_default(None)
		return answ

	def _get_preferred_extruder(self):
		abbr = self._configuration.get_value("preferences", "stdextruder")
		answ = sqp.SQQuery(self._fact, Extruder).where(Extruder.Abbreviation==abbr).first_or_default(None)
		return answ
	
	def refresh_dash(self):
		self.m_experimentsDataViewListCtrl.DeleteAllItems()
		for exp in self._experiments:
			visr = [str(exp.carriedoutdt), exp.description]
			self.m_experimentsDataViewListCtrl.AppendItem(visr)
		
	def get_experiments(self):
		q = sqp.SQQuery(self._fact, Experiment).where(Experiment.IsArchived == False).order_by(Experiment.CarriedOutDt)
		experiments = []
		for exp in q:
			self._fact.fill_joins(exp, Experiment.Factors)
			experiments.append(exp)

		return experiments

	def _initandseeddb(self):
		pclasses = [sqp.PCatalog, Unit, Experiment, Printer, Extruder, FactorDefinition, FactorValue]
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

		if FactorDefinition in createds:
			sdr = sqp.SQPSeeder(self._fact, "./PexSeeds/factordefinitions.json")
			sdr.create_seeddata()

		if Printer in createds:
			sdr = sqp.SQPSeeder(self._fact, "./PexSeeds/printers.json")
			sdr.create_seeddata()

		if Extruder in createds:
			sdr = sqp.SQPSeeder(self._fact, "./PexSeeds/extruders.json")
			sdr.create_seeddata()
	
	# Handlers for PexViewerMainFrame events.
	def quit_PexViewer( self, event ):
		"""The user selected the menu item "close PexDbViewer"
		"""
		self.Close()
		
	def create_new_experiment( self, event ):
		"""The user selected the menuitem "create new experiment"
		"""
		exp = Experiment(carriedoutdt=datetime.now(), 
			description="Neues Experiment")
		
		if self._prefextruder is not None:
			exp.extruderused = self._prefextruder
			exp.extruderusedid = self._prefextruder._id

		if self._prefprinter is not None:
			exp.printerused = self._prefprinter
			exp.printerusedid = self._prefprinter._id

		self._fact.flush(exp)

		#create new settings for the experiment from all the active parameters
		exp.factors = []
		factdef_q = sqp.SQQuery(self._fact, FactorDefinition).where(FactorDefinition.IsActive==True)
		for fdef in factdef_q:
			fval = FactorValue(factordefinitionid=fdef._id, experimentid=exp._id, factordefinition=fdef)
			self._fact.flush(fval)
			exp.factors.append(fval)

		self._experiments.append(exp)
		self.refresh_dash()

	def experimentDWLC_selchanged( self, event):
		"""The user selected a row in the list of experiments"""
		idx = self.m_experimentsDataViewListCtrl.GetSelectedRow()
		if idx == wx.NOT_FOUND:
			return

		selexp = self._experiments[idx]
		self.refresh_expview(selexp, self._expgui)
		self._currentexperiment = selexp

	def refresh_expview(self, exp, expgui : WxGuiMapperExperiment):
		"""refresh the experiment data on the gui with the data of the given experiment"""

		#flatten the experiment data to da key, value dict
		vd = {}
		vd["description"] = exp.description
		vd["carriedoutdt"] = exp.carriedoutdt
		vd["extruderused"] = exp.extruderused
		vd["printerused"] = exp.printerused
		for setg in exp.factors:
			vd[setg.factordefinition.name] = setg.value

		expgui.object2gui(vd, self.m_experimentPG)
			

	def get_changed_exp(self, exppg : pg.PropertyGrid, exp: Experiment):
		valdict = self._expgui.gui2object(exppg)

		exp.carriedoutdt = valdict["carriedoutdt"]
		exp.description = valdict["description"]
		exp.printerused = valdict["printerused"]
		exp.extruderused = valdict["extruderused"]
		exp.printerusedid = valdict["printerusedid"]
		exp.extruderusedid = valdict["extruderusedid"]

		#now handle alle the settings of the experiment

		for setg in exp.factors:
			key = setg.factordefinition.name
			setg.value = valdict[key]
		


	def propgridChanged( self, event ):
		"""handles PropertyGridChanged event"""
		self.get_changed_exp(self.m_experimentPG, self._currentexperiment)
		self._fact.flush(self._currentexperiment)
		for setg in self._currentexperiment.factors:
			self._fact.flush(setg)

		self.refresh_dash()

if __name__ == '__main__':
	app = wx.App()
	frm = PexViewerMain(None)
	frm.Show()
	app.MainLoop()
	


