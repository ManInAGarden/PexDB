"""Subclass of AddFactorDialog, which is generated by wxFormBuilder."""

import wx
import GeneratedGUI
from PersistClasses import *
import sqlitepersist as sqp

# Implementing AddFactorDialog
class PexDbViewerAddFactorDialog( GeneratedGUI.AddFactorDialog ):
	def __init__( self, parent, fact : sqp.SQFactory, alreadyconnected : list):
		GeneratedGUI.AddFactorDialog.__init__( self, parent )
		self._alrconn = alreadyconnected
		self._fact = fact
		self._selectedfactor = None
		self._factorlist = []

	@property
	def selectedfactor(self):
		return self._selectedfactor

	def AddFactorDialogOnShow(self, event):

		if event.Show is False:
			return

		factdef_q = sqp.SQQuery(self._fact, FactorDefinition).where(FactorDefinition.IsActive==True and sqp.NotIsIn(FactorDefinition.Id, self._alrconn))
		
		self.m_factorsLCTR.ClearAll()
		self.m_factorsLCTR.InsertColumn(0, "Name")
		self.m_factorsLCTR.InsertColumn(1, "Unit")
		self._factorlist = list(factdef_q)
		ct = 0
		for fact in self._factorlist:
			idx = self.m_factorsLCTR.InsertItem(self.m_factorsLCTR.GetColumnCount(), fact.name)
			self.m_factorsLCTR.SetItemData(idx, ct)
			self.m_factorsLCTR.SetItem(idx, 1, fact.unit.abbreviation)
			ct += 1

	def m_sdbSizer3OnOKButtonClick(self, event):
		selidx = self.m_factorsLCTR.GetFirstSelected()
		if selidx == wx.NOT_FOUND:
			wx.MessageBox("Please select a factor in the list")
			return
		
		idx = self.m_factorsLCTR.GetItemData(selidx)
		self._selectedfactor = self._factorlist[idx]
		self.EndModal(wx.ID_OK)
