"""Subclass of LinRegrDialog.py, which is generated by wxFormBuilder."""
from cProfile import label
from pandas.core.frame import DataFrame
import wx
import wx.propgrid as pg
import GeneratedGUI
from PersistClasses import *
from MultiReg import *
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar2Wx

# Implementing LinRegrDialog.py
class PexDbViewerLinRegrDialog( GeneratedGUI.LinRegrDialog ):
	def __init__( self, parent, fact : sqp.SQFactory, proj : Project ):
		GeneratedGUI.LinRegrDialog.__init__(self, parent)
		self._f = fact
		self._p = proj
		self._floatpreci = 3
		self._forms = "{:." + str(self._floatpreci) + "f}" 
		self._float_factorpreci = 2
		self._factorforms = "{:." + str(self._float_factorpreci) + "f}" 
		self._currenttargabbr = None
		self._normalized = False

	def LinRegrDialogOnInitDialog( self, event ):
		self.m_projectNameSTXT.SetLabelText(self._p.name)
		self.m_linRegNBCK.SetSelection(0)
		self._solver = MultiReg(self._f, self._p, self._normalized)
		self._solver.read_data()

		done = False
		for respabbr, response in self._solver.respdict.items():
			self.m_targetCHOI.Append(response.name, respabbr)
			self.m_resiTargetCHOI.Append(response.name, respabbr)
			done = True

		if done:
			self.m_targetCHOI.Select(0)
			self.m_resiTargetCHOI.Select(0)

		self.m_factorPrecisionCHOI.Select(self._floatpreci)
		self.m_factorPrecisionCHOI.Select(self._float_factorpreci)

		self.m_summaryHTMLWIN.AppendToPage("Calculate to show summary here")
		self._crea_factnresprops()

	def m_targetCHOIOnChoice(self, event):
		sel = self.m_targetCHOI.GetSelection()

		if sel == wx.NOT_FOUND:
			return

		targresp = self._solver.resp_abbreviations[sel]
		self.m_formulaTBX.SetValue(self._solver.get_formula(self._factorforms, targresp))
		
		
		
	def _crea_factnresprops(self):
		for abbr, factdef in self._solver.factdict.items():
			lbl = factdef.name
			if factdef.unit is not None:
				lbl = lbl + " " + factdef.unit.abbreviation
			prp = pg.FloatProperty(label=lbl, name=abbr)
			self.m_factorsPGRD.Append(prp)

		for abbr, respdef in self._solver.respdict.items():
			lbl = respdef.name
			if respdef.unit is not None:
				lbl += " " + respdef.unit.abbreviation
			prp = pg.FloatProperty(label=lbl, name=abbr)
			self.m_responsesPGRD.Append(prp)
		
	def _get_floatstr(self, flnum):
		return self._forms.format(flnum)

	def show_input(self):
		df = self._solver.dataframe #already contains mean values in case of repetitions in the experiments
		
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
		for idx, row in df.iterrows():
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

	def _replaceabbr(self, txt : str):
		"""replace all abbreviations for factors and responses with their full names"""
		if txt is None: 
			return None

		answ = txt
		for key, resp in self._solver.respdict.items():
			answ = answ.replace(key, resp.name)
		for key, fact in self._solver.factdict.items():
			answ = answ.replace(key, fact.name)

		return answ

	def htmlsummary(self, coefs, intercs):
		answ = "<html>"
		answ += "<body>"
		answ += "<h1>Summary for project: " + self._p.name + "</h1>"

		answ += "<h2>{}</h2>".format("Coefficients and constants")
		if self._p.domergecalculation == True:
			answ += "Formula for merged_response: {}".format(self._p.mergeformula)

		answ += "<table>"

		answ += "<tr>"
		answ += "<td><b>{}</b></td>".format("/") 
		answ += "<td><b>{}</b></td>".format("c") 

		for key, fact in self._solver.factdict.items():
			answ += "<td><b>{}</b></td>".format(fact.name) 
		answ += "</tr>"
		fforms = "<td>" + self._forms + "</td>"
		l = 0
		for key, resp in self._solver.respdict.items():
			answ += "<tr>"
			answ += "<td><b>{}</b></td>".format(resp.name) 
			c = 0

			answ += fforms.format(intercs[l]) 

			for key, fact in self._solver.factdict.items():
				answ += fforms.format(coefs[l][c]) 
				c += 1
			answ += "</tr>"

			l += 1
		
		answ += "</table>"
		answ += "</body>"
		answ += "</html>"

		return answ

	def m_normalzedCHKBOnCheckBox(self, event):
		self._normalized = self.m_normalzedCHKB.GetValue()
		self._solver = MultiReg(self._f, self._p, self._normalized)
		self._solver.read_data()
		self.show_input()
		self.m_inputDataDLCTRL.Refresh()

	def doCalcBUTOnButtonClick(self, event):
		self._coefs, self._interc = self._solver.solve_for_all()
		self.m_summaryHTMLWIN.SetPage(self.htmlsummary(self._coefs, self._interc))

	def m_linRegNBCKOnNotebookPageChanged(self, event):
		if event.Selection == 1:
			self._initresidualspage()
		elif event.Selection == 2: #we have changed to page 1
			self._initpredictpage()

	def is_solved(self):
		if self._solver is None:
			return False
		if not hasattr(self._solver, "model"):
			return False
		if self._solver.model is None:
			return False

		return True

	def get_selected_predresp(self):
		selit = self.m_resiTargetCHOI.GetSelection()
		rabbr = self.m_resiTargetCHOI.GetClientData(selit)
		return rabbr

	def _showcurrentresidual(self):
		rabbr = self.get_selected_predresp()
		ress = self._solver.get_residuals(rabbr)
		self.m_axes.clear()
		self.m_axes.scatter(ress.axes[0], ress["realval"], color="r")
		self.m_axes.scatter(ress.axes[0], ress["predval"], color="b")
		self.m_axes.set_xlabel("experiment data point")
		self.m_axes.set_ylabel("response value")
		self.m_axes.set_title(self._solver.respdict[rabbr].name)
		self.m_axes.legend(labels=("measured response", "predicted response"))
		self.m_canvas.draw()
		#self.m_resiHelperPNL.Refresh()
	
	def _initresidualspage(self):
		"""initialise the page for showing the residuals"""
		if not self.is_solved():
			wx.MessageBox("Please execute solve first")
			return
		self._showcurrentresidual()
		

	def m_resiTargetCHOIOnChoice(self, event):
		self._showcurrentresidual()
	
	def _initpredictpage(self):
		if not self.is_solved():
			wx.MessageBox("Please execute solve first")
			return

		firsttarg = self._solver.resp_abbreviations[0]
		self.m_formulaTBX.SetLabelText(self._solver.get_formula(self._factorforms, firsttarg))
	
	def m_factorPrecisionCHOIOnChoice(self, event):
		if event.Selection is wx.NOT_FOUND: #get precision
			return
		
		self._float_factorpreci = event.Selection
		self._factorforms = "{:." + str(event.Selection) + "f}"

		sel = self.m_targetCHOI.GetSelection() #get target
		if sel == wx.NOT_FOUND:
			return

		targresp = self._solver.resp_abbreviations[sel]
		self.m_formulaTBX.SetLabelText(self._solver.get_formula(self._factorforms, targresp))
			

	def m_calcAllBUTOnButtonClick(self, event):
		if not self.is_solved():
			wx.MessageBox("Please do a solve before any predicting")

		fdict = {}
		for respabb in self._solver.resp_abbreviations:
			c = 0
			fdict.clear()
			for factabb in self._solver.fact_abbreviations:
				fdict[factabb] = self.m_factorsPGRD.GetPropertyValue(factabb)

			y = self._solver.predict(respabb, fdict)
			self.m_responsesPGRD.SetPropertyValue(respabb, y)

			
		