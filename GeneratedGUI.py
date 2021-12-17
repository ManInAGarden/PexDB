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
		self.quit_menuitem = wx.MenuItem( self.file_menu, wx.ID_ANY, _(u"Quit program"), wx.EmptyString, wx.ITEM_NORMAL )
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

		self.m_menubar1.Append( self.factors_menu, _(u"Faktoren") )

		self.result_menu = wx.Menu()
		self.edit_result_definitions_menuItem = wx.MenuItem( self.result_menu, wx.ID_ANY, _(u"Edit result definitions"), wx.EmptyString, wx.ITEM_NORMAL )
		self.result_menu.Append( self.edit_result_definitions_menuItem )

		self.m_menubar1.Append( self.result_menu, _(u"Results") )

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
		main_gsizer.Add( self.m_experimentPG, 0, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( main_gsizer )
		self.Layout()
		self.m_menu6 = wx.Menu()
		self.Bind( wx.EVT_RIGHT_DOWN, self.PexViewerMainFrameOnContextMenu )


		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_MENU, self.quit_PexViewer, id = self.quit_menuitem.GetId() )
		self.Bind( wx.EVT_MENU, self.create_new_experiment, id = self.newExperiment_menuitem.GetId() )
		self.Bind( wx.EVT_MENU, self.dupicate_experiment_menuitemOnMenuSelection, id = self.dupicate_experiment_menuitem.GetId() )
		self.Bind( wx.EVT_MENU, self.delete_experiment_menuItemOnMenuSelection, id = self.delte_experiment_menuItem.GetId() )
		self.Bind( wx.EVT_MENU, self.m_edit_factors_menuitemOnMenuSelection, id = self.m_edit_factors_menuitem.GetId() )
		self.m_experimentsDataViewListCtrl.Bind( wx.dataview.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.m_experimentsDataViewListCtrlOnDataViewListCtrlItemContextMenu, id = wx.ID_ANY )
		self.m_experimentsDataViewListCtrl.Bind( wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.experimentDWLC_selchanged, id = wx.ID_ANY )
		self.m_experimentPG.Bind( pg.EVT_PG_CHANGED, self.propgridChanged )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
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

	def m_experimentsDataViewListCtrlOnDataViewListCtrlItemContextMenu( self, event ):
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


