"""Subclass of CreateFractDetail, which is generated by wxFormBuilder."""
from email.message import Message
from tkinter import messagebox
from xml.dom import NotSupportedErr
import wx
import GeneratedGUI
from creators.CreaBasics import CreaSequenceEnum
from creators.CreaFractFactorial import CreaFractFactorial

import sqlitepersist as sqp
import creators as cr
from PersistClasses import *

# Implementing CreateFractDetail
class PexDbViewerCreateFractDetailDialog( GeneratedGUI.CreateFractDetail ):
	def __init__( self, parent, dbfact, project, printer, extruder ):
		GeneratedGUI.CreateFractDetail.__init__( self, parent)
		self._fact = dbfact
		self._project = project
		self._printer = printer
		self._extruder = extruder
		self._sequence = cr.CreaSequenceEnum.LINEAR

	def _getformula(self, cprep):
		answ = ""

		if cprep.factordefs is None:
			return answ

		if cprep.isnegated:
			answ += "-"

		for finter in cprep.factordefs:
			answ += "<{}>".format(finter.factordefinition.name)

		return answ
		
	def _getstr(self, ins):
		if ins is None:
			return ""
		else:
			return str(ins)

	def _get_factordefstr(self):
		havesome = False
		first = True
		for fprep in self._factpreps:
			if first:
				fstr = "<p>" + fprep.factordefinition.name
				first = False
			else:
				fstr += "<br><p>" + fprep.factordefinition.name

			if fprep.iscombined:
				havesome = True
				self._fact.fill_joins(fprep, ProjectFactorPreparation.FactorCombiDefs)
				first_2 = True
				if fprep.isnegated:
					fstr += " = -"
				else:
					fstr += " = "

				for fcdinter in fprep.factorcombidefs:
					if first_2:
						first_2 = False
						fstr += "&lt;" + fcdinter.factordefinition.name + "&gt"
					else:
						fstr += "*" + "&lt;" + fcdinter.factordefinition.name  + "&gt"
				
			fstr += "</p>"

		return havesome, fstr

	def fill_combipreps_gui(self):
		havesome, factstr = self._get_factordefstr()
		html = "<html><body>"
		if havesome:
			html += "<h1>Combination definition</h1>"
			html += "<p>(like defined in project factor preparations)</p>"
			html += "<p>"
			html += factstr
			html += "</p>"
		else:
			html += "No factor combinations are defined in the factor factor preparations of this project. "
			html += "A full factorial scheme will be used to create the experiments."
		html += "</body></html>"

		self.m_combiInfoHTML.SetPage(html)

	# Handlers for CreateFractDetail events.
	def CreateFractDetailOnInitDialog( self, event ):
		self._factpreps = list(sqp.SQQuery(self._fact, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==self._project._id))
		self.fill_combipreps_gui()

	def CreateFractDetailOnShow( self, event ):
		if not event.Show:
			return

	def _get_sequence_enum(self) -> CreaSequenceEnum:
		seqidx = self.m_sequenceCHOI.GetSelection()
		if seqidx == wx.NOT_FOUND:
			raise Exception("No sequence selected - please select a sequence")

		if seqidx == 0:
			return CreaSequenceEnum.LINEAR
		elif seqidx == 1:
			return CreaSequenceEnum.MIXED
		else:
			raise NotSupportedErr("Usupported choice index for sequence")
		
	def _get_datetime(self, wxdt : wx.DateTime):
		# mostly stolen from here:
		# https://www.blog.pythonlibrary.org/2014/08/27/wxpython-converting-wx-datetime-python-datetime/
		
		if wxdt is None:
			return None
		assert isinstance(wxdt, wx.DateTime)
		if wxdt.IsValid():
			ymd = map(int, wx.FormatISODate().split('-'))
			return datetime.date(*ymd)
		else:
			return None

	def m_sdbSizer6OnOKButtonClick( self, event ):
		try:
			seq = self._get_sequence_enum()
			plandt = self._get_datetime(self.m_datePicker1.GetValue())
			reps = self.m_repetitionsSPCTRL.GetValue()
			docentre = self.m_createCentreExpCKBX.GetValue()
			crea = CreaFractFactorial(self._fact,
				self._project,
				self._printer,
				self._extruder,
				seq,
				plandt,
				reps,
				docentre)
			
			experi_ct = crea.create()

			wx.MessageBox("{} experiments have been created.".format(experi_ct))
			
			self.EndModal(wx.ID_OK)
		except Exception as exc:
			wx.MessageBox("Error during experiment creation. Original message: {}".format(str(exc)))



