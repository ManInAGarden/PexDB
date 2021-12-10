# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview
import wx.propgrid as pg

import gettext
_ = gettext.gettext

###########################################################################
## Class PexViewerMainFrame
###########################################################################

class PexViewerMainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"PexViewer"), pos = wx.DefaultPosition, size = wx.Size( 741,524 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		self.m_menubar1 = wx.MenuBar( 0 )
		self.file_menu = wx.Menu()
		self.quit_menuitem = wx.MenuItem( self.file_menu, wx.ID_ANY, _(u"Beenden"), wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.Append( self.quit_menuitem )

		self.m_menubar1.Append( self.file_menu, _(u"Datei") )

		self.edit_menu = wx.Menu()
		self.newExperiment_menuitem = wx.MenuItem( self.edit_menu, wx.ID_ANY, _(u"Neues Experiment"), wx.EmptyString, wx.ITEM_NORMAL )
		self.edit_menu.Append( self.newExperiment_menuitem )

		self.m_menubar1.Append( self.edit_menu, _(u"Bearbeiten") )

		self.help_menu = wx.Menu()
		self.help_menuItem = wx.MenuItem( self.help_menu, wx.ID_ANY, _(u"Hilfe"), wx.EmptyString, wx.ITEM_NORMAL )
		self.help_menu.Append( self.help_menuItem )

		self.about_menuitem = wx.MenuItem( self.help_menu, wx.ID_ANY, _(u"Über PexViewer"), wx.EmptyString, wx.ITEM_NORMAL )
		self.help_menu.Append( self.about_menuitem )

		self.m_menubar1.Append( self.help_menu, _(u"Hilfe") )

		self.SetMenuBar( self.m_menubar1 )

		main_gsizer = wx.GridSizer( 0, 2, 0, 0 )

		self.m_experimentsDataViewListCtrl = wx.dataview.DataViewListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_CarriedOutDtDWLC = self.m_experimentsDataViewListCtrl.AppendTextColumn( _(u"Ausführungsdatum"), wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.m_DescriptionDWLC = self.m_experimentsDataViewListCtrl.AppendTextColumn( _(u"Beschreibung"), wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.m_DescriptionDWLC.GetRenderer().EnableEllipsize( wx.ELLIPSIZE_END );
		main_gsizer.Add( self.m_experimentsDataViewListCtrl, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_experimentPG = pg.PropertyGrid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE|wx.propgrid.PG_SPLITTER_AUTO_CENTER|wx.TAB_TRAVERSAL)
		self.m_carriedoutdtPGI = self.m_experimentPG.Append( pg.DateProperty( _(u"Datum"), _(u"Datum") ) )
		self.m_descriptionPGI = self.m_experimentPG.Append( pg.LongStringProperty( _(u"Beschreibung"), _(u"Beschreibung") ) )
		self.m_printerPGI = self.m_experimentPG.Append( pg.MultiChoiceProperty( _(u"Drucker"), _(u"Drucker") ) )
		self.m_extruderPGI = self.m_experimentPG.Append( pg.MultiChoiceProperty( _(u"Extruder"), _(u"Extruder") ) )
		self.m_propertyGridItem13 = self.m_experimentPG.Append( pg.StringProperty( _(u"Name"), _(u"Name") ) )
		self.m_settingsPGI = self.m_experimentPG.Append( pg.PropertyCategory( _(u"Einstellungen"), _(u"Einstellungen") ) )
		self.m_nozzleTempPGI = self.m_experimentPG.Append( pg.FloatProperty( _(u"Düsentemperatur"), _(u"Düsentemperatur") ) )
		main_gsizer.Add( self.m_experimentPG, 0, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( main_gsizer )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.quit_PexViewer, id = self.quit_menuitem.GetId() )
		self.Bind( wx.EVT_MENU, self.create_new_experiment, id = self.newExperiment_menuitem.GetId() )
		self.m_experimentsDataViewListCtrl.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.experimentDWLC_selchanged, id = wx.ID_ANY )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def quit_PexViewer( self, event ):
		event.Skip()

	def create_new_experiment( self, event ):
		event.Skip()

	def experimentDWLC_selchanged( self, event ):
		event.Skip()


