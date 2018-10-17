#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Список образов, ориентированный на образы комопнентов.
"""

__version__=(0,0,0,1)

import wx

class icImgList:
    """
    Список образов, ориентированный на образы комопнентов.
    """
    def __init__(self,Parent_,ImgWidth_,ImgHeight_):
        """ Конструктор."""
        self._Parent=Parent_
        # Вызов консктруктора предка
        self._img_lst=wx.ImageList(ImgWidth_,ImgHeight_)
        # Используемые образы компонентов
        self._ImgIdx={}
        # Используемые образы компонентов
        self._ImgExtendedIdx={}
       
        #self.Add(wx.NullBitmap)

    def getImageList(self):
        return self._img_lst

    def setImgIdx(self,ID_,Img_,ImgExt_=None):
        """ Установить компонент для редактирования.
        @param ID_: Идентификатор объекта асоциированного с образом.
        """
        # Если тип компонента не зарегистрирован, то зарегистрировать его
        if ID_ not in self._ImgIdx:
            # Образ типа компонента
            self._ImgIdx[ID_]=self.setImg(Img_)
            if ImgExt_:
                self._ImgExtendedIdx[ID_]=self.setImg(ImgExt_)
            else:
                self._ImgExtendedIdx[ID_]=-1
        
        #print 'IMG LIST DBG:::',ID_,Img_,ImgExt_
        return (self._ImgIdx[ID_],self._ImgExtendedIdx[ID_])

    def getImgIdx(self,ID_):
        """ Получить данные о компоненте для редактирования.
        @param ID_: Идентификатор объекта асоциированного с образом.
        """
        if ID_ in self._ImgIdx:
            return self._ImgIdx[ID_]
        return -1

    def getImgExtendedIdx(self,ID_):
        """ Получить данные о компоненте для редактирования.
        @param ID_: Идентификатор объекта асоциированного с образом.
        """
        if ID_ in self._ImgExtendedIdx:
            return self._ImgExtendedIdx[ID_]
        return -1

    def getImgIdxTuple(self,ID_):
        """
        Получить сразу два идентификатора в виде кортежа.
        @param ID_: Идентификатор объекта асоциированного с образом.
        """
        return (self.getImgIdx(ID_),self.getImgExtendedIdx(ID_))
    
    def setImg(self,Img_,ImgIdx_=-1):
        """ Добавить картинку компонента в список образов.
        @param Img_: Имя файла образа компонента или сам образ.
        @param ImgIdx_: Указание на какое место поместить картинку.
        @return: Возвращает индекс соответствующий этому образу.
        """
        # Заменять картинку в списке не надо
        if ImgIdx_<0:
            # Добавить в список образ
            if type(Img_)==type(''):
                # Указание файла
                return self._img_lst.Add(hydra.img.NodeImg(Img_))
            elif issubclass(Img_.__class__,wx.Bitmap):
                # Указание непосредственно картинки
                return self._img_lst.Add(Img_)
        # Надо заменить картинку на ImgIdx_
        else:
            # Заменить в списке образ
            if type(Img_)==type(''):
                # Указание файла
                return self.ReplaceImg(ImgIdx_,hydra.img.NodeImg(Img_))
            elif issubclass(Img_.__class__,wx.Bitmap):
                # Указание непосредственно картинки
                return self.ReplaceImg(ImgIdx_,Img_)
        return -1

    def ReplaceImg(self, ImgIdx_, Img_):
        """ Заменить образ в списке образов.
        @param ImgIdx_: Индекс заменяемого образа.
        @param Img_: Сам wx.Bitmap образ.
        @return: Функция возвращает новый индекс образа.
        """
        try:
            self._img_lst.Replace(ImgIdx_,Img_)
        except:
            print(('%s from %s %s '%(ImgIdx_,self._img_lst.GetImageCount(), Img_)))
        return ImgIdx_
