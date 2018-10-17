#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс работы с папкой конфигурации 1с, разобранной V8Unpack v2.0.
"""
import os,os.path

#from cf_obj import iccfresource
from cf_obj import iccfroot

class icCFDirManager:
    """
    Класс работы с папкой конфигурации 1с, разобранной V8Unpack v2.0.
    """
    
    def __init__(self,CFDir_=None):
        """
        Конструктор.
        @param CFDir_: Папка конфигурации 1с.
        """
        self.cf_dir=CFDir_
        
        #Корневой элемент дерева объектов конфигурации
        self.cf_root=None
        
    def buildMetaObjects(self,CFDir_=None):
        """
        Построить дерево объектов конфигурации.
        @param CFDir_: Папка конфигурации 1с.
        """
        if CFDir_:
            self.cf_dir=CFDir_
        
        #Очистить предыдущее дерево объектов
        self.cf_root=None
        self.cf_root=iccfroot.icCFRoot(None,None,self.cf_dir)
        self.cf_root.build()
        
def test():
    """
    """
    cur_dir=os.getcwd()
    #cf_dir=os.path.dirname(cur_dir)+'/testcf'
    cf_dir=os.path.dirname(cur_dir)+'/tst_doc'
    print(('CF DIR:::',cf_dir))
    cf=icCFDirManager(cf_dir)
    cf.buildObjects()
    
if __name__=='__main__':
    test()