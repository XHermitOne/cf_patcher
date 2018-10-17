#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Функции изменения конфигурации.
"""
__version__ = (0,0,0,1)

import re

#Глобальный список метаобъектов
METAOBJECTS=None

#Корневой элемент дерева метаобъектов
ROOT_METAOBJECT=None

#def addCFModule(PrgText_,MetaObject_=None):
#    """
#    Добавить текст программы в модуль.
#    @param PrgText_: Текст процедуры 1с.
#    @param MetaObject_: Указание метаобъекта конфигурации 1с,
#    в модуле которого надо сделать изменения.
#    """
#    if MetaObject_:
#        return MetaObject_.addInModule(PrgText_)

#def delCFModule(PrgText_,MetaObject_=None):
#    """
#    Удалить текст из модуля.
#    @param PrgText_: Текст процедуры 1с.
#    @param MetaObject_: Указание метаобъекта конфигурации 1с,
#    в модуле которого надо сделать изменения.
#    """
#    if MetaObject_:
#        return MetaObject_.delInModule(PrgText_)
    
#def replaceCFModule(SrcPrgText_,DstPrgText_,MetaObject_=None):
#    """
#    Заменить текст программы в модуле.
#    @param SrcPrgText_: Изменяемый текст процедуры 1с.
#    @param DstPrgText_: Текст, на который будем менять.
#    @param MetaObject_: Указание метаобъекта конфигурации 1с,
#    в модуле которого надо сделать изменения.
#    """
#    if MetaObject_:
#        return MetaObject_.replaceInModule(SrcPrgText_,DstPrgText_)

def _filter_metaobjects_by_name(MetaObjects_=None,NameFilter_=None):
    """
    Отфильтровать метаобъекты по фильтру имени.
    Фильтр задается в виде регулярного выражения.
    @param MetaObjects_: Список метаобъектов конфигурации 1с,
    в которых надо сделать изменения.
    @param NameFilter_: Дополнительный фильтр по имени метаобъекта.
    Если None, то фильтрацию делать не надо.
    @return: Возвращает отфильтрованный список.
    """
    if NameFilter_:
        if NameFilter_[0]=='<' and NameFilter_[-1]=='>':
            NameFilter_=NameFilter_[1:-1]
        if MetaObjects_:
            return [metaobject for metaobject in MetaObjects_ if bool(re.search(NameFilter_,metaobject.name))]
    return MetaObjects_

from utils import progress_dlg

def _progress_metaobjects(MetaObjects_=None,Msg_=u'',MethodName_=None,**kwargs):
    """
    Выполнить обработку списка метаобъектов с прогресс диалогом.
    @param MetaObjects_: Список метаобъектов конфигурации 1с,
    в которых надо сделать изменения.
    @param Msg_: Сообщение функции.
    @param MethodName_: Имя Функции-метода обработки. И дальше идут ее параметры.
    @return: True/False.    
    """
    try:
        metaobjects=MetaObjects_
        if metaobjects is None:
            metaobjects=[]
        metaobjects_count=len(metaobjects)

        progress_dlg.openProgressDlg(u'Обработка метаобъектов',u'',0,metaobjects_count)

        for i,metaobject in enumerate(metaobjects):
            metaobject_name=metaobject.getStructUnicodeName()
            msg=u'Метаобъект: %s \nДействие: %s'%(metaobject_name,Msg_)
            progress_dlg.updateProgressDlg(i,msg)

            #Т.к. метаобъект сам знает как его могут обрабатывать
            #то соответственно и вызываем его метод
            if MethodName_ and hasattr(metaobject,MethodName_):
                #print 'DBG:::',metaobject,kwargs,MethodName_
                getattr(metaobject,MethodName_)(**kwargs)

        progress_dlg.closeProgressDlg()
        return True
    except:
        progress_dlg.closeProgressDlg()
        raise

#--- Пользовательские функции скрипта ---
def addCF(AttrName_,Value_,MetaObjects_=None,NameFilter_=None,**kwargs):
    """
    Добавить значение в конфигурацию.
    @param AttrName_: Наименование атрибута.
    @param Value_: Добавляемое значение атрибута.
    @param MetaObjects_: Список метаобъектов конфигурации 1с,
    в которых надо сделать изменения.
    @param NameFilter_: Дополнительный фильтр по имени метаобъекта.
    """
    if MetaObjects_ is None:
        MetaObjects_=METAOBJECTS

    if not MetaObjects_:
        MetaObjects_=ROOT_METAOBJECT.getAllChildrenByFilter(NameFilter_)
    else:
        MetaObjects_=_filter_metaobjects_by_name(MetaObjects_,NameFilter_)
        
    #print 'ROOT_METAOBJECT:',ROOT_METAOBJECT
    
    attr_name=AttrName_.lower()
    if attr_name==u'модуль':
        #for metaobject in MetaObjects_:
        #    if hasattr(metaobject,'addInModule'):
        #        metaobject.addInModule(Value_,**kwargs)
        _progress_metaobjects(MetaObjects_,u'Добавить в модуль',
            'addInModule',Txt_=Value_,**kwargs)
    elif attr_name==u'модульформы':
        #for metaobject in MetaObjects_:
        #    if hasattr(metaobject,'addInFormModule'):
        #        metaobject.addInFormModule(Value_,**kwargs)
        _progress_metaobjects(MetaObjects_,u'Добавить в модуль формы',
            'addInFormModule',Txt_=Value_,**kwargs)
    elif attr_name==u'реквизитформы':
        #for metaobject in MetaObjects_:
        #    if hasattr(metaobject,'addFormRequisite'):
        #        metaobject.addFormRequisite(Value_,**kwargs)
        _progress_metaobjects(MetaObjects_,u'Добавить реквизит формы',
            'addFormRequisite',Name_=Value_,**kwargs)
    elif attr_name==u'событиеформы':
        #for metaobject in MetaObjects_:
        #    if hasattr(metaobject,'addFormObjEvent'):
        #        metaobject.addFormObjEvent(Name_=kwargs['Name_'],Value_=Value_)
        _progress_metaobjects(MetaObjects_,u'Добавить событие формы',
            'addFormObjEvent',Name_=kwargs['Name_'],Value_=Value_)
    else:
        print(('Not support CF attribute name:',AttrName_))

def delCF(AttrName_,Value_,MetaObjects_=None,NameFilter_=None,**kwargs):
    """
    Удалить значение из конфигурацию.
    @param AttrName_: Наименование атрибута.
    @param Value_: Удаляемое значение атрибута.
    @param MetaObjects_: Список метаобъектов конфигурации 1с,
    в которых надо сделать изменения.
    @param NameFilter_: Дополнительный фильтр по имени метаобъекта.
    """
    if MetaObjects_ is None:
        MetaObjects_=METAOBJECTS

    if not MetaObjects_:
        MetaObjects_=ROOT_METAOBJECT.getAllChildrenByFilter(NameFilter_)
    else:
        MetaObjects_=_filter_metaobjects_by_name(MetaObjects_,NameFilter_)
    
    attr_name=AttrName_.lower()
    if attr_name==u'модуль':
        #for metaobject in MetaObjects_:
        #    metaobject.delInModule(Value_,**kwargs)
        _progress_metaobjects(MetaObjects_,u'Удалить из модуля',
            'delInModule',Txt_=Value_,**kwargs)
    elif attr_name==u'модульформы':
        pass
    elif attr_name==u'реквизитформы':
        #for metaobject in MetaObjects_:
        #    metaobject.delFormRequisite(Value_,**kwargs)
        _progress_metaobjects(MetaObjects_,u'Удалить реквизит формы',
            'delFormRequisite',Name_=Value_,**kwargs)
    else:
        print(('Not support CF attribute name:',AttrName_))

def replaceCF(AttrName_,SrcValue_,DstValue_,MetaObjects_=None,NameFilter_=None,**kwargs):
    """
    Заменить значение в конфигурации на другое.
    @param AttrName_: Наименование атрибута.
    @param SrcValue_: Заменяемое значение атрибута.
    @param DstValue_: Заменяющее значение атрибута.
    @param MetaObjects_: Список метаобъектов конфигурации 1с,
    в которых надо сделать изменения.
    @param NameFilter_: Дополнительный фильтр по имени метаобъекта.
    """
    pass

def updateCF(AttrName_,Value_,MetaObjects_=None,NameFilter_=None,**kwargs):
    """
    Заменить значение в конфигурации на другое.
    @param AttrName_: Наименование атрибута.
    @param Value_: Заменяющее значение атрибута.
    @param MetaObjects_: Список метаобъектов конфигурации 1с,
    в которых надо сделать изменения.
    @param NameFilter_: Дополнительный фильтр по имени метаобъекта.
    """
    if MetaObjects_ is None:
        MetaObjects_=METAOBJECTS

    if not MetaObjects_:
        MetaObjects_=ROOT_METAOBJECT.getAllChildrenByFilter(NameFilter_)
    else:
        MetaObjects_=_filter_metaobjects_by_name(MetaObjects_,NameFilter_)
    
    attr_name=AttrName_.lower()
    if attr_name==u'модуль':
        pass
    elif attr_name==u'модульформы':
        #for metaobject in MetaObjects_:
        #    if hasattr(metaobject,'updateInFormModule'):
        #        metaobject.updateInFormModule(Value_,**kwargs)
        _progress_metaobjects(MetaObjects_,u'Обновить в модуле формы',
            'updateInFormModule',Txt_=Value_,**kwargs)
    elif attr_name==u'реквизитформы':
        pass
    elif attr_name==u'событиеформы':
        pass
    else:
        print(('Not support CF attribute name:',AttrName_))

def test_function(MetaObjects_=None):
    """
    Тестовая функция.
    """
    if MetaObjects_ is None:
        MetaObjects_=METAOBJECTS
        
    print(('metaobjects:::',METAOBJECTS,MetaObjects_))