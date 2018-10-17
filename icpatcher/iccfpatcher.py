# !/usr/bin/env python
#  -*- coding: utf-8 -*-
""" 
Класс патчера конфигурации 1с.
"""

#--- Imports ---
import os,os.path

from iccfscriptfunc import *
import iccfscriptfunc

from utils import log

#--- Classes ---
class icCFPatcher:
    """
    Класс патчера конфигурации 1с.
    """
    def __init__(self,CFDir_=None,ObjectList_=None,ScriptList_=None,Root_=None):
        """
        Конструктор.
        @param CFDir_: Имя папки конфигурации 1с.
        @param ObjectList_: Список изменяемых метаобъектов.
        @param ScriptList_: Список файлов скриптов изменений.
        @param Root_: Корневой метаобъект.
        """
        self.cf_dir=CFDir_
        
        #Метаобъекты
        self.metaobjects=ObjectList_
        
        #Скрипты изменений
        self.scripts=ScriptList_

        #Корневой метаобъект
        self.root=Root_
        
    def patch(self,CFDir_=None,ObjectList_=None,ScriptList_=None,Root_=None):
        """
        Пропатчить.
        @param CFDir_: Имя папки конфигурации 1с.
        @param ObjectList_: Список изменяемых метаобъектов.
        @param ScriptList_: Список файлов скриптов изменений.
        @param Root_: Корневой метаобъект.
        """
        if CFDir_ is not None:
            self.cf_dir=os.path.abspath(CFDir_)
        if ObjectList_ is not None:
            self.metaobjects=ObjectList_
        if ScriptList_ is not None:
            self.scripts=ScriptList_
        if Root_ is not None:
            self.root=Root_
            
        iccfscriptfunc.METAOBJECTS=self.metaobjects
        iccfscriptfunc.ROOT_METAOBJECT=self.root
        
        for script_file in self.scripts:
            if os.path.exists(script_file):
                try:
                    execfile(script_file,globals(),locals())
                    #execfile(script_file)
                except:
                    log.log_to_file('ERROR EXEC SCRIPT FILE: '+str(script_file))
                    #print 'LOCALS:',locals()
                    #print 'GLOBALS:',globals()
                    raise
            else:
                log.log_to_file('ERROR SCRIPT FILE:'+str(script_file)+'NOT EXISTS!')
            
def test():
    """
    Тестовая функция.
    """
    if not os.path.dirname(__file__):
        script_dir=os.path.dirname(os.getcwd())+'/scripts/'
    else:
        script_dir=os.path.dirname(os.path.dirname(__file__))+'/scripts/'
        
    test_script_file_name=script_dir+'test_script.py'
    print(('TEST SCRIPT FILE NAME>>>',test_script_file_name))
    
    patcher=icCFPatcher(ObjectList_=[1,2,3],ScriptList_=[test_script_file_name])
    patcher.patch()
    
if __name__=='__main__':
    test()