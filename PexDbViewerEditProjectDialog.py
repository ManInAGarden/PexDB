"""Subclass of EditProjectDialog, which is generated by wxFormBuilder."""

import wx
from wx.core import NOT_FOUND
import GeneratedGUI
from PersistClasses import *
from PexDbViewerAddFactorDialog import PexDbViewerAddFactorDialog
from PexDbViewerAddResponseDialog import PexDbViewerAddResponseDialog
from PexDbViewerEditPreparation import PexDbViewerEditPreparation
import sqlitepersist as sqp

# Implementing EditProjectDialog
class PexDbViewerEditProjectDialog( GeneratedGUI.EditProjectDialog ):

	@property
	def project(self):
		return self._project

	def __init__( self, parent, fact : sqp.SQFactory, proj : Project ):
		GeneratedGUI.EditProjectDialog.__init__( self, parent )

		self._fact = fact
		self._project = proj

	def EditProjectDialogOnShow( self, event ):
		if event.Show is False:
			return

		self._factorpreps = []
		self._responsepreps = []
		connf_q = sqp.SQQuery(self._fact, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==self._project._id)
		self._factorpreps = list(connf_q)

		connr_q = sqp.SQQuery(self._fact, ProjectResponsePreparation).where(ProjectResponsePreparation.ProjectId==self._project._id)
		self._responsepreps = list(connr_q)

		self.fill_gui(self._project, self._factorpreps, self._responsepreps)

	def get_txtval(self, text):
		if text is None:
			return ""
		else:
			return text

	def fill_gui(self, pro, factpreps, resppreps):
		self.m_nameTB.SetValue(pro.name)
		self.m_isArchivedCBX.SetValue(pro.isarchived)
		self.m_descriptionTBX.SetValue(self.get_txtval(pro.description))
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

		self.m_respPrepsLCTR.ClearAll()
		self.m_respPrepsLCTR.InsertColumn(0, "Response", width=200)

		ct = 0
		for rprep in self._responsepreps:
			idx = self.m_respPrepsLCTR.InsertItem(self.m_prepsLCTRL.GetColumnCount(), rprep.responsedefinition.name)
			self.m_respPrepsLCTR.SetItemData(idx, ct)
			ct += 1
		

	def m_okcancelBUTSOnOKButtonClick( self, event ):
		self._project.name = self.m_nameTB.GetValue()
		self._project.isarchived = self.m_isArchivedCBX.GetValue()
		self._project.description = self.m_descriptionTBX.GetValue()

		statidx = self.m_projectstatusCOB.GetSelection()
		if statidx == wx.NOT_FOUND:
			self._project.status = None
		else:
			self._project.status = self._pstatcat[statidx]

		self.EndModal(wx.ID_OK)

	def m_connfactorBUOnButtonClick( self, event ):
		dial = PexDbViewerAddFactorDialog(self, self._fact, list(map(lambda pr : pr.factordefinitionid, self._factorpreps)))
		res = dial.ShowModal()

		if res == wx.ID_CANCEL:
			return

		newfact = dial.selectedfactor

		newprep = ProjectFactorPreparation(projectid=self._project._id, 
			factordefinitionid = newfact._id,
			factordefinition=newfact,
			minvalue = newfact.defaultmin,
			maxvalue = newfact.defaultmax,
			levelnum = newfact.defaultlevelnum)

		self._fact.flush(newprep)
		self._factorpreps.append(newprep)
		self.fill_gui(self._project, self._factorpreps, self._responsepreps)


	def m_removefactorBUOnButtonClick( self, event ):
		selidx = self.m_prepsLCTRL.GetFirstSelected()

		if selidx==wx.NOT_FOUND:
			wx.MessageBox("please select a factor preparation to be removed")
			return

		idx = self.m_prepsLCTRL.GetItemData(selidx)
		remoprep = self._factorpreps.pop(idx)

		self._fact.delete(remoprep)		
		self.fill_gui(self._project, self._factorpreps, self._responsepreps)

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
		self.fill_gui(self._project, self._factorpreps, self._responsepreps)

	def m_addRespPrepBUTOnButtonClick(self, event):
		dial = PexDbViewerAddResponseDialog(self, self._fact, list(map(lambda pr : pr.responsedefinitionid, self._responsepreps)))
		res = dial.ShowModal()

		if res == wx.ID_CANCEL:
			return

		selresp = dial.selectedresponse

		newprep = ProjectResponsePreparation(projectid=self._project._id, 
		 	responsedefinitionid = selresp._id,
		 	responsedefinition=selresp)

		self._fact.flush(newprep)
		self._responsepreps.append(newprep)
		self.fill_gui(self._project, self._factorpreps, self._responsepreps)

	def m_deleteRespPrepBUTOnButtonClick(self, event):
		selidx = self.m_respPrepsLCTR.GetFirstSelected()

		if selidx==wx.NOT_FOUND:
			wx.MessageBox("please select a response preparation to be removed")
			return

		idx = self.m_respPrepsLCTR.GetItemData(selidx)
		remoprep = self._responsepreps.pop(idx)

		self._fact.delete(remoprep)		
		self.fill_gui(self._project, self._factorpreps, self._responsepreps)

