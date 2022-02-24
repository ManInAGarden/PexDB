"""Subclass of AboutDialog, which is generated by wxFormBuilder."""
import importlib.metadata
import json
from os import path
import wx
import GeneratedGUI

# Implementing AboutDialog
class PexDbViewerAboutDialog( GeneratedGUI.AboutDialog ):
	def __init__( self, parent, apppath ):
		GeneratedGUI.AboutDialog.__init__(self, parent,)
		self._progversion = parent._version
		self._apppath = apppath
		self._do_init_dialog()

	def _do_init_dialog(self):
		deps = self.read_deps()
		htxt = "<html><body>"
		htxt += "</body></html>"
		htxt += "<h1>About PexDB V{}</h1><p>".format(self._progversion)
		htxt += "PexDB is a database and calculation tool for planning and evaluation of experiments with the "
		htxt += "aim of optimising the quality of FDM 3D prints. Ideas derived from DOE (design of experiments) "
		htxt += "are applied to achieve this."
		htxt += "</p><p>"

		htxt += "The following python modules and program libraries are used for PexDB:"
		htxt += "</p><p>"

		htxt += "<table>"
		htxt += "<tr>"
		htxt += "<td><b>{}</b></td>".format("Name") 
		htxt += "<td><b>{}</b></td>".format("Version") 
		htxt += "<td><b>{}</b></td>".format("Summary") 
		htxt += "</tr>"
		for dep in deps:
			htxt += self._modinfo(dep)
		htxt += "</table></p>"
		htxt += "<p>Some of the icons in this application were taken from:<br>"
		htxt += "https://icons8.com"
		htxt += "</p>"
		self.m_aboutTxtHTML.SetPage(htxt)
		self.Fit()

	def read_deps(self):
		depfname = path.join(self._apppath, "ressources", "dependencies.json")
		with open(depfname, mode="r") as rfp:
			jdi = json.load(rfp)

		return jdi

	#evt handler for OK BU Click
	def m_okBUTOnButtonClick(self, event):
		self.Close()

	def _modinfo(self, md : dict) -> str:
		name = md["Name"]
		vers = md["Version"]
		summ = md["Summary"]
		
		return "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(name, vers, summ)


