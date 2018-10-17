# !/usr/bin/env python
#  -*- coding: utf-8 -*-
""" 
Класс панели патчинга конфигурации 1с.
"""
__version__ = (0,0,0,1)

#--- Imports ---
import os,os.path
import wx
import sys

import icWizardPanelProto

from utils import dlg
from utils import util

class icPatcherPanel(icWizardPanelProto.icPatcherPanelPrototype):
    """
    Класс панели патчинга конфигурации 1с.
    """
    def __init__(self,*args,**kwargs):
        """
        Конструтор.
        """
        icWizardPanelProto.icPatcherPanelPrototype.__init__(self,*args,**kwargs)

    def onCFDirChoiceButtonMouseClick(self,event):
        """
        Обработчик кнопки выбора папки конфигурации 1с.
        """
        default_dir=os.getcwd()
        cf_dir_path=dlg.getDirDlg(self,u'Выберите папку конфигурации 1с',default_dir)
        if cf_dir_path:
            self.cfDirTxt.SetValue(cf_dir_path)
            
        event.Skip()
