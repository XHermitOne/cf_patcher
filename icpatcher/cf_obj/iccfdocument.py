# !/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
Класс элемента документа конфигурации 1с.
"""
__version__ = (0,0,0,1)

import os,os.path

import iccfresource
import iccfobject
import iccfdocform

from utils import util

class icCFDocRequisite(iccfobject.icCFObject):
    """
    Класс элемента реквизита документа.
    """
    def __init__(self,*args,**kwargs):
        """
        Конструктор.
        ВНИМАНИЕ! Если UID не определн (NONE_UID), то должен 
        UID-любой (ANY_UID), чтобы отличать объекты от папок.
        """
        iccfobject.icCFObject.__init__(self,UID_=iccfobject.ANY_UID,*args,**kwargs)
        
        self.img_filename=os.path.dirname(os.path.dirname(__file__))+'/img/ui-button.png'
        

    def init(self,Res_=None):
        """
        Инициализировать внутренние атрибуты по ресурсу.
        """
        if Res_ is None:
            return

        self.name=Res_[0][1][1][1][2]

        #idx=util.ValueIndexPath(Res_,'Реквизит1')
        #print 'name>>>',idx
        

class icCFDocTab(iccfobject.icCFObject):
    """
    Класс элемента табличной части документа.
    """
    def __init__(self,*args,**kwargs):
        """
        Конструктор.
        ВНИМАНИЕ! Если UID не определн (NONE_UID), то должен 
        UID-любой (ANY_UID), чтобы отличать объекты от папок.
        """
        iccfobject.icCFObject.__init__(self,UID_=iccfobject.ANY_UID,*args,**kwargs)

        self.requisites=[]
        
        self.img_filename=os.path.dirname(os.path.dirname(__file__))+'/img/table.png'
        
        
    def init(self,Res_=None):
        """
        Инициализировать внутренние атрибуты по ресурсу.
        """
        if Res_ is None:
            return

        #idx=util.ValueIndexPath(Res_,'ТабличнаяЧасть1')
        #print 'tab name>>>',idx
        self.name=Res_[0][1][5][1][2]  
        #print 'tab name:',self.name 
        
        #print '@@@@@@@@@@@@@@@@@@@@',Res_[2]
        self.requisites=[]
        for res in Res_[2][2:]:
            requisite=icCFDocTabRequisite(self)
            requisite.init(res)
            self.requisites.append(requisite)
            
        self.children=self.requisites        

class icCFDocTabRequisite(iccfobject.icCFObject):
    """
    Класс элемента реквизита табличной части документа.
    """
    def __init__(self,*args,**kwargs):
        """
        Конструктор.
        ВНИМАНИЕ! Если UID не определн (NONE_UID), то должен 
        UID-любой (ANY_UID), чтобы отличать объекты от папок.
        """
        iccfobject.icCFObject.__init__(self,UID_=iccfobject.ANY_UID,*args,**kwargs)
        
        self.img_filename=os.path.dirname(os.path.dirname(__file__))+'/img/ui-button.png'

    def init(self,Res_=None):
        """
        Инициализировать внутренние атрибуты по ресурсу.
        """
        if Res_ is None:
            return

        #idx=util.ValueIndexPath(Res_,'Реквизит11')
        #print 'tab requisite name>>>',idx
        
        self.name=Res_[0][1][1][1][2]
        #print 'tab requisite name:',self.name
        
class icCFDocument(iccfobject.icCFObject):
    """
    Класс элемента документа конфигурации 1с.
    """
    def __init__(self,*args,**kwargs):
        """
        Конструктор.
        """
        iccfobject.icCFObject.__init__(self,*args,**kwargs)

        self.description=''
        
        #Список реквизитов документа
        self.requisites=[]
        #Список табличных частей документа
        self.tabs=[]
        #Список форм документа
        self.forms=[]
        
        self.img_filename=os.path.dirname(os.path.dirname(__file__))+'/img/document-text.png'
        
        
    def build(self):
        """
        Инициализировать объект и создать все его дочерние объекты.
        """
        cf_doc_filename=os.path.abspath(self.cf_dir)+'/'+self.uid
        #print 'DOCUMENT PATH:::',cf_doc_filename
        cf_doc_res=iccfresource.icCFResource(cf_doc_filename)
        cf_doc_res.loadData()
        
        #print 'DOCUMENT RESOURCE:::'
        #print util.StructToTxt(cf_doc_res.data)
        
#        idx=util.ValueIndexPath(cf_doc_res.data,'ДокументБляБляБля')
#        print 'name>>>',idx
        
#        idx=util.ValueIndexPath(cf_doc_res.data,'Документ бля бля бля')
#        print 'description>>>',idx
        
#        idx=util.ValueIndexPath(cf_doc_res.data,'ТабличнаяЧасть1')
#        print 'tabs>>>' #,idx
#        print util.StructToTxt(cf_doc_res.data[3])
        
#        idx=util.ValueIndexPath(cf_doc_res.data,'Реквизит1')
#        print 'requisites>>>',idx
#        print util.StructToTxt(cf_doc_res.data[5])
        
        self.name=cf_doc_res.data[1][9][1][2]
        self.description=''
        if len(cf_doc_res.data[1][9][1][3])>1:
            self.description=cf_doc_res.data[1][9][1][3][2]
        
        #После определения имени метаобъекта можно изменить прогресс бар
        iccfobject.icCFObject.build(self)

        self.requisites=[]
        for res in cf_doc_res.data[5][2:]:
            requisite=icCFDocRequisite(self)
            requisite.init(res)
            self.requisites.append(requisite)
        
        self.tabs=[]
        for res in cf_doc_res.data[3][2:]:
            tab=icCFDocTab(self)
            tab.init(res)
            self.tabs.append(tab)

        #idx=util.ValueIndexPath(cf_doc_res.data,'037fc040-bdea-42ad-956c-f226f96ed61c')
        #print 'forms>>>',len(cf_doc_res.data),cf_doc_res.data[-1]
        #print util.StructToTxt(cf_doc_res.data[5])

        frm_uid_lst=cf_doc_res.data[7][2:]
        self.forms=[iccfdocform.icCFDocForm(self,uid) for uid in frm_uid_lst]
        for frm in self.forms:
            frm.build()
            
        self.children=[iccfobject.icCFFolder(Parent_=self,
            Name_='Реквизиты',Children_=self.requisites,
            ImgFileName_=os.path.dirname(os.path.dirname(__file__))+'/img/ui-buttons.png'),
            iccfobject.icCFFolder(Parent_=self,
            Name_='Табличные части',Children_=self.tabs,
            ImgFileName_=os.path.dirname(os.path.dirname(__file__))+'/img/tables-stacks.png'),
            iccfobject.icCFFolder(Parent_=self,
            Name_='Формы',Children_=self.forms,
            ImgFileName_=os.path.dirname(os.path.dirname(__file__))+'/img/applications.png')]

    #--- Функции изменения метаобъекта в конфигурации ---
    def createModule(self,Txt_=None):
        """
        Создать модуль.
        @param Txt_: Добавляемый текст.
        @return: True - добавление прошло успешно, False - добавления не произошло.
        """
        module_dir=os.path.normpath(self.getCFDir()+'/'+self.uid+'.0')
        module_info=os.path.normpath(module_dir+'/info')
        module_txt=os.path.normpath(module_dir+'/text')
        #print 'DBG@@@@@@@',os.path.exists(module_dir),module_dir
        if not os.path.isdir(module_dir):
            #print 'CREATE DIR:',module_dir
            os.makedirs(module_dir)
        if not os.path.exists(module_info):
            file.createTxtFile(module_info,u'{3,1,0,"",0}')
        if not os.path.exists(module_txt):
            file.createTxtFile(module_txt,u' ')
        return True
        
    def addInModule(self,Txt_):
        """
        Добавить в модуль объекта текст.
        @param Txt_: Добавляемый текст.
        @return: True - добавление прошло успешно, False - добавления не произошло.
        """
        Txt_=util.encodeText(Txt_)
        
        module_filename=os.path.normpath(self.getCFDir()+'/'+self.uid+'.0/text')
        if not os.path.exists(module_filename):
            #self.createModule()
            return
        
        f=None
        try:
            f=open(module_filename,'r')
            txt=f.read()
            f.close()
            f=None
            if Txt_ not in txt:
                try:
                    f=open(module_filename,'a')
                    f.write(Txt_)
                    f.close()
                except:
                    if f:
                        f.close()
                        f=None
                    raise
            return True
        except:
            if f:
                f.close()
                f=None
            raise
        return False

    def delInModule(self,Txt_):
        """
        Удалить из модуля объекта текст.
        @param Txt_: Удаляемый текст.
        @return: True - удаление прошло успешно, False - удаления не произошло.
        """
        Txt_=util.encodeText(Txt_)
        
        module_filename=os.path.normpath(self.getCFDir()+'/'+self.uid+'.0/text')
        
        f=None
        try:
            f=open(module_filename,'w')
            txt=f.read()
            txt=txt.replace(Txt_,'')
            f.write(txt)
            f.close()
            return True
        except:
            if f:
                f.close()
                f=None
            raise
        return False
        
    def replaceInModule(self,SrcTxt_,DstTxt_):
        """
        Заменить текст в модуле объекта.
        @param SrcTxt_: Заменяемый текст.
        @param DstTxt_: Заменяющий текст.
        @return: True - замена прошла успешно, False - замена не произошла.
        """
        if self.delInModule(SrcTxt_):
            return self.addInModule(DtsTxt_)
        return False
        