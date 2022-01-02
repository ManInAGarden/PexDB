"""Subclass of PexViewerMainFrame, which is generated by wxFormBuilder."""

from datetime import datetime
import csv
import wx
from wx.core import CENTRE, YES_NO
import wx.propgrid as pg
import creators as cr
import GeneratedGUI as gg #import generated GUI
from ConfigReader import *
from PexDbViewerEditFactorDefinitions import PexDbViewerEditFactorDefinitions
from PexDbViewerEditProjectDialog import PexDbViewerEditProjectDialog
from PexDbViewerEditResponseDefinitions import PexDbViewerEditResponseDefinitions
from PexDbViewerOpenProjectDialog import PexDbViewerOpenProjectDialog
from PropGridGUIMappers import *
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

		self._currentproject = self._get_current_proj()

		
	def _get_current_proj(self):
		"""get the youngest not archive project"""
		proj = sqp.SQQuery(self._fact, Project).where(Project.IsArchived==False).order_by(sqp.OrderInfo(Project.Created, 
																	sqp.OrderDirection.DESCENDING)).first_or_default(None)

		if proj is None:
			raise Exception("strangely no project was found to be used as an initial/default project")

		return proj

	def create_exp_gui(self):
		self._expgui = WxGuiMapperExperiment(self._fact, self.m_experimentPG, self._currentproject)
		#self._expgui.emptyallitems()
		self.m_experimentPG.Enable(False) #disable in case we have no data
		
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
	
	def _get_visr(self, exp):
		return [str(exp.sequence), exp.description]

	def refresh_dash(self):
		self.m_experimentsDataViewListCtrl.DeleteAllItems()
		ct = 0
		for exp in self._experiments:
			visr = self._get_visr(exp)
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
			self._expgui.emptyallitems()
			self.m_experimentPG.Enable(False)

	def refresh_dash_current(self):
		idx = -1
		for i in range(len(self._experiments)):
			if self._experiments[i]._id == self._currentexperiment._id:
				idx = i
				break

		if idx < 0:
			raise Exception("No current experiment found in list of experiments")

		self._experiments[idx] = self._currentexperiment
		self.m_experimentsDataViewListCtrl.DeleteItem(idx)
		self.m_experimentsDataViewListCtrl.InsertItem(idx, 
			self._get_visr(self._currentexperiment))

		self.m_experimentsDataViewListCtrl.Refresh()
		
	def get_experiments(self):
		q = sqp.SQQuery(self._fact, Experiment).where(Experiment.IsArchived == False 
			and Experiment.ProjectId==self._currentproject._id).order_by(Experiment.Sequence)
		experiments = []
		for exp in q:
			self._fact.fill_joins(exp,
				Experiment.Factors,
				Experiment.Responses)

			experiments.append(exp)

		return experiments

	def _initandseeddb(self):
		pclasses = [sqp.PCatalog, 
			Unit, 
			Project,
			ProjectFactorPreparation,
			Experiment, 
			Printer, 
			Extruder, 
			FactorDefinition, 
			FactorValue, 
			ResponseDefinition, 
			ProjectResponsePreparation,
			ResponseValue,
			ExperimentDoc]

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

		if ResponseDefinition in createds:
			sdr = sqp.SQPSeeder(self._fact, "./PexSeeds/responsedefinitions.json")
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
		"""The user selected the menuitem "create a single new experiment"
		"""
		if self._currentproject is None:
			raise Exception("We have no current project! Experiment cannot be created!")

		creator = cr.CreaSingle(self._fact, self._currentproject, self._prefprinter, self._prefextruder)
		ct, exp = creator.create()

		if ct==1 and exp is not None:
			self._experiments.append(exp)

		self.refresh_dash()


	def save_exp(self):
		self.get_changed_exp(self._currentexperiment)
		self._fact.flush(self._currentexperiment)
		for factor in self._currentexperiment.factors:
			self._fact.flush(factor)

		for response in self._currentexperiment.responses:
			self._fact.flush(response)

		self.refresh_dash_current()


	def experimentDWLC_selchanged( self, event):
		"""The user selected a row in the list of experiments"""

		if self._expgui.has_changed():
			self.save_exp()

		idx = self.m_experimentsDataViewListCtrl.GetSelectedRow()
		if idx == wx.NOT_FOUND:
			return

		selexp = self._experiments[idx]
		self.refresh_expview(selexp, self._expgui)
		self._currentexperiment = selexp
		self.m_experimentPG.Enable() #enable prop grid which should be filled with editable data now

	def refresh_expview(self, exp, expgui : WxGuiMapperExperiment):
		"""refresh the experiment data on the gui with the data of the given experiment"""

		#flatten the experiment data to a key, value dict
		vd = {}
		vd["sequence"] = exp.sequence
		vd["description"] = exp.description
		cdt = exp.carriedoutdt
		if cdt is not None:
			vd["carriedout_dt"] = exp.carriedoutdt.date()
			vd["carriedout_ti"] = exp.carriedoutdt.time()
		else:
			vd["carriedout_dt"] = None
			vd["carriedout_ti"] = None

		vd["extruderused"] = exp.extruderused
		vd["printerused"] = exp.printerused
		for setg in exp.factors:
			vd[setg.factordefinition.name] = self.get_typed_factor_value(setg.value, setg.factordefinition.disptype)

		for respg in exp.responses:
			vd[respg.responsedefinition.name] = respg.value

		expgui.object2gui(vd)
			
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
		elif vt is str:
			return val
		else:
			raise Exception("unsupported type {0} in get_store_str() for value <{1}>".format(str(vt), val))

	def get_changed_exp(self, exp: Experiment):
		valdict = self._expgui.gui2object()

		dt = valdict["carriedout_dt"]
		time = valdict["carriedout_ti"]
		if time is not None:
			if dt is not None:
				exp.carriedoutdt = datetime(dt.year, dt.month, dt.day, time.hour, time.minute, time.second)
			else:
				exp.carriedoutdt = None
		else:
			if dt is not None:
				exp.carriedoutdt = datetime(dt.year, dt.month, dt.day)
			else:
				exp.carriedoutdt = None

		exp.description = valdict["description"]
		exp.printerused = valdict["printerused"]
		exp.extruderused = valdict["extruderused"]
		exp.printerusedid = valdict["printerusedid"]
		exp.extruderusedid = valdict["extruderusedid"]

		#now handle alle the settings of the experiment

		for setg in exp.factors:
			key = setg.factordefinition.name
			setg.value = self.get_store_str(valdict[key])

		for setg in exp.responses:
			key = setg.responsedefinition.name
			setg.value = valdict[key]
		

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

	def edit_response_definitions(self, event):
		"""user clicked on edit result defs menu item"""
		dia = PexDbViewerEditResponseDefinitions(self, self._fact)
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
				self.create_exp_gui()
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

		seeder = sqp.SQPSeeder(self._fact, fpath)
		updct, insct = seeder.update_seeddata(FactorDefinition.Abbreviation)
		if updct > 0 or insct > 0:
			wx.MessageBox("{0} factor defintions were updated and {1} ned defintions were inserted".format(updct, insct))
		else:
			wx.MessageBox("No factor defintions were update or inserted")

	def get_crea_sequence(self):
		"""get the sequence value as an enum from the configuration"""
		cval = self._configuration.get_value("experimentcreation", "sequence")
		cvall = cval.lower()
		if cvall == "linear":
			return cr.CreaSequenceEnum.LINEAR
		elif cvall == "mixed":
			return cr.CreaSequenceEnum.MIXED
		else:
			wx.MessageBox("Configuration error, unknown sequence value <{}> in section experimentcreation".format(cval))
		

	def m_createFullFactorialMEIOnMenuSelection(self, event):
		if self._currentproject is None:
			wx.MessageBox("The current project is not defined. Experiment creation is impossible.")
			return

		q = sqp.SQQuery(self._fact, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==self._currentproject._id).select(lambda prep : prep._id)
		prpct = len(list(q))

		if prpct==0:
			wx.MessageBox("Please define some factor preparations by editing the project")
			return

		crea = cr.CreaFullFactorial(self._fact, 
			self._currentproject, 
			self._prefprinter, 
			self._prefextruder,
			self.get_crea_sequence())

		numexps = crea.create()

		self._experiments = self.get_experiments()
		self.refresh_dash()
		wx.MessageBox("{} Experiments were created under the current project".format(numexps))

	def m_deleteAllExperimentsMEIOnMenuSelection(self, event):
		res = wx.MessageBox("Are you sure to delete all experiments in the current project", "Delete all experiments", style=YES_NO|CENTRE)
		if res!=wx.YES:
			return

		exps_q = sqp.SQQuery(self._fact, Experiment).where(Experiment.ProjectId==self._currentproject._id)
		for exp in exps_q:
			self._fact.delete(exp) #we rely on cascaded deletes for factors and responses

		self._experiments = self.get_experiments()
		self.refresh_dash()

	def m_exportExperimentsCsvMEIOnMenuSelection(self, event):
		"""export all experiemnts to a csv ment to be imported in Excel or LibreOffice or ..."""
		filename = wx.FileSelector("Select csv file", 
			default_extension="csv", 
			wildcard="csv files (*.csv)|*.csv", 
			default_filename=self._currentproject.name + ".csv",
			flags=wx.FD_SAVE,
			parent=self)

		header = ["experiment"]
		factstart = len(header)
		fprep_q = sqp.SQQuery(self._fact, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==self._currentproject._id)
		fpreps = list(fprep_q)
		rprep_q = sqp.SQQuery(self._fact, ProjectResponsePreparation).where(ProjectResponsePreparation.ProjectId==self._currentproject._id)
		rpreps = list(rprep_q)

		for fprep in fpreps:
			fdef = fprep.factordefinition
			head = fdef.name
			if fdef.unit is not None:
				head += "[{}]".format(fdef.unit.abbreviation)

			header.append(head)

		for rprep in rpreps:
			fdef = rprep.responsedefinition
			head = fdef.name
			if fdef.unit is not None:
				head += "[{}]".format(fdef.unit.abbreviation)

			header.append(head)


		with open(filename, mode="w", encoding="UTF-8", newline="\n") as f:
			cwr = csv.writer(f)
			cwr.writerow(header)

			for exp in self._experiments:
				data = []
				data.append(exp.description)
				for fv in exp.factors:
					data.append(fv.value)
				for rv in exp.responses:
					data.append(rv.value)

				cwr.writerow(data)

if __name__ == '__main__':
	app = wx.App()
	frm = PexViewerMain(None)
	frm.Show()
	app.MainLoop()
	


