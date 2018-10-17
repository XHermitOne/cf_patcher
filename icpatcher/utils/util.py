# !/usr/bin/env python
#  -*- coding: utf-8 -*-
""" 
Сервисные функции программиста.
"""
__version__ = (0,0,0,1)

import types
import os,os.path
import imp
import wx

#Наполнитель позиций при отображении вложенности пунктов в компоненте списка
DEFAULT_PADDING='....'
#Перевод словарно-списковой структуры в форматированный текст
def StructToTxt(Struct_, Level_=0,PADDING=DEFAULT_PADDING):
    """ 
    Перевод словарно-списковой структуры в форматированный текст.
    @param Struct_ : словарно-списковая структура.
    @param Level_: уровень вложенности (д.б. 0).
    """
    try:
        txt=''
        obj_type=type(Struct_)
        if obj_type==types.ListType:
            txt=txt+'\n'+Level_*PADDING+'[\n'
            for obj in Struct_:
                txt+=Level_*PADDING
                txt+=StructToTxt(obj, Level_+1,PADDING)
                txt+=',\n'
            if len(Struct_)<>0:
                txt=txt[:-2]
            txt=txt+'\n'+Level_*PADDING+']'
        elif obj_type==types.DictType:
            txt=txt+'\n'+Level_*PADDING+'{\n'
            keys=Struct_.keys()
            values=Struct_.values()
            for key in keys:
                txt=txt+Level_*PADDING+'\''+key+'\':'
                txt+=StructToTxt(Struct_[key], Level_+1,PADDING)
                txt+=',\n'
            if len(keys)<>0:
                txt=txt[:-2]
            txt=txt+'\n'+Level_*PADDING+'}'
        elif obj_type==types.StringType:
            #Появляется косяк с разделителем папок в именах путей
            #Struct_=Struct_.replace('\\','/')
            #Проверка на кавычки
            txt=txt+'\''+Struct_.replace('\'','\\\'').replace('\'','\\\'').replace('\r','\\r').replace('\n','\\n').replace('\t','\\t')+'\''
        elif obj_type==types.UnicodeType:
            #Появляется косяк с разделителем папок в именах путей
            #Struct_=Struct_.encode('CP1251').replace('\\','/')
            #Проверка на кавычки
            txt=txt+'u\''+Struct_.replace('\'','\\\'').replace('\'','\\\'').replace('\r','\\r').replace('\n','\\n').replace('\t','\\t')+'\''
#        elif obj_type==IntType:
#            txt=txt+str(Struct_)
        else:
            txt=txt+str(Struct_)

        #Убрать первый перевод каретки
        if txt[0]=='\n' and (not Level_):
            txt=txt[1:]
        return txt
    except:
        print(('ERROR! Level: %d'%(Level_)))
        raise

def ValueIndexPath(List_,Value_,Idx_=None):
    """
    Функция позволяет найти значение в сложном списке списков и 
    возвращает кореж индексов-пути до этого элемента.
    """
    if Idx_ is None:
        Idx_=[]
    if type(Idx_) is types.TupleType:
        Idx_=list(Idx_)
        
    if Value_ in List_:
        idx=List_.index(Value_)
        Idx_.append(idx)
        return tuple(Idx_)
    else:
        #Поиск в подсписках
        Idx_.append(-1)
        for i,element in enumerate(List_):
            if type(element) is types.ListType:
                Idx_[-1]=i
                idx_lst=ValueIndexPath(element,Value_,tuple(Idx_))
                if idx_lst:
                    return idx_lst
    #Ничего найти не удалось
    return None

def getModuleDoc(ModuleFileName_):
    """
    Определить текст документации модуля.
    @param ModuleFileName_: Полное имя файла модуля.
    """
    module_name=None
    try:
        module_name=os.path.splitext(os.path.basename(ModuleFileName_))[0]
        module=imp.load_source(module_name,ModuleFileName_)
        if hasattr(module,'__doc__'):
            if wx.Platform=='__WXGTK__':
               return module.__doc__
            elif wx.Platform=='__WXMSW__':
                return unicode(module.__doc__,'utf-8')
            else:
               return module.__doc__
    except:
        print(('ERROR: In function \'util.getModuleDoc\'.Module file: %s Module name: %s'%(ModuleFileName_,module_name)))
        #raise
    return None
        
def genUID():
    """
    Функция генерации уникального идентификатора UID в формате
    XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX.
    """
    import pythoncom
    uid=pythoncom.CreateGuid()
    return str(uid)[1:-1]

def encodeText(Text_,SrcCP_=None,DstCP_='utf-8'):
    """
    Перекодировать текст из одной кодировки в другую.
    @param Text_: Сам текст.
    @param SrcCP_: Кодировка исходного текста.
    @param DstCP_: Кодировка результата.
    @return: Текст в нужной кодировке.
    """
    if (DstCP_ is None) or (DstCP_.lower()=='unicode'):
        if type(Text_)==types.StringType:
            return unicode(Text_,SrcCP_)
        elif type(Text_)==types.UnicodeType:
            return Text_
        return Text_

    if type(Text_)==types.StringType:
        if (SrcCP_ is not None) and (SrcCP_.lower()<>'unicode'):
            txt=unicode(Text_,SrcCP_)
        else:
            txt=unicode(Text_,'utf-8')
        
    elif type(Text_)==types.UnicodeType:
        txt=Text_
        
    return txt.encode(DstCP_)

def listStrRecode(List_,SrcCP_,DstCP_):
    """ 
    Перекодировать все строки в списке рекурсивно в другую кодировку.
    Перекодировка производится также внутри вложенных словарей и кортежей.
    @param List_: Сам список.
    @param SrcCP_: Кодовая страница строки.
    @param DstCP_: Новая кодовая страница строки.
    @return: Возвращает преобразованный список.
    """
    lst=[]
    #Перебор всех элементов списка
    for i in range(len(List_)):
        if type(List_[i])==types.ListType:
            #Елемент - список
            value=listStrRecode(List_[i],SrcCP_,DstCP_)
        elif type(List_[i])==types.DictType:
            #Елемент списка - словарь
            value=dictStrRecode(List_[i],SrcCP_,DstCP_)
        elif type(List_[i])==types.TupleType:
            #Елемент списка - кортеж
            value=tupleStrRecode(List_[i],SrcCP_,DstCP_)
        elif type(List_[i])==types.StringType or type(List_[i])==types.UnicodeType:
            value=encodeText(List_[i],SrcCP_,DstCP_)
        else:
            value=List_[i]
        lst.append(value)
    return lst

def _isRUSString(String_):
    """ Строка с рускими буквами?"""
    if type(String_)==type(''):
        rus_chr=[c for c in String_ if ord(c)>128]
        return bool(rus_chr)
    return False

def dictStrRecode(Dict_,SrcCP_,DstCP_):
    """ 
    Перекодировать все строки в словаре рекурсивно в другую кодировку. 
    Перекодировка производится также внутри вложенных словарей и кортежей.
    @param Dict_: Сам словарь.
    @param SrcCP_: Кодовая страница строки.
    @param DstCP_: Новая кодовая страница строки.
    @return: Возвращает преобразованный словарь.
    """
    keys_=Dict_.keys()
    #Перебор всех ключей словаря
    for cur_key in keys_:
        value=Dict_[cur_key]
        #Нужно ключи конвертировать?
        if _isRUSString(cur_key):
            new_key=encodeText(cur_key,SrcCP_,DstCP_)
            del Dict_[cur_key]
        else:
            new_key=cur_key
            
        if type(value)==types.ListType:
            #Елемент - список
            Dict_[new_key]=listStrRecode(value,SrcCP_,DstCP_)
        elif type(value)==types.DictType:
            #Елемент - cловарь
            Dict_[new_key]=dictStrRecode(value,SrcCP_,DstCP_)
        elif type(value)==types.TupleType:
            #Елемент - кортеж
            Dict_[new_key]=tupleStrRecode(value,SrcCP_,DstCP_)
        elif type(value)==types.StringType or type(value)==types.UnicodeType:
            Dict_[new_key]=encodeText(value,SrcCP_,DstCP_)

    return Dict_

def tupleStrRecode(Tuple_,SrcCP_,DstCP_):
    """ 
    Перекодировать все строки в кортеже рекурсивно в другую кодировку.
    Перекодировка производится также внутри вложенных словарей и кортежей.
    @param Tuple_: Сам кортеж.
    @param SrcCP_: Кодовая страница строки.
    @param DstCP_: Новая кодовая страница строки.
    @return: Возвращает преобразованный кортеж.
    """
    #Перевести кортеж в список
    lst=list(Tuple_)
    #и обработать как список
    list_=listStrRecode(lst,SrcCP_,DstCP_)
    #Обратно перекодировать
    return tuple(list_)

def structStrRecode(Struct_,SrcCP_,DstCP_):
    """ 
    Перекодировать все строки в структуре рекурсивно в другую кодировку.
    @param Struct_: Сруктура (список, словарь, кортеж).
    @param SrcCP_: Кодовая страница строки.
    @param DstCP_: Новая кодовая страница строки.
    @return: Возвращает преобразованную структру.
    """
    if type(Struct_)==types.ListType:
        #Список
        struct=listStrRecode(Struct_,SrcCP_,DstCP_)
    elif type(Struct_)==types.DictType:
        #Словарь
        struct=dictStrRecode(Struct_,SrcCP_,DstCP_)
    elif type(Struct_)==types.TupleType:
        #Кортеж
        struct=tupleStrRecode(Struct_,SrcCP_,DstCP_)
    elif type(Struct_)==types.StringType or type(Struct_)==types.UnicodeType:
        #Строка
        struct=encodeText(Struct_,SrcCP_,DstCP_)
    else:
        #Тип не определен
        struct=Struct_
    return struct

rusRegUpperDict={'а':'А','б':'Б','в':'В','г':'Г','д':'Д','е':'Е','ё':'Ё','ж':'Ж',
              'з':'З','и':'И', 'й':'Й','к':'К','л':'Л','м':'М','н':'Н','о':'О','п':'П',
              'р':'Р','с':'С','т':'Т','у':'У','ф':'Ф','х':'Х','ц':'Ц','ч':'Ч',
              'ш':'Ш','щ':'Щ','ь':'Ь','ы':'Ы','ъ':'Ъ','э':'Э','ю':'Ю','я':'Я'}
def icUpper(str):
    """
    Тупой перевод к верхнему регистру русских букв.
    """
    pyUpper = str.upper()
    upper_str = list(pyUpper)
    upper_str=[rusRegUpperDict.setdefault(pyUpper[ch[0]],ch[1]) for ch in enumerate(upper_str)]
    return ''.join(upper_str)


rusRegLowerDict={'А':'а','Б':'б','В':'в','Г':'г','Д':'д','Е':'е','Ё':'ё','Ж':'ж',
              'З':'з','И':'и','Й':'й','К':'к','Л':'л','М':'м','Н':'н','О':'о','П':'п',
              'Р':'р','С':'с','Т':'т','У':'у','Ф':'ф','Х':'х','Ц':'ц','Ч':'ч',
              'Ш':'ш','Щ':'щ','Ь':'ь','Ы':'ы','Ъ':'ъ','Э':'э','Ю':'ю','Я':'я'}

u_rusRegLowerDict={u'А':u'а',u'Б':u'б',u'В':u'в',u'Г':u'г',u'Д':u'д',u'Е':u'е',u'Ё':u'ё',u'Ж':u'ж',
              u'З':u'з',u'И':u'и',u'Й':u'й',u'К':u'к',u'Л':u'л',u'М':u'м',u'Н':u'н',u'О':u'о',u'П':u'п',
              u'Р':u'р',u'С':u'с',u'Т':u'т',u'У':u'у',u'Ф':u'ф',u'Х':u'х',u'Ц':u'ц',u'Ч':u'ч',
              u'Ш':u'ш',u'Щ':u'щ',u'Ь':u'ь',u'Ы':u'ы',u'Ъ':u'ъ',u'Э':u'э',u'Ю':u'ю',u'Я':u'я'}
            
rusRegLowerLst = ['а','б','в','г','д','е','ё','ж',
              'з','и','й','к','л','м','н','о','п',
              'р','с','т','у','ф','х','ц','ч',
              'ш','щ','ь','ы','ъ','э','ю','я']

u_rusRegLowerLst = [u'а',u'б',u'в',u'г',u'д',u'е',u'ё',u'ж',
              u'з',u'и',u'й',u'к',u'л',u'м',u'н',u'о',u'п',
              u'р',u'с',u'т',u'у',u'ф',u'х',u'ц',u'ч',
              u'ш',u'щ',u'ь',u'ы',u'ъ',u'э',u'ю',u'я']

rusRegUpperLst = ['А','Б','В','Г','Д','Е','Ё','Ж',
              'З','И','Й','К','Л','М','Н','О','П',
              'Р','С','Т','У','Ф','Х','Ц','Ч',
              'Ш','Щ','Ь','Ы','Ъ','Э','Ю','Я']

u_rusRegUpperLst = [u'А',u'Б',u'В',u'Г',u'Д',u'Е',u'Ё',u'Ж',
              u'З',u'И',u'Й',u'К',u'Л',u'М',u'Н',u'О',u'П',
              u'Р',u'С',u'Т',u'У',u'Ф',u'Х',u'Ц',u'Ч',
              u'Ш',u'Щ',u'Ь',u'Ы',u'Ъ',u'Э',u'Ю',u'Я']

def icLower(s):
    """
    Тупой перевод к нижнему регистру русских букв.
    """
    #print '******** type=', type(s)
    pyLower = s.lower()
    lower_str = list(pyLower)
    lower_str=[rusRegLowerDict.setdefault(pyLower[ch[0]],ch[1]) for ch in enumerate(lower_str)]
    return ''.join(lower_str)

def cmpLower(s1, s2):
    """ Сравнивает два символа в нижнем регистре."""
    if s1 in rusRegLowerLst and s2 in rusRegLowerLst:
        p1 = rusRegLowerLst.index(s1)
        p2 = rusRegLowerLst.index(s2)
    
        if p1 > p2:
            return -1
        elif p1 < p2:
            return 1
        else:
            return 0
    else:
        if s1 > s2:
            return -1
        elif s1 < s2:
            return 1
        else:
            return 0

def cmpLowerU(str1, str2):
    """ Сравнивает два символа в нижнем регистре."""
    for i in xrange(min(len(str1), len(str2))):
        s1 = str1[i]
        s2 = str2[i]
        if s1 in u_rusRegLowerLst and s2 in u_rusRegLowerLst:
            p1 = u_rusRegLowerLst.index(s1)
            p2 = u_rusRegLowerLst.index(s2)
        
            if p1 > p2:
                return -1
            elif p1 < p2:
                return 1
            else:
                return 0
        else:
            if s1 > s2:
                return -1
            elif s1 < s2:
                return 1
    if len(str1) > len(str2):
        return -1
    elif len(str1) < len(str2):
        return 1

    return 0

def isLATText(Text_):
    """
    Текст написан в латинице?
    """
    if type(Text_) in (type(''),type(u'')):
        rus_chr=[c for c in Text_ if ord(c)>128]
        return not bool(rus_chr)
    else:
        #Это не строка
        return False
    return True

def isRUSText(Text_):
    """ 
    Строка с рускими буквами?
    """
    if type(String_) in (type(''),type(u'')):
        rus_chr=[c for c in String_ if ord(c)>128]
        return bool(rus_chr)
    else:
        #Это не строка
        return False
    return False

def _rus2lat(Text_,TranslateDict_):
    """
    Перевод русских букв в латинские по словарю замен.
    """
    if type(Text_)<>type(u''):
        #Привести к юникоду
        Text_=unicode(Text_,'utf-8')
        
    txt_list=list(Text_)
    txt_list=[TranslateDict_.setdefault(ch,ch) for ch in txt_list]
    return ''.join(txt_list)
    
    
RUS2LATDict={u'а':'a',u'б':'b',u'в':'v',u'г':'g',u'д':'d',u'е':'e',u'ё':'yo',u'ж':'j',
            u'з':'z',u'и':'i',u'й':'y',u'к':'k',u'л':'l',u'м':'m',u'н':'n',u'о':'o',u'п':'p',
            u'р':'r',u'с':'s',u'т':'t',u'у':'u',u'ф':'f',u'х':'h',u'ц':'c',u'ч':'ch',
            u'ш':'sh',u'щ':'sch',u'ь':'',u'ы':'y',u'ъ':'',u'э':'e',u'ю':'yu',u'я':'ya',
            u'А':'A',u'Б':'B',u'В':'V',u'Г':'G',u'Д':'D',u'Е':'E',u'Ё':'YO',u'Ж':'J',
            u'З':'Z',u'И':'I',u'Й':'Y',u'К':'K',u'Л':'L',u'М':'M',u'Н':'N',u'О':'O',u'П':'P',
            u'Р':'R',u'С':'S',u'Т':'T',u'У':'U',u'Ф':'F',u'Х':'H',u'Ц':'C',u'Ч':'CH',
            u'Ш':'SH',u'Щ':'SCH',u'Ь':'',u'Ы':'Y',u'Ъ':'',u'Э':'E',u'Ю':'YU',u'Я':'YA'}
def rus2lat(Text_):
    """
    Перевод русских букв в латинские.
    """
    return _rus2lat(Text_,RUS2LATDict)
    
RUS2LATKeyboardDict={u'а':'f',u'б':'_',u'в':'d',u'г':'u',u'д':'l',u'е':'t',u'ё':'_',u'ж':'_',
            u'з':'p',u'и':'b',u'й':'q',u'к':'r',u'л':'k',u'м':'v',u'н':'y',u'о':'j',u'п':'g',
            u'р':'h',u'с':'c',u'т':'n',u'у':'e',u'ф':'a',u'х':'_',u'ц':'w',u'ч':'x',
            u'ш':'i',u'щ':'o',u'ь':'m',u'ы':'s',u'ъ':'_',u'э':'_',u'ю':'_',u'я':'z',
            u'А':'F',u'Б':'_',u'В':'D',u'Г':'U',u'Д':'L',u'Е':'T',u'Ё':'_',u'Ж':'_',
            u'З':'P',u'И':'B',u'Й':'Q',u'К':'R',u'Л':'K',u'М':'V',u'Н':'Y',u'О':'J',u'П':'G',
            u'Р':'H',u'С':'C',u'Т':'N',u'У':'E',u'Ф':'A',u'Х':'_',u'Ц':'W',u'Ч':'X',
            u'Ш':'I',u'Щ':'O',u'Ь':'M',u'Ы':'S',u'Ъ':'_',u'Э':'_',u'Ю':'_',u'Я':'Z'}
def rus2lat_keyboard(Text_):
    """
    Перевод русских букв в латинские по раскладке клавиатуры.
    """
    return _rus2lat(Text_,RUS2LATKeyboardDict)

def splitName1CWord(Txt_):
    """
    Разделить текст имен объектов на слова как в 1С.
    Например:
    'ДокументСписокПередНачаломДобавления'->'Документ список перед началом добавления'.
    """
    if type(Txt_)==types.UnicodeType:
        return _splitName1CWordUNICODE(Txt_)
    elif type(Txt_)==types.StringType:
        return _splitName1CWordUTF8(Txt_)
    return Txt_

def _splitName1CWordUTF8(Txt_):
    result=''
    if len(Txt_):
        result=Txt_[0]
        for symbol in Txt_[1:]:
            if symbol in rusRegUpperLst:
                symbol=' '+rusRegLowerDict[symbol]
            result+=symbol
    return result

def _splitName1CWordUNICODE(Txt_):
    result=u''
    if len(Txt_):
        result=Txt_[0]
        for symbol in Txt_[1:]:
            if symbol in u_rusRegUpperLst:
                symbol=u' '+u_rusRegLowerDict[symbol]
            result+=symbol
    return result
