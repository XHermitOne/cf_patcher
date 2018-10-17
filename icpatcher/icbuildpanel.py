# !/usr/bin/env python
#  -*- coding: utf-8 -*-
""" 
Класс панели построения файла CF конфигурации 1с.
"""
__version__ = (0,0,0,1)

#--- Imports ---
import os,os.path
import wx
import sys

import icWizardPanelProto

from utils import dlg
from utils import util

class icBuildPanel(icWizardPanelProto.icBuildPanelPrototype):
    """
    Класс панели построения файла CF конфигурации 1с.
    """
    def __init__(self,*args,**kwargs):
        """
        Конструтор.
        """
        icWizardPanelProto.icBuildPanelPrototype.__init__(self,*args,**kwargs)

    def onCFFileChoiceButtonMouseClick(self,event):
        """
        Обработчик кнопки выбора CF файла конфигурации 1с.
        """
        default_dir=os.getcwd()
        cf_file_name=dlg.getFileNameDlg(self,u'Выберите файл конфигурации 1с',
            u'Файл конфигурации 1с(*.cf)|*.cf',default_dir)
        if cf_file_name:
            self.cfFileTxt.SetValue(cf_file_name)
            default_dir=os.path.dir_name(cf_file_name)+'/'+os.path.basename(cf_file_name).replace('.','_')
            self.cfDirTxt.SetValue(default_dir)
        event.Skip()
