# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

ADD_TOOL_ID = 1000
DEL_TOOL_ID = 1001
EDT_TOOL_ID = 1002
UP_TOOL_ID = 1003
DOWN_TOOL_ID = 1004
CF_FILE_BTN_ID = 1005
CF_DIR_BTN_ID = 1006

###########################################################################
## Class icScriptChoicePanelPrototype
###########################################################################

class icScriptChoicePanelPrototype ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.ctrlToolBar = wx.ToolBar( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL ) 
		self.ctrlToolBar.AddLabelTool( ADD_TOOL_ID, u"tool", wx.Bitmap( u"img/script--plus.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString ) 
		self.ctrlToolBar.AddLabelTool( DEL_TOOL_ID, u"tool", wx.Bitmap( u"img/script--minus.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString ) 
		self.ctrlToolBar.AddLabelTool( EDT_TOOL_ID, u"tool", wx.Bitmap( u"img/script--pencil.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString ) 
		self.ctrlToolBar.AddSeparator()
		self.ctrlToolBar.AddLabelTool( UP_TOOL_ID, u"tool", wx.Bitmap( u"img/arrow-090.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString ) 
		self.ctrlToolBar.AddLabelTool( DOWN_TOOL_ID, u"tool", wx.Bitmap( u"img/arrow-270.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString ) 
		self.ctrlToolBar.Realize()
		
		bSizer1.Add( self.ctrlToolBar, 0, wx.EXPAND, 5 )
		
		self.scriptListCtrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_HRULES|wx.LC_REPORT|wx.LC_VRULES )
		bSizer1.Add( self.scriptListCtrl, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_TOOL, self.onAddToolMouseClick, id = ADD_TOOL_ID )
		self.Bind( wx.EVT_TOOL, self.onDelToolMouseClick, id = DEL_TOOL_ID )
		self.Bind( wx.EVT_TOOL, self.onEditToolMouseClick, id = EDT_TOOL_ID )
		self.Bind( wx.EVT_TOOL, self.onMoveUpToolMouseClick, id = UP_TOOL_ID )
		self.Bind( wx.EVT_TOOL, self.onMoveDownToolMouseClick, id = DOWN_TOOL_ID )
		self.scriptListCtrl.Bind( wx.EVT_LIST_ITEM_SELECTED, self.onListItemSelected )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onAddToolMouseClick( self, event ):
		event.Skip()
	
	def onDelToolMouseClick( self, event ):
		event.Skip()
	
	def onEditToolMouseClick( self, event ):
		event.Skip()
	
	def onMoveUpToolMouseClick( self, event ):
		event.Skip()
	
	def onMoveDownToolMouseClick( self, event ):
		event.Skip()
	
	def onListItemSelected( self, event ):
		event.Skip()
	

###########################################################################
## Class icParsePanelPrototype
###########################################################################

class icParsePanelPrototype ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 3, 3, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"img/1c.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_bitmap1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.cfFileTxt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		fgSizer1.Add( self.cfFileTxt, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.cfFileChoiceButton = wx.Button( self, CF_FILE_BTN_ID, u"...", wx.DefaultPosition, wx.Size( 26,-1 ), 0 )
		fgSizer1.Add( self.cfFileChoiceButton, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_bitmap2 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"img/folder-open.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_bitmap2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.cfDirTxt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.cfDirTxt, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.cfDirChoiceButton = wx.Button( self, CF_DIR_BTN_ID, u"...", wx.DefaultPosition, wx.Size( 26,-1 ), 0 )
		fgSizer1.Add( self.cfDirChoiceButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		bSizer2.Add( fgSizer1, 0, wx.EXPAND, 5 )
		
		self.logTxt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP )
		self.logTxt.SetForegroundColour( wx.Colour( 0, 255, 0 ) )
		self.logTxt.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
		
		bSizer2.Add( self.logTxt, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.SetSizer( bSizer2 )
		self.Layout()
		
		# Connect Events
		self.cfFileChoiceButton.Bind( wx.EVT_BUTTON, self.onCFFileChoiceButtonMouseClick )
		self.cfDirChoiceButton.Bind( wx.EVT_BUTTON, self.onCFDirChoiceButtonMouseClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCFFileChoiceButtonMouseClick( self, event ):
		event.Skip()
	
	def onCFDirChoiceButtonMouseClick( self, event ):
		event.Skip()
	

###########################################################################
## Class icPatcherPanelPrototype
###########################################################################

class icPatcherPanelPrototype ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bitmap3 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"img/folder-open.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_bitmap3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.cfDirTxt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.cfDirTxt, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.cfDirChoiceButton = wx.Button( self, CF_DIR_BTN_ID, u"...", wx.DefaultPosition, wx.Size( 26,-1 ), 0 )
		bSizer4.Add( self.cfDirChoiceButton, 0, wx.ALL, 5 )
		
		bSizer3.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		self.logTxt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.logTxt.SetForegroundColour( wx.Colour( 0, 255, 0 ) )
		self.logTxt.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
		
		bSizer3.Add( self.logTxt, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.SetSizer( bSizer3 )
		self.Layout()
		
		# Connect Events
		self.cfDirChoiceButton.Bind( wx.EVT_BUTTON, self.onCFDirChoiceButtonMouseClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCFDirChoiceButtonMouseClick( self, event ):
		event.Skip()
	

###########################################################################
## Class icBuildPanelPrototype
###########################################################################

class icBuildPanelPrototype ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bitmap4 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"img/1c.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_bitmap4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.cfFileTxt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.cfFileTxt, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.cfFileChoiceButton = wx.Button( self, CF_FILE_BTN_ID, u"...", wx.DefaultPosition, wx.Size( 26,-1 ), 0 )
		bSizer6.Add( self.cfFileChoiceButton, 0, wx.ALL, 5 )
		
		bSizer5.Add( bSizer6, 0, wx.EXPAND, 5 )
		
		self.logTxt = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.logTxt.SetForegroundColour( wx.Colour( 0, 255, 0 ) )
		self.logTxt.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
		
		bSizer5.Add( self.logTxt, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.SetSizer( bSizer5 )
		self.Layout()
		
		# Connect Events
		self.cfFileChoiceButton.Bind( wx.EVT_BUTTON, self.onCFFileChoiceButtonMouseClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onCFFileChoiceButtonMouseClick( self, event ):
		event.Skip()
	

