#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple dialog functions.
"""
import wx
import os.path

def getFileNameDlg(parent=None,sTitle=u'',sFilter=u'',sDefaultDir=''):
    """
    Open select file name dialog.
    @param parent: Parent window.
    @param sTitle: Dialog title.
    @param sFilter: File filter.
    @param sDefaultDir: Default directory.
    @return: Full file name.
    """
    try:
        dlg=None
        
        if parent is None:
           parent=wx.GetApp().GetTopWindow()

        wildcard=sFilter+u'|All Files (*.*)|*.*'
        dlg=wx.FileDialog(parent,sTitle,u'',u'',wildcard,wx.OPEN)
        if sDefaultDir:
            dlg.SetDirectory(os.path.normpath(sDefaultDir))
        
        if dlg.ShowModal()==wx.ID_OK:
            result=dlg.GetPaths()[0]
        else:
            result=u''
        dlg.Destroy()
        return result
    finally:
        if dlg:
            dlg.Destroy()

    return None

def getDirDlg(parent=None,sTitle=u'',sDefaultDir=''):
    """
    Open select directory path dialog.
    @param parent: Parent window.
    @param sTitle: Dialog title.
    @param sDefaultDir: Default directory.
    @return: Full directory path.
    """
    try:
        dlg=None
        
        if parent is None:
           parent=wx.GetApp().GetTopWindow()

        dlg=wx.DirDialog(parent,sTitle,
            style=wx.DD_DEFAULT_STYLE|wx.DD_NEW_DIR_BUTTON)
        if sDefaultDir:
            dlg.SetPath(os.path.normpath(sDefaultDir))
        
        if dlg.ShowModal()==wx.ID_OK:
            result=dlg.GetPath()
        else:
            result=u''
        dlg.Destroy()
        return result
    finally:
        if dlg:
            dlg.Destroy()

    return None

def getAskDlg(sTitle=u'',sMsg=u''):
    """
    Ask message box YES or NO.
    @return: True-yes/False-no.
    """
    return wx.MessageBox(sMsg,sTitle,wx.YES_NO)==wx.YES

def MsgBox(sTitle=u'',sMsg=u''):
    """
    Simple message box.
    """
    return wx.MessageBox(sMsg,sTitle,wx.OK)
    