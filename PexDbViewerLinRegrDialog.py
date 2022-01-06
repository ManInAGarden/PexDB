"""Subclass of LinRegrDialog.py, which is generated by wxFormBuilder."""
from pandas.core.frame import DataFrame
import wx
import GeneratedGUI
from PersistClasses import *
from MultiReg import *

# Implementing LinRegrDialog.py
class PexDbViewerLinRegrDialog( GeneratedGUI.LinRegrDialog ):
	def __init__( self, parent, fact : sqp.SQFactory, proj : Project ):
		GeneratedGUI.LinRegrDialog.__init__(self, parent)
		self._f = fact
		self._p = proj
		self._floatpreci = 3
		self._forms = "{:." + str(self._floatpreci) + "f}" 

	def LinRegrDialogOnInitDialog( self, event ):
		self.m_projectNameSTXT.SetLabelText(self._p.name)
		self._solver = MultiReg(self._f, self._p)
		self._solver.read_data()
		
	def _get_floatstr(self, flnum):
		return self._forms.format(flnum)

	def show_input(self):
		df = self._solver.dataframe
		
		meanl = []
		for rprep in sqp.SQQuery(self._f, ProjectResponsePreparation).where(ProjectResponsePreparation.ProjectId==self._p._id):
			meanl.append(rprep.responsedefinition.abbreviation)	
		
		mi = df.mean(meanl)
		std= df.std()
	
		if self.m_inputDataDLCTRL.GetColumnCount() <= 0: #we do this the first time, we have to add columns
			self.m_inputDataDLCTRL.AppendTextColumn("#",
				align=wx.ALIGN_RIGHT)
			for abbr, fact in self._solver.factdict.items():
				col = self.m_inputDataDLCTRL.AppendTextColumn(fact.name, 
					align=wx.ALIGN_RIGHT)

			for abbr, resp in self._solver.respdict.items():
				self.m_inputDataDLCTRL.AppendTextColumn(resp.name,
					align=wx.ALIGN_RIGHT)
		else: #we are just refreshing the data,we have do remove any existing rows
			self.m_inputDataDLCTRL.DeleteAllItems()
		
		drow = []
		ct = 0
		for idx, row in mi.iterrows():
			drow.clear()
			ct += 1
			drow.append(str(ct))
			for abbr in self._solver.factdict:
				drow.append(self._get_floatstr(row[abbr]))

			for abbr in self._solver.respdict:
				drow.append(self._get_floatstr(row[abbr]))

			self.m_inputDataDLCTRL.AppendItem(drow)	

	def LinRegrDialogOnShow( self, event ):
		if event.Show is False:
			return

		self.show_input()
		
	def m_precisionCHOIOnChoice(self, event):
		choi = self.m_precisionCHOI.GetSelection()

		if choi == wx.NOT_FOUND:
			self._floatpreci = 3
		else:
			self._floatpreci = choi

		self._forms = "{:." + str(self._floatpreci) + "f}" 
		self.show_input()
		self.m_inputDataDLCTRL.Refresh()
		