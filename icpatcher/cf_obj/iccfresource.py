#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс работы с ресурсом элемента конфигурации 1с, разобранной V8Unpack v2.0.
"""

import os,os.path
import re
import types

try:
    from utils import util
except:
    pass

RE_UID_PATTERN=r'........-....-....-....-............'
#RE_FLAG_PATTERN=r',([0-1][0-1][0-1][0-1][0-1][0-1][0-1][0-1][0-1][0-1][0-1][0-1][0-1][0-1]),'
RE_DATE_PATTERN=r',([0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]),'
RE_BINARY_PATTERN=r',([0-9a-zA-Z+!?/=\s]*)=]'
RE_BASE64_PATTERN=r'#base64:([0-9a-zA-Z+!?/=\s]*)]'

RESOURCE_PREFIX='\xef\xbb\xbf'

class icCFResource:
    """
    Класс менеджера управления ресурсом объекта конфигурации.
    """
    def __init__(self,CFResFileName_=None):
        """
        Конструктор.
        @param CFResFileName_: Полное имя ресурса объекта конфигурации.
        """
        self.cf_res_filename=None
        if CFResFileName_:
            self.cf_res_filename=os.path.abspath(CFResFileName_)
        
        #Непосредственно данные ресурса
        self.data=None
        
    def loadData(self,CFResFileName_=None):
        """
        Загрузить данные из ресурсного файла.
        @param CFResFileName_: Полное имя ресурса объекта конфигурации.
        """
        if CFResFileName_:
            self.cf_res_filename=os.path.abspath(CFResFileName_)
        
        if os.path.exists(self.cf_res_filename):
            f_res=None            
            try:
                f_res=open(self.cf_res_filename)
                txt_data=f_res.read()
                f_res.close()
            except:
                if f_res:
                    f_res.close()
                f_res=None
            
            try:    
                self.data=self._parseTxt2Data(txt_data)
            except:
                print(('ERROR: Parse resource file:',self.cf_res_filename))
                raise
        else:
            print(('ERROR: CF resource file',self.cf_res_filename,'not found!'))
        
    def _parseTxt2Data(self,TxtData_):
        """
        Пропарсить текстовые данные.
        """
        txt_data=TxtData_.replace('{','[').replace('}',']').replace('"','"""')
        #txt_data=txt_data.replace('\'\'\'\'\'\'','\'\'')
        #txt_data=txt_data.replace('\n','').replace('\r','')
        txt_data=txt_data.replace('\r','')        
        txt_data.strip()
   
        #Обрамить бинарные данные кавычками
        re_binary_list=re.findall(RE_BINARY_PATTERN,txt_data)
        #print 'DBG:::',re_binary_list
        binary_lst=[]
        for binary in re_binary_list:
            if binary not in binary_lst:
                binary_lst.append(binary)
        for binary in binary_lst:
            #txt_data=txt_data.replace(','+binary+'==]',',\'\'\''+binary+'==\'\'\']')
            txt_data=txt_data.replace(binary+'=','\'\'\''+binary+'=\'\'\'')
        re_binary_list=re.findall(RE_BASE64_PATTERN,txt_data)
        binary_lst=[]
        for binary in re_binary_list:
            if binary not in binary_lst:
                binary_lst.append(binary)
        for binary in binary_lst:
            txt_data=txt_data.replace('#base64:'+binary+']','\'\'\'#base64:'+binary+'\'\'\']')
        
        #Обрамление всех UIDов кавычками
        re_uid_list=re.findall(RE_UID_PATTERN,txt_data)
        #print 'UID:::::',uid_list
        uid_lst=[]
        for uid in re_uid_list:
            if uid not in uid_lst:
                uid_lst.append(uid)
        #print 'result:',result
        for uid in uid_lst:
            txt_data=txt_data.replace(uid,'\''+uid+'\'')

        #Обрамление всех флагов кавычками
        #re_flag_list=re.findall(RE_FLAG_PATTERN,txt_data)
        #flag_lst=[]
        #for flag in re_flag_list:
        #    if flag not in flag_lst:
        #        flag_lst.append(flag)
        #for flag in flag_lst:
        #    txt_data=txt_data.replace(flag,',\''+flag+'\',').replace(',,',',')
        
        #Обрамление всех дат кавычками
        re_date_list=re.findall(RE_DATE_PATTERN,txt_data)
        date_lst=[]
        for date in re_date_list:
            if date not in date_lst:
                date_lst.append(date)
        for date in date_lst:
            txt_data=txt_data.replace(date,',\''+date+'\',')

        #txt_data=txt_data.replace('[=','[\'\'\'=').replace('=]','=\'\'\']')
        #txt_data=txt_data.replace('[+','[\'\'\'+').replace('+]','+\'\'\']')
        #txt_data=txt_data.replace('[#base64:','[\'\'\'#base64:').replace('=]','=\'\'\']')
        #txt_data=txt_data.replace(',=',',\'\'\'=').replace('=,','=\'\'\',')
        #txt_data=txt_data.replace(',+',',\'\'\'+').replace('+,','+\'\'\',')
        #txt_data=txt_data.replace(',#',',\'\'\'#').replace('#,','#\'\'\',')
        
        #print 'DBG1:::',txt_data,

        #Убрать все двойные запятые из текста
        while (',,' in txt_data) or (', ,' in txt_data):
            txt_data=txt_data.replace(',,',',').replace(', ,',',')

        try:
            data=eval(txt_data)
        except:
            print(('ERROR! Resource syntax error: ',txt_data))
            data=None
            raise
        
        #print ':',data
        return data

    def _str(self,Data_):
        if type(Data_)==types.StringType:
            if Data_[:8]=='#base64:':
                return Data_.replace('\n','\r\r\n').replace('\\n','\r\r\n')
            else:
                return '"'+Data_.replace('\n','\r\n')+'"'
        elif type(Data_)==types.UnicodeType:
            return '"'+Data_.encode('utf-8')+'"'
        else:
            return str(Data_)
        
    def _data2txt(self,Data_):
        """
        Преобразовать данные в текст в формате необходимым для конвертации.
        """
        result_txt=''
        if type(Data_)==types.ListType:
            result_txt+='{'
            count=len(Data_)-1
            for i,value in enumerate(Data_):
                if type(value)==types.ListType:
                    result_txt+='\r\n'
                    result_txt+=self._data2txt(value)
                    if i==count:
                        result_txt+='\r\n'                        
                else:
                    result_txt+=self._str(value)
                #Если элемент не последний, то добавить запятую
                if i<count:
                    result_txt+=','
            result_txt+='}'
        return result_txt
        
    def _parseData2Txt(self,Data_):
        """
        Преобразовать данные в текст.
        """
        Data_=util.structStrRecode(Data_,'unicode','utf-8')
        #txt_data=util.StructToTxt(Data_,0,'')
        txt_data=self._data2txt(Data_)
        txt_data=RESOURCE_PREFIX+txt_data
        
        #все UIDы
        uid_list=re.findall(RE_UID_PATTERN,txt_data)
        uid_lst=[]
        for uid in uid_list:
            if uid not in uid_lst:
                uid_lst.append(uid)
        #print 'result:',result
        for uid in uid_lst:
            txt_data=txt_data.replace('"'+uid+'"',uid)

        #все флаги
        #flag_list=re.findall(RE_FLAG_PATTERN,txt_data)
        #flag_lst=[]
        #for flag in flag_list:
        #    if flag not in flag_lst:
        #        flag_lst.append(flag)
        #for flag in flag_lst:
        #    txt_data=txt_data.replace('"'+flag+'"',flag)

        #все даты
        date_list=re.findall(RE_DATE_PATTERN,txt_data)
        date_lst=[]
        for date in date_list:
            if date not in date_lst:
                date_lst.append(date)
        for date in date_lst:
            txt_data=txt_data.replace('"'+date+'"',date)

        #txt_data=txt_data.replace('[','{').replace(']','}').replace('\'\'\'','"').replace('\'','\"')
        #txt_data=txt_data.replace('\n','\r\n')
        txt_data=txt_data.replace('\\n','\r\n')
        txt_data=txt_data.replace('\\t','\t')

        #бинарные данные
#        txt_data=txt_data.replace('[\'\'\'=','[=').replace('=\'\'\']','=]')
#        txt_data=txt_data.replace('[\'=','[=').replace('=\']','=]')
#        txt_data=txt_data.replace('[\'\'\'+','[+').replace('+\'\'\']','+]')
#        txt_data=txt_data.replace('[\'+','[+').replace('+\']','+]')
#        txt_data=txt_data.replace('[\'\'\'#','[#').replace('#\'\'\']','#]')
#        txt_data=txt_data.replace('[\'#','[#').replace('#\']','#]')
#        txt_data=txt_data.replace(',\'\'\'=',',=').replace('=\'\'\',','=,')
#        txt_data=txt_data.replace(',\'=',',=').replace('=\',','=,')
#        txt_data=txt_data.replace(',\'\'\'+',',+').replace('+\'\'\',','+,')
#        txt_data=txt_data.replace(',\'+',',+').replace('+\',','+,')
#        txt_data=txt_data.replace(',\'\'\'#',',#').replace('#\'\'\',','#,')
#        txt_data=txt_data.replace(',\'#',',#').replace('#\',','#,')
#        txt_data=txt_data.replace('{#,','{"#",')
        #txt_data=txt_data.replace('"#base64:','#base64:')
        #txt_data=txt_data.replace('="','=')
            
        return txt_data

    def saveData(self,CFResFileName_=None):
        """
        Записать данные в ресурсный файл.
        @param CFResFileName_: Полное имя ресурса объекта конфигурации.
        """
        if CFResFileName_:
            self.cf_res_filename=os.path.abspath(CFResFileName_)

        txt_data=self._parseData2Txt(self.data)
        
        f=None
        try:
            f=open(self.cf_res_filename,'w')
            f.write(txt_data)
            f.close()
            return True
        except:
            if f:
                f.close()
                f=None
            raise
        return False
    
    def getByIdxList(self,IdxList_,Res_=None):
        """
        Получить часть ресурса по списку индексов.
        """
        if Res_ is None:
            Res_=self.data
        if len(IdxList_)>1:
            return self.getByIdxList(IdxList_[1:],Res_[IdxList_[0]])
        else:
            return Res_[IdxList_[0]]        
        
        
def test():
    """
    Функция тестирования.
    """
    import sys
    
    dir_path=os.path.dirname(__file__)
    if not dir_path:
        dir_path=os.getcwd()
        
    sys.path.append(os.path.dirname(dir_path))
    
    res_filename=os.path.abspath(dir_path+'/test/root')
    print(('RES FILE:',res_filename))
    if os.path.exists(res_filename):
        res=icCFResource(res_filename)
        res.loadData()
        print(('RES:',res.data))

def test1():
    """
    Функция тестирования.
    """
    dir_path=os.path.dirname(__file__)
    if not dir_path:
        dir_path=os.getcwd()
        
    res_filename=os.path.dirname(os.path.dirname(dir_path))+'/example/form'
    print(('RES FILE:',res_filename))
    if os.path.exists(res_filename):
        res=icCFResource(res_filename)
        res.loadData()
        print(('RES:',res.data[2]))

if __name__=='__main__':
    test()