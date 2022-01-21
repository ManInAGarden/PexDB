from datetime import datetime
from genericpath import isdir
import os
import tempfile as tmpf
import csv
import wx
from wx.core import CENTRE, YES_NO, Bitmap, FileDialog, FileSelector, Image, MessageBox, NullBitmap
from wx.dataview import DATAVIEW_CELL_EDITABLE
import wx.propgrid as pg
from ExtOpener import ExtOpener
from PexDbViewerLinRegrDialog import PexDbViewerLinRegrDialog
import creators as cr
import GeneratedGUI as gg #import generated GUI
from ConfigReader import *
from DocArchiver import *
from PexDbViewerEditFactorDefinitions import PexDbViewerEditFactorDefinitions
from PexDbViewerEditProjectDialog import PexDbViewerEditProjectDialog
from PexDbViewerEditResponseDefinitions import PexDbViewerEditResponseDefinitions
from PexDbViewerOpenProjectDialog import PexDbViewerOpenProjectDialog
from PexDbViewerCreateFullDetailsDialog import PexDbViewerCreateFullDetailsDialog
from PropGridGUIMappers import *
import sqlitepersist as sqp
from PersistClasses import *
from sqlitepersist.SQLitePersistBasicClasses import PCatalog

# Implementing PexViewerMainFrame
class PexViewerMain( gg.PexViewerMainFrame ):
	"""Subclass of PexViewerMainFrame, which is generated by wxFormBuilder."""
	def __init__(self, parent ):
		#gg.PexViewerMainFrame.__init__( self, parent )
		super().__init__(parent)
		self.init_prog()
		self.init_archive()
		self.init_db()
		self.init_gui()

	def init_prog(self):
		self._configuration = ConfigReader("./PexDb.conf")

	def init_archive(self):
		tdir = tmpf.gettempdir()
		extdir = tdir + path.sep + self._configuration.get_value("archivestore", "localtemp")
		if not path.exists(extdir):
			mkdir(extdir)

		self._extractionpath = extdir

		apath = self._configuration.get_value_interp("archivestore","path")
		if os.path.exists(apath):
			self._docarchive = DocArchiver(apath) #use existing archive
			return

		dnum = self._configuration.get_value("archivestore", "dirnum")
		if dnum <= 0:
			raise Exception("Configuration Error - dirnum must be a positive integer")
		
		#we are starting for the first time, so we initialize the document archive here
		DocArchiver.prepare_archive(apath, dnum)
		self._docarchive = DocArchiver(apath) #use neew archive


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

		self.m_docNameDVLC = self.m_expDocsDVLCTR.AppendTextColumn( "Name", wx.dataview.DATAVIEW_CELL_EDITABLE, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE)
		self.m_docNameDVLC.GetRenderer().EnableEllipsize( wx.ELLIPSIZE_END )
		self.m_filePathDVLC = self.m_expDocsDVLCTR.AppendTextColumn("File path", 
			wx.dataview.DATAVIEW_CELL_INERT, 
			-1, 
			wx.ALIGN_LEFT, 
			wx.dataview.DATAVIEW_COL_RESIZABLE)
		self.m_filePathDVLC.GetRenderer().EnableEllipsize( wx.ELLIPSIZE_START )
		self.m_docTypeDVLC = self.m_expDocsDVLCTR.AppendTextColumn( "Document type", wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE|wx.dataview.DATAVIEW_COL_SORTABLE)
		self.m_docTypeDVLC.GetRenderer().EnableEllipsize( wx.ELLIPSIZE_END )

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
			self.refresh_exp_docs()
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
				Experiment.Responses,
				Experiment.Docs)

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
			ProjectEnviroPreparation,
			EnviroDefinition,
			EnviroValue,
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

		if EnviroDefinition in createds:
			sdr = sqp.SQPSeeder(self._fact, "./PexSeeds/envirodefinitions.json")
			sdr.create_seeddata()

		if Project in createds:
			newproj = Project(name="std", status=self._fact.getcat(ProjectStatusCat, "INIT"))
			self._fact.flush(newproj)

	def cleanup_temp(self):
		if not os.path.exists(self._extractionpath):
			return

		if not os.path.isdir(self._extractionpath):
			return

		list_of_files = []
		for root, dirs, files in os.walk(self._extractionpath):
			for filename in files:
				list_of_files.append(os.path.join(root,filename))

		for filename in list_of_files:
			if os.path.isfile(filename):
				os.remove(filename)
			elif os.path.isdir(filename):
				os.rmdir(filename)

		#lastly remove the temp-dir used for temporary extraction
		os.rmdir(self._extractionpath)

	# Handlers for PexViewerMainFrame events.
	def quit_PexViewer( self, event ):
		"""The user selected the menu item "close PexDbViewer"
		"""
		self.cleanup_temp()
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
		self.refresh_exp_docs()
		self.m_experimentPG.Enable() #enable prop grid which should be filled with editable data now

	def refresh_exp_docs(self):
		"""refreshes the view of the current experiment's documents"""
		if self._currentexperiment is None:
			return

		self.m_expDocsDVLCTR.DeleteAllItems()
		if self._currentexperiment.docs is not None and len(self._currentexperiment.docs) > 0:
			ct = 0
			for doc in self._currentexperiment.docs:
				att = None
				if doc.attachmenttype is not None:
					att = doc.attachmenttype.value

				line = [doc.name, doc.filepath, att]
				self.m_expDocsDVLCTR.AppendItem(line, ct)
				ct += 1

	def refresh_expview(self, exp, expgui : WxGuiMapperExperiment):
		"""refresh the experiment data on the gui with the data of the given experiment"""

		#flatten the experiment data to a key, value dict
		vd = {}
		vd["sequence"] = exp.sequence
		vd["repnum"] = exp.repnum
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
		
		#exp.sequence = valdict["sequence"]
		#exp.repnum = valdict["repnum"]
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
		aexp.responses = []

		for factval in exp.factors:
			nfact = FactorValue(experimentid=aexp._id,
				factordefinitionid=factval.factordefinitionid,
				factordefinition=factval.factordefinition,
				value = factval.value)
			aexp.factors.append(nfact)
			self._fact.flush(nfact)

		for respval in exp.responses:
			nresp = ResponseValue(experimentid=aexp._id,
				responsedefinitionid=respval.responsedefinitionid,
				responsedefinition=respval.responsedefinition,
				value=respval.value)
			aexp.responses.append(nresp)

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
			wx.MessageBox("{0} factor defintions were updated and {1} defintions were inserted".format(updct, insct))
		else:
			wx.MessageBox("No factor defintions were updated or inserted")

	def m_reseedCatsMEITOnMenuSelection(self, event):
		fpath = wx.FileSelector("Select catalog definitions seed file", default_extension="json")

		if fpath is None:
			return

		seeder = sqp.SQPSeeder(self._fact, fpath)
		updct, insct = seeder.update_seeddata3k(PCatalog.Type, PCatalog.Code, PCatalog.LangCode)
		if updct > 0 or insct > 0:
			wx.MessageBox("{0} catalog defintions were updated and {1} defintions were inserted".format(updct, insct))
		else:
			wx.MessageBox("No catalog defintions were updated or inserted")

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

		dial = PexDbViewerCreateFullDetailsDialog(self, 
			self._fact, 
			self._currentproject,
			self._prefprinter,
			self._prefextruder)

		res = dial.ShowModal()

		if res==wx.ID_OK:
			self._experiments = self.get_experiments()
			self.refresh_dash()
			wx.MessageBox("{} Experiments were created under the current project".format(dial.numexps))


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

	def m_linearRegrMEIOnMenuSelection(self, event):
		dial = PexDbViewerLinRegrDialog(self, self._fact, self._currentproject)
		res = dial.ShowModal()

	def m_newExpDocBUOnButtonClick(self, event):
		if self._currentexperiment is None:
			return

		doc = ExperimentDoc(experimentid=self._currentexperiment._id,
			name = "New document")
		self._fact.flush(doc)
		if self._currentexperiment.docs is None:
			self._currentexperiment.docs = []

		self._currentexperiment.docs.append(doc)
		self.refresh_exp_docs()

	def _getseldocnum(self):
		seldoci = self.m_expDocsDVLCTR.GetSelection()
		if not seldoci.IsOk():
			return None

		return self.m_expDocsDVLCTR.GetItemData(seldoci)

	def m_delExpDocBUOnButtonClick(self, event):
		if self._currentexperiment is None or self._currentexperiment.docs is None or len(self._currentexperiment.docs) <= 0:
			return

		docnum = self._getseldocnum()
		if not docnum is None:
			doc = self._currentexperiment.docs[docnum]
			#NICHT NÖTIG ES GIBT on_after_delete!
			# if doc.filepath is not None and len(doc.filepath) > 0:
			# 	self._docarchive.remove_file(doc.filepath)

			self._fact.delete(doc)
			self._currentexperiment.docs.remove(doc)
			self.refresh_exp_docs()

	def m_uploadExpDocBUTOnButtonClick(self, event):
		if self._currentexperiment is None or self._currentexperiment.docs is None:
			return
		if len(self._currentexperiment.docs) <= 0:
			return

		selidx = self._getseldocnum()
		if selidx is None:
			MessageBox("Select a document entry fist to upload a fle document to")
			return
		
		selexpdoc = self._currentexperiment.docs[selidx]
		fname = FileSelector("Select a document",
			flags = wx.FD_OPEN)

		if fname is None:
			return

		archipath, ext = self._docarchive.archive_file(fname)
		selexpdoc.filepath = archipath
		selexpdoc.attachmenttype = self.get_attach_type(ext)
		self._fact.flush(selexpdoc)
		self.refresh_exp_docs()

	def get_attach_type(self, ext):
		tstr = ext.removeprefix(".")
		tstr = tstr.upper()
		return self._fact.getcat(ExpAttachmentTypeCat, tstr)

	def m_openExpDocAttachmntBUTOnButtonClick(self, event):
		"""open attachment of an experiment doc"""
		if self._currentexperiment is None or self._currentexperiment.docs is None:
			return
		if len(self._currentexperiment.docs) <= 0:
			return

		selidx = self._getseldocnum()
		if selidx is None:
			MessageBox("Select a document entry first to open the attachment of that document")
			return

		seldoc = self._currentexperiment.docs[selidx]
		if seldoc.filepath is not None and len(seldoc.filepath) > 0:
			extrname = self._docarchive.extract_file(seldoc.filepath, self._extractionpath)
			opn = ExtOpener(extrname).open(showshell=True)

	def m_expDocsDVLCTROnDataViewListCtrlItemEditingDone(self, event):
		edicol = event.Column
		newval = event.Value
		selidx = event.Selection

		docidx = self.m_expDocsDVLCTR.GetItemData(event.Item)
		doc = self._currentexperiment.docs[docidx]
		dosave = False
		if edicol==0:
			doc.name = newval
			dosave = True

		self.m_expDocsDVLCTR.SetValue(newval, docidx, edicol)		
		if dosave:
			self._fact.flush(doc)

if __name__ == '__main__':
	app = wx.App()
	frm = PexViewerMain(None)
	frm.Show()
	app.MainLoop()
	


