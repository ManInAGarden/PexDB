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
		self.newExperiment_menuitem = wx.MenuItem( self.experiment_menu, wx.ID_ANY, _(u"New experiment"), wx.EmptyString, wx.ITEM_NORMAL )
		self.experiment_menu.Append( self.newExperiment_menuitem )

		self.experiment_menu.AppendSeparator()

		self.dupicate_experiment_menuitem = wx.MenuItem( self.experiment_menu, wx.ID_ANY, _(u"Duplicate Experiment"), wx.EmptyString, wx.ITEM_NORMAL )
		self.experiment_menu.Append( self.dupicate_experiment_menuitem )

		self.delte_experiment_menuItem = wx.MenuItem( self.experiment_menu, wx.ID_ANY, _(u"Delete experiment"), wx.EmptyString, wx.ITEM_NORMAL )
		self.experiment_menu.Append( self.delte_experiment_menuItem )

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

		self.help_menu = wx.Menu()
		self.help_menuItem = wx.MenuItem( self.help_menu, wx.ID_ANY, _(u"Help"), wx.EmptyString, wx.ITEM_NORMAL )
		self.help_menu.Append( self.help_menuItem )

		self.about_menuitem = wx.MenuItem( self.help_menu, wx.ID_ANY, _(u"About PexViewer"), wx.EmptyString, wx.ITEM_NORMAL )
		self.help_menu.Append( self.about_menuitem )

		self.m_menubar1.Append( self.help_menu, _(u"Help") )

		self.SetMenuBar( self.m_menubar1 )

		main_gsizer = wx.GridSizer( 0, 2, 0, 0 )

		self.m_experimentsDataViewListCtrl = wx.dataview.DataViewListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_CarriedOutDtDWLC = self.m_experimentsDataViewListCtrl.AppendTextColumn( _(u"Ausführungsdatum"), wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.m_DescriptionDWLC = self.m_experimentsDataViewListCtrl.AppendTextColumn( _(u"Beschreibung"), wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.m_DescriptionDWLC.GetRenderer().EnableEllipsize( wx.ELLIPSIZE_END );
		main_gsizer.Add( self.m_experimentsDataViewListCtrl, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_experimentPG = pg.PropertyGrid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE|wx.propgrid.PG_SPLITTER_AUTO_CENTER|wx.TAB_TRAVERSAL)
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
		self.Bind( wx.EVT_MENU, self.dupicate_experiment_menuitemOnMenuSelection, id = self.dupicate_experiment_menuitem.GetId() )
		self.Bind( wx.EVT_MENU, self.delete_experiment_menuItemOnMenuSelection, id = self.delte_experiment_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.m_edit_factors_menuitemOnMenuSelection, id = self.m_edit_factors_menuitem.GetId() )
		self.Bind( wx.EVT_MENU, self.reseed_factors_menuItemOnMenuSelection, id = self.reseed_factors_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.edit_response_definitions, id = self.edit_response_definitions_menuItem.GetId() )
		self.m_experimentsDataViewListCtrl.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.experimentDWLC_selchanged, id = wx.ID_ANY )
		self.m_experimentPG.Bind( pg.EVT_PG_CHANGED, self.propgridChanged )

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

	def dupicate_experiment_menuitemOnMenuSelection( self, event ):
		event.Skip()

	def delete_experiment_menuItemOnMenuSelection( self, event ):
		event.Skip()

	def m_edit_factors_menuitemOnMenuSelection( self, event ):
		event.Skip()

	def reseed_factors_menuItemOnMenuSelection( self, event ):
		event.Skip()

	def edit_response_definitions( self, event ):
		event.Skip()

	def experimentDWLC_selchanged( self, event ):
		event.Skip()

	def propgridChanged( self, event ):
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
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Edit project"), pos = wx.DefaultPosition, size = wx.Size( 503,423 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

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

		self.m_prepsLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_SORT_ASCENDING )
		gbSizer3.Add( self.m_prepsLCTRL, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_connfactorBU = wx.Button( self, wx.ID_ANY, _(u"Add factor prerparation"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_connfactorBU, 0, wx.ALL, 5 )

		self.m_removefactorBU = wx.Button( self, wx.ID_ANY, _(u"Remove preperation"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_removefactorBU, 0, wx.ALL, 5 )

		self.editPrepBU = wx.Button( self, wx.ID_ANY, _(u"Edit preparation"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.editPrepBU, 0, wx.ALL, 5 )


		gbSizer3.Add( bSizer7, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		m_okcancelBUTS = wx.StdDialogButtonSizer()
		self.m_okcancelBUTSOK = wx.Button( self, wx.ID_OK )
		m_okcancelBUTS.AddButton( self.m_okcancelBUTSOK )
		self.m_okcancelBUTSCancel = wx.Button( self, wx.ID_CANCEL )
		m_okcancelBUTS.AddButton( self.m_okcancelBUTSCancel )
		m_okcancelBUTS.Realize();

		gbSizer3.Add( m_okcancelBUTS, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )


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
		self.m_checkBox2.Bind( wx.EVT_CHECKBOX, self.m_checkBox2OnCheckBox )
		self.m_sdbSizer2OK.Bind( wx.EVT_BUTTON, self.m_sdbSizer2OnOKButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def OpenProjectDialogOnShow( self, event ):
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
		self.m_sdbSizer3OK.Bind( wx.EVT_BUTTON, self.m_sdbSizer3OnOKButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def AddFactorDialogOnShow( self, event ):
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


