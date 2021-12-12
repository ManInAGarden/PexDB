"""Subclass of PexViewerMainFrame, which is generated by wxFormBuilder."""

from datetime import datetime
import wx
import wx.propgrid as pg
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


	def repair_exp_properties(self):
		"""repair things for the property items that were not generated sufficiently"""
		#repair the names
		self.m_carriedoutdtPGI.SetName("carriedoutdt")
		self.m_carriedoutdtPGI.SetAttribute("DateFormat", "%Y.%d.%m %H:%M:%S")

		self.m_descriptionPGI.SetName("description")
		self.m_printerPGI.SetName("printer")
		self.m_extruderPGI.SetName("extruder")

		#fill the choices
		prchoices = []
		for prid, pr in self._printers.items():
			prchoices.append(str(pr))

		prprop = self.m_experimentPG.GetProperty("printer")
		prprop.SetChoices(pg.PGChoices(prchoices))

		extchoices = []
		for prid, pr in self._extruders.items():
			extchoices.append(str(pr))

		prprop = self.m_experimentPG.GetProperty("extruder")
		prprop.SetChoices(pg.PGChoices(extchoices))
		
		
	def init_gui(self):
		self._printers = self._get_all_printers()
		self._extruders = self._get_all_extruders()

		self._prefprinter = self._get_preferred_printer()
		self._prefextruder = self._get_preferred_extruder()

		self.repair_exp_properties()
		self._experiments = self.get_experiments()
		self.refresh_dash()

	def _get_all_printers(self):
		q = sqp.SQQuery(self._fact, Printer)
		answ = {}
		for pr in q:
			answ[pr._id] = pr

		return answ

	def _get_all_extruders(self):
		q = sqp.SQQuery(self._fact, Extruder)
		answ = {}
		for extr in q:
			answ[extr._id] = extr

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
			self._fact.fill_joins(exp, Experiment.Settings)
			experiments.append(exp)

		return experiments

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
		exp.settings = []
		actparaq = sqp.SQQuery(self._fact, Parameter).where(Parameter.IsActive==True)
		for acts in actparaq:
			setg = Setting(parameterid=acts._id, experimentid=exp._id, parameterdefinition=acts)
			self._fact.flush(setg)
			exp.settings.append(setg)

		self._experiments.append(exp)
		self.refresh_dash()

	def experimentDWLC_selchanged( self, event ):
		"""The user selected a row in the list of experiments"""
		idx = self.m_experimentsDataViewListCtrl.GetSelectedRow()
		if idx == wx.NOT_FOUND:
			return

		selexp = self._experiments[idx]
		self.refresh_expview(selexp)

	def refresh_expview(self, exp):
		self._currentexperiment = exp
		membs = ["description", "carriedoutdt"]
		for memb in membs:
			self.m_experimentPG.SetPropertyValue(memb, exp.__getattribute__(memb))

		if exp.printerused is not None:
			self.m_experimentPG.SetPropertyValue("printer", str(exp.printerused))

		if exp.extruderused is not None:
			self.m_experimentPG.SetPropertyValue("extruder", str(exp.extruderused))

		for se in exp.settings:
			v = se.value
			pd = se.parameterdefinition
			n = pd.abbreviation
			l = pd.name

			try:
				self.m_experimentPG.DeleteProperty(n)
			except Exception:
				pass

			if pd.disptype=="FLOAT":
				if pd.unit is not None:
					l += " [{0}]".format(pd.unit.abbreviation)
				if v is None:
					v = 0.0
				fp = pg.FloatProperty(l, n, v)
				fp.SetAttribute("Precision", 3)
				self.m_experimentPG.Append(fp)
			elif pd.disptype=="BOOLEAN":
				if v is None:
					v = False
				bp = pg.BoolProperty(l, n, v)
				bp.SetAttribute("UseCheckbox", 1)
				self.m_experimentPG.Append(bp)

	def killFocus( self, event ):
		lim = event.EventObject.LastItem
		val = lim.GetValue()
		pi = self.m_experimentPG.GetIterator(pg.PG_ITERATE_DEFAULT)
		while not pi.AtEnd():
			prop = pi.GetProperty()
			pname =prop.GetName()
			val = prop.GetValue()

			pi.Next()

	def setFocus( self, event ):
		print("set focus")




if __name__ == '__main__':
	app = wx.App()
	frm = PexViewerMain(None)
	frm.Show()
	app.MainLoop()
	


