# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class icCFPatcherFramePrototype
###########################################################################

class icCFPatcherFramePrototype ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Изменить конфигурацию 1С:", pos = wx.DefaultPosition, size = wx.Size( 896,429 ), style = wx.DEFAULT_FRAME_STYLE|wx.RAISED_BORDER|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"img/1c_wiz.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_bitmap1, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Файл конфигурации:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer8.Add( self.m_staticText1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.cfFileTxt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizer8.Add( self.cfFileTxt, 1, wx.ALL, 5 )
		
		self.CFFileButton = wx.Button( self, wx.ID_ANY, u"...", wx.DefaultPosition, wx.Size( 24,-1 ), 0 )
		bSizer8.Add( self.CFFileButton, 0, wx.ALL, 5 )
		
		bSizer6.Add( bSizer8, 0, wx.EXPAND, 5 )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		self.ScriptToolbar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.ScriptToolbar.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"img/script--plus.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString ) 
		self.ScriptToolbar.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"img/script--minus.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString ) 
		self.ScriptToolbar.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"img/script--pencil.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString ) 
		self.ScriptToolbar.AddSeparator()
		self.ScriptToolbar.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"img/arrow-090.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString ) 
		self.ScriptToolbar.AddLabelTool( wx.ID_ANY, u"tool", wx.Bitmap( u"img/arrow-270.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString ) 
		self.ScriptToolbar.Realize()
		
		bSizer9.Add( self.ScriptToolbar, 0, wx.EXPAND, 5 )
		
		self.scriptListCtrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_HRULES|wx.LC_REPORT|wx.LC_VRULES )
		bSizer9.Add( self.scriptListCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer6.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Результирующий файл:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer10.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.resultFileTxt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.resultFileTxt, 1, wx.ALL, 5 )
		
		self.ResultFileButton = wx.Button( self, wx.ID_ANY, u"...", wx.DefaultPosition, wx.Size( 24,-1 ), 0 )
		bSizer10.Add( self.ResultFileButton, 0, wx.ALL, 5 )
		
		bSizer6.Add( bSizer10, 0, wx.EXPAND, 5 )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.runButton = wx.Button( self, wx.ID_ANY, u"Запуск", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.runButton.SetDefault() 
		bSizer11.Add( self.runButton, 0, wx.ALL, 5 )
		
		bSizer6.Add( bSizer11, 0, wx.ALIGN_RIGHT, 5 )
		
		bSizer7.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer7 )
		self.Layout()
		self.logStatusBar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.CFFileButton.Bind( wx.EVT_BUTTON, self.CFFileButtonOnButtonClick )
		self.Bind( wx.EVT_TOOL, self.addToolOnToolClicked, id = wx.ID_ANY )
		self.Bind( wx.EVT_TOOL, self.delToolOnToolClicked, id = wx.ID_ANY )
		self.Bind( wx.EVT_TOOL, self.editToolOnToolClicked, id = wx.ID_ANY )
		self.Bind( wx.EVT_TOOL, self.moveUpToolOnToolClicked, id = wx.ID_ANY )
		self.Bind( wx.EVT_TOOL, self.moveDownToolOnToolClicked, id = wx.ID_ANY )
		self.scriptListCtrl.Bind( wx.EVT_LIST_ITEM_SELECTED, self.scriptListCtrlOnListItemSelected )
		self.ResultFileButton.Bind( wx.EVT_BUTTON, self.ResultFileButtonOnButtonClick )
		self.runButton.Bind( wx.EVT_BUTTON, self.runButtonOnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def CFFileButtonOnButtonClick( self, event ):
		event.Skip()
	
	def addToolOnToolClicked( self, event ):
		event.Skip()
	
	def delToolOnToolClicked( self, event ):
		event.Skip()
	
	def editToolOnToolClicked( self, event ):
		event.Skip()
	
	def moveUpToolOnToolClicked( self, event ):
		event.Skip()
	
	def moveDownToolOnToolClicked( self, event ):
		event.Skip()
	
	def scriptListCtrlOnListItemSelected( self, event ):
		event.Skip()
	
	def ResultFileButtonOnButtonClick( self, event ):
		event.Skip()
	
	def runButtonOnButtonClick( self, event ):
		event.Skip()
	

