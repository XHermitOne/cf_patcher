# !/usr/bin/env python
#  -*- coding: utf-8 -*-
""" 
Класс панели списка скриптов изменения конфигурации 1с.
"""
__version__ = (0,0,0,1)

#--- Imports ---
import os,os.path
import wx
import sys

#import icScriptListPanelProto
import icWizardPanelProto

from utils import dlg
from utils import util

class icScriptListPanel(icWizardPanelProto.icScriptChoicePanelPrototype):
    """
    Класс панели списка скриптов изменения конфигурации 1с.
    """
    def __init__(self,*args,**kwargs):
        """
        Конструтор.
        """
        icWizardPanelProto.icScriptChoicePanelPrototype.__init__(self,*args,**kwargs)
        
        #Текущий выбранный элемент списка
        self.CurrentItemIdx=-1
        
        #Добавить колонки
        self.scriptListCtrl.InsertColumn(0,u'Имя файла')
        self.scriptListCtrl.SetColumnWidth(0,100)        
        self.scriptListCtrl.InsertColumn(1,u'Описание')
        self.scriptListCtrl.SetColumnWidth(1,200) #wx.LIST_AUTOSIZE)        
        self.scriptListCtrl.InsertColumn(2,u'Полный путь')
        self.scriptListCtrl.SetColumnWidth(2,300) # wx.LIST_AUTOSIZE)        

    def addScriptFileInList(self,ScriptFileName_):
        """
        Добавить файл скрипта в список скриптов.
        """
        if ScriptFileName_:
            #Файл выбран
            print(('SELECT SCRIPT FILE:::',ScriptFileName_))
            #idx=self.scriptListCtrl.GetItemCount()
            idx=self.scriptListCtrl.InsertStringItem(sys.maxint,
                os.path.basename(ScriptFileName_))
            description=util.getModuleDoc(ScriptFileName_)
            if description is None:
                description=u''
            else:
                description.strip()
            self.scriptListCtrl.SetStringItem(idx,1,description)
            self.scriptListCtrl.SetStringItem(idx,2,ScriptFileName_)
            #self.scriptListCtrl.Update()
            #self.scriptListCtrl.Refresh()

    def delScriptFileInList(self,Idx_=None):
        """
        Удалить файл скрипта из списка скриптов.
        """
        if Idx_ is None:
            Idx_=self.CurrentItemIdx
            
        if Idx_>=0 and Idx_<self.scriptListCtrl.GetItemCount():
            self.scriptListCtrl.DeleteItem(Idx_)            
        
    def editScriptFileInList(self,Idx_=None):
        """
        Редактировать файл скрипта из списка скриптов.
        """
        if Idx_ is None:
            Idx_=self.CurrentItemIdx
            
        if Idx_>=0 and Idx_<self.scriptListCtrl.GetItemCount():
            script_file_name=self.scriptListCtrl.GetItem(Idx_,2).GetText()
            if wx.Platform=='__WXGTK__':
                cmd='gedit %s'%script_file_name
                print(('RUN CMD:::',cmd))
                os.system(cmd)
            elif wx.Platform=='__WXMSW__':
                cmd='notebook.exe %s'%script_file_name
                print(('RUN CMD:::',cmd))
                os.system(cmd)                

    def moveScriptFileInList(self,Idx_=None,Step_=1):
        """
        Передвинуть файл скрипта в списке скриптов.
        """
        if Idx_ is None:
            Idx_=self.CurrentItemIdx
            if Idx_<0:
                return
        
        if Idx_>=0 and Idx_<self.scriptListCtrl.GetItemCount():
            #Вычислить новое положение строки
            new_idx=min(self.scriptListCtrl.GetItemCount(),max(0,Idx_+Step_+int(bool(Step_>0))))
            
            #Количество колонок
            col_count=self.scriptListCtrl.GetColumnCount()
            #Список записи
            rec=[self.scriptListCtrl.GetItem(Idx_,col).GetText() for col in range(col_count)]
            #Встевить 
            new_idx=self.scriptListCtrl.InsertStringItem(new_idx,rec[0])
            for i_col in range(1,len(rec[1:])):
                col_str=rec[i_col]
                self.scriptListCtrl.SetStringItem(new_idx,i_col,col_str)
            
            del_idx=Idx_+int(bool(Step_<0))
            
            #print 'DBG!!!',new_idx,del_idx
            #Выделить строку
            self.selectScriptFileInList(del_idx,False)
            self.focusScriptFileInList(new_idx)
            self.selectScriptFileInList(new_idx)
            
            #Удалить старую запись
            self.scriptListCtrl.DeleteItem(del_idx)

    def focusScriptFileInList(self,Idx_):
        """ 
        Переместить фокус/выделение строки/записи.
        @param Idx_: Номер записи.
        """
        Idx_=min(self.scriptListCtrl.GetItemCount()-1,max(0,Idx_))
        self.CurrentItemIdx=Idx_
        self.scriptListCtrl.Focus(Idx_)
        
    def selectScriptFileInList(self,Idx_,SelectOn_=True):
        """ 
        Выделить строку/запись с индексом.
        @param Idx_: Номер записи.
        @param SelectOn_: Вкл/Выкл выделение.
        """
        Idx_=min(self.scriptListCtrl.GetItemCount()-1,max(0,Idx_))
        return self.scriptListCtrl.Select(Idx_,int(SelectOn_))
        
    def getScriptFiles(self):
        """
        Список выбранных скриптов.
        """
        return [self.scriptListCtrl.GetItem(i,2).GetText() for i in range(self.scriptListCtrl.GetItemCount())]
    
    #--- Обработчики событий ---
    def onAddToolMouseClick(self,event):
        """
        Обработчик нажатия кнопки мыши на инструмент добавления скрипта.
        """
        default_script_dir=os.path.dirname(os.path.dirname(__file__))+'/scripts' if __file__ else os.getcwd()
        script_file_name=dlg.getFileNameDlg(self,u'Выберите файл скрипта',
            u'Python scripts(*.py)|*.py',default_script_dir)
        #wx.CallAfter(self.addScriptFileInList,script_file_name)
        self.addScriptFileInList(script_file_name)
        event.Skip()
    
    def onDelToolMouseClick(self,event):
        """
        Обработчик нажатия кнопки мыши на инструмент удаления скрипта.
        """
        self.delScriptFileInList()
        event.Skip()
    
    def onEditToolMouseClick(self,event):
        """
        Обработчик нажатия кнопки мыши на инструмент редактирования скрипта.
        """
        self.editScriptFileInList()
        event.Skip()
    
    def onMoveUpToolMouseClick(self,event):
        """
        Обработчик нажатия кнопки мыши на инструмент перемещения выше скрипта.
        """
        self.moveScriptFileInList(Step_=-1)
        event.Skip()
    
    def onMoveDownToolMouseClick(self,event):
        """
        Обработчик нажатия кнопки мыши на инструмент перемещения ниже скрипта.
        """
        self.moveScriptFileInList(Step_=1)
        event.Skip()

    def onListItemSelected(self,event):
        """
        Обработчик выбора элемента списка.
        """
        self.CurrentItemIdx=event.m_itemIndex
        event.Skip()
