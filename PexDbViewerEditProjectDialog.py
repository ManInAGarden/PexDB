"""Subclass of EditProjectDialog, which is generated by wxFormBuilder."""

import wx
from wx.core import NOT_FOUND
import GeneratedGUI
from PersistClasses import *
from PexDbViewerAddSubElementDialog import PexDbViewerAddSubElementDialog
from PexDbViewerEditPreparation import PexDbViewerEditPreparation
from PexDbViewerEditResponsePreparation import PexDbViewerEditResponsePreparation
import sqlitepersist as sqp
from Validators import MergeFormulaValidator

# Implementing EditProjectDialog
class PexDbViewerEditProjectDialog( GeneratedGUI.EditProjectDialog ):

	@property
	def project(self):
		return self._project

	def __init__( self, parent, fact : sqp.SQFactory, proj : Project ):
		GeneratedGUI.EditProjectDialog.__init__( self, parent )

		self._fact = fact
		self._project = proj
		self._factorpreps = []
		self._responsepreps = []
		self._enviropreps = []

	def replace_spaces(self, inps : str) -> str:
		if inps is None:
			return None

		return inps.replace(" ", "_")

	def EditProjectDialogOnInitDialog(self, event):
		connf_q = sqp.SQQuery(self._fact, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==self._project._id)
		self._factorpreps = list(connf_q)

		connr_q = sqp.SQQuery(self._fact, ProjectResponsePreparation).where(ProjectResponsePreparation.ProjectId==self._project._id)
		self._responsepreps = list(connr_q)

		globals = {}
		for respprep in self._responsepreps:
			globals[self.replace_spaces(respprep.responsedefinition.name)] = 1.0

		self.m_mergeFormulaTBX.SetValidator(MergeFormulaValidator(globals))

		enviro_q = sqp.SQQuery(self._fact, ProjectEnviroPreparation).where(ProjectEnviroPreparation.ProjectId==self._project._id)
		self._enviropreps = list(enviro_q)

	def EditProjectDialogOnShow( self, event ):
		if event.Show is False:
			return

		self.fill_gui(self._project)

	def get_txtval(self, text, default=""):
		if text is None:
			return default
		else:
			return text

	def get_boolval(self, bo, default=False):
		if bo is None:
			return default
		else:
			return bo

	def fill_gui(self, pro : Project):
		self.m_nameTB.SetValue(pro.name)
		self.m_isArchivedCBX.SetValue(pro.isarchived)
		self.m_descriptionTBX.SetValue(self.get_txtval(pro.description))
		self.m_doMergeCBX.SetValue(self.get_boolval(pro.domergecalculation))
		self.m_mergeFormulaTBX.SetValue(self.get_txtval(pro.mergeformula))
		if pro.domergecalculation is not None:
			self.m_mergeFormulaTBX.Enable(pro.domergecalculation)
		else:
			self.m_mergeFormulaTBX.Enable(False)

		ps_q = sqp.SQQuery(self._fact, ProjectStatusCat).where(ProjectStatusCat.LangCode==self._fact.lang)
		self._pstatcat = []
		ct = 0
		sel = wx.NOT_FOUND
		for ps in ps_q:
			self._pstatcat.append(ps)
			if not pro.status is None and ps.code == pro.status.code:
				sel = ct
			ct += 1
		choicevals = list(map(lambda ps : ps.value, self._pstatcat))
		self.m_projectstatusCOB.SetItems(choicevals)
		self.m_projectstatusCOB.SetSelection(sel)

		self.m_prepsLCTRL.ClearAll()
		self.m_prepsLCTRL.InsertColumn(0, "Factor", width=200)
		self.m_prepsLCTRL.InsertColumn(1, "Minimum value", wx.LIST_FORMAT_RIGHT)
		self.m_prepsLCTRL.InsertColumn(2, "Maximum value",  wx.LIST_FORMAT_RIGHT)
		self.m_prepsLCTRL.InsertColumn(3, "Number of levels",  wx.LIST_FORMAT_RIGHT)

		ct = 0
		for fprep in self._factorpreps:
			idx = self.m_prepsLCTRL.InsertItem(self.m_prepsLCTRL.GetColumnCount(), fprep.factordefinition.name)
			self.m_prepsLCTRL.SetItemData(idx, ct)
			self.m_prepsLCTRL.SetItem(idx, 1, str(fprep.minvalue))
			self.m_prepsLCTRL.SetItem(idx, 2, str(fprep.maxvalue))
			self.m_prepsLCTRL.SetItem(idx, 3, str(fprep.levelnum))
			ct += 1

		#self._fill_list(self.m_prepsLCTRL, self._factorpreps)
		self._fill_list(self.m_respPrepsLCTR, self._responsepreps)
		self._fill_list(self.m_envoroPrepsLCTRL, self._enviropreps)

	def _fill_list(self, lctr, litems : list):
		lctr.ClearAll()
		lctr.InsertColumn(0, "Name", width=200)
		lctr.InsertColumn(1, "Unit", width=80)

		ct = 0
		for litem in litems:
			idx = lctr.InsertItem(lctr.GetColumnCount(), litem.name)
			lctr.SetItemData(idx, ct)
			lctr.SetItem(idx, 1, str(litem.unit))
			ct += 1
		

	def m_okcancelBUTSOnOKButtonClick( self, event ):
		if not self.Validate():
			return

		self._project.name = self.m_nameTB.GetValue()
		self._project.isarchived = self.m_isArchivedCBX.GetValue()
		self._project.description = self.m_descriptionTBX.GetValue()
		self._project.domergecalculation = self.m_doMergeCBX.GetValue()
		self._project.mergeformula = self.m_mergeFormulaTBX.GetValue()

		statidx = self.m_projectstatusCOB.GetSelection()
		if statidx == wx.NOT_FOUND:
			self._project.status = None
		else:
			self._project.status = self._pstatcat[statidx]

		self.EndModal(wx.ID_OK)

	def m_doMergeCBXOnCheckBox(self, event):
		formactive = self.m_doMergeCBX.GetValue()
		if formactive is not None and formactive==True:
			self.m_mergeFormulaTBX.Enable(True)
		else:
			self.m_mergeFormulaTBX.Enable(False)

	def m_connfactorBUOnButtonClick( self, event ):
		dial = PexDbViewerAddSubElementDialog(self, self._fact,
			FactorDefinition,
			"factor definition",
			list(map(lambda pr : pr.factordefinitionid, self._factorpreps)) )

		res = dial.ShowModal()
		if res == wx.ID_CANCEL:
			return

		newfact = dial.selected

		newprep = ProjectFactorPreparation(projectid=self._project._id, 
			factordefinitionid = newfact._id,
			factordefinition=newfact,
			minvalue = newfact.defaultmin,
			maxvalue = newfact.defaultmax,
			levelnum = newfact.defaultlevelnum)

		self._fact.flush(newprep)
		self._factorpreps.append(newprep)
		self.fill_gui(self._project)


	def m_removefactorBUOnButtonClick( self, event ):
		selidx = self.m_prepsLCTRL.GetFirstSelected()

		if selidx==wx.NOT_FOUND:
			wx.MessageBox("please select a factor preparation to be removed")
			return

		idx = self.m_prepsLCTRL.GetItemData(selidx)
		remoprep = self._factorpreps.pop(idx)

		self._fact.delete(remoprep)		
		self.fill_gui(self._project)

	def editPrepBUOnButtonClick(self, event):
		selidx = self.m_prepsLCTRL.GetFirstSelected()

		if selidx==wx.NOT_FOUND:
			wx.MessageBox("please select a factor preparation to be edited")
			return

		idx = self.m_prepsLCTRL.GetItemData(selidx)
		
		dial = PexDbViewerEditPreparation(self, self._factorpreps[idx])
		res = dial.ShowModal()
		if res == wx.ID_CANCEL:
			return

		self._fact.flush(dial.editedprep)
		self._factorpreps[idx] = dial.editedprep
		self.fill_gui(self._project)

	def m_editRespPrepBUTOnButtonClick(self, event):
		selit = self.m_respPrepsLCTR.GetFirstSelected()
		if selit is wx.NOT_FOUND:
			return

		selidx = self.m_respPrepsLCTR.GetItemData(selit)
		rprep = self._responsepreps[selidx]
		dial = PexDbViewerEditResponsePreparation(self, rprep)
		res = dial.ShowModal()

		if res != wx.ID_OK:
			return

		self._responsepreps[selidx] = dial.respprep
		self._fact.flush(dial.respprep)
		self.fill_gui(self._project)


	def m_addRespPrepBUTOnButtonClick(self, event):
		dial = PexDbViewerAddSubElementDialog(self,
			self._fact,
			ResponseDefinition,
			"response definition",
			list(map(lambda pr : pr.responsedefinitionid, self._responsepreps)))
		res = dial.ShowModal()

		if res == wx.ID_CANCEL:
			return

		selresp = dial.selected

		newprep = ProjectResponsePreparation(projectid=self._project._id, 
		 	responsedefinitionid = selresp._id,
		 	responsedefinition=selresp)

		self._fact.flush(newprep)
		self._responsepreps.append(newprep)
		self.fill_gui(self._project)

	def m_deleteRespPrepBUTOnButtonClick(self, event):
		selidx = self.m_respPrepsLCTR.GetFirstSelected()

		if selidx==wx.NOT_FOUND:
			wx.MessageBox("please select a response preparation to be removed")
			return

		idx = self.m_respPrepsLCTR.GetItemData(selidx)
		remoprep = self._responsepreps.pop(idx)

		self._fact.delete(remoprep)		
		self.fill_gui(self._project)

	def m_editEnviroBUTOnButtonClick(self, event):
		pass

	def m_addEnviroBUTOnButtonClick(self, event):
		dial = PexDbViewerAddSubElementDialog(self, 
			self._fact, 
			EnviroDefinition, 
			"environment definition",
			list(map(lambda envp : envp.envirodefinitionid, self._enviropreps)))
		res = dial.ShowModal()

		if res != wx.ID_OK:
			return

		evp = ProjectEnviroPreparation(projectid=self._project._id,
			envirodefinition=dial.selected,
			envirodefinitionid = dial.selected._id)

		self._fact.flush(evp)
		self._enviropreps.append(evp)
		self.fill_gui(self._project)



	def m_removeEnviroBUTOnButtonClick(self, event):
		pass
