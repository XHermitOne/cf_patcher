#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс анализитора конфигураци.
"""
__version__ = (0,0,0,1)

import iccfdirmanager
from cf_obj import iccfobject

class icCFAnalyzer:
    """
    Класс анализитора конфигураци.
    """
    def __init__(self,CFDir_=None):
        """
        Конструктор.
        @param CFDir_: Имя папки конфигурации 1с.
        """
        self.cf_dir_manager=iccfdirmanager.icCFDirManager(CFDir_)

        #Список объектов конфигурации
        self.cf_list=None
        
    def createCFList(self,CFDir_=None):
        """
        Создать список объектов конфигурации 1с.
        """
        if CFDir_:
            self.cf_dir_manager.buildMetaObjects(CFDir_)
        else:
            self.cf_dir_manager.buildMetaObjects()
        
        self.cf_list=self._createCFList(self.cf_dir_manager.cf_root)
        return self.cf_list
        
    def _createCFList(self,Root_):
        """
        Создать список объектов конфигурации 1с.
        """
        result=[]
        
        if Root_:
            for child in Root_.children:
                obj={}
                obj['name']=unicode(child.name,'utf-8')
                obj['img']=child.getImage()
                obj['img_exp']=child.getImageExpand()
                obj['checkable']=True
                obj['check']=True
                #obj['__type__']=1
                obj['__record__']=(child.uid,child.name)
                obj['children']=self._createCFList(child)
            
                result.append(obj)
                
        return result
    
    def getMetaobjects(self,CFList_):
        """
        Получить список метаобъектов по списку описаний объектов конфигурации 1с.
        """
        metaobjects=[]
        for cf_child in CFList_:
            checked=cf_child.get('check',False)
            uid=cf_child['__record__'][0]
            #print 'DBG>>>',cf_child['name'],checked,uid
            if checked:
                if uid<>iccfobject.NONE_UID:
                    metaobject=self.cf_dir_manager.cf_root.findByUID(uid)
                    if metaobject:
                        metaobjects.append(metaobject)
                
            if 'children' in cf_child and cf_child['children']:
                metaobjects+=self.getMetaobjects(cf_child['children'])
        return metaobjects

    def getRootMetaobject(self):
        """
        Корневой метаобъект.
        """
        return self.cf_dir_manager.cf_root
    
