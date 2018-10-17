# !/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
Класс элемента конфигурации.
"""
__version__ = (0,0,0,1)

import os,os.path

import iccfresource
import iccfobject
import iccfdocument

from utils import util
from utils import log

import config

class icCFConfiguration(iccfobject.icCFObject):
    """
    Класс элемента конфигурации.
    """
    def __init__(self,*args,**kwargs):
        """
        Конструктор.
        """
        iccfobject.icCFObject.__init__(self,*args,**kwargs)
        
        #Список документов
        self.documents=[]
        
        self.img_filename=os.path.dirname(os.path.dirname(__file__))+'/img/brightness.png'
        #print 'CONF IMG FILE:',self.img_filename

    def build(self):
        """
        Инициализировать объект и создать все его дочерние объекты.
        """
        cf_cfg_filename=os.path.abspath(self.cf_dir)+'/'+self.uid
        #print 'CONFIGURATION PATH:::',cf_cfg_filename
        cf_cfg_res=iccfresource.icCFResource(cf_cfg_filename)
        cf_cfg_res.loadData()
        
        
        #print 'CONFIGURATION RESOURCE:::'
        #print util.StructToTxt(cf_cfg_res.data)
                
        self.name=cf_cfg_res.data[3][1][1][1][1][2]
        #После определения имени метаобъекта можно изменить прогресс бар
        iccfobject.icCFObject.build(self)

        if config.DEBUG_MODE:
            log.log_to_file('CONFIGURATION RESOURCE: '+self.name)
        
        idx=util.ValueIndexPath(cf_cfg_res.data,'4938909f-92f5-4cd8-992f-6c53996d1af9')
        #print '1>>>',idx
        
        #print 'SPRAV:::'
        #print util.StructToTxt(cf_cfg_res.data[3][1][1][27])
        #print util.StructToTxt(cf_cfg_res.data[3])
        
        #print 'DOCS:::'
        #print util.StructToTxt(cf_cfg_res.data[4][1][1][4])
        #print util.StructToTxt(cf_cfg_res.data[4])
        doc_uid_lst=cf_cfg_res.data[4][1][1][4][2:]
        #print util.StructToTxt(doc_uid_lst)

        if config.DEBUG_MODE:
            log.log_to_file('DOC UIDs: '+str(doc_uid_lst))
        
        #doc=iccfdocument.icCFDocument(self,doc_uid_lst[0])
        #doc.build()
        
        self.documents=[iccfdocument.icCFDocument(self,uid) for uid in doc_uid_lst]
        for doc in self.documents:
            doc.build()
            
        self.children=[iccfobject.icCFFolder(Parent_=self,
            Name_='Документы',Children_=self.documents,
            ImgFileName_=os.path.dirname(os.path.dirname(__file__))+'/img/documents-text.png')]
        
