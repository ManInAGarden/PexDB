"""Subclass of PexViewerMainFrame, which is generated by wxFormBuilder."""

from datetime import datetime
import wx
import wx.propgrid as pg
import GeneratedGUI as gg #import generated GUI
from ConfigReader import *
from PexDbViewerEditFactorDefinitions import PexDbViewerEditFactorDefinitions
from PexDbViewerEditProjectDialog import PexDbViewerEditProjectDialog
from PexDbViewerEditResultDefinitions import PexDbViewerEditResultDefinitions
from PexDbViewerOpenProjectDialog import PexDbViewerOpenProjectDialog
from PropGridGUIMappers import *
import sqlitepersist as sqp
from PersistClasses import *
from sqlitepersist.SQLitePersistBasicClasses import OrderDirection
from sqlitepersist.SQLitePersistSeeder import SQPSeeder

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

		self._currentproject = self._get_current_proj()

		
	def _get_current_proj(self):
		"""get the youngest not archive project"""
		proj = sqp.SQQuery(self._fact, Project).where(Project.IsArchived==False).order_by(sqp.OrderInfo(Project.Created, OrderDirection.DESCENDING)).first_or_default(None)

		if proj is None:
			raise Exception("strangely no project was found to be used as an initial/default project")

		return proj

	def create_exp_gui(self):
		self._expgui = WxGuiMapperExperiment(self._fact, self.m_experimentPG)
		self.m_experimentPG.Enable(False) #disable in case we have no data
		self._expgui.emptyallitems(self.m_experimentPG)
		
	def displayprojinsb(self):
		self.m_mainSBA.SetStatusText("Project: {0}".format(self._currentproject.name), 1)

	def init_gui(self):
		self._printers = self._get_all_printers()
		self._extruders = self._get_all_extruders()

		self._prefprinter = self._get_preferred_printer()
		self._prefextruder = self._get_preferred_extruder()

		self.m_mainSBA.SetStatusText("DB: {0}".format(self._fact._dbfilename), 0)
		self.displayprojinsb()
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
		ct = 0
		for exp in self._experiments:
			visr = [str(exp.carriedoutdt), exp.description]
			self.m_experimentsDataViewListCtrl.AppendItem(visr)

			ct += 1

		if ct > 0:
			self.m_experimentPG.Enable()
			self.m_experimentsDataViewListCtrl.SelectRow(0)
			#selection change does not get called, so we have to this here
			#well - the selection did not change actually
			selexp = self._experiments[0]
			self.refresh_expview(selexp, self._expgui)
			self._currentexperiment = selexp
		else:
			self._expgui.emptyallitems(self.m_experimentPG)
			self.m_experimentPG.Enable(False)
		
	def get_experiments(self):
		q = sqp.SQQuery(self._fact, Experiment).where(Experiment.IsArchived == False 
			and Experiment.ProjectId==self._currentproject._id).order_by(Experiment.CarriedOutDt)
		experiments = []
		for exp in q:
			self._fact.fill_joins(exp, Experiment.Factors)
			experiments.append(exp)

		return experiments

	def _initandseeddb(self):
		pclasses = [sqp.PCatalog, 
			Unit, 
			Project,
			Experiment, 
			Printer, 
			Extruder, 
			FactorDefinition, 
			FactorValue, 
			ResultDefinition, 
			ResultValue]

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

		if ResultDefinition in createds:
			sdr = sqp.SQPSeeder(self._fact, "./PexSeeds/resultdefinitions.json")
			sdr.create_seeddata()

		if Project in createds:
			newproj = Project(name="std", status=self._fact.getcat(ProjectStatusCat, "INIT"))
			self._fact.flush(newproj)

	# Handlers for PexViewerMainFrame events.
	def quit_PexViewer( self, event ):
		"""The user selected the menu item "close PexDbViewer"
		"""
		self.Close()
		
	def create_new_experiment( self, event ):
		"""The user selected the menuitem "create new experiment"
		"""
		if self._currentproject is None:
			raise Exception("We have no current project! Experiment cannot be created!")

		exp = Experiment(carriedoutdt=datetime.now(), 
			description="Neues Experiment")
		
		exp.projectid = self._currentproject._id
		self.project = self._currentproject
		
		if self._prefextruder is not None:
			exp.extruderused = self._prefextruder
			exp.extruderusedid = self._prefextruder._id

		if self._prefprinter is not None:
			exp.printerused = self._prefprinter
			exp.printerusedid = self._prefprinter._id

		self._fact.flush(exp)

		#create/prepare new factorvalues for the experiment from all the active parameters
		exp.factors = []
		factdef_q = sqp.SQQuery(self._fact, FactorDefinition).where(FactorDefinition.IsActive==True)
		for fdef in factdef_q:
			fval = FactorValue(factordefinitionid=fdef._id, experimentid=exp._id, factordefinition=fdef)
			self._fact.flush(fval)
			exp.factors.append(fval)

		exp.results = []
		resdef_q = sqp.SQQuery(self._fact, ResultDefinition).where(ResultDefinition.IsActive==True)
		for rdef in resdef_q:
			rval = ResultValue(resultdefinitionid=rdef._id, experimentid=exp._id, resultdefinition=rdef)
			self._fact.flush(rval)
			exp.results.append(rval)

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
		self.m_experimentPG.Enable() #enable prop grid which should be filled with editable data now

	def refresh_expview(self, exp, expgui : WxGuiMapperExperiment):
		"""refresh the experiment data on the gui with the data of the given experiment"""

		#flatten the experiment data to da key, value dict
		vd = {}
		vd["description"] = exp.description
		vd["carriedoutdt"] = exp.carriedoutdt
		vd["extruderused"] = exp.extruderused
		vd["printerused"] = exp.printerused
		for setg in exp.factors:
			vd[setg.factordefinition.name] = self.get_typed_factor_value(setg.value, setg.factordefinition.disptype)

		expgui.object2gui(vd, self.m_experimentPG)
			
	def get_typed_factor_value(self, vals : str, disptype : str):
		#factors are always stored as strings in the db, so we have to change them to the correct type here

		if vals is None:
			return None

		if disptype == "BOOLEAN":
			return vals == "1" or vals.lower()=="true"
		elif disptype == "FLOAT":
			return float(vals)
		else:
			raise Exception("unsupported displaytyp <{0}>".format(disptype))


	def get_store_str(self, val):
		#factor values are stored as strings in the database so we have to change them back.
		if val is None:
			return None

		vt = type(val)
		if vt is bool:
			if val is True:
				return "1"
			else:
				return "0"
		elif vt is float:
			return str(val)
		else:
			raise Exception("unsupported type in get_store_str()")

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
			setg.value = self.get_store_str(valdict[key])
		


	def propgridChanged( self, event ):
		"""handles PropertyGridChanged event"""
		self.get_changed_exp(self.m_experimentPG, self._currentexperiment)
		self._fact.flush(self._currentexperiment)
		for setg in self._currentexperiment.factors:
			self._fact.flush(setg)

		self.refresh_dash()


	def delete_experiment_menuItemOnMenuSelection( self, event ):
		idx = self.m_experimentsDataViewListCtrl.GetSelectedRow()
		if idx >= 0:
			delex = self._experiments[idx]
			self._fact.delete(delex)
			self._experiments.remove(delex)
			self.refresh_dash()

	def exp_deepcopy(self, exp):
		"""deep copy an experiment"""
		aexp = Experiment(description=exp.description,
			carriedoutdt=exp.carriedoutdt, 
			printerusedid=exp.printerusedid,
			extruderusedid=exp.extruderusedid,
			printerused=exp.printerused,
			extruderused=exp.extruderused)
		
		self._fact.flush(aexp)
		aexp.factors = []
		for factval in exp.factors:
			nfact = FactorValue(experimentid=aexp._id,
				factordefinitionid=factval.factordefinitionid,
				factordefinition=factval.factordefinition,
				value = factval.value)
			aexp.factors.append(nfact)
			self._fact.flush(nfact)

		return aexp #return the deeply cloned experiment

	def dupicate_experiment_menuitemOnMenuSelection( self, event ):
		idx = self.m_experimentsDataViewListCtrl.GetSelectedRow()
		if idx >= 0:
			fexp = self._experiments[idx]
			sexp = self.exp_deepcopy(fexp)
			self._experiments.append(sexp)
			self.refresh_dash()

	def m_edit_factors_menuitemOnMenuSelection(self, event):
		"""user clicked on edit factors menu item"""
		dia = PexDbViewerEditFactorDefinitions(self, self._fact)
		dia.ShowModal()

	def edit_result_definitions(self, event):
		"""user clicked on edit result defs menu item"""
		dia = PexDbViewerEditResultDefinitions(self, self._fact)
		dia.ShowModal()


	def openproject_menuItemOnMenuSelection(self, event):
		"""user wants to switch over to another project, so we open a selection dialog
		for him"""

		dial = PexDbViewerOpenProjectDialog(self, self._fact, self._currentproject)
		res = dial.ShowModal()

		if res == wx.ID_OK:
			assert(dial.chosenproject is not None)
			if self._currentproject._id != dial.chosenproject._id:
				self._currentproject = dial.chosenproject
				self.displayprojinsb()
				#now refresh the gui parts to show the experiments of the new project (should be none at all)
				self._experiments = self.get_experiments()
				self.refresh_dash()

	def newproj_menutitemOnMenuSelection( self, event ):
		"""user selected "new project" in menu
		we create a new standard project and make it the current project"""
		self._currentproject = Project(name="New project")
		self._fact.flush(self._currentproject)
		self.displayprojinsb()
		#now refresh the gui parts to show the experiments of the new project (should be none at all)
		self._experiments = self.get_experiments()
		self.refresh_dash()

	def editproject_menuItemOnMenuSelection( self, event ):
		"""user selected "edit project" in menu.
		we let him edit the current project"""

		dial = PexDbViewerEditProjectDialog(self, self._fact, self._currentproject)
		res = dial.ShowModal()
		if res == wx.ID_CANCEL:
			return
		
		self._currentproject = dial.project
		self._fact.flush(self._currentproject)
		self.displayprojinsb()

	def reseed_factors_menuItemOnMenuSelection( self, event ):
		fpath = wx.FileSelector("Select factor definitions seed file",default_extension="json")

		if fpath is None:
			return

		seeder = SQPSeeder(self._fact, fpath)
		updct, insct = seeder.update_seeddata(FactorDefinition.Abbreviation)
		if updct > 0 or insct > 0:
			wx.MessageBox("{0} factor defintions were updated and {1} ned defintions were inserted".format(updct, insct))
		else:
			wx.MessageBox("No factor defintions were update or inserted")

if __name__ == '__main__':
	app = wx.App()
	frm = PexViewerMain(None)
	frm.Show()
	app.MainLoop()
	


