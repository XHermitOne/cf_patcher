# !/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
Класс корневого элемента конфигурации.
"""

__version__ = (0,0,0,1)

import os,os.path

import iccfobject
import iccfresource
import iccfconfiguration

from utils import progress_dlg

class icCFRoot(iccfobject.icCFObject):
    """
    Класс корневого элемента конфигурации.
    """
    def __init__(self,*args,**kwargs):
        """
        Конструктор.
        """
        iccfobject.icCFObject.__init__(self,*args,**kwargs)

        self.img_filename=os.path.dirname(os.path.dirname(__file__))+'/img/1c.png'
        
    def build(self):
        """
        Инициализировать объект и создать все его дочерние объекты.
        """
        try:
            progress_dlg.openProgressDlg(u'Построение дерева метаобъектов',
                u'Корневой объект',0,100)

            cf_root_filename=os.path.abspath(self.cf_dir)+'/root'
            #print 'ROOT PATH:::',cf_root_filename
            cf_root_res=iccfresource.icCFResource(cf_root_filename)
            cf_root_res.loadData()   
        
            #Построение конфигурации
            uid_cfg=cf_root_res.data[1]
            #print 'CONFIGURATION UID:::',uid_cfg
        
            cfg=iccfconfiguration.icCFConfiguration(self,uid_cfg)
            cfg.build()
        
            self.children=[cfg]

            progress_dlg.closeProgressDlg()
        except:
            progress_dlg.closeProgressDlg()
            raise
        
    def getConfiguration(self):
        """
        Объект конфигурации.
        """
        if self.children:
            return self.children[0]
        return None

