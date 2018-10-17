#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Класс пользовательского визуального компонента.
Компонент древовидного представления данных.
Работает с простой словарно-списковой структурой:
[
    {
    'name':Имя узла,
    'img': Файл картинки узла,
    'img_exp': Файл картинки раскрытого узла,
    'checkable': Может отмечаться пользователем?
    'children':[...], Список словарей дочерних узлов
    '__type__': Тип узла: 0 - обычный, 1- Отмечаеемый, 2- Переключаемый
    '__record__':Данные, прикреплямые к узлу  в виде списка.
    },
    ...
]

ПРИМЕЧАНИЕ!!!
Обработчик нажатия клавиши на дереве цепляется через
wx.EVT_TREE_KEY_DOWN, а не wx.EVT_KEY_DOWN, как у других компонентов.
"""

import wx
import wx.gizmos as gizmos

_ = wx.GetTranslation

import wx.lib.agw.hypertreelist as hypertreelist
from wx.lib.agw import customtreectrl

from utils import img_lst

#   Версия компонента
__version__ = (0,0,0,1)

DEFAULT_ENCODING='utf-8'

class icColTreeInfo(hypertreelist.TreeListColumnInfo):
    def __init__(self, input="", width=hypertreelist._DEFAULT_COL_WIDTH, flag=wx.ALIGN_LEFT,
                 image=-1, shown=True, colour=None, edit=False):
        if type(input) in (type(""), type(u"")):
            self._text = input
            self._width = width
            self._flag = flag
            self._image = image
            self._selected_image = -1
            self._shown = shown
            self._edit = edit
            self._font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            if colour is None:
                self._colour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWTEXT)
        else:
            self._text = input._text
            self._width = input._width
            self._flag = input._flag
            self._image = input._image
            self._selected_image = input._selected_image
            self._shown = input._shown
            self._edit = input._edit
            self._colour = input._colour
            self._font = input._font

class icSmartTreeListCtrl(hypertreelist.HyperTreeList):
    """ 
    Описание пользовательского компонента.
    """

    def __init__(self,parent,id,position,size,style,labels,wcols=None,**kwargs):
        """ 
        Конструктор базового класса пользовательских компонентов.
        """
        if wx.VERSION < (2, 8, 11, 0, ''):
            hypertreelist.HyperTreeList.__init__(self,parent,id,position,size,style=style)
        else:
            hypertreelist.HyperTreeList.__init__(self,parent,id,position,size,
                                        agwStyle=style,style=style)
            
        self.setVistaStyle()

        if 'foregroundColor' in kwargs:
            foregroundColor=kwargs['foregroundColor']
            if type(foregroundColor)==type(()):
                self.SetForegroundColour(wx.Colour(*foregroundColor))

        if 'backgroundColor' in kwargs:
            backgroundColor=kwargs['backgroundColor']
            if type(backgroundColor)==type(()):
                self.SetBackgroundColour(wx.Colour(*backgroundColor))
        
        self.tree=[]
        
        #Последний выбранный элемент дерева
        self._last_selection=None
        #Последний найденный элемент
        #self._last_find_item=None
        #Последняя найденная колонка
        self._last_find_col_idx=0

        #self.spravDict = {}
        import newstyle_img
        isz = (16,16)
        # Установка списка образов компонентов
        self._img_list=img_lst.icImgList(self,isz[0], isz[1])
        self.fldridx,self.fldropenidx=self._img_list.setImgIdx('FOLDER',newstyle_img.folder,newstyle_img.openfolder)
        self.fileidx=self._img_list.setImgIdx('NEW_DOC',newstyle_img.newdoc)[0]
        self.curidx=self._img_list.setImgIdx('PAGE_COMMENT',newstyle_img.pageComment)[0]
        #self.SetImageList(self._img_list.getImageList())
        self.AssignImageList(self._img_list.getImageList())
        
        self.labels=labels if labels is not None else []

        #Установки колонок
        self.SetMainColumn(0) # the one with the tree in it...
        
        for indx, label in enumerate(self.labels):
            #Перевод подписей колонок в строковое представление
            if wcols and len(wcols) > indx:
                w = wcols[indx]
            else:
                w = hypertreelist._DEFAULT_COL_WIDTH
                
            colInfo = icColTreeInfo(label, w, wx.ALIGN_LEFT, -1, True, None, False)            
            self.AddColumnInfo(colInfo)
                
        #   Определяем корень
        self.titleRoot=u''
        if 'titleRoot' in kwargs and kwargs['titleRoot']:
            self.titleRoot=kwargs['titleRoot']
        self.imgRoot=None
        if 'imgRoot' in kwargs and kwargs['imgRoot']:
            self.imgRoot=kwargs['imgRoot']
        self.imgExpRoot=None
        if 'imgExpRoot' in kwargs and kwargs['imgExpRoot']:
            self.imgExpRoot=kwargs['imgExpRoot']
        
        #print 'DBG:::',self.titleRoot,self.labels
        self.root = self.AddRoot(self.titleRoot)
        #print 'ROOT IMAGE:::::::',self.imgRoot, kwargs['imgRoot'] #,root_img_idx
        if self.imgRoot is None:
            self.SetItemImage(self.root,self.fldridx,which=wx.TreeItemIcon_Normal)
            self.SetItemImage(self.root,self.fldropenidx,which=wx.TreeItemIcon_Expanded)
        else:
            root_img_idx=self._img_list.setImgIdx('ROOT',self.imgRoot,self.imgExpRoot)
            self.SetItemImage(self.root,root_img_idx[0],which=wx.TreeItemIcon_Normal)
            if root_img_idx[1]>=0:
                self.SetItemImage(self.root,root_img_idx[1],which=wx.TreeItemIcon_Expanded)            

        self.SetCheckRadio()
        if 'hideHeader' in kwargs and kwargs['hideHeader']:
            self.HideHeader()

        #   Регистрация обработчиков событий
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectChanged)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_TREE_KEY_DOWN, self.OnTreeListKeyDown)
        self.Bind(customtreectrl.EVT_TREE_ITEM_CHECKED, self.OnItemChecked)

        self.textload = wx.StaticText(self._main_win, -1, label=_('Load data ...'), pos=(70,70))
        self.textload.Show(False)        
            
    def begin_load(self):
        self.Enable(False)
        self.textload.Show(True)

    def end_load(self):
        self.textload.Show(False)
        self.Enable()
        
    def setVistaStyle(self):
        """ Установка стиля Vista. Стиль по умолчанию."""
        self.EnableSelectionVista(True)        

    def expandAllRoot(self):
        """ Раскрыть всю ветку от корня."""
        return self.ExpandAll()
        
    def getSelectionName(self):
        """ Имя выбранного узла."""
        selection_item=self.GetSelection()
        return self.GetItemText(selection_item)
    
    def addNode(self, root, res, level=0, start_level=0):
        """ Добавить дочерние узлы, описанные словарем."""
        id_pic, id_exp_pic = self._getPicturesId(res)
        
        if len(self.labels) == 1 and len(res['__record__']) > 1:
            st = u'  ' + (unicode(res['__record__'][1]) or '')
        else:
            st = u''
        node_ct_type=int(res.get('checkable', 0)) if 'checkable' in res  else res.get('__type__', 0)
        child = self.AppendItem(root, res['name']+st, ct_type=node_ct_type)
        self.SetItemImage(child, id_pic, which=wx.TreeItemIcon_Normal)
        self.SetItemImage(child, id_exp_pic, which=wx.TreeItemIcon_Expanded)
        self.SetPyData(child, (level+start_level, res))
        if '__record__' in res:
            self.setItemRecord(child,res['__record__'])
        
        #Обработка дочерних элементов
        if 'children' in res and res['children']:
            for node in res['children']:
                self.addNode(child, node, level+1, start_level)
            
    def _isChildrenRes(self,Res_):
        """ Есть ли в описании ресурса описание дочерних элементов?
        @param Res_: Ресурс.
        @return: Возвращает True/False.
        """
        if 'children' in Res_ and Res_['children']:
            return True
        return False
        
    def _getPicturesId(self,Res_):
        """ Определение картинок для изобращения узла по ресурсу этого узла.
        @param Res_: Ресурс узла.
        @return: Кортеж из 2-х элементов - идентификаторов картинок.
        """
        #print 'PIC DBG:::',Res_['name'].encode('utf-8'),Res_['img']
        #Если нет дочерних элементов в описании, тогда картинки-файлы
        if not self._isChildrenRes(Res_):
            default_img_idx=(self.fileidx, self.curidx)
        else:
            default_img_idx=(self.fldridx, self.fldropenidx)

        if 'img' in Res_ and Res_['img']:
            img_exp=None
            if 'img_exp' in Res_ and Res_['img_exp']:
                img_exp=Res_['img_exp']
            img_idx=self._img_list.setImgIdx(Res_['name'],Res_['img'],img_exp)
            return img_idx
        
        return default_img_idx
        
    def setItemRecord(self,Item_,Record_):
        """ Установить список записи на узле.
        @param Item_: ID узла у которого устанавливается запись.
        @param Record_: Запись узла. Список.
        """
        if Record_ and self.isList(Record_):
            for idx,value in enumerate(Record_[1:]):
                if type(value)<>type(u''):
                    value=unicode(str(value),DEFAULT_ENCODING)
                self.SetItemText(Item_, value, idx+1)
        return Item_
        
    def getItemRecord(self,Item_):
        """ Список записи на узле.
        @param Item_: ID узла у которого устанавливается запись.
        @return: Возвращает список строк записи узла. 
            Или None в случае ошибки.
        """
        try:
            item_py_data=self.GetPyData(Item_)
            if item_py_data is None:
                return None
            res=item_py_data[1]
            if type(res)==type({}) and '__record__' in res:
                return res['__record__']
            return None
        except:
            io_prnt.outErr(u'ОШИБКА компонента %s метода getItemRecord'%(self.name))
            return None

    def getSelectionRecord(self):
        """ Список записи выбранного узла.
        @return: Возвращает список строк записи узла. 
            Или None в случае ошибки.
        """
        selection_item=self.GetSelection()
        return self.getItemRecord(selection_item)
        
    def setLabelCols(self,LabelCols_):
        """ Установить надписи колонок.
        @param LabelCols_: Надписи колонок. Список строк.
        @return: Возвращает результат выполнения функции True/False.
        """
        try:
            col_count=self.GetColumnCount()
            for i_col,col_label in enumerate(LabelCols_):
                if i_col<col_count:
                    self.SetColumnText(i_col,col_label)
                else:
                    break
            return True
        except:
            io_prnt.outErr(u'ОШИБКА компонента %s метода setLabelCols'%(self.name))
            return False
        
    def getElementName(self, res, indx):
        """ Возвращает имя элемента списка."""
        return 'element %s:' % unicode(indx)
        
    def isDict(self, res):
        """ Признак словарного интерфейса."""
        return type(res)==type({})

    def isList(self, res):
        """ Признак интерфейса последовательности."""
        return type(res)==type([])
        
    def clearRoot(self):
        """ Полностью очистить содержимо корневого элемента."""
        root=self.GetRootItem()
        return self.DeleteChildren(root)
        
    def GetCount(self):
        tree = self.GetMainWindow()
        return tree.GetCount()
    
    def LoadTree(self, Tree_=None,AutoSelect_=True,AutoExpand_=True):
        """ Заполняем дерево.
        
        @type Tree_: C{list}
        @param Tree_: Словарно-списковая структура, отображаемая в дереве.
        @type AutoSelect_: C{bool}
        @param AutoSelect_: Автоматически выбрать последний элемент.
        @type AutoExpand_: C{bool}
        @param AutoExpand_: Автоматически развернуть корневой элемент.
        """
        #Если включен автовыбор элемента
        #то сначала сбросить выделение всех элементов
        if AutoSelect_:
            self.UnselectAll()
            
        if Tree_ is None:
            Tree_=self.tree
        else:
            self.tree = Tree_
        
        self.DeleteChildren(self.root)
        self.SetPyData(self.root, (-1, Tree_))
        
        if Tree_ is not None:
            for node in Tree_:
                self.addNode(self.root, node)
        else:
            self._testTree()
            
        #Автовыбор элемента
        if AutoSelect_:
            if self._last_selection:
                self.selectItemPath(self._last_selection)
            else:
                if not self.IsSelected(self.root):
                    self.SelectItem(self.root)
                
        #Авторазворачивание верхнего уровня
        if AutoExpand_:
            try:
                self.Expand(self.root)
            except: pass

        self.end_load()
        
    def selectItemPath(self,ItemPath_,CurItem_=None):
        """ Выбрать элемент по пути.
        @param ItemPath_: Путь до элемента.
        @param CurItem_: Текущий элемент поиска. 
            Если None, то поиск начиниется с корня.
        """
        if CurItem_ is None:
            CurItem_=self.root
        if ItemPath_:
            cur_item=self.FindItem(CurItem_,ItemPath_[0])
            #Есть дочерние элементы
            if ItemPath_[1:]:
                self.Expand(cur_item)
            return self.selectItemPath(ItemPath_[1:],cur_item)
        if not self.IsSelected(CurItem_):
            return self.SelectItem(CurItem_)
        return None
        
    def getItemPath(self,Item_,Path_=None):
        """ Путь до элемента. Путь - список имен элементов.
        @param Item_: Элемент дерева.
        @param Path_: Текущий заполненный путь.
        """
        parent=self.GetItemParent(Item_)
        #Если есть родительский элемент, то вызвать рекурсивно
        if parent:
            if Path_ is None:
                Path_=[]
            Path_.insert(-1,self.GetItemText(Item_))
            return self.getItemPath(parent,Path_)
        return Path_        
        
    def reFresh(self):
        """ Обновление дерева."""
        return self.LoadTree(self.GetPyData(self.root)[1])
    
    def getItemChildren(self,Item_=None):
        """ Список дочерних элементов узла дерева.
        @param Item_: Узел/элемент дерева. Если None, то корневой элемент.
        @return: Список дочерних элементов узла дерева 
            или None в случае ошибки.
        """
        try:
            #Определить узел
            if Item_ is None:
                Item_=self.root
                
            #Список дочерних элементов
            children=[]

            children_count=self.GetChildrenCount(Item_,False)
            for i in range(children_count):
                if i == 0:
                    child, cookie = self.GetFirstChild(Item_)
                else:
                    child, cookie = self.GetNextChild(Item_, cookie)
                if child.IsOk():
                    children.append(child)
            return children
        except:
            io_prnt.outErr(u'ОШИБКА компонента %s метода определения списка дочерних элементов'%(self.name))
            return None
        
    def findItemColumnString(self,string,curItem=None,columns=None,curColIdx=0,bILike=True):
        """ Функция ищет подстроку в массиве данных. 
        @type string: C{string}
        @param string: Строка поиска
        @type curItem: C{int}
        @param curItem: Элемент дерева, с которого начинается поиск.
        @type columns: C{list}
        @param columns: Список колонок записи каждого элемента, по которым ведется поиск.
        @type curColIdx: C{int}
        @param curColIdx: Индекс текущей колонки из списка колонок.
        @type bILike: C{bool}
        @param bILike: Признак поиска без учета регистра. Если False - то поиск ведется
        на точное соответствие.
        @return: Возвращает кортеж (номер элемента дерева, где найдена искомая строка,
        индекс номера колонки, где найдена искомая строка).
        """
        try:
            #Текущий элемент дерева
            if curItem is None:
                curItem=self.root
                
            cur_item_rec=self.getItemRecord(curItem)
            #Колонки
            if columns is None and cur_item_rec:
                columns=range(curColIdx,len(cur_item_rec))
                
            #Поискать в текущем элементе
            if columns:
                for i,col in enumerate(columns[curColIdx:]):
                    if cur_item_rec:
                        #Получить значение поля
                        if bILike:
                            #Без учета регистра?
                            value=ic_str.icUpper(unicode(cur_item_rec[col]))
                            find_str=ic_str.icUpper(string)
                            find_col_idx=i
                        else:
                            value=unicode(cur_item_rec[col])
                            find_str=string
                            find_col_idx=i
                        #Проверка на совпадение подстроки
                        if find_str in value:
                            return (curItem,find_col_idx)
                        
            #Обработка дочерних элементов
            children=self.getItemChildren(curItem)
            if children:
                for child in children:
                    result=self.findItemColumnString(string,child,columns,0,bILike)
                    if result is not None:
                        #Если нашли в дочерних элементах, то вернуть результат
                        return result

            #Ну если и в дочерних узлах не нашли, 
            #то вызвать поиск для следующего элемента
            next=self.GetNextSibling(curItem)
            if next:
                if next.IsOk():
                    result=self.findItemColumnString(string,next,columns,0,bILike)
                    if result is not None:
                        return result
            
            #Если не нашли в следующих элементах,
            #тогда поискать в следующем элементе родительского элемента
            parent_item=curItem.GetParent()
            if parent_item:
                parent_next=self.GetNextSibling(parent_item)
                if parent_next:
                    if parent_next.IsOk():
                        result=self.findItemColumnString(string,parent_next,columns,0,bILike)
                        if result is not None:
                            return result
            
            print(('FIND INTO!!!!',curItem.GetText()))
            #Все равно не нашли
            return None
        except:
            io_prnt.outErr(u'ОШИБКА компонента %s метода поиска узла по строке'%(self.name))
            return None
        
    def selectFindItemColumn(self,string,columns=None,bILike=True):
        """ Поиск и выделение пункта по строке.
        @type string: C{string}
        @param string: Строка поиска
        @type columns: C{list}
        @param columns: Список колонок записи каждого элемента, по которым ведется поиск.
        @type bILike: C{bool}
        @param bILike: Признак поиска без учета регистра. Если False - то поиск ведется
            на точное соответствие.
        @return: Возвращает номер элемента дерева, где найдена искомая строка.
        """
        cur_item=self.GetSelection()
        cur_item.Expand()

        if not cur_item.IsOk():
            cur_item=None
        find_result=self.findItemColumnString(string,curItem=cur_item,
            columns=columns,curColIdx=self._last_find_col_idx,bILike=bILike)
        #print 'DEBUG:',find_result,string,self._last_find_col_idx

        if find_result is not None:
            item,find_col_idx=find_result
            self._last_find_col_idx=find_col_idx+1
            self.SelectItem(item)
        else:
            if ic_dlg.icAskDlg(u'ПОИСК',u'Строка <%s> не найдена. Начать поиск сначала?'%(string))==wx.YES:
                #Начать поиск сначала
                find_result=self.findItemColumnString(string,None,columns,0,bILike)
                if find_result is not None:
                    item,find_col_idx=find_result
                    self._last_find_col_idx=find_col_idx+1
                    self.SelectItem(item)
        return None
        
    def findItemString(self,string,curItem=None,bILike=True):
        """ Функция ищет подстроку в массиве данных. Поиск производится по
        надписям элементов.
        @type string: C{string}
        @param string: Строка поиска
        @type curItem: C{int}
        @param curItem: Элемент дерева, с которого начинается поиск.
        @type bILike: C{bool}
        @param bILike: Признак поиска без учета регистра. Если False - то поиск ведется
        на точное соответствие.
        @return: Возвращает кортеж (номер элемента дерева, где найдена искомая строка,
        индекс номера колонки, где найдена искомая строка).
        """
        try:
            #Текущий элемент дерева
            if curItem is None:
                curItem=self.root

            label=curItem.GetText()
            #Поискать в текущем элементе
            if label:
                #Получить значение
                if bILike:
                    #Без учета регистра?
                    value=ic_str.icUpper(label)
                    find_str=ic_str.icUpper(string)
                else:
                    value=label
                    find_str=string
                #Проверка на совпадение подстроки
                if find_str in value:
                    return curItem
                        
            #Обработка дочерних элементов
            children=self.getItemChildren(curItem)
            if children:
                for child in children:
                    result=self.findItemString(string,child,bILike)
                    if result is not None:
                        #Если нашли в дочерних элементах, то вернуть результат
                        return result

            #Ну если и в дочерних узлах не нашли, 
            #то вызвать поиск для следующего элемента
            next=self.GetNextSibling(curItem)
            #print 'NEXT',next
            if next and next.IsOk():
                result=self.findItemString(string,next,bILike)
                if result is not None:
                    return result
            
            #Если не нашли в следующих элементах,
            #тогда поискать в следующем элементе родительского элемента
            parent_item=curItem.GetParent()
            if parent_item and parent_item.IsOk():
                parent_next=self.GetNextSibling(parent_item)
                if parent_next and parent_next.IsOk():
                    result=self.findItemString(string,parent_next,bILike)
                    if result is not None:
                        return result
            
            #Все равно не нашли
            return None
        except:
            io_prnt.outErr(u'ОШИБКА компонента %s метода поиска узла по строке'%(self.name))
            return None
        
    def _getNextItem4Find(self,Item_):
        """
        Получить следующий элемент для поиска.
        """
        if Item_.HasChildren():
            return Item_.GetChildren()[0]
        next_item=self.GetNextSibling(Item_)
        if next_item and next_item.IsOk():
            return next_item
        parent_item=Item_.GetParent()
        if parent_item:
            parent_next=self.GetNextSibling(parent_item)
            if parent_next and parent_next.IsOk():
                return parent_next
        return None
        
    def selectFindItem(self,string,bILike=True):
        """ Поиск и выделение пункта по строке. Поиск производится по
        надписям элементов.
        @type string: C{string}
        @param string: Строка поиска
        @type bILike: C{bool}
        @param bILike: Признак поиска без учета регистра. Если False - то поиск ведется
            на точное соответствие.
        @return: Возвращает номер элемента дерева, где найдена искомая строка.
        """
        cur_item=self.GetSelection()

        if not cur_item.IsOk():
            cur_item=None
        else:
            #Начинать поиск со следующего элемента
            cur_item=self._getNextItem4Find(cur_item)
        find_item=self.findItemString(string,curItem=cur_item,bILike=bILike)

        if find_item is not None:
            self.SelectItem(find_item)
        else:
            if ic_dlg.icAskDlg(u'ПОИСК',u'Строка <%s> не найдена. Начать поиск сначала?'%(string))==wx.YES:
                #Начать поиск сначала
                find_item=self.findItemString(string,None,bILike)
                if find_item is not None:
                    self.SelectItem(find_item)
        return None
        
    def isRootSelected(self):
        """ Определить является ли корень выделенным."""
        return self.IsSelected(self.GetRootItem())
        
    #--- Обработчики событий ---
    def OnItemExpanded(self, event):
        """ Разворачивание узла."""
        pass
    
    def OnItemCollapsed(self, event):
        """ Сворачивание узла."""
        pass
        
    def OnSelectChanged(self, event):
        """ Изменение выделенного узла."""
        select_item=event.GetItem()
        self._last_selection=None
        if select_item:
            self._last_selection=self.getItemPath(select_item)
            
        #--- НАЧАЛО: БЛОК ИСПРАВЛЕНИЯ БАГИ ПОЯВЛЕНИЯ ВТОРОГО КУРСОРА В ДЕРЕВЕ ---
        if not self.HasFlag(wx.TR_MULTIPLE):
            selections=self.GetSelections()
            if len(selections)>1:
                for selection in selections:
                    if selection<>select_item:
                        selection.SetHilight(0)
                        self._main_win.RefreshLine(selection)
        #--- КОНЕЦ: БЛОК ИСПРАВЛЕНИЯ БАГИ ПОЯВЛЕНИЯ ВТОРОГО КУРСОРА В ДЕРЕВЕ ---
        
    def OnItemActivated(self, event):
        """ Активизация узла."""
        pass
        
    def OnItemChecked(self, event):
        """ Выбор узла."""
        item=event.GetItem()
        self.checkItemChildren(item,self.IsItemChecked(item))
        event.Skip()
        
    def OnTreeListKeyDown(self,event):
        """ Нажатие клавиши на дереве.
        ВНИМАНИЕ!!!
        Обработчик нажатия клавиши на дереве цепляется через
        wx.EVT_TREE_KEY_DOWN, а не wx.EVT_KEY_DOWN, как у других компонентов.
        """
        pass
        
    def HideHeader(self):
        self._headerHeight = 0
        self.DoHeaderLayout()
    
    def SetCheckRadio(self, selection=0):
        """ Устанавливаем тип checkbox/radiobox картинок."""
        if selection == 0:
            self.SetImageListCheck(13, 13)
        else:
            import newstyle_img
            il = wx.ImageList(16, 16)
            il.Add(newstyle_img.check_on)
            il.Add(newstyle_img.check_off)
            il.Add(newstyle_img.radio_on)
            il.Add(newstyle_img.radio_off)
            self.SetImageListCheck(16, 16, il)        
        
    def _testTree(self):
        """
        """
        print('TEST SIMPLE TREE LIST CTRL')
        for x in range(5):
            txt = 'Item %d' % x
            child = self.AppendItem(self.root, txt)
            self.SetItemText(child, txt + '(c1)')
            self.SetItemImage(child, self.fldridx, which = wx.TreeItemIcon_Normal)
            self.SetItemImage(child, self.fldropenidx, which = wx.TreeItemIcon_Expanded)
    
    def load_data(self, func, *arg, **kwarg):
        self.begin_load()
        self.tree = func(*arg, **kwarg)
    
    def view_data(self, *arg, **kwarg):
        self.LoadTree(self.tree)

    def getItemCheckList(self,Item_=None):
        """
        Получить список выбранных элементов дерева.
        """
        if Item_ is None:
            Item_=self.GetRootItem()

        check_list=[]
        
        if Item_.HasChildren():
            for child in Item_.GetChildren():
                #child_check=self.getItemCheckList(child)
                check_data={
                    'name':self.GetItemText(child),
                    '__record__':self.getItemRecord(child),
                    'check':self.IsItemChecked(child),
                     }
                if child.HasChildren():
                    check_data['children']=self.getItemCheckList(child)
                check_list.append(check_data)                
        else:
            check_data={
                'name':self.GetItemText(Item_),
                '__record__':self.getItemRecord(child),
                'check':self.IsItemChecked(Item_),
                     }
            return check_data
        
        return check_list        
    
    def checkItemChildren(self,Item_=None,Check_=True):
        """
        Отметить все дочерние элементы.
        @param Item_: Указанный элемент дерева.
        @param Check_: True - установить отметку, False - убрать отметку.
        """
        if Item_ is None:
            Item_=self.GetRootItem()
            
        if Item_.HasChildren():
            for child in Item_.GetChildren():
                self.CheckItem(child,Check_)
                self.checkItemChildren(child,Check_)        
        
    def LoadData(self, func=None, *arg, **kwarg):
        """ Функция загрузки данных.
        @param func: Функция загрузки данных, которая должна вернуть словарно-
            списковую структуру, описывающую дерево. 
        """
        import delayedres
        pr = delayedres.DelayedFunction(self.load_data, self.view_data, func, *arg, **kwarg)
        pr.start()
    
    def LoadData2(self, func=None, view_func=None, *arg, **kwarg):
        """ Функция загрузки данных.
        @param func: Функция загрузки данных, которая должна вернуть словарно-
            списковую структуру, описывающую дерево. 
        """
        import delayedres
        pr = delayedres.DelayedFunction(self.load_data, view_func or self.view_data, func, *arg, **kwarg)
        pr.start()
    
    #   Обработчики событий

def __load_data(tree=None):
    res0 = { 'd1':{'__record__':[1,2,3,4]},
            'd2':{'cc1':'a1','cc2':'a2','__record__':[1,2,3,4]},
            'd3':{'ee1':'a1','ee2':'a2','__record__':[1,2,3,4]},
            '__record__':[1,2,3,4],
            }
     
    res1 = {'name':'A2',
            'children':[],
            '__record__':['1',2,3,4],
            }

    res2 = {'name':'A3',
            'children':[],
            '__record__':['1',2,3,4],
            }
    res3 = {'name':'A4',
            'children':[res1,res2],
            '__type__':1,
            '__record__':[u'Дополнительный код',2,3,4],
            }
     
    res = [{'name':'A1',
            'children':[res1,res2,res3],
            '__record__':[1,2,3,4],
            }]

#    tree.tree = res
    return res

def __view_data(obj):
    obj.LoadTree(obj.tree)
    
def test(par=0):
    """ Тестируем пользовательский класс.
    @type par: C{int}
    @param par: Тип консоли.
    """
    app=wx.PySimpleApp()
    
    frame = wx.Frame(None, -1, 'Test')
    win = wx.Panel(frame, -1)
    tree = icSmartTreeListCtrl(win, -1, position=(10,10),size=(200,300),
                    style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_BUTTONS,
                    labels=[u'col1','col2',u'Колонка 3'])
    tree.LoadData(__load_data)
    
    
    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    """
    Тестируем пользовательский класс.
    """
    test()