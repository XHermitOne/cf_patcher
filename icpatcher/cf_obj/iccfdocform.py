# !/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
Класс элемента формы документа конфигурации 1с.
"""
__version__ = (0,0,0,1)

import os,os.path
import copy

import iccfresource
import iccfobject

from utils import util

import types1c

#Шаблоны
CTRL_FORM_REQUISITE_TEMPLATE=[9,[2],0,
    'ДеревоКолонки',[1,1,['ru','Дерево колонки']],
    ['Pattern',['#','e603c0f2-92fb-4d47-8f38-a44a381cf235']],
    [0,[0,['B',1],0]],[0,[0,['B',1],0]],
    [0,0],[0,0],0,0,0,0,[0,0],[0,0]]

STD_FORM_REQUISITE_TEMPLATE=[[3],0,1,'Реквизит',
    ['Pattern',['#','e603c0f2-92fb-4d47-8f38-a44a381cf235']]]

CTRL_BEFORE_ADD_START_EVENT_TEMPLATE=[1,'2391e7b8-7235-45d7-ab7e-6ff3dc086396','СписокПередНачаломДобавления']

STD_BEFORE_ADD_START_EVENT_TEMPLATE=[40,'e1692cc2-605b-4535-84dd-28440238746c',
    [3,'ДокументСписокПередНачаломДобавления',
    [1,'ДокументСписокПередНачаломДобавления',
    [1,1,['ru','Документ список перед началом добавления']],
    [1,1,['ru','Документ список перед началом добавления']],
    [1,1,['ru','Документ список перед началом добавления']],
    [3,0,[0],'',-1,-1,1,0],[0,0,0]]]]

class icCFDocForm(iccfobject.icCFObject):
    """
    Класс элемента формы документа конфигурации 1с.
    """
    def __init__(self,*args,**kwargs):
        """
        """
        iccfobject.icCFObject.__init__(self,*args,**kwargs)
        
        self.img_filename=os.path.dirname(os.path.dirname(__file__))+'/img/application-form.png'

    def build(self):
        """
        Инициализировать объект и создать все его дочерние объекты.
        """
        cf_cfg_filename=os.path.abspath(self.cf_dir)+'/'+self.uid
        #print 'DOCUMENT FORM PATH:::',cf_cfg_filename
        cf_cfg_res=iccfresource.icCFResource(cf_cfg_filename)
        cf_cfg_res.loadData()
        
        #print 'DOCUMENT FORM RESOURCE:::'
        #print util.StructToTxt(cf_cfg_res.data)

        self.name=cf_cfg_res.data[1][1][1][2]
        
        self.description=''
        try:
            self.description=cf_cfg_res.data[1][1][1][3][2]
        except IndexError:
            pass
        
        #print 'DOCUMENT FORM:::',self.name,self.description
        
    def getResFileName(self):
        """
        Имя файла ресурса формы.
        """
        res_filename=os.path.normpath(self.getCFDir()+'/'+self.uid+'.0')
        if not os.path.exists(res_filename) or not os.path.isfile(res_filename):
            res_filename=res_filename+'/form'
            if not os.path.exists(res_filename) or not os.path.isfile(res_filename):
                return None            
        return res_filename
        
    def addInFormModule(self,Txt_):
        """
        Добавить в модуль формы текст.
        @param Txt_: Добавляемый текст.
        @return: True - добавление прошло успешно, False - добавления не произошло.
        """
        res_filename=os.path.normpath(self.getCFDir()+'/'+self.uid+'.0')
        if os.path.exists(res_filename) and os.path.isfile(res_filename):
            return self._addInFormModuleCtrl(res_filename,Txt_)
        else:
            mod_filename=os.path.normpath(res_filename+'/module')
            if os.path.exists(mod_filename) and os.path.isfile(mod_filename):
                return self._addInFormModuleStd(mod_filename,Txt_)
        print(('ERROR! Form %s (UID:%s) module file not found!'%(self.name,self.uid)))
        return None
        
    def _addInFormModuleStd(self,ModFileName_,Txt_):
        """
        Добавить в модуль формы текст. Обычная форма.
        @param ModFileName_: Имя файла модуля формы.
        @param Txt_: Добавляемый текст.
        @return: True - добавление прошло успешно, False - добавления не произошло.
        """
        prg_txt=util.encodeText(Txt_,'unicode','utf-8')
        
        f=None
        try:
            f=open(ModFileName_,'r')
            txt=f.read()
            f.close()
            f=None
            if prg_txt not in txt:
                try:
                    f=open(ModFileName_,'a')
                    f.write(prg_txt)
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
        
    def _addInFormModuleCtrl(self,ResFileName_,Txt_):
        """
        Добавить в модуль формы текст. Управляемая форма.
        @param ResFileName_: Имя файла ресурса формы.
        @param Txt_: Добавляемый текст.
        @return: True - добавление прошло успешно, False - добавления не произошло.
        """
        res=iccfresource.icCFResource(ResFileName_)
        res.loadData()

        Txt_=util.encodeText(Txt_,'unicode','utf-8')
        if Txt_ not in res.data[2]:
            prg_txt=res.data[2]+Txt_
        res.data[2]=prg_txt
        
        return res.saveData()
    
    def delInFormModule(self,Txt_):
        """
        Удалить из модуля формы текст.
        @param Txt_: Удаляемый текст.
        @return: True - удаление прошло успешно, False - удаления не произошло.
        """
        pass
    
    def replaceInFormModule(self,SrcTxt_,DstTxt_):
        """
        Заменить текст в модуле формы.
        @param SrcTxt_: Заменяемый текст.
        @param DstTxt_: Заменяющий текст.
        @return: True - замена прошла успешно, False - замена не произошла.
        """
        pass
    
    def updateInFormModule(self,Txt_,*args,**kwargs):
        """
        Заменить текст всех процедур и функций.
        @param Txt_: Заменяемый текст.
        @return: True - замена прошла успешно, False - замена не произошла.
        """
        res_filename=os.path.normpath(self.getCFDir()+'/'+self.uid+'.0')
        if os.path.exists(res_filename) and os.path.isfile(res_filename):
            #return self._updateInFormModuleCtrl(res_filename,Txt_,*args,**kwargs)
            pass
        else:
            mod_filename=os.path.normpath(res_filename+'/module')
            if os.path.exists(mod_filename) and os.path.isfile(mod_filename):
                return self._updateInFormModuleStd(mod_filename,Txt_,*args,**kwargs)
        print(('ERROR! Form %s (UID:%s) resource file not found!'%(self.name,self.uid)))
        return None    

    def _splitModuleProcBlock(self,Txt_):
        """
        Разбить текст модуля на блоки процедур и функций.
        @param Txt_: Текст модуля.
        """
        txt_lines=Txt_.split('\n')
        
        blocks=[]
        cur_block=[None,'']
        end_block=False
        first_proc=False
        for line in txt_lines:
            if ('Процедура' in line) or ('Функция' in line):
                new_block=[line.strip(),line+'\n']
                if not first_proc:
                    #end_block=True
                    first_proc=True
                end_block=True               
            elif ('КонецПроцедуры' in line) or ('КонецФункции' in line):
                cur_block[1]+=line+'\n'
                new_block=[None,'']
                end_block=True
            else:
                cur_block[1]+=line+'\n'

            if end_block:
                blocks.append(cur_block)
                cur_block=new_block
                end_block=False
                
        blocks.append(cur_block)
        
        #Если первый блок пустой, то удалить его
        if blocks[0]==[None,'']:
            del blocks[0]
            
        return blocks
    
    def _appendInModuleBlocks(self,ModuleBlocks_,PrgBlock_):
        """
        Добавить блок процедуры/функции в блоки модуля.
        @param ModuleBlocks_:Список блоков модуля.
        @param PrgBlock_: Добавляемый блок.
        @return: Обновленный ModuleBlocks_
        """
        max_i=0
        for i,block in enumerate(ModuleBlocks_):
            if ('КонецПроцедуры' in block[1]) or ('КонецФункции' in block[1]):
               max_i=max(i,max_i)
        ModuleBlocks_.insert(max_i+1,PrgBlock_)
        return ModuleBlocks_
    
    def _updateInFormModuleStd(self,ModFileName_,Txt_,*args,**kwargs):
        """
        Заменить текст всех процедур и функций.
        @param ModFileName_: Имя файла модуля формы.
        @param Txt_: Заменяемый текст.
        @return: True - замена прошла успешно, False - замена не произошла.
        """
        Txt_=util.encodeText(Txt_,'unicode','utf-8')
        
        f=None
        try:
            f=open(ModFileName_,'r')
            mod_txt=f.read()
            f.close()
            f=None
        except:
            if f:
                f.close()
                f=None
            raise
        #Обновить блоки процедур/функций
        mod_blocks=self._splitModuleProcBlock(mod_txt)
        #print 'MODULE>>>>>>',mod_blocks
        update_blocks=self._splitModuleProcBlock(Txt_)
        #print 'UPDATE>>>>>>',update_blocks
        for update_block in update_blocks:
            if update_block[0]:
                is_add=True
                for i,mod_block in enumerate(mod_blocks):
                    if update_block[0]==mod_block[0]:
                        #print '>>>',update_block[0],mod_block[0]
                        #Заменить блок
                        mod_blocks[i]=update_block
                        is_add=False
                        break
                #Если такой процедуры нет в тексте модуля, то добавить ее
                if is_add:
                    #mod_blocks.append(update_block)
                    mod_blocks=self._appendInModuleBlocks(mod_blocks,update_block)

        #Собрать текст модуля из обновленных блоков
        mod_txt=''
        for mod_block in mod_blocks:
            mod_txt+=mod_block[1]+'\n'
        mod_txt=mod_txt.replace('\r\n','\n').replace('\n','\r\n')
        try:
            f=open(ModFileName_,'w')
            f.write(mod_txt)
            f.close()
            f=None
        except:
            if f:
                f.close()
                f=None
            raise
        return True
        
    def addFormRequisite(self,Name_,Type_,*args,**kwargs):
        """
        Добавить реквизит формы. Обычная форма.
        @param Name_: Имя реквизита формы.
        @param Type_: Тип реквизита формы.
        """
        res_filename=os.path.normpath(self.getCFDir()+'/'+self.uid+'.0')
        if os.path.exists(res_filename) and os.path.isfile(res_filename):
            return self._addFormRequisiteCtrl(res_filename,Name_,Type_,*args,**kwargs)
        else:
            res_filename=os.path.normpath(res_filename+'/form')
            if os.path.exists(res_filename) and os.path.isfile(res_filename):
                return self._addFormRequisiteStd(res_filename,Name_,Type_,*args,**kwargs)
        print(('ERROR! Form %s (UID:%s) resource file not found!'%(self.name,self.uid)))
        return None
        
    def _addFormRequisiteStd(self,ResFileName_,Name_,Type_,*args,**kwargs):
        """
        Добавить реквизит формы. Обычная форма.
        @param ResFileName_: Имя файла ресурса формы.
        @param Name_: Имя реквизита формы.
        @param Type_: Тип реквизита формы.
        """
        res=iccfresource.icCFResource(ResFileName_)
        res.loadData()
        
        #idx=util.ValueIndexPath(res.data,'Реквизит')
        #print 'requisite>>>',idx
        #print 'requisite>>>',res.data[2][2]
        
        requisite_template=copy.deepcopy(STD_FORM_REQUISITE_TEMPLATE)
        requisite_template[3]=Name_
        type=types1c.types[Type_]
        requisite_template[4][1]=type
        prev_idx=res.data[2][2][-1][0][0] 
        requisite_template[0][0]=prev_idx+1
        if res.data[-2:]==[1,1] and res.data[0]==27:
            requisite_template.insert(1,0)
        
        res.data[2][2].append(requisite_template)
        
        #Увеличить счетчик реквизитов формы
        res.data[2][2][0]+=1
        
        return res.saveData()
        
    def _addFormRequisiteCtrl(self,ResFileName_,Name_,Type_,*args,**kwargs):
        """
        Добавить реквизит формы. Управляемая форма.
        @param ResFileName_: Имя файла ресурса формы.
        @param Name_: Имя реквизита формы.
        @param Type_: Тип реквизита формы.
        """
        res=iccfresource.icCFResource(ResFileName_)
        res.loadData()
        
        #print 'FORM RESOURCE:'
        #print util.StructToTxt(res.data)
        requisite_template=copy.deepcopy(CTRL_FORM_REQUISITE_TEMPLATE)
        requisite_template[3]=Name_
        description=''
        if 'Description_' in kwargs:
            description=kwargs['Description_']
        requisite_template[4][2][1]=description
        type=types1c.types[Type_]
        requisite_template[5][1]=type 
        
        res.data[3]=res.data[3][:-3]+[requisite_template]+res.data[3][-3:]
        
        #Увеличить счетчик реквизитов формы
        #print 'DBG!!!:',res.data[3][1]
        res.data[3][1]+=1
        
        #idx=util.ValueIndexPath(res.data,'ДеревоКолонки')
        #print 'name>>>',idx
        #print util.StructToTxt(res.data[3])
        
        return res.saveData()
    
    def delFormRequisite(self,Name_):
        """
        Удалить реквизит формы по имени.
        @param Name_: Имя реквизита формы.
        """
        pass

    def _findObjResIdx(self,ResData_,ObjName_):
        """
        Найти индекс ресурса объекта в ресурсе формы по его имени.
        """
        idx=util.ValueIndexPath(ResData_,ObjName_)
        if idx:
            return idx[:-1]
        return None
        
    def addFormObjEvent(self,Name_,Value_,*args,**kwargs):
        """
        Добавить событие в объект формы.
        @param Name_: Имя объекта формы и события в формате
        <Имя объекта>.<Имя события>
        @param Value_: Значение которое необходимо прописать в событии.
        """
        res_filename=os.path.normpath(self.getCFDir()+'/'+self.uid+'.0')
        if os.path.exists(res_filename) and os.path.isfile(res_filename):
            #return self._addFormObjEventCtrl(res_filename,Name_,Value_,*args,**kwargs)
            print(('CTRL FORM!',res_filename))
        else:
            res_filename=os.path.normpath(res_filename+'/form')
            if os.path.exists(res_filename) and os.path.isfile(res_filename):
                return self._addFormObjEventStd(res_filename,Name_,Value_,*args,**kwargs)
        print(('ERROR! Form %s (UID:%s) resource file not found!'%(self.name,self.uid)))
        return None

    def _addFormObjEventCtrl(self,ResFileName_,Name_,Value_):
        """
        Добавить событие в объект формы. Управляемая форма.
        @param ResFileName_: Имя файла ресурса формы.
        @param Name_: Имя объекта формы и события в формате
        <Имя объекта>.<Имя события>
        @param Value_: Значение которое необходимо прописать в событии.
        """
        res=iccfresource.icCFResource(ResFileName_)
        res.loadData()

        names=Name_.split('.')
        if len(names)<>2:
            print(('Object name and event name not define!',names))
            return

        obj_name=util.encodeText(names[0],'unicode','utf-8')
        evt_name=util.encodeText(names[1],'unicode','utf-8')        
        obj_idx=self._findObjResIdx(res.data,obj_name)
        
        #idx=util.ValueIndexPath(res.data,'СписокПередНачаломДобавления')
        #print 'event>>>',idx
        if evt_name=='ПередНачаломДобавления':
            if obj_idx:
                evt_idx=(1,27,73)
                evt_res=res.getByIdxList(evt_idx)
                if evt_res==[0]:
                    #Если событие не определено
                    evt_template=copy.deepcopy(CTRL_BEFORE_ADD_START_EVENT_TEMPLATE)
                    evt_template[-1]=util.encodeText(Value_,'unicode','utf-8')
                    res.data[1][27][73]=evt_template
                #print 'EVENT::',evt_res
        else:
            print(('Event \'%s\' not support'%evt_name))
            return
        
        return res.saveData()

    _evtID={'ПередНачаломДобавления':40,
            'ПриПовторномОткрытии':70008,
            'ПередОткрытием':70000,
            'ПриОткрытии':70001,
            }
    def _createFormObjEventResStd(self,EventName_,Value_,ID_):
        """
        """
        evt_template=copy.deepcopy(STD_BEFORE_ADD_START_EVENT_TEMPLATE)
        evt_template[0]=ID_
        evt_template[2][1]=EventName_
        evt_template[2][2][1]=Value_
        description=util.splitName1CWord(EventName_)
        evt_template[2][2][2][2][1]=description
        evt_template[2][2][3][2][1]=description
        evt_template[2][2][4][2][1]=description
        return evt_template
        
    _SupportEventNames=('ПередНачаломДобавления','ПередОткрытием')
    def _addFormObjEventStd(self,ResFileName_,Name_,Value_):
        """
        Добавить событие в объект формы. Обычная форма.
        @param ResFileName_: Имя файла ресурса формы.
        @param Name_: Имя объекта формы и события в формате
        <Имя объекта>.<Имя события>
        @param Value_: Значение которое необходимо прописать в событии.
        """
        res=iccfresource.icCFResource(ResFileName_)
        res.loadData()

#        idx=util.ValueIndexPath(res.data,'ПриПовторномОткрытии')
#        print 'event>>>',idx
#        idx=util.ValueIndexPath(res.data,'ДокументСписокПередНачаломДобавления')
#        print 'event1>>>',idx

        names=Name_.split('.')
        if len(names)<>2:
            print(('Object name and event name not define!',names))
            return

        obj_name=util.encodeText(names[0],'unicode','utf-8')
        evt_name=util.encodeText(names[1],'unicode','utf-8') 
        value=util.encodeText(Value_,'unicode','utf-8') 
        
        if evt_name in self._SupportEventNames:
            if obj_name:
                #Если имя объекта указано, то это объект формы
                for obj_res in res.data[1][2][2][1:]:
                    #print 'OBJ RES:',obj_res
                    if obj_res[4][1]==obj_name:
                        full_evt_name=obj_name+evt_name
                        res_evt_names=[evt[2][1] for evt in obj_res[2][4][1:]]
                        if full_evt_name not in res_evt_names:
                            evt_template=self._createFormObjEventResStd(full_evt_name,
                                value,self._evtID[evt_name])
                            obj_res[2][4].append(evt_template)
                            #Увеличить счетчик событий формы
                            obj_res[2][4][0]+=1
                        break
            else:
                res_evt_names=[evt[2][1] for evt in res.data[4][1:]]
                if evt_name not in res_evt_names:
                    #Если имя объекта не указано, то это сама форма
                    evt_template=self._createFormObjEventResStd(evt_name,value,
                        self._evtID[evt_name])
                    res.data[4].append(evt_template)
                    #Увеличить счетчик событий формы
                    res.data[4][0]+=1
        else:
            print(('Event \'%s\' not support'%evt_name))
            return
        
        return res.saveData()
        
    def delFormObjEvent(self,Name_):
        """
        Удалить событие из объекта формы.
        @param Name_: Имя объекта формы и события в формате
        <Имя объекта>.<Имя события>
        """
        pass
    
