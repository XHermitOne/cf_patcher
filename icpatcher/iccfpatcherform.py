# !/usr/bin/env python
#  -*- coding: utf-8 -*-
""" 
Класс формы CF конфигурации 1с.
"""
__version__ = (0,0,0,1)

#--- Imports ---
import os,os.path
import wx
import sys

import icCFPatcherFormProto

from utils import dlg
from utils import util
from utils import log

import patch_cmd

class icCFPatcherForm(icCFPatcherFormProto.icCFPatcherFramePrototype):
    """
    Класс формы CF конфигурации 1с.
    """
    def __init__(self,*args,**kwargs):
        """
        Конструктор.
        """
        icCFPatcherFormProto.icCFPatcherFramePrototype.__init__(self,*args,**kwargs)


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

    def genResultCFFileName(self):
        """
        Генерация имени файла результирующего CF файла.
        """
        import time
        
        default_patch_time_ext=time.strftime('_patch_%Y_%m_%d_%H_%M_%S.cf',time.localtime(time.time()))
        cf_filename=self.cfFileTxt.GetValue()
        default_cf_filename=cf_filename.replace('.cf',default_patch_time_ext)
        self.resultFileTxt.SetValue(default_cf_filename)

    #--- Обработчики событий ---
    def CFFileButtonOnButtonClick( self, event ):
        """
        Обработчик кнопки выбора CF файла конфигурации 1с.
        """
        default_dir=os.getcwd()
        cf_file_name=dlg.getFileNameDlg(self,u'Выберите файл конфигурации 1с',
            u'Файл конфигурации 1с(*.cf)|*.cf',default_dir)
        if cf_file_name:
            self.cfFileTxt.SetValue(cf_file_name)
            #default_dir=os.path.dirname(cf_file_name)+'/'+os.path.basename(cf_file_name).replace('.','_').replace(' ','_')
            self.genResultCFFileName()
        event.Skip()

    def addToolOnToolClicked( self, event ):
        """
        Обработчик нажатия кнопки мыши на инструмент добавления скрипта.
        """
        default_script_dir=os.path.dirname(os.path.dirname(__file__))+'/scripts' if __file__ else os.getcwd()
        script_file_name=dlg.getFileNameDlg(self,u'Выберите файл скрипта',
            u'Python scripts(*.py)|*.py',default_script_dir)
        #wx.CallAfter(self.addScriptFileInList,script_file_name)
        self.addScriptFileInList(script_file_name)
        event.Skip()

    def delToolOnToolClicked( self, event ):
        """
        Обработчик нажатия кнопки мыши на инструмент удаления скрипта.
        """
        self.delScriptFileInList()
        event.Skip()

    def editToolOnToolClicked( self, event ):
        """
        Обработчик нажатия кнопки мыши на инструмент редактирования скрипта.
        """
        self.editScriptFileInList()
        event.Skip()

    def moveUpToolOnToolClicked( self, event ):
        """
        Обработчик нажатия кнопки мыши на инструмент перемещения выше скрипта.
        """
        self.moveScriptFileInList(Step_=-1)
        event.Skip()

    def moveDownToolOnToolClicked( self, event ):
        """
        Обработчик нажатия кнопки мыши на инструмент перемещения ниже скрипта.
        """
        self.moveScriptFileInList(Step_=1)
        event.Skip()

    def scriptListCtrlOnListItemSelected( self, event ):
        """
        Обработчик выбора элемента списка.
        """
        self.CurrentItemIdx=event.m_itemIndex
        event.Skip()
        
    def ResultFileButtonOnButtonClick( self, event ):
        """
        Обработчик кнопки выбора результирующего CF файла конфигурации 1с.
        """
        default_dir=os.getcwd()
        cf_file_name=dlg.getFileNameDlg(self,u'Выберите результирующий файл конфигурации 1с',
            u'Файл конфигурации 1с(*.cf)|*.cf',default_dir)
        if cf_file_name:
            self.resultFileTxt.SetValue(cf_file_name)
            default_dir=os.path.dirname(cf_file_name)+'/'+os.path.basename(cf_file_name).replace('.','_').replace(' ','_')
        event.Skip()

    def runButtonOnButtonClick( self, event ):
        """
        Запуск патчера на исполнение.
        """
        import time
        
        cf_filename=self.cfFileTxt.GetValue()
        result_cf_filename=self.resultFileTxt.GetValue()
        script_files=self.getScriptFiles()
        
        time_start=time.time()
        print('CF Patcher Run')
        log.log_to_file('CF Patcher Run')
        print(('CF file name:',cf_filename))
        log.log_to_file('CF file name: '+cf_filename)
        for script_file in script_files:
            print(('Script:',script_file))
            log.log_to_file('Script: '+script_file)
        print(('Result CF file name:',result_cf_filename))
        log.log_to_file('Result CF file name: '+result_cf_filename)
        
        result=patch_cmd.do_patch(cf_filename,script_files,result_cf_filename)
        print(('CF Patcher result:',result))
        log.log_to_file('CF Patcher result: '+str(result))
        work_time=time.time()-time_start
        print(('Time:',work_time))
        log.log_to_file('Time: '+str(work_time))
        
        event.Skip()

        self.Close()


def run():
    app=wx.PySimpleApp()
    form=icCFPatcherForm(None)
    form.Show(True)
    app.MainLoop()
    
def test():
    return run()
    
if __name__=='__main__':
    test()