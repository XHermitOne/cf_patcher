# !/usr/bin/env python
#  -*- coding: utf-8 -*-
""" 
Страницы визарда патчера.
"""
__version__ = (0,0,0,1)

#--- Imports ---
import sys
import os
import shutil

import wx
import wx.wizard

#import util
from utils import log
from utils import dlg

import patch_cmd

#--- Constants ---
#INSTALL_PACKAGES_DIR_DEFAULT='/packages/'

#Режимы доступа к инсталлируемым файлам/папкам
#PUBLIC_MODE='public'
#PROTECT_MODE='protect'


#--- Functions ---
def makeStdPageTitle(wizPg, title):
    """
    Функция стандартного создания заголовка страницы
    """
    sizer = wx.BoxSizer(wx.VERTICAL)
    wizPg.SetSizer(sizer)
    title = wx.StaticText(wizPg, -1, title)
    title.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
    sizer.Add(title, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    sizer.Add(wx.StaticLine(wizPg, -1), 0, wx.EXPAND|wx.ALL, 5)
    return sizer

#--- Classes ---
import icparsepanel
class icCFParsePage(wx.wizard.PyWizardPage):
    """
    Страница парсинга CF файла конфигурации 1с.
    """
    def __init__(self, parent, title):
        """
        Конструктор.
        @param parent: Родительский визард, в который вставляется страница.
        @param title: Заголовок страницы.
        """
        
        wx.wizard.PyWizardPage.__init__(self, parent)
        
        self.next = None
        self.prev = None
        
        self.sizer = makeStdPageTitle(self, title)

        self.cf_parse_panel=icparsepanel.icParsePanel(self)
        self.sizer.Add(self.cf_parse_panel, 1, wx.EXPAND|wx.GROW, 5)        

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        """
        """
        wizard=self.GetParent()
        cf_filename=self.cf_parse_panel.cfFileTxt.GetValue()
        cf_dir=self.cf_parse_panel.cfDirTxt.GetValue()
        if not cf_filename or not cf_dir:
            self.SetNext(wizard.getFinishPage())
        return self.next
        
    def GetPrev(self):
        return self.prev

    def on_changing(self,event):
        """
        Обработчик смены страницы визарда.
        Это обработчик срабатывает после нажатия на кнопку <Next>.
        """
        wizard=self.GetParent()

        #Сохранить в окружении визарда выбранный CF файл 
        #и директорию конфигурации 1с
        wizard.environment['cf_filename']=self.cf_parse_panel.cfFileTxt.GetValue()
        wizard.environment['cf_dir']=self.cf_parse_panel.cfDirTxt.GetValue()
#        if not wizard.environment['cf_filename'] or not wizard.environment['cf_dir']:
#            self.SetNext(wizard.getFinishPage())
#            return
        
        #Запустить парсинг файла конфигурации
        self.parse_cf_file(wizard.environment['cf_filename'],wizard.environment['cf_dir'])

    def parse_cf_file(self,CFFileName_,CFDir_):
        """
        Парсинг файла конфигурации 1с.
        @param CFFileName_: Полное имя CF файла конфигурации 1c.
        @param CFDir_: Директория, в которую бедет происходить парсинг.
        """
        return patch_cmd.parse_cf_file(CFFileName_,CFDir_)
    
import icsmarttreelistctrl    
class icCFChoicePage(wx.wizard.PyWizardPage):
    """
    Страница выбора метаобъектов конфигурации 1с для изменения.
    """
    def __init__(self, parent, title):
        """
        Конструктор.
        @param parent: Родительский визард, в который вставляется страница.
        @param title: Заголовок страницы.
        """
        
        wx.wizard.PyWizardPage.__init__(self, parent)
        
        self.next = None
        self.prev = None
        
        self.sizer = makeStdPageTitle(self, title)
        
        id=wx.NewId()
        wizard=self.GetParent()
        
        title_root=u'----'
        if 'cf_filename' in wizard.environment:
            title_root=os.path.basename(wizard.environment['cf_filename'])
        img_root_filename=os.path.dirname(__file__)+'/img/1c.png'   
        img_root=None
        if os.path.exists(img_root_filename):
            img_root=wx.Image(img_root_filename,wx.BITMAP_TYPE_PNG).ConvertToBitmap()            
        #print 'IMG ROOT:::',img_root_filename,os.path.exists(img_root_filename),img_root
            
        self.cf_tree_list_ctrl=icsmarttreelistctrl.icSmartTreeListCtrl(self, 
            id,position=wx.DefaultPosition,size=wx.DefaultSize,
            style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_BUTTONS,
            labels=[u'Метаобъект',u''],wcols=[300,100],
            titleRoot=title_root,imgRoot=img_root)
        self.sizer.Add(self.cf_tree_list_ctrl, 1, wx.EXPAND|wx.GROW, 5)        

    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next
        
    def GetPrev(self):
        return self.prev
    
    def on_changed(self,event):
        """
        Перед открытием этой страницы.
        """
        #Построить список метаобъектов конфигурации 1с для компонента выбора
        wizard=self.GetParent()
        cf_analyzer=wizard.getCFAnalyzer()
        cf_obj_lst=cf_analyzer.createCFList(wizard.environment['cf_dir'])
        #print 'CFLIST:::',cf_obj_lst
        self.cf_tree_list_ctrl.LoadTree(cf_obj_lst)

    def on_changing(self,event):
        """
        Обработчик смены страницы визарда.
        Этот обработчик срабатывает после нажатия на кнопку <Next>.
        """
        wizard=self.GetParent()
        cf_analyzer=wizard.getCFAnalyzer()
        metaobjects=cf_analyzer.getMetaobjects(self.cf_tree_list_ctrl.getItemCheckList())
        #print 'METAOBJECTS:::',metaobjects
        wizard.environment['cf_metaobjects']=metaobjects
        wizard.environment['cf_root']=cf_analyzer.getRootMetaobject()
        
import icscriptlistpanel
class icCFScriptPage(wx.wizard.PyWizardPage):
    """
    Страница выбора сценариев изменения метаобъектов конфигурации 1с.
    """
    def __init__(self, parent, title):
        """
        Конструктор.
        @param parent: Родительский визард, в который вставляется страница.
        @param title: Заголовок страницы.
        """
        
        wx.wizard.PyWizardPage.__init__(self, parent)
        
        self.next = None
        self.prev = None
        
        self.sizer = makeStdPageTitle(self, title)
        
        self.cf_script_list_panel=icscriptlistpanel.icScriptListPanel(self)
        self.sizer.Add(self.cf_script_list_panel, 1, wx.EXPAND|wx.GROW, 5)        
        
    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next
        
    def GetPrev(self):
        return self.prev
    
    def on_changing(self,event):
        """
        Обработчик смены страницы визарда.
        Это обработчик срабатывает после нажатия на кнопку <Next>.
        """
        wizard=self.GetParent()
    
        wizard.environment['cf_scripts']=self.cf_script_list_panel.getScriptFiles()
        
import icpatchpanel
class icCFPatchPage(wx.wizard.PyWizardPage):
    """
    Страница изменения метаобъектов конфигурации 1с.
    """
    def __init__(self, parent, title):
        """
        Конструктор.
        @param parent: Родительский визард, в который вставляется страница.
        @param title: Заголовок страницы.
        """
        
        wx.wizard.PyWizardPage.__init__(self, parent)
        
        self.next = None
        self.prev = None
        
        self.sizer = makeStdPageTitle(self, title)

        self.cf_patch_panel=icpatchpanel.icPatcherPanel(self)
        self.sizer.Add(self.cf_patch_panel, 1, wx.EXPAND|wx.GROW, 5)        
        
    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next
        
    def GetPrev(self):
        return self.prev

    def on_changed(self,event):
        """
        Перед открытием этой страницы.
        """
        wizard=self.GetParent()
        
        default_dir=wizard.environment['cf_dir']
        self.cf_patch_panel.cfDirTxt.SetValue(default_dir)
        
    def on_changing(self,event):
        """
        Обработчик смены страницы визарда.
        Это обработчик срабатывает после нажатия на кнопку <Next>.
        """
        wizard=self.GetParent()
        
        cf_dir=self.cf_patch_panel.cfDirTxt.GetValue()
        cf_dir=os.path.abspath(cf_dir)
        if wizard.environment['cf_dir']<>cf_dir:
            #Если папки не равны тогда скопировать одну в другую
            if os.path.exists(cf_dir):
                shutil.rmtree(cf_dir,True)
            shutil.copytree(wizard.environment['cf_dir'],cf_dir)
        wizard.environment['cf_patch_dir']=cf_dir
        #
        self.patch_cf_dir(cf_dir)
    
    def patch_cf_dir(self,CFDir_):
        """
        Пропатчить конфигурацию.
        @param CFDir_: Директория конфигурации 1с.
        """
        wizard=self.GetParent()
        patcher=wizard.environment['cf_patcher']
        return patcher.patch(CFDir_,
            wizard.environment['cf_metaobjects'],
            wizard.environment['cf_scripts'],
            wizard.environment['cf_root'])

import icbuildpanel
class icCFBuildPage(wx.wizard.PyWizardPage):
    """
    Страница построения CF файла конфигурации 1с.
    """
    def __init__(self, parent, title):
        """
        Конструктор.
        @param parent: Родительский визард, в который вставляется страница.
        @param title: Заголовок страницы.
        """
        
        wx.wizard.PyWizardPage.__init__(self, parent)
        
        self.next = None
        self.prev = None
        
        self.sizer = makeStdPageTitle(self, title)

        self.cf_build_panel=icbuildpanel.icBuildPanel(self)
        self.sizer.Add(self.cf_build_panel, 1, wx.EXPAND|wx.GROW, 5)        
        
    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next
        
    def GetPrev(self):
        return self.prev

    def on_changed(self,event):
        """
        Перед открытием этой страницы.
        """
        wizard=self.GetParent()
        
        import time
        
        default_patch_time_ext=time.strftime('_patch_%Y_%m_%d_%H_%M_%S.cf',time.localtime(time.time()))
        default_cf_filename=wizard.environment['cf_filename'].replace('.cf',default_patch_time_ext)
        self.cf_build_panel.cfFileTxt.SetValue(default_cf_filename)

    def on_changing(self,event):
        """
        Обработчик смены страницы визарда.
        Это обработчик срабатывает после нажатия на кнопку <Next>.
        """
        wizard=self.GetParent()
        
        cf_filename=self.cf_build_panel.cfFileTxt.GetValue()
        cf_filename=os.path.abspath(cf_filename)
        if os.path.exists(cf_filename):
            os.remove(cf_filename)
        wizard.environment['cf_patch_filename']=cf_filename
        #
        self.build_cf_file(wizard.environment['cf_patch_dir'],cf_filename)

    def build_cf_file(self,CFDir_,CFFileName_):
        """
        Построить CF файл конфигурации 1с.
        @param CFDir_: Директория из которой будет происходить сборка.
        @param CFFileName_: Полное имя CF файла конфигурации 1c.
        """
        return patch_cmd.build_cf_file(CFDir_,CFFileName_)
        
class icCFEndPage(wx.wizard.PyWizardPage):
    """
    Страница окончания установки.
    """
    def __init__(self, parent, title, Txt_=None):
        """
        Конструктор.
        @param parent: Родительский визард, в который вставляется страница.
        @param title: Заголовок страницы.
        @param Txt_: Текст.
        """
        
        wx.wizard.PyWizardPage.__init__(self, parent)
        
        self.next = None
        self.prev = None
        
        self.sizer = makeStdPageTitle(self, title)
        
    def SetNext(self, next):
        self.next = next

    def SetPrev(self, prev):
        self.prev = prev

    def GetNext(self):
        return self.next
        
    def GetPrev(self):
        return self.prev
