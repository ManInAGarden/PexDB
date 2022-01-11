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
import wx.adv
import wx.html

import gettext
_ = gettext.gettext

###########################################################################
## Class PexViewerMainFrame
###########################################################################

class PexViewerMainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"PexViewer"), pos = wx.DefaultPosition, size = wx.Size( 741,524 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.m_menubar1 = wx.MenuBar( 0 )
		self.file_menu = wx.Menu()
		self.openproject_menuItem = wx.MenuItem( self.file_menu, wx.ID_ANY, _(u"Open project")+ u"\t" + u"CTRL+O", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.Append( self.openproject_menuItem )

		self.editproject_menuItem = wx.MenuItem( self.file_menu, wx.ID_ANY, _(u"Edit project"), wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.Append( self.editproject_menuItem )

		self.newproj_menutitem = wx.MenuItem( self.file_menu, wx.ID_ANY, _(u"New project")+ u"\t" + u"CTRL+N", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.Append( self.newproj_menutitem )

		self.file_menu.AppendSeparator()

		self.quit_menuitem = wx.MenuItem( self.file_menu, wx.ID_ANY, _(u"Quit program")+ u"\t" + u"CTRL+Q", wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.Append( self.quit_menuitem )

		self.m_menubar1.Append( self.file_menu, _(u"File") )

		self.experiment_menu = wx.Menu()
		self.m_menu1 = wx.Menu()
		self.newExperiment_menuitem = wx.MenuItem( self.m_menu1, wx.ID_ANY, _(u"Create single experiment"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.newExperiment_menuitem )

		self.m_createFullFactorialMEI = wx.MenuItem( self.m_menu1, wx.ID_ANY, _(u"Create full factorial"), _(u"Creates experiments for all combinations of facor-levels."), wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_createFullFactorialMEI )

		self.experiment_menu.AppendSubMenu( self.m_menu1, _(u"Create experiments") )

		self.dupicate_experiment_menuitem = wx.MenuItem( self.experiment_menu, wx.ID_ANY, _(u"Duplicate Experiment"), wx.EmptyString, wx.ITEM_NORMAL )
		self.experiment_menu.Append( self.dupicate_experiment_menuitem )

		self.experiment_menu.AppendSeparator()

		self.m_deleteExperimentsMenu = wx.Menu()
		self.delte_experiment_menuItem = wx.MenuItem( self.m_deleteExperimentsMenu, wx.ID_ANY, _(u"Delete single experiment"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_deleteExperimentsMenu.Append( self.delte_experiment_menuItem )

		self.m_deleteAllExperimentsMEI = wx.MenuItem( self.m_deleteExperimentsMenu, wx.ID_ANY, _(u"Delete all experiments"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_deleteExperimentsMenu.Append( self.m_deleteAllExperimentsMEI )

		self.experiment_menu.AppendSubMenu( self.m_deleteExperimentsMenu, _(u"Delete experiments") )

		self.experiment_menu.AppendSeparator()

		self.m_exportExperimentsCsvMEI = wx.MenuItem( self.experiment_menu, wx.ID_ANY, _(u"Export to csv"), wx.EmptyString, wx.ITEM_NORMAL )
		self.experiment_menu.Append( self.m_exportExperimentsCsvMEI )

		self.m_menubar1.Append( self.experiment_menu, _(u"Experimente") )

		self.factors_menu = wx.Menu()
		self.m_edit_factors_menuitem = wx.MenuItem( self.factors_menu, wx.ID_ANY, _(u"Edit factor definitions"), wx.EmptyString, wx.ITEM_NORMAL )
		self.factors_menu.Append( self.m_edit_factors_menuitem )

		self.reseed_factors_menuItem = wx.MenuItem( self.factors_menu, wx.ID_ANY, _(u"Re-seed factors"), wx.EmptyString, wx.ITEM_NORMAL )
		self.factors_menu.Append( self.reseed_factors_menuItem )

		self.m_menubar1.Append( self.factors_menu, _(u"Factors") )

		self.response_menu = wx.Menu()
		self.edit_response_definitions_menuItem = wx.MenuItem( self.response_menu, wx.ID_ANY, _(u"Edit response definitions"), wx.EmptyString, wx.ITEM_NORMAL )
		self.response_menu.Append( self.edit_response_definitions_menuItem )

		self.m_menubar1.Append( self.response_menu, _(u"Responses") )

		self.m_calculationsMENU = wx.Menu()
		self.m_linearRegrMEI = wx.MenuItem( self.m_calculationsMENU, wx.ID_ANY, _(u"Linear regression"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_calculationsMENU.Append( self.m_linearRegrMEI )

		self.m_menubar1.Append( self.m_calculationsMENU, _(u"Calculations") )

		self.help_menu = wx.Menu()
		self.help_menuItem = wx.MenuItem( self.help_menu, wx.ID_ANY, _(u"Help"), wx.EmptyString, wx.ITEM_NORMAL )
		self.help_menu.Append( self.help_menuItem )

		self.about_menuitem = wx.MenuItem( self.help_menu, wx.ID_ANY, _(u"About PexViewer"), wx.EmptyString, wx.ITEM_NORMAL )
		self.help_menu.Append( self.about_menuitem )

		self.m_menubar1.Append( self.help_menu, _(u"Help") )

		self.SetMenuBar( self.m_menubar1 )

		main_gsizer = wx.GridSizer( 0, 2, 0, 0 )

		self.m_experimentsDataViewListCtrl = wx.dataview.DataViewListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_sequenceDVLC = self.m_experimentsDataViewListCtrl.AppendTextColumn( _(u"Sequence #"), wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.m_descriptionDVLC = self.m_experimentsDataViewListCtrl.AppendTextColumn( _(u"Description"), wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.m_descriptionDVLC.GetRenderer().EnableEllipsize( wx.ELLIPSIZE_END );
		main_gsizer.Add( self.m_experimentsDataViewListCtrl, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_experimentPG = pg.PropertyGrid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_BOLD_MODIFIED|wx.propgrid.PG_DEFAULT_STYLE|wx.propgrid.PG_SPLITTER_AUTO_CENTER|wx.TAB_TRAVERSAL)
		main_gsizer.Add( self.m_experimentPG, 0, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( main_gsizer )
		self.Layout()
		self.m_menu6 = wx.Menu()
		self.Bind( wx.EVT_RIGHT_DOWN, self.PexViewerMainFrameOnContextMenu )

		self.m_mainSBA = self.CreateStatusBar( 2, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.openproject_menuItemOnMenuSelection, id = self.openproject_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.editproject_menuItemOnMenuSelection, id = self.editproject_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.newproj_menutitemOnMenuSelection, id = self.newproj_menutitem.GetId() )
		self.Bind( wx.EVT_MENU, self.quit_PexViewer, id = self.quit_menuitem.GetId() )
		self.Bind( wx.EVT_MENU, self.create_new_experiment, id = self.newExperiment_menuitem.GetId() )
		self.Bind( wx.EVT_MENU, self.m_createFullFactorialMEIOnMenuSelection, id = self.m_createFullFactorialMEI.GetId() )
		self.Bind( wx.EVT_MENU, self.dupicate_experiment_menuitemOnMenuSelection, id = self.dupicate_experiment_menuitem.GetId() )
		self.Bind( wx.EVT_MENU, self.delete_experiment_menuItemOnMenuSelection, id = self.delte_experiment_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.m_deleteAllExperimentsMEIOnMenuSelection, id = self.m_deleteAllExperimentsMEI.GetId() )
		self.Bind( wx.EVT_MENU, self.m_exportExperimentsCsvMEIOnMenuSelection, id = self.m_exportExperimentsCsvMEI.GetId() )
		self.Bind( wx.EVT_MENU, self.m_edit_factors_menuitemOnMenuSelection, id = self.m_edit_factors_menuitem.GetId() )
		self.Bind( wx.EVT_MENU, self.reseed_factors_menuItemOnMenuSelection, id = self.reseed_factors_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.edit_response_definitions, id = self.edit_response_definitions_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.m_linearRegrMEIOnMenuSelection, id = self.m_linearRegrMEI.GetId() )
		self.m_experimentsDataViewListCtrl.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.experimentDWLC_selchanged, id = wx.ID_ANY )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def openproject_menuItemOnMenuSelection( self, event ):
		event.Skip()

	def editproject_menuItemOnMenuSelection( self, event ):
		event.Skip()

	def newproj_menutitemOnMenuSelection( self, event ):
		event.Skip()

	def quit_PexViewer( self, event ):
		event.Skip()

	def create_new_experiment( self, event ):
		event.Skip()

	def m_createFullFactorialMEIOnMenuSelection( self, event ):
		event.Skip()

	def dupicate_experiment_menuitemOnMenuSelection( self, event ):
		event.Skip()

	def delete_experiment_menuItemOnMenuSelection( self, event ):
		event.Skip()

	def m_deleteAllExperimentsMEIOnMenuSelection( self, event ):
		event.Skip()

	def m_exportExperimentsCsvMEIOnMenuSelection( self, event ):
		event.Skip()

	def m_edit_factors_menuitemOnMenuSelection( self, event ):
		event.Skip()

	def reseed_factors_menuItemOnMenuSelection( self, event ):
		event.Skip()

	def edit_response_definitions( self, event ):
		event.Skip()

	def m_linearRegrMEIOnMenuSelection( self, event ):
		event.Skip()

	def experimentDWLC_selchanged( self, event ):
		event.Skip()

	def PexViewerMainFrameOnContextMenu( self, event ):
		self.PopupMenu( self.m_menu6, event.GetPosition() )


###########################################################################
## Class EditFactorDefinitions
###########################################################################

class EditFactorDefinitions ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Edit factor definitions"), pos = wx.DefaultPosition, size = wx.Size( 659,387 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		fgSizer2 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer2.AddGrowableCol( 0 )
		fgSizer2.AddGrowableRow( 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		gbSizer1 = wx.GridBagSizer( 0, 0 )
		gbSizer1.SetFlexibleDirection( wx.BOTH )
		gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_splitter21 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter21.Bind( wx.EVT_IDLE, self.m_splitter21OnIdle )

		self.m_panel11 = wx.Panel( self.m_splitter21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.m_factorDefsLC = wx.ListCtrl( self.m_panel11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_SORT_ASCENDING )
		bSizer11.Add( self.m_factorDefsLC, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panel11.SetSizer( bSizer11 )
		self.m_panel11.Layout()
		bSizer11.Fit( self.m_panel11 )
		self.m_panel8 = wx.Panel( self.m_splitter21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		self.m_factorDtaPG = pg.PropertyGrid(self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE|wx.TAB_TRAVERSAL)
		bSizer6.Add( self.m_factorDtaPG, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panel8.SetSizer( bSizer6 )
		self.m_panel8.Layout()
		bSizer6.Fit( self.m_panel8 )
		self.m_splitter21.SplitVertically( self.m_panel11, self.m_panel8, 346 )
		gbSizer1.Add( self.m_splitter21, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_closeBU = wx.Button( self, wx.ID_ANY, _(u"close"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_closeBU.SetToolTip( _(u"close this dialog") )

		bSizer4.Add( self.m_closeBU, 0, wx.ALL, 5 )

		self.m_newBU = wx.Button( self, wx.ID_ANY, _(u"create new"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_newBU.SetToolTip( _(u"create a new active factor defintion") )

		bSizer4.Add( self.m_newBU, 0, wx.ALL, 5 )

		self.m_show_inactiveBU = wx.Button( self, wx.ID_ANY, _(u"toggle active/inactive"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_show_inactiveBU.SetToolTip( _(u"also show inactive factor definitions") )

		bSizer4.Add( self.m_show_inactiveBU, 0, wx.ALL, 5 )


		gbSizer1.Add( bSizer4, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )


		gbSizer1.AddGrowableCol( 0 )
		gbSizer1.AddGrowableRow( 0 )

		fgSizer2.Add( gbSizer1, 1, wx.EXPAND, 5 )


		self.SetSizer( fgSizer2 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_SHOW, self.EditFactorDefinitionsOnShow )
		self.m_factorDefsLC.Bind( wx.EVT_LIST_ITEM_SELECTED, self.m_factorDefsLCOnListItemSelected )
		self.m_factorDtaPG.Bind( pg.EVT_PG_CHANGED, self.m_factorDtaPGOnPropertyGridChanged )
		self.m_closeBU.Bind( wx.EVT_BUTTON, self.m_closeBUOnButtonClick )
		self.m_newBU.Bind( wx.EVT_BUTTON, self.m_newBUOnButtonClick )
		self.m_show_inactiveBU.Bind( wx.EVT_BUTTON, self.m_show_inactiveBUOnButtonClick )
		self.m_show_inactiveBU.Bind( wx.EVT_LEFT_DCLICK, self.m_show_inactiveBUOnLeftDClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def EditFactorDefinitionsOnShow( self, event ):
		event.Skip()

	def m_factorDefsLCOnListItemSelected( self, event ):
		event.Skip()

	def m_factorDtaPGOnPropertyGridChanged( self, event ):
		event.Skip()

	def m_closeBUOnButtonClick( self, event ):
		event.Skip()

	def m_newBUOnButtonClick( self, event ):
		event.Skip()

	def m_show_inactiveBUOnButtonClick( self, event ):
		event.Skip()

	def m_show_inactiveBUOnLeftDClick( self, event ):
		event.Skip()

	def m_splitter21OnIdle( self, event ):
		self.m_splitter21.SetSashPosition( 346 )
		self.m_splitter21.Unbind( wx.EVT_IDLE )


###########################################################################
## Class EditResponseDefinitions
###########################################################################

class EditResponseDefinitions ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Edit response definitions"), pos = wx.DefaultPosition, size = wx.Size( 659,387 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		fgSizer2 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer2.AddGrowableCol( 0 )
		fgSizer2.AddGrowableRow( 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		gbSizer1 = wx.GridBagSizer( 0, 0 )
		gbSizer1.SetFlexibleDirection( wx.BOTH )
		gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_splitter21 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.m_splitter21.Bind( wx.EVT_IDLE, self.m_splitter21OnIdle )

		self.m_panel11 = wx.Panel( self.m_splitter21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.m_factorDefsLC = wx.ListCtrl( self.m_panel11, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_SORT_ASCENDING )
		bSizer11.Add( self.m_factorDefsLC, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panel11.SetSizer( bSizer11 )
		self.m_panel11.Layout()
		bSizer11.Fit( self.m_panel11 )
		self.m_panel8 = wx.Panel( self.m_splitter21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		self.m_resultDtaPG = pg.PropertyGrid(self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE|wx.TAB_TRAVERSAL)
		bSizer6.Add( self.m_resultDtaPG, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panel8.SetSizer( bSizer6 )
		self.m_panel8.Layout()
		bSizer6.Fit( self.m_panel8 )
		self.m_splitter21.SplitVertically( self.m_panel11, self.m_panel8, 346 )
		gbSizer1.Add( self.m_splitter21, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_closeBU = wx.Button( self, wx.ID_ANY, _(u"close"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_closeBU.SetToolTip( _(u"close this dialog") )

		bSizer4.Add( self.m_closeBU, 0, wx.ALL, 5 )

		self.m_newBU = wx.Button( self, wx.ID_ANY, _(u"create new"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_newBU.SetToolTip( _(u"create a new active factor defintion") )

		bSizer4.Add( self.m_newBU, 0, wx.ALL, 5 )

		self.m_show_inactiveBU = wx.Button( self, wx.ID_ANY, _(u"toggle active/inactive"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_show_inactiveBU.SetToolTip( _(u"also show inactive factor definitions") )

		bSizer4.Add( self.m_show_inactiveBU, 0, wx.ALL, 5 )


		gbSizer1.Add( bSizer4, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )


		gbSizer1.AddGrowableCol( 0 )
		gbSizer1.AddGrowableRow( 0 )

		fgSizer2.Add( gbSizer1, 1, wx.EXPAND, 5 )


		self.SetSizer( fgSizer2 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_SHOW, self.EditFactorDefinitionsOnShow )
		self.m_factorDefsLC.Bind( wx.EVT_LIST_ITEM_SELECTED, self.m_factorDefsLCOnListItemSelected )
		self.m_resultDtaPG.Bind( pg.EVT_PG_CHANGED, self.m_factorDtaPGOnPropertyGridChanged )
		self.m_closeBU.Bind( wx.EVT_BUTTON, self.m_closeBUOnButtonClick )
		self.m_newBU.Bind( wx.EVT_BUTTON, self.m_newBUOnButtonClick )
		self.m_show_inactiveBU.Bind( wx.EVT_BUTTON, self.m_show_inactiveBUOnButtonClick )
		self.m_show_inactiveBU.Bind( wx.EVT_LEFT_DCLICK, self.m_show_inactiveBUOnLeftDClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def EditFactorDefinitionsOnShow( self, event ):
		event.Skip()

	def m_factorDefsLCOnListItemSelected( self, event ):
		event.Skip()

	def m_factorDtaPGOnPropertyGridChanged( self, event ):
		event.Skip()

	def m_closeBUOnButtonClick( self, event ):
		event.Skip()

	def m_newBUOnButtonClick( self, event ):
		event.Skip()

	def m_show_inactiveBUOnButtonClick( self, event ):
		event.Skip()

	def m_show_inactiveBUOnLeftDClick( self, event ):
		event.Skip()

	def m_splitter21OnIdle( self, event ):
		self.m_splitter21.SetSashPosition( 346 )
		self.m_splitter21.Unbind( wx.EVT_IDLE )


###########################################################################
## Class EditProjectDialog
###########################################################################

class EditProjectDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Edit project"), pos = wx.DefaultPosition, size = wx.Size( 478,752 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer3 = wx.GridBagSizer( 3, 3 )
		gbSizer3.SetFlexibleDirection( wx.BOTH )
		gbSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_ALL )

		self.nameL = wx.StaticText( self, wx.ID_ANY, _(u"Name"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.nameL.Wrap( -1 )

		gbSizer3.Add( self.nameL, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_nameTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer3.Add( self.m_nameTB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, _(u"Status"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		gbSizer3.Add( self.m_staticText2, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_projectstatusCOBChoices = []
		self.m_projectstatusCOB = wx.ComboBox( self, wx.ID_ANY, _(u"Combo!"), wx.DefaultPosition, wx.DefaultSize, m_projectstatusCOBChoices, 0 )
		gbSizer3.Add( self.m_projectstatusCOB, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _(u"Is archived"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		gbSizer3.Add( self.m_staticText3, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_isArchivedCBX = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer3.Add( self.m_isArchivedCBX, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, _(u"Description"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		gbSizer3.Add( self.m_staticText9, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_descriptionTBX = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_AUTO_URL|wx.TE_BESTWRAP|wx.TE_MULTILINE )
		gbSizer3.Add( self.m_descriptionTBX, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_prepsLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_SORT_ASCENDING )
		gbSizer3.Add( self.m_prepsLCTRL, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, _(u"Factor preparations for this project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		gbSizer3.Add( self.m_staticText10, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_connfactorBU = wx.Button( self, wx.ID_ANY, _(u"Add factor preparation"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_connfactorBU, 0, wx.ALL, 5 )

		self.m_removefactorBU = wx.Button( self, wx.ID_ANY, _(u"Remove preperation"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_removefactorBU, 0, wx.ALL, 5 )

		self.editPrepBU = wx.Button( self, wx.ID_ANY, _(u"Edit preparation"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.editPrepBU, 0, wx.ALL, 5 )


		gbSizer3.Add( bSizer7, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, _(u"Response preparations for this project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )

		gbSizer3.Add( self.m_staticText13, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_respPrepsLCTR = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_SORT_ASCENDING )
		gbSizer3.Add( self.m_respPrepsLCTR, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_addRespPrepBUT = wx.Button( self, wx.ID_ANY, _(u"Add response preparation"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.m_addRespPrepBUT, 0, wx.ALL, 5 )

		self.m_deleteRespPrepBUT = wx.Button( self, wx.ID_ANY, _(u"Delete preparation"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.m_deleteRespPrepBUT, 0, wx.ALL, 5 )


		gbSizer3.Add( bSizer8, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND, 5 )

		m_okcancelBUTS = wx.StdDialogButtonSizer()
		self.m_okcancelBUTSOK = wx.Button( self, wx.ID_OK )
		m_okcancelBUTS.AddButton( self.m_okcancelBUTSOK )
		self.m_okcancelBUTSCancel = wx.Button( self, wx.ID_CANCEL )
		m_okcancelBUTS.AddButton( self.m_okcancelBUTSCancel )
		m_okcancelBUTS.Realize();

		gbSizer3.Add( m_okcancelBUTS, wx.GBPosition( 10, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer3.AddGrowableCol( 1 )
		gbSizer3.AddGrowableRow( 3 )

		self.SetSizer( gbSizer3 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_SHOW, self.EditProjectDialogOnShow )
		self.m_connfactorBU.Bind( wx.EVT_BUTTON, self.m_connfactorBUOnButtonClick )
		self.m_removefactorBU.Bind( wx.EVT_BUTTON, self.m_removefactorBUOnButtonClick )
		self.editPrepBU.Bind( wx.EVT_BUTTON, self.editPrepBUOnButtonClick )
		self.m_addRespPrepBUT.Bind( wx.EVT_BUTTON, self.m_addRespPrepBUTOnButtonClick )
		self.m_deleteRespPrepBUT.Bind( wx.EVT_BUTTON, self.m_deleteRespPrepBUTOnButtonClick )
		self.m_okcancelBUTSOK.Bind( wx.EVT_BUTTON, self.m_okcancelBUTSOnOKButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def EditProjectDialogOnShow( self, event ):
		event.Skip()

	def m_connfactorBUOnButtonClick( self, event ):
		event.Skip()

	def m_removefactorBUOnButtonClick( self, event ):
		event.Skip()

	def editPrepBUOnButtonClick( self, event ):
		event.Skip()

	def m_addRespPrepBUTOnButtonClick( self, event ):
		event.Skip()

	def m_deleteRespPrepBUTOnButtonClick( self, event ):
		event.Skip()

	def m_okcancelBUTSOnOKButtonClick( self, event ):
		event.Skip()


###########################################################################
## Class OpenProjectDialog
###########################################################################

class OpenProjectDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Open project"), pos = wx.DefaultPosition, size = wx.Size( 345,279 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer4 = wx.GridBagSizer( 5, 5 )
		gbSizer4.SetFlexibleDirection( wx.BOTH )
		gbSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, _(u"Select a project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		gbSizer4.Add( self.m_staticText4, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_projectsLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		gbSizer4.Add( self.m_projectsLCTRL, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_checkBox2 = wx.CheckBox( self, wx.ID_ANY, _(u"Archived projects"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer4.Add( self.m_checkBox2, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_sdbSizer2 = wx.StdDialogButtonSizer()
		self.m_sdbSizer2OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer2.AddButton( self.m_sdbSizer2OK )
		self.m_sdbSizer2Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer2.AddButton( self.m_sdbSizer2Cancel )
		m_sdbSizer2.Realize();

		gbSizer4.Add( m_sdbSizer2, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND, 5 )


		gbSizer4.AddGrowableCol( 0 )
		gbSizer4.AddGrowableCol( 1 )
		gbSizer4.AddGrowableRow( 1 )
		gbSizer4.AddGrowableRow( 2 )

		self.SetSizer( gbSizer4 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_SHOW, self.OpenProjectDialogOnShow )
		self.m_projectsLCTRL.Bind( wx.EVT_LEFT_DCLICK, self.m_projectsLCTRLOnLeftDClick )
		self.m_projectsLCTRL.Bind( wx.EVT_LIST_ITEM_DESELECTED, self.m_projectsLCTRLOnListItemDeselected )
		self.m_projectsLCTRL.Bind( wx.EVT_LIST_ITEM_SELECTED, self.m_projectsLCTRLOnListItemSelected )
		self.m_checkBox2.Bind( wx.EVT_CHECKBOX, self.m_checkBox2OnCheckBox )
		self.m_sdbSizer2OK.Bind( wx.EVT_BUTTON, self.m_sdbSizer2OnOKButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def OpenProjectDialogOnShow( self, event ):
		event.Skip()

	def m_projectsLCTRLOnLeftDClick( self, event ):
		event.Skip()

	def m_projectsLCTRLOnListItemDeselected( self, event ):
		event.Skip()

	def m_projectsLCTRLOnListItemSelected( self, event ):
		event.Skip()

	def m_checkBox2OnCheckBox( self, event ):
		event.Skip()

	def m_sdbSizer2OnOKButtonClick( self, event ):
		event.Skip()


###########################################################################
## Class AddFactorDialog
###########################################################################

class AddFactorDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Select a factor"), pos = wx.DefaultPosition, size = wx.Size( 403,327 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer5 = wx.GridBagSizer( 0, 0 )
		gbSizer5.SetFlexibleDirection( wx.BOTH )
		gbSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, _(u"Factors not already present"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		gbSizer5.Add( self.m_staticText5, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_factorsLCTR = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		gbSizer5.Add( self.m_factorsLCTR, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		m_sdbSizer3 = wx.StdDialogButtonSizer()
		self.m_sdbSizer3OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer3.AddButton( self.m_sdbSizer3OK )
		self.m_sdbSizer3Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer3.AddButton( self.m_sdbSizer3Cancel )
		m_sdbSizer3.Realize();

		gbSizer5.Add( m_sdbSizer3, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND, 5 )


		gbSizer5.AddGrowableCol( 0 )
		gbSizer5.AddGrowableCol( 1 )
		gbSizer5.AddGrowableRow( 1 )
		gbSizer5.AddGrowableRow( 2 )
		gbSizer5.AddGrowableRow( 3 )

		self.SetSizer( gbSizer5 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_SHOW, self.AddFactorDialogOnShow )
		self.m_factorsLCTR.Bind( wx.EVT_LEFT_DCLICK, self.m_factorsLCTROnLeftDClick )
		self.m_factorsLCTR.Bind( wx.EVT_LIST_ITEM_DESELECTED, self.m_factorsLCTROnListItemDeselected )
		self.m_factorsLCTR.Bind( wx.EVT_LIST_ITEM_SELECTED, self.m_factorsLCTROnListItemSelected )
		self.m_sdbSizer3OK.Bind( wx.EVT_BUTTON, self.m_sdbSizer3OnOKButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def AddFactorDialogOnShow( self, event ):
		event.Skip()

	def m_factorsLCTROnLeftDClick( self, event ):
		event.Skip()

	def m_factorsLCTROnListItemDeselected( self, event ):
		event.Skip()

	def m_factorsLCTROnListItemSelected( self, event ):
		event.Skip()

	def m_sdbSizer3OnOKButtonClick( self, event ):
		event.Skip()


###########################################################################
## Class AddResponseDialog
###########################################################################

class AddResponseDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Select a response"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer5 = wx.GridBagSizer( 0, 0 )
		gbSizer5.SetFlexibleDirection( wx.BOTH )
		gbSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, _(u"Responses not already present"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		gbSizer5.Add( self.m_staticText5, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_responsesLCTR = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		gbSizer5.Add( self.m_responsesLCTR, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		m_sdbSizer3 = wx.StdDialogButtonSizer()
		self.m_sdbSizer3OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer3.AddButton( self.m_sdbSizer3OK )
		self.m_sdbSizer3Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer3.AddButton( self.m_sdbSizer3Cancel )
		m_sdbSizer3.Realize();

		gbSizer5.Add( m_sdbSizer3, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND, 5 )


		gbSizer5.AddGrowableCol( 0 )
		gbSizer5.AddGrowableCol( 1 )
		gbSizer5.AddGrowableRow( 1 )
		gbSizer5.AddGrowableRow( 2 )
		gbSizer5.AddGrowableRow( 3 )

		self.SetSizer( gbSizer5 )
		self.Layout()
		gbSizer5.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_SHOW, self.AddResponseDialogOnShow )
		self.m_responsesLCTR.Bind( wx.EVT_LEFT_DCLICK, self.m_factorsLCTROnLeftDClick )
		self.m_responsesLCTR.Bind( wx.EVT_LIST_ITEM_DESELECTED, self.m_factorsLCTROnListItemDeselected )
		self.m_responsesLCTR.Bind( wx.EVT_LIST_ITEM_SELECTED, self.m_factorsLCTROnListItemSelected )
		self.m_sdbSizer3OK.Bind( wx.EVT_BUTTON, self.m_sdbSizer3OnOKButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def AddResponseDialogOnShow( self, event ):
		event.Skip()

	def m_factorsLCTROnLeftDClick( self, event ):
		event.Skip()

	def m_factorsLCTROnListItemDeselected( self, event ):
		event.Skip()

	def m_factorsLCTROnListItemSelected( self, event ):
		event.Skip()

	def m_sdbSizer3OnOKButtonClick( self, event ):
		event.Skip()


###########################################################################
## Class EditPreparation
###########################################################################

class EditPreparation ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Edit factor preparation"), pos = wx.DefaultPosition, size = wx.Size( 252,176 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer6 = wx.GridBagSizer( 5, 5 )
		gbSizer6.SetFlexibleDirection( wx.BOTH )
		gbSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, _(u"Minimum value"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		gbSizer6.Add( self.m_staticText6, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_minValTBX = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer6.Add( self.m_minValTBX, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, _(u"Maximum value"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		gbSizer6.Add( self.m_staticText7, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_maxValTBX = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer6.Add( self.m_maxValTBX, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, _(u"Number of levels"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		gbSizer6.Add( self.m_staticText8, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_numLvlsTBX = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer6.Add( self.m_numLvlsTBX, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		m_sdbSizer4 = wx.StdDialogButtonSizer()
		self.m_sdbSizer4OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer4.AddButton( self.m_sdbSizer4OK )
		self.m_sdbSizer4Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer4.AddButton( self.m_sdbSizer4Cancel )
		m_sdbSizer4.Realize();

		gbSizer6.Add( m_sdbSizer4, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND, 5 )


		gbSizer6.AddGrowableCol( 1 )
		gbSizer6.AddGrowableRow( 3 )

		self.SetSizer( gbSizer6 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_SHOW, self.EditPreparationOnShow )
		self.m_sdbSizer4OK.Bind( wx.EVT_BUTTON, self.OnOKButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def EditPreparationOnShow( self, event ):
		event.Skip()

	def OnOKButtonClick( self, event ):
		event.Skip()


###########################################################################
## Class CreateFullDetailsDialog
###########################################################################

class CreateFullDetailsDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Create full factorial details"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer8 = wx.GridBagSizer( 0, 0 )
		gbSizer8.SetFlexibleDirection( wx.BOTH )
		gbSizer8.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, _(u"Repetitions"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )

		self.m_staticText13.SetToolTip( _(u"Number of repetitions for each combinations of factors") )

		gbSizer8.Add( self.m_staticText13, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_repetitionsSPCTRL = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 20, 1 )
		gbSizer8.Add( self.m_repetitionsSPCTRL, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, _(u"Planned date"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		gbSizer8.Add( self.m_staticText14, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_datePicker1 = wx.adv.DatePickerCtrl( self, wx.ID_ANY, wx.DefaultDateTime, wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_ALLOWNONE|wx.adv.DP_DEFAULT|wx.adv.DP_DROPDOWN )
		gbSizer8.Add( self.m_datePicker1, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText15 = wx.StaticText( self, wx.ID_ANY, _(u"Sequence"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )

		gbSizer8.Add( self.m_staticText15, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_sequenceCHOIChoices = [ _(u"linear"), _(u"random mixed") ]
		self.m_sequenceCHOI = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_sequenceCHOIChoices, wx.CB_SORT )
		self.m_sequenceCHOI.SetSelection( 0 )
		gbSizer8.Add( self.m_sequenceCHOI, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_progressGAUGE = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
		self.m_progressGAUGE.SetValue( 0 )
		gbSizer8.Add( self.m_progressGAUGE, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.ALL, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer8.Add( self.m_staticline1, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		m_sdbSizer6 = wx.StdDialogButtonSizer()
		self.m_sdbSizer6OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer6.AddButton( self.m_sdbSizer6OK )
		self.m_sdbSizer6Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer6.AddButton( self.m_sdbSizer6Cancel )
		m_sdbSizer6.Realize();

		gbSizer8.Add( m_sdbSizer6, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer8.AddGrowableCol( 1 )
		gbSizer8.AddGrowableRow( 1 )

		self.SetSizer( gbSizer8 )
		self.Layout()
		gbSizer8.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_sdbSizer6OK.Bind( wx.EVT_BUTTON, self.m_sdbSizer6OnOKButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def m_sdbSizer6OnOKButtonClick( self, event ):
		event.Skip()


###########################################################################
## Class LinRegrDialog
###########################################################################

class LinRegrDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Multiple linear regression"), pos = wx.DefaultPosition, size = wx.Size( 711,606 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer9 = wx.GridBagSizer( 0, 0 )
		gbSizer9.SetFlexibleDirection( wx.BOTH )
		gbSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_projectNameSTXT = wx.StaticText( self, wx.ID_ANY, _(u"<projectname>"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_projectNameSTXT.Wrap( -1 )

		gbSizer9.Add( self.m_projectNameSTXT, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_linRegNBCK = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_TOP )
		self.m_panel5 = wx.Panel( self.m_linRegNBCK, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer13 = wx.GridBagSizer( 0, 0 )
		gbSizer13.SetFlexibleDirection( wx.BOTH )
		gbSizer13.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText18 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"Float precision"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )

		gbSizer13.Add( self.m_staticText18, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_precisionCHOIChoices = [ _(u"0"), _(u"1"), _(u"2"), _(u"3"), _(u"4"), _(u"5"), _(u"6") ]
		self.m_precisionCHOI = wx.Choice( self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_precisionCHOIChoices, 0 )
		self.m_precisionCHOI.SetSelection( 3 )
		gbSizer13.Add( self.m_precisionCHOI, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText19 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"Revised input data"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )

		gbSizer13.Add( self.m_staticText19, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_inputDataDLCTRL = wx.dataview.DataViewListCtrl( self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_inputDataDLCTRL.SetMinSize( wx.Size( 100,200 ) )

		gbSizer13.Add( self.m_inputDataDLCTRL, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.doCalcBUT = wx.Button( self.m_panel5, wx.ID_ANY, _(u"Solve"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer13.Add( self.doCalcBUT, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText16 = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"Summary"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		gbSizer13.Add( self.m_staticText16, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_summaryHTMLWIN = wx.html.HtmlWindow( self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_SCROLLBAR_AUTO )
		self.m_summaryHTMLWIN.SetMinSize( wx.Size( 100,100 ) )

		gbSizer13.Add( self.m_summaryHTMLWIN, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer13.AddGrowableCol( 1 )
		gbSizer13.AddGrowableRow( 2 )
		gbSizer13.AddGrowableRow( 5 )

		self.m_panel5.SetSizer( gbSizer13 )
		self.m_panel5.Layout()
		gbSizer13.Fit( self.m_panel5 )
		self.m_linRegNBCK.AddPage( self.m_panel5, _(u"Regression Calculation"), True )
		self.m_panel6 = wx.Panel( self.m_linRegNBCK, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer11 = wx.GridBagSizer( 0, 0 )
		gbSizer11.SetFlexibleDirection( wx.BOTH )
		gbSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText24 = wx.StaticText( self.m_panel6, wx.ID_ANY, _(u"Formula"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText24.Wrap( -1 )

		gbSizer11.Add( self.m_staticText24, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_targetCHOIChoices = []
		self.m_targetCHOI = wx.Choice( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_targetCHOIChoices, 0 )
		self.m_targetCHOI.SetSelection( 0 )
		gbSizer11.Add( self.m_targetCHOI, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText27 = wx.StaticText( self.m_panel6, wx.ID_ANY, _(u"Factor precision"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )

		gbSizer11.Add( self.m_staticText27, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_factorPrecisionCHOIChoices = [ _(u"0"), _(u"1"), _(u"2"), _(u"3"), _(u"4"), _(u"5"), _(u"6") ]
		self.m_factorPrecisionCHOI = wx.Choice( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_factorPrecisionCHOIChoices, wx.CB_SORT )
		self.m_factorPrecisionCHOI.SetSelection( 0 )
		gbSizer11.Add( self.m_factorPrecisionCHOI, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_formulaTBX = wx.TextCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer11.Add( self.m_formulaTBX, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticline2 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer11.Add( self.m_staticline2, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )

		self.m_staticText25 = wx.StaticText( self.m_panel6, wx.ID_ANY, _(u"Target"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText25.Wrap( -1 )

		gbSizer11.Add( self.m_staticText25, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText241 = wx.StaticText( self.m_panel6, wx.ID_ANY, _(u"Factors"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText241.Wrap( -1 )

		gbSizer11.Add( self.m_staticText241, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_factorsPGRD = pg.PropertyGrid(self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE)
		gbSizer11.Add( self.m_factorsPGRD, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_calcAllBUT = wx.Button( self.m_panel6, wx.ID_ANY, _(u"Calculate All"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer11.Add( self.m_calcAllBUT, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText251 = wx.StaticText( self.m_panel6, wx.ID_ANY, _(u"Responses"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText251.Wrap( -1 )

		gbSizer11.Add( self.m_staticText251, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_responsesPGRD = pg.PropertyGrid(self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE)
		gbSizer11.Add( self.m_responsesPGRD, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer11.AddGrowableCol( 1 )

		self.m_panel6.SetSizer( gbSizer11 )
		self.m_panel6.Layout()
		gbSizer11.Fit( self.m_panel6 )
		self.m_linRegNBCK.AddPage( self.m_panel6, _(u"Prediction"), False )

		gbSizer9.Add( self.m_linRegNBCK, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		m_sdbSizer7 = wx.StdDialogButtonSizer()
		self.m_sdbSizer7OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer7.AddButton( self.m_sdbSizer7OK )
		m_sdbSizer7.Realize();

		gbSizer9.Add( m_sdbSizer7, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer9.AddGrowableCol( 0 )
		gbSizer9.AddGrowableRow( 1 )

		self.SetSizer( gbSizer9 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.LinRegrDialogOnInitDialog )
		self.Bind( wx.EVT_SHOW, self.LinRegrDialogOnShow )
		self.m_linRegNBCK.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.m_linRegNBCKOnNotebookPageChanged )
		self.m_precisionCHOI.Bind( wx.EVT_CHOICE, self.m_precisionCHOIOnChoice )
		self.doCalcBUT.Bind( wx.EVT_BUTTON, self.doCalcBUTOnButtonClick )
		self.m_targetCHOI.Bind( wx.EVT_CHOICE, self.m_targetCHOIOnChoice )
		self.m_factorPrecisionCHOI.Bind( wx.EVT_CHOICE, self.m_factorPrecisionCHOIOnChoice )
		self.m_calcAllBUT.Bind( wx.EVT_BUTTON, self.m_calcAllBUTOnButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def LinRegrDialogOnInitDialog( self, event ):
		event.Skip()

	def LinRegrDialogOnShow( self, event ):
		event.Skip()

	def m_linRegNBCKOnNotebookPageChanged( self, event ):
		event.Skip()

	def m_precisionCHOIOnChoice( self, event ):
		event.Skip()

	def doCalcBUTOnButtonClick( self, event ):
		event.Skip()

	def m_targetCHOIOnChoice( self, event ):
		event.Skip()

	def m_factorPrecisionCHOIOnChoice( self, event ):
		event.Skip()

	def m_calcAllBUTOnButtonClick( self, event ):
		event.Skip()


