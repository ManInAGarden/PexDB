"""Subclass of CreateFullDetailsDialog, which is generated by wxFormBuilder."""

import wx
import GeneratedGUI
import creators as cr
from PersistClasses import *
import logging

# Implementing CreateFullDetailsDialog
class PexDbViewerCreateFullDetailsDialog( GeneratedGUI.CreateFullDetailsDialog ):
	def __init__( self, parent, dbfact, project, printer, extruder):
		GeneratedGUI.CreateFullDetailsDialog.__init__( self, parent )
		self._fact = dbfact
		self._project = project
		self._printer = printer
		self._extruder = extruder
		self._sequence = cr.CreaSequenceEnum.LINEAR
		self._logger = logging.getLogger("mainprog")
		self._logger.debug("Dialog %s inited", self.__class__.__name__)


	def _get_sequence(self):
		idx = self.m_sequenceCHOI.GetSelection()
		if idx != wx.NOT_FOUND:
			if idx == 0:
				return cr.CreaSequenceEnum.LINEAR
			elif idx == 1:
				return cr.CreaSequenceEnum.MIXED
			else:
				raise Exception("Unknown sequence!")


	def _get_repetions(self):
		reps = self.m_repetitionsSPCTRL.GetValue()
		if reps == 0:
			reps = 1

		return reps

	def _get_planneddt(self):
		wxdt = self.m_datePicker1.GetValue()

		if wxdt.IsValid():
			return datetime(wxdt.year, wxdt.month+1, wxdt.day)
		else:
			return None

	def _get_do_centre(self):
		return self.m_createCentreExpCKBX.GetValue()

	def m_sdbSizer6OnOKButtonClick(self, event):
		"""User clicked OK which means we have to do the creation now"""
		self._sequence = self._get_sequence()
		self._repetitions = self._get_repetions()
		self._planneddt = self._get_planneddt()
		self._docenctre = self._get_do_centre()
		
		try:
			self._do_create()
		except Exception as exc:
			self._logger.error("A problem occured during creation of the experiments. Original msg: %s", str(exc))
			wx.MessageBox("A problem occured during creation of the experiments. Original msg: {}".format(str(exc)))
			
		self.EndModal(wx.ID_OK)

	def _do_create(self):
		q = sqp.SQQuery(self._fact, ProjectFactorPreparation).where(ProjectFactorPreparation.ProjectId==self._project._id).select(lambda prep : prep._id)
		prpct = len(list(q))

		if prpct==0:
			wx.MessageBox("Please define some factor preparations by editing the project")
			return

		crea = cr.CreaFullFactorial(self._fact, 
			self._project, 
			self._printer, 
			self._extruder,
			self._sequence,
			self._planneddt,
			self._repetitions,
			self._docenctre)

		self.numexps = crea.create()

	



