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
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar2Wx

import gettext
_ = gettext.gettext

###########################################################################
## Class PexViewerMainFrame
###########################################################################

class PexViewerMainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"PexViewer"), pos = wx.DefaultPosition, size = wx.Size( 933,801 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

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

		self.m_reseedCatsMEIT = wx.MenuItem( self.file_menu, wx.ID_ANY, _(u"Reseed catalog data"), wx.EmptyString, wx.ITEM_NORMAL )
		self.file_menu.Append( self.m_reseedCatsMEIT )

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

		self.m_creaFractFactMEI = wx.MenuItem( self.m_menu1, wx.ID_ANY, _(u"Create fractional factorial"), wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.Append( self.m_creaFractFactMEI )

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

		self.m_menu6 = wx.Menu()
		self.Bind( wx.EVT_RIGHT_DOWN, self.PexViewerMainFrameOnContextMenu )

		gbSizer12 = wx.GridBagSizer( 0, 0 )
		gbSizer12.SetFlexibleDirection( wx.BOTH )
		gbSizer12.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_experimentsDataViewListCtrl = wx.dataview.DataViewListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_sequenceDVLC = self.m_experimentsDataViewListCtrl.AppendTextColumn( _(u"Sequence #"), wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.m_descriptionDVLC = self.m_experimentsDataViewListCtrl.AppendTextColumn( _(u"Description"), wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.m_descriptionDVLC.GetRenderer().EnableEllipsize( wx.ELLIPSIZE_END );
		gbSizer12.Add( self.m_experimentsDataViewListCtrl, wx.GBPosition( 0, 0 ), wx.GBSpan( 2, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_experimentPG = pg.PropertyGrid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_BOLD_MODIFIED|wx.propgrid.PG_DEFAULT_STYLE|wx.propgrid.PG_SPLITTER_AUTO_CENTER|wx.TAB_TRAVERSAL)
		self.m_experimentPG.SetMinSize( wx.Size( -1,200 ) )

		gbSizer12.Add( self.m_experimentPG, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		gbSizer13 = wx.GridBagSizer( 0, 0 )
		gbSizer13.SetFlexibleDirection( wx.BOTH )
		gbSizer13.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_expDocsDVLCTR = wx.dataview.DataViewListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer13.Add( self.m_expDocsDVLCTR, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_newExpDocBU = wx.Button( self, wx.ID_ANY, _(u"New document"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_newExpDocBU, 0, wx.ALL, 5 )

		self.m_delExpDocBU = wx.Button( self, wx.ID_ANY, _(u"Delete document"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_delExpDocBU, 0, wx.ALL, 5 )

		self.m_uploadExpDocBUT = wx.Button( self, wx.ID_ANY, _(u"Upload attachment"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_uploadExpDocBUT, 0, wx.ALL, 5 )

		self.m_openExpDocAttachmntBUT = wx.Button( self, wx.ID_ANY, _(u"Open attachment"), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_openExpDocAttachmntBUT, 0, wx.ALL, 5 )


		gbSizer13.Add( bSizer10, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer13.AddGrowableCol( 0 )
		gbSizer13.AddGrowableRow( 0 )

		gbSizer12.Add( gbSizer13, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer12.AddGrowableCol( 0 )
		gbSizer12.AddGrowableCol( 1 )
		gbSizer12.AddGrowableRow( 0 )
		gbSizer12.AddGrowableRow( 1 )

		self.SetSizer( gbSizer12 )
		self.Layout()
		self.m_mainSBA = self.CreateStatusBar( 2, wx.STB_SIZEGRIP, wx.ID_ANY )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.openproject_menuItemOnMenuSelection, id = self.openproject_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.editproject_menuItemOnMenuSelection, id = self.editproject_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.newproj_menutitemOnMenuSelection, id = self.newproj_menutitem.GetId() )
		self.Bind( wx.EVT_MENU, self.m_reseedCatsMEITOnMenuSelection, id = self.m_reseedCatsMEIT.GetId() )
		self.Bind( wx.EVT_MENU, self.quit_PexViewer, id = self.quit_menuitem.GetId() )
		self.Bind( wx.EVT_MENU, self.create_new_experiment, id = self.newExperiment_menuitem.GetId() )
		self.Bind( wx.EVT_MENU, self.m_createFullFactorialMEIOnMenuSelection, id = self.m_createFullFactorialMEI.GetId() )
		self.Bind( wx.EVT_MENU, self.m_creaFractFactMEIOnMenuSelection, id = self.m_creaFractFactMEI.GetId() )
		self.Bind( wx.EVT_MENU, self.dupicate_experiment_menuitemOnMenuSelection, id = self.dupicate_experiment_menuitem.GetId() )
		self.Bind( wx.EVT_MENU, self.delete_experiment_menuItemOnMenuSelection, id = self.delte_experiment_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.m_deleteAllExperimentsMEIOnMenuSelection, id = self.m_deleteAllExperimentsMEI.GetId() )
		self.Bind( wx.EVT_MENU, self.m_exportExperimentsCsvMEIOnMenuSelection, id = self.m_exportExperimentsCsvMEI.GetId() )
		self.Bind( wx.EVT_MENU, self.m_edit_factors_menuitemOnMenuSelection, id = self.m_edit_factors_menuitem.GetId() )
		self.Bind( wx.EVT_MENU, self.reseed_factors_menuItemOnMenuSelection, id = self.reseed_factors_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.edit_response_definitions, id = self.edit_response_definitions_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.m_linearRegrMEIOnMenuSelection, id = self.m_linearRegrMEI.GetId() )
		self.m_experimentsDataViewListCtrl.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.experimentDWLC_selchanged, id = wx.ID_ANY )
		self.m_expDocsDVLCTR.Bind( wx.dataview.EVT_DATAVIEW_ITEM_EDITING_DONE, self.m_expDocsDVLCTROnDataViewListCtrlItemEditingDone, id = wx.ID_ANY )
		self.m_newExpDocBU.Bind( wx.EVT_BUTTON, self.m_newExpDocBUOnButtonClick )
		self.m_delExpDocBU.Bind( wx.EVT_BUTTON, self.m_delExpDocBUOnButtonClick )
		self.m_uploadExpDocBUT.Bind( wx.EVT_BUTTON, self.m_uploadExpDocBUTOnButtonClick )
		self.m_openExpDocAttachmntBUT.Bind( wx.EVT_BUTTON, self.m_openExpDocAttachmntBUTOnButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def openproject_menuItemOnMenuSelection( self, event ):
		event.Skip()

	def editproject_menuItemOnMenuSelection( self, event ):
		event.Skip()

	def newproj_menutitemOnMenuSelection( self, event ):
		event.Skip()

	def m_reseedCatsMEITOnMenuSelection( self, event ):
		event.Skip()

	def quit_PexViewer( self, event ):
		event.Skip()

	def create_new_experiment( self, event ):
		event.Skip()

	def m_createFullFactorialMEIOnMenuSelection( self, event ):
		event.Skip()

	def m_creaFractFactMEIOnMenuSelection( self, event ):
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

	def m_expDocsDVLCTROnDataViewListCtrlItemEditingDone( self, event ):
		event.Skip()

	def m_newExpDocBUOnButtonClick( self, event ):
		event.Skip()

	def m_delExpDocBUOnButtonClick( self, event ):
		event.Skip()

	def m_uploadExpDocBUTOnButtonClick( self, event ):
		event.Skip()

	def m_openExpDocAttachmntBUTOnButtonClick( self, event ):
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


		gbSizer1.Add( bSizer4, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND|wx.ALIGN_RIGHT, 5 )


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


		gbSizer1.Add( bSizer4, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.EXPAND|wx.ALIGN_RIGHT, 5 )


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
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Edit project"), pos = wx.DefaultPosition, size = wx.Size( 764,847 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer3 = wx.GridBagSizer( 3, 3 )
		gbSizer3.SetFlexibleDirection( wx.BOTH )
		gbSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_ALL )

		self.nameL = wx.StaticText( self, wx.ID_ANY, _(u"Name"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.nameL.Wrap( -1 )

		gbSizer3.Add( self.nameL, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_nameTB = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer3.Add( self.m_nameTB, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

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
		gbSizer3.Add( self.m_descriptionTBX, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_prepsLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_SORT_ASCENDING )
		gbSizer3.Add( self.m_prepsLCTRL, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, _(u"Factor preparations for this project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		gbSizer3.Add( self.m_staticText10, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText29 = wx.StaticText( self, wx.ID_ANY, _(u"Environmental Values to be surveyed"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )

		gbSizer3.Add( self.m_staticText29, wx.GBPosition( 4, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_envoroPrepsLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		gbSizer3.Add( self.m_envoroPrepsLCTRL, wx.GBPosition( 5, 2 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_addEnviroBUT = wx.Button( self, wx.ID_ANY, _(u"Edit"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_addEnviroBUT.SetBitmap( wx.Bitmap( u"ressources/Data-Add-Row-icon.png", wx.BITMAP_TYPE_ANY ) )
		self.m_addEnviroBUT.SetToolTip( _(u"Add a new environmental factor") )

		bSizer11.Add( self.m_addEnviroBUT, 0, wx.ALL, 5 )

		self.m_removeEnviroBUT = wx.Button( self, wx.ID_ANY, _(u"MyButton"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_removeEnviroBUT.SetBitmap( wx.Bitmap( u"ressources/Actions-file-close-icon.png", wx.BITMAP_TYPE_ANY ) )
		self.m_removeEnviroBUT.SetToolTip( _(u"Delete selected environmental factor") )

		bSizer11.Add( self.m_removeEnviroBUT, 0, wx.ALL, 5 )

		self.m_editEnviroBUT = wx.Button( self, wx.ID_ANY, _(u"Edit envoronment value"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_editEnviroBUT.SetBitmap( wx.Bitmap( u"ressources/edit-icon.png", wx.BITMAP_TYPE_ANY ) )
		self.m_editEnviroBUT.Hide()
		self.m_editEnviroBUT.SetToolTip( _(u"Edit selected envoironmental factor") )

		bSizer11.Add( self.m_editEnviroBUT, 0, wx.ALL, 5 )


		gbSizer3.Add( bSizer11, wx.GBPosition( 6, 2 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_connfactorBU = wx.Button( self, wx.ID_ANY, _(u"Add factor preparation"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_connfactorBU.SetBitmap( wx.Bitmap( u"ressources/Data-Add-Row-icon.png", wx.BITMAP_TYPE_ANY ) )
		self.m_connfactorBU.SetToolTip( _(u"Add a new factor  preperation") )

		bSizer7.Add( self.m_connfactorBU, 0, wx.ALL, 5 )

		self.m_removefactorBU = wx.Button( self, wx.ID_ANY, _(u"Remove preperation"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_removefactorBU.SetBitmap( wx.Bitmap( u"ressources/Actions-file-close-icon.png", wx.BITMAP_TYPE_ANY ) )
		self.m_removefactorBU.SetToolTip( _(u"Delete selected factor preparation") )

		bSizer7.Add( self.m_removefactorBU, 0, wx.ALL, 5 )

		self.editPrepBU = wx.Button( self, wx.ID_ANY, _(u"Edit preparation"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.editPrepBU.SetBitmap( wx.Bitmap( u"ressources/edit-icon.png", wx.BITMAP_TYPE_ANY ) )
		self.editPrepBU.SetToolTip( _(u"Edit selected factor preparation") )

		bSizer7.Add( self.editPrepBU, 0, wx.ALL, 5 )


		gbSizer3.Add( bSizer7, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, _(u"Response preparations for this project"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )

		gbSizer3.Add( self.m_staticText13, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_respPrepsLCTR = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_SORT_ASCENDING )
		gbSizer3.Add( self.m_respPrepsLCTR, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_addRespPrepBUT = wx.Button( self, wx.ID_ANY, _(u"Add response preparation"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_addRespPrepBUT.SetBitmap( wx.Bitmap( u"ressources/Data-Add-Row-icon.png", wx.BITMAP_TYPE_ANY ) )
		self.m_addRespPrepBUT.SetToolTip( _(u"Add a response preparation") )

		bSizer8.Add( self.m_addRespPrepBUT, 0, wx.ALL, 5 )

		self.m_deleteRespPrepBUT = wx.Button( self, wx.ID_ANY, _(u"Remove preparation"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_deleteRespPrepBUT.SetBitmap( wx.Bitmap( u"ressources/Actions-file-close-icon.png", wx.BITMAP_TYPE_ANY ) )
		self.m_deleteRespPrepBUT.SetToolTip( _(u"Delete selected response preparation") )

		bSizer8.Add( self.m_deleteRespPrepBUT, 0, wx.ALL, 5 )

		self.m_editRespPrepBUT = wx.Button( self, wx.ID_ANY, _(u"Edit preperation"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_editRespPrepBUT.SetBitmap( wx.Bitmap( u"ressources/edit-icon.png", wx.BITMAP_TYPE_ANY ) )
		self.m_editRespPrepBUT.Hide()
		self.m_editRespPrepBUT.SetToolTip( _(u"Edit selected response preparation") )

		bSizer8.Add( self.m_editRespPrepBUT, 0, wx.ALL, 5 )


		gbSizer3.Add( bSizer8, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND, 7 )

		self.m_staticText27 = wx.StaticText( self, wx.ID_ANY, _(u"Calculate merged response"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )

		gbSizer3.Add( self.m_staticText27, wx.GBPosition( 10, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText28 = wx.StaticText( self, wx.ID_ANY, _(u"Merge formula"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText28.Wrap( -1 )

		gbSizer3.Add( self.m_staticText28, wx.GBPosition( 11, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_mergeFormulaTBX = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_BESTWRAP|wx.TE_MULTILINE )
		gbSizer3.Add( self.m_mergeFormulaTBX, wx.GBPosition( 11, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_doMergeCBX = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.CHK_2STATE )
		gbSizer3.Add( self.m_doMergeCBX, wx.GBPosition( 10, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_okcancelBUTS = wx.StdDialogButtonSizer()
		self.m_okcancelBUTSOK = wx.Button( self, wx.ID_OK )
		m_okcancelBUTS.AddButton( self.m_okcancelBUTSOK )
		self.m_okcancelBUTSCancel = wx.Button( self, wx.ID_CANCEL )
		m_okcancelBUTS.AddButton( self.m_okcancelBUTSCancel )
		m_okcancelBUTS.Realize();

		gbSizer3.Add( m_okcancelBUTS, wx.GBPosition( 12, 0 ), wx.GBSpan( 1, 4 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer3.AddGrowableCol( 1 )
		gbSizer3.AddGrowableCol( 3 )
		gbSizer3.AddGrowableRow( 3 )

		self.SetSizer( gbSizer3 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.EditProjectDialogOnInitDialog )
		self.Bind( wx.EVT_SHOW, self.EditProjectDialogOnShow )
		self.m_addEnviroBUT.Bind( wx.EVT_BUTTON, self.m_addEnviroBUTOnButtonClick )
		self.m_removeEnviroBUT.Bind( wx.EVT_BUTTON, self.m_removeEnviroBUTOnButtonClick )
		self.m_editEnviroBUT.Bind( wx.EVT_BUTTON, self.m_editEnviroBUTOnButtonClick )
		self.m_connfactorBU.Bind( wx.EVT_BUTTON, self.m_connfactorBUOnButtonClick )
		self.m_removefactorBU.Bind( wx.EVT_BUTTON, self.m_removefactorBUOnButtonClick )
		self.editPrepBU.Bind( wx.EVT_BUTTON, self.editPrepBUOnButtonClick )
		self.m_addRespPrepBUT.Bind( wx.EVT_BUTTON, self.m_addRespPrepBUTOnButtonClick )
		self.m_deleteRespPrepBUT.Bind( wx.EVT_BUTTON, self.m_deleteRespPrepBUTOnButtonClick )
		self.m_editRespPrepBUT.Bind( wx.EVT_BUTTON, self.m_editRespPrepBUTOnButtonClick )
		self.m_doMergeCBX.Bind( wx.EVT_CHECKBOX, self.m_doMergeCBXOnCheckBox )
		self.m_okcancelBUTSOK.Bind( wx.EVT_BUTTON, self.m_okcancelBUTSOnOKButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def EditProjectDialogOnInitDialog( self, event ):
		event.Skip()

	def EditProjectDialogOnShow( self, event ):
		event.Skip()

	def m_addEnviroBUTOnButtonClick( self, event ):
		event.Skip()

	def m_removeEnviroBUTOnButtonClick( self, event ):
		event.Skip()

	def m_editEnviroBUTOnButtonClick( self, event ):
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

	def m_editRespPrepBUTOnButtonClick( self, event ):
		event.Skip()

	def m_doMergeCBXOnCheckBox( self, event ):
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
## Class AddSubElementDialog
###########################################################################

class AddSubElementDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Select a {}"), pos = wx.DefaultPosition, size = wx.Size( 500,349 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer5 = wx.GridBagSizer( 0, 0 )
		gbSizer5.SetFlexibleDirection( wx.BOTH )
		gbSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_listHeadingSTXT = wx.StaticText( self, wx.ID_ANY, _(u"{}s not already present"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_listHeadingSTXT.Wrap( -1 )

		gbSizer5.Add( self.m_listHeadingSTXT, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_objectsLLCTR = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		self.m_objectsLLCTR.SetMinSize( wx.Size( 200,-1 ) )

		gbSizer5.Add( self.m_objectsLLCTR, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

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
		self.Bind( wx.EVT_INIT_DIALOG, self.AddSubElementDialogOnInitDialog )
		self.Bind( wx.EVT_SHOW, self.AddSubElementDialogOnShow )
		self.m_objectsLLCTR.Bind( wx.EVT_LEFT_DCLICK, self.m_objectsLLCTROnLeftDClick )
		self.m_objectsLLCTR.Bind( wx.EVT_LIST_ITEM_DESELECTED, self.m_objectsLLCTROnListItemDeselected )
		self.m_objectsLLCTR.Bind( wx.EVT_LIST_ITEM_SELECTED, self.m_objectsLLCTROnListItemSelected )
		self.m_sdbSizer3OK.Bind( wx.EVT_BUTTON, self.m_sdbSizer3OnOKButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def AddSubElementDialogOnInitDialog( self, event ):
		event.Skip()

	def AddSubElementDialogOnShow( self, event ):
		event.Skip()

	def m_objectsLLCTROnLeftDClick( self, event ):
		event.Skip()

	def m_objectsLLCTROnListItemDeselected( self, event ):
		event.Skip()

	def m_objectsLLCTROnListItemSelected( self, event ):
		event.Skip()

	def m_sdbSizer3OnOKButtonClick( self, event ):
		event.Skip()


###########################################################################
## Class EditPreparation
###########################################################################

class EditPreparation ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Edit factor preparation"), pos = wx.DefaultPosition, size = wx.Size( 807,556 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer6 = wx.GridBagSizer( 5, 5 )
		gbSizer6.SetFlexibleDirection( wx.BOTH )
		gbSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, _(u"Minimum value"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		gbSizer6.Add( self.m_staticText6, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_minValTBX = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer6.Add( self.m_minValTBX, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, _(u"Maximum value"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		gbSizer6.Add( self.m_staticText7, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_maxValTBX = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer6.Add( self.m_maxValTBX, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, _(u"Number of levels"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		gbSizer6.Add( self.m_staticText8, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_numLvlsTBX = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer6.Add( self.m_numLvlsTBX, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText381 = wx.StaticText( self, wx.ID_ANY, _(u"Can be combined"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText381.Wrap( -1 )

		gbSizer6.Add( self.m_staticText381, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_isCombinedCBX = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.CHK_2STATE )
		gbSizer6.Add( self.m_isCombinedCBX, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText39 = wx.StaticText( self, wx.ID_ANY, _(u"Combination Is negated"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText39.Wrap( -1 )

		gbSizer6.Add( self.m_staticText39, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_isNegatedCBX = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.CHK_2STATE )
		gbSizer6.Add( self.m_isNegatedCBX, wx.GBPosition( 3, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText38 = wx.StaticText( self, wx.ID_ANY, _(u"Combined from"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText38.Wrap( -1 )

		gbSizer6.Add( self.m_staticText38, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_factCombisLCTRL = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		gbSizer6.Add( self.m_factCombisLCTRL, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_addFactorBUT = wx.Button( self, wx.ID_ANY, _(u"MyButton"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_addFactorBUT.SetBitmap( wx.Bitmap( u"ressources/Data-Add-Row-icon.png", wx.BITMAP_TYPE_ANY ) )
		bSizer12.Add( self.m_addFactorBUT, 0, wx.ALL, 5 )

		self.m_removeFactorBUT = wx.Button( self, wx.ID_ANY, _(u"MyButton"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_removeFactorBUT.SetBitmap( wx.Bitmap( u"ressources/Actions-file-close-icon.png", wx.BITMAP_TYPE_ANY ) )
		bSizer12.Add( self.m_removeFactorBUT, 0, wx.ALL, 5 )


		gbSizer6.Add( bSizer12, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 3 ), wx.EXPAND, 5 )

		m_sdbSizer4 = wx.StdDialogButtonSizer()
		self.m_sdbSizer4OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer4.AddButton( self.m_sdbSizer4OK )
		self.m_sdbSizer4Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer4.AddButton( self.m_sdbSizer4Cancel )
		m_sdbSizer4.Realize();

		gbSizer6.Add( m_sdbSizer4, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 4 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer6.AddGrowableCol( 3 )
		gbSizer6.AddGrowableRow( 4 )

		self.SetSizer( gbSizer6 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.EditPreparationOnInitDialog )
		self.Bind( wx.EVT_SHOW, self.EditPreparationOnShow )
		self.m_addFactorBUT.Bind( wx.EVT_BUTTON, self.m_addFactorBUTOnButtonClick )
		self.m_removeFactorBUT.Bind( wx.EVT_BUTTON, self.m_removeFactorBUTOnButtonClick )
		self.m_sdbSizer4OK.Bind( wx.EVT_BUTTON, self.OnOKButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def EditPreparationOnInitDialog( self, event ):
		event.Skip()

	def EditPreparationOnShow( self, event ):
		event.Skip()

	def m_addFactorBUTOnButtonClick( self, event ):
		event.Skip()

	def m_removeFactorBUTOnButtonClick( self, event ):
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

		self.m_staticText29 = wx.StaticText( self, wx.ID_ANY, _(u"Create centre exp."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )

		gbSizer8.Add( self.m_staticText29, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer8.Add( self.m_staticline1, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_createCentreExpCKBX = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.CHK_2STATE )
		gbSizer8.Add( self.m_createCentreExpCKBX, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

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
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Multiple linear regression"), pos = wx.DefaultPosition, size = wx.Size( 827,734 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer9 = wx.GridBagSizer( 0, 0 )
		gbSizer9.SetFlexibleDirection( wx.BOTH )
		gbSizer9.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_projectNameSTXT = wx.StaticText( self, wx.ID_ANY, _(u"<projectname>"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_projectNameSTXT.Wrap( -1 )

		gbSizer9.Add( self.m_projectNameSTXT, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_linRegNBCK = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NB_TOP )
		self.m_regressionPNL = wx.Panel( self.m_linRegNBCK, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer13 = wx.GridBagSizer( 0, 0 )
		gbSizer13.SetFlexibleDirection( wx.BOTH )
		gbSizer13.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText18 = wx.StaticText( self.m_regressionPNL, wx.ID_ANY, _(u"Float precision"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )

		gbSizer13.Add( self.m_staticText18, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_precisionCHOIChoices = [ _(u"0"), _(u"1"), _(u"2"), _(u"3"), _(u"4"), _(u"5"), _(u"6") ]
		self.m_precisionCHOI = wx.Choice( self.m_regressionPNL, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_precisionCHOIChoices, 0 )
		self.m_precisionCHOI.SetSelection( 3 )
		gbSizer13.Add( self.m_precisionCHOI, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_normalzedCHKB = wx.CheckBox( self.m_regressionPNL, wx.ID_ANY, _(u"Normalised"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.CHK_2STATE )
		gbSizer13.Add( self.m_normalzedCHKB, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText19 = wx.StaticText( self.m_regressionPNL, wx.ID_ANY, _(u"Revised input data"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )

		gbSizer13.Add( self.m_staticText19, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_inputDataDLCTRL = wx.dataview.DataViewListCtrl( self.m_regressionPNL, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_inputDataDLCTRL.SetMinSize( wx.Size( 100,200 ) )

		gbSizer13.Add( self.m_inputDataDLCTRL, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.doCalcBUT = wx.Button( self.m_regressionPNL, wx.ID_ANY, _(u"Solve"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer13.Add( self.doCalcBUT, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText16 = wx.StaticText( self.m_regressionPNL, wx.ID_ANY, _(u"Summary"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		gbSizer13.Add( self.m_staticText16, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_summaryHTMLWIN = wx.html.HtmlWindow( self.m_regressionPNL, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_SCROLLBAR_AUTO )
		self.m_summaryHTMLWIN.SetMinSize( wx.Size( 100,100 ) )

		gbSizer13.Add( self.m_summaryHTMLWIN, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer13.AddGrowableCol( 2 )
		gbSizer13.AddGrowableRow( 2 )
		gbSizer13.AddGrowableRow( 5 )

		self.m_regressionPNL.SetSizer( gbSizer13 )
		self.m_regressionPNL.Layout()
		gbSizer13.Fit( self.m_regressionPNL )
		self.m_linRegNBCK.AddPage( self.m_regressionPNL, _(u"Regression Calculation"), False )
		self.m_residualsPNL = wx.Panel( self.m_linRegNBCK, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer14 = wx.GridBagSizer( 0, 0 )
		gbSizer14.SetFlexibleDirection( wx.BOTH )
		gbSizer14.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText252 = wx.StaticText( self.m_residualsPNL, wx.ID_ANY, _(u"Target response"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText252.Wrap( -1 )

		gbSizer14.Add( self.m_staticText252, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_resiTargetCHOIChoices = []
		self.m_resiTargetCHOI = wx.Choice( self.m_residualsPNL, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_resiTargetCHOIChoices, 0 )
		self.m_resiTargetCHOI.SetSelection( 0 )
		self.m_resiTargetCHOI.SetMinSize( wx.Size( 250,-1 ) )

		gbSizer14.Add( self.m_resiTargetCHOI, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_resiHelperPNL = wx.Panel( self.m_residualsPNL, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_resiHelperPNL.SetMinSize( wx.Size( 400,400 ) )

		gbSizer14.Add( self.m_resiHelperPNL, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer14.AddGrowableCol( 1 )
		gbSizer14.AddGrowableRow( 1 )

		self.m_residualsPNL.SetSizer( gbSizer14 )
		self.m_residualsPNL.Layout()
		gbSizer14.Fit( self.m_residualsPNL )
		self.m_linRegNBCK.AddPage( self.m_residualsPNL, _(u"Residuals"), True )
		self.m_predictionPNL = wx.Panel( self.m_linRegNBCK, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		gbSizer11 = wx.GridBagSizer( 0, 0 )
		gbSizer11.SetFlexibleDirection( wx.BOTH )
		gbSizer11.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText24 = wx.StaticText( self.m_predictionPNL, wx.ID_ANY, _(u"Formula"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText24.Wrap( -1 )

		gbSizer11.Add( self.m_staticText24, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_targetCHOIChoices = []
		self.m_targetCHOI = wx.Choice( self.m_predictionPNL, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_targetCHOIChoices, 0 )
		self.m_targetCHOI.SetSelection( 0 )
		gbSizer11.Add( self.m_targetCHOI, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticText27 = wx.StaticText( self.m_predictionPNL, wx.ID_ANY, _(u"Factor precision"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )

		gbSizer11.Add( self.m_staticText27, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_factorPrecisionCHOIChoices = [ _(u"0"), _(u"1"), _(u"2"), _(u"3"), _(u"4"), _(u"5"), _(u"6") ]
		self.m_factorPrecisionCHOI = wx.Choice( self.m_predictionPNL, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_factorPrecisionCHOIChoices, wx.CB_SORT )
		self.m_factorPrecisionCHOI.SetSelection( 0 )
		gbSizer11.Add( self.m_factorPrecisionCHOI, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_formulaTBX = wx.TextCtrl( self.m_predictionPNL, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer11.Add( self.m_formulaTBX, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_staticline2 = wx.StaticLine( self.m_predictionPNL, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer11.Add( self.m_staticline2, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 2 ), wx.EXPAND |wx.ALL, 5 )

		self.m_staticText25 = wx.StaticText( self.m_predictionPNL, wx.ID_ANY, _(u"Target response"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText25.Wrap( -1 )

		gbSizer11.Add( self.m_staticText25, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText241 = wx.StaticText( self.m_predictionPNL, wx.ID_ANY, _(u"Factors"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText241.Wrap( -1 )

		gbSizer11.Add( self.m_staticText241, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_factorsPGRD = pg.PropertyGrid(self.m_predictionPNL, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE)
		gbSizer11.Add( self.m_factorsPGRD, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_calcAllBUT = wx.Button( self.m_predictionPNL, wx.ID_ANY, _(u"Calculate All"), wx.DefaultPosition, wx.DefaultSize, 0 )
		gbSizer11.Add( self.m_calcAllBUT, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_staticText251 = wx.StaticText( self.m_predictionPNL, wx.ID_ANY, _(u"Responses"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText251.Wrap( -1 )

		gbSizer11.Add( self.m_staticText251, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_responsesPGRD = pg.PropertyGrid(self.m_predictionPNL, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.propgrid.PG_DEFAULT_STYLE)
		gbSizer11.Add( self.m_responsesPGRD, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer11.AddGrowableCol( 1 )
		gbSizer11.AddGrowableRow( 4 )
		gbSizer11.AddGrowableRow( 6 )

		self.m_predictionPNL.SetSizer( gbSizer11 )
		self.m_predictionPNL.Layout()
		gbSizer11.Fit( self.m_predictionPNL )
		self.m_linRegNBCK.AddPage( self.m_predictionPNL, _(u"Prediction"), False )

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
		self.m_figure = Figure()
		self.m_axes = self.m_figure.add_subplot(111)
		self.m_canvas = FigureCanvas(self.m_resiHelperPNL, -1, self.m_figure)
		#self.m_toolbar = NavigationToolbar2Wx(self.m_canvas)
		#self.m_toolbar.Realize()
		#gbSizer14.Add(self.m_canvas, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.LEFT | wx.EXPAND | wx.GROW, 5)
		#gbSizer14.Add(self.m_toolbar, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.LEFT | wx.EXPAND, 5)

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.LinRegrDialogOnInitDialog )
		self.Bind( wx.EVT_SHOW, self.LinRegrDialogOnShow )
		self.m_linRegNBCK.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.m_linRegNBCKOnNotebookPageChanged )
		self.m_precisionCHOI.Bind( wx.EVT_CHOICE, self.m_precisionCHOIOnChoice )
		self.m_normalzedCHKB.Bind( wx.EVT_CHECKBOX, self.m_normalzedCHKBOnCheckBox )
		self.doCalcBUT.Bind( wx.EVT_BUTTON, self.doCalcBUTOnButtonClick )
		self.m_resiTargetCHOI.Bind( wx.EVT_CHOICE, self.m_resiTargetCHOIOnChoice )
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

	def m_normalzedCHKBOnCheckBox( self, event ):
		event.Skip()

	def doCalcBUTOnButtonClick( self, event ):
		event.Skip()

	def m_resiTargetCHOIOnChoice( self, event ):
		event.Skip()

	def m_targetCHOIOnChoice( self, event ):
		event.Skip()

	def m_factorPrecisionCHOIOnChoice( self, event ):
		event.Skip()

	def m_calcAllBUTOnButtonClick( self, event ):
		event.Skip()


###########################################################################
## Class EditResponsePreparation
###########################################################################

class EditResponsePreparation ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Response Preparation"), pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gbSizer15 = wx.GridBagSizer( 0, 0 )
		gbSizer15.SetFlexibleDirection( wx.BOTH )
		gbSizer15.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText26 = wx.StaticText( self, wx.ID_ANY, _(u"Combination Weight"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )

		gbSizer15.Add( self.m_staticText26, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_combiWeightTCTRL = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_combiWeightTCTRL.SetToolTip( _(u"enter a float to be used as a weight for the combined response") )

		gbSizer15.Add( self.m_combiWeightTCTRL, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_sdbSizer8 = wx.StdDialogButtonSizer()
		self.m_sdbSizer8OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer8.AddButton( self.m_sdbSizer8OK )
		self.m_sdbSizer8Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer8.AddButton( self.m_sdbSizer8Cancel )
		m_sdbSizer8.Realize();

		gbSizer15.Add( m_sdbSizer8, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( gbSizer15 )
		self.Layout()
		gbSizer15.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.EditResponsePreparationOnInitDialog )
		self.m_sdbSizer8OK.Bind( wx.EVT_BUTTON, self.m_sdbSizer8OnOKButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def EditResponsePreparationOnInitDialog( self, event ):
		event.Skip()

	def m_sdbSizer8OnOKButtonClick( self, event ):
		event.Skip()


###########################################################################
## Class CreateFractDetail
###########################################################################

class CreateFractDetail ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Create fractional factoial details"), pos = wx.DefaultPosition, size = wx.Size( 515,551 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

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

		self.m_staticText29 = wx.StaticText( self, wx.ID_ANY, _(u"Create centre exp."), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText29.Wrap( -1 )

		gbSizer8.Add( self.m_staticText29, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_createCentreExpCKBX = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.CHK_2STATE )
		gbSizer8.Add( self.m_createCentreExpCKBX, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_combiPrepsLCTR = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		gbSizer8.Add( self.m_combiPrepsLCTR, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_addCombiBUT = wx.Button( self, wx.ID_ANY, _(u"MyButton"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_addCombiBUT.SetBitmap( wx.Bitmap( u"ressources/Data-Add-Row-icon.png", wx.BITMAP_TYPE_ANY ) )
		bSizer11.Add( self.m_addCombiBUT, 0, wx.ALL, 5 )

		self.m_removeCombiBUT = wx.Button( self, wx.ID_ANY, _(u"MyButton"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_removeCombiBUT.SetBitmap( wx.Bitmap( u"ressources/Actions-file-close-icon.png", wx.BITMAP_TYPE_ANY ) )
		bSizer11.Add( self.m_removeCombiBUT, 0, wx.ALL, 5 )

		self.m_editCombiBUT = wx.Button( self, wx.ID_ANY, _(u"MyButton"), wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT|wx.BU_NOTEXT )

		self.m_editCombiBUT.SetBitmap( wx.Bitmap( u"ressources/edit-icon.png", wx.BITMAP_TYPE_ANY ) )
		bSizer11.Add( self.m_editCombiBUT, 0, wx.ALL, 5 )


		gbSizer8.Add( bSizer11, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		gbSizer8.Add( self.m_staticline1, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		m_sdbSizer6 = wx.StdDialogButtonSizer()
		self.m_sdbSizer6OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer6.AddButton( self.m_sdbSizer6OK )
		self.m_sdbSizer6Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer6.AddButton( self.m_sdbSizer6Cancel )
		m_sdbSizer6.Realize();

		gbSizer8.Add( m_sdbSizer6, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )


		gbSizer8.AddGrowableCol( 1 )
		gbSizer8.AddGrowableRow( 4 )

		self.SetSizer( gbSizer8 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.CreateFractDetailOnInitDialog )
		self.Bind( wx.EVT_SHOW, self.CreateFractDetailOnShow )
		self.m_addCombiBUT.Bind( wx.EVT_BUTTON, self.m_addCombiBUTOnButtonClick )
		self.m_removeCombiBUT.Bind( wx.EVT_BUTTON, self.m_removeCombiBUTOnButtonClick )
		self.m_editCombiBUT.Bind( wx.EVT_BUTTON, self.m_editCombiBUTOnButtonClick )
		self.m_sdbSizer6OK.Bind( wx.EVT_BUTTON, self.m_sdbSizer6OnOKButtonClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def CreateFractDetailOnInitDialog( self, event ):
		event.Skip()

	def CreateFractDetailOnShow( self, event ):
		event.Skip()

	def m_addCombiBUTOnButtonClick( self, event ):
		event.Skip()

	def m_removeCombiBUTOnButtonClick( self, event ):
		event.Skip()

	def m_editCombiBUTOnButtonClick( self, event ):
		event.Skip()

	def m_sdbSizer6OnOKButtonClick( self, event ):
		event.Skip()


