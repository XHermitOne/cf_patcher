#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""


"""

import wx

#--- Диалоговые функции прогресс бара ---
class icProgressDlg(wx.ProgressDialog):
    """
    Класс диалогового окна прогресс бара.
    """

    def __init__(self,Win_=None,Title_='',Msg_='',Min_=0,Max_=100,Style_=wx.PD_CAN_ABORT):
        """
        Конструктор. Создает и открывает прогресс бар.
        @param Win_: Ссылка на окно.
        @param Title_: Заголовок диалогового окна.
        @param Msg_: Текст диалога.
        @param Min_: Минимальное значение.
        @param Max_: Максимальное занчение.
        @param Style_: Стиль диалога.
        @return: Объект диалога.
        """
        self.cur_value=0

        #--- Атрибуты класса ---
        self._ProgressFrame=Win_ #Фрейм прогресс бара
        #self._MyFrame=False
        if self._ProgressFrame is None:
            #self._ProgressFrame=wx.Frame(None, -1, '')
            #self._MyFrame=True
            self._ProgressFrame=wx.GetApp().GetTopWindow()

        self._ProgressMIN=Min_ #Минимальное значение
        self._ProgressMAX=Max_ #Максимальное значение
        if self._ProgressMIN>self._ProgressMAX:
            tmp_value=self._ProgressMAX
            self._ProgressMAX=self._ProgressMIN
            self._ProgressMIN=tmp_value
        try:
            #Вызов конструктор а предка
            wx.ProgressDialog.__init__(self,Title_,Msg_, \
                self._ProgressMAX-self._ProgressMIN, \
                self._ProgressFrame,Style_|wx.PD_APP_MODAL)

            #Образмерить и отцентровать диалоговое окно
            self.SetSize(wx.Size(500,130))
            self.CenterOnScreen()
        except:
            print(u'ERROR: Ошибка создания диалогового окна прогресс бара.')
            raise

    def UpdateDlg(self,Value_=-1,NewMsg_=u''):
        """
        Обновить данные програсс бара.
        @param Value_: Значение.
        @param NewMsg_: Текст диалога.
        """
        try:
            self.cur_value=Value_

            #Ограничение значения
            value=self.cur_value%(self._ProgressMAX-self._ProgressMIN)
            value=max(min(value,self._ProgressMAX),self._ProgressMIN)
            #return self.Update(Value_-self._ProgressMIN,NewMsg_)
            return self.Update(value,NewMsg_)
        except:
            print(u'ERROR: Ошибка обновления диалогового окна прогресс бара.')
            raise

    def IncDlg(self,NewMsg_=u''):
        """
        Увеличить значение прогресс бара на 1.
        @param NewMsg_: Текст диалога.
        """
        return self.UpdateDlg(self.cur_value+1,NewMsg_)

    def DecDlg(self,NewMsg_=u''):
        """
        Уменьшить значение прогресс бара на 1.
        @param NewMsg_: Текст диалога.
        """
        return self.UpdateDlg(self.cur_value-1,NewMsg_)

    def CloseDlg(self):
        """
        Закрыть прогресс бар.
        """
        self.Close()
        #Если фрейм диалогового окна создавался, то удалить его
        #if self._MyFrame==True:
        #    self._ProgressFrame.Close()
        #    self._ProgressFrame.Destroy()
        #    self._ProgressFrame=None

#--- Функции пользователя для прогресс бара (без знаний класса) ---
_PROGRESS_DLG=None #Сам диалог прогресс бара

def openProgressDlg(Title_='',Msg_='',Min_=0,Max_=100,
    Style_=wx.PD_AUTO_HIDE,Win_=None):
    """
    Создает и открывает прогресс бар.
    @param Title_: Заголовок диалогового окна.
    @param Msg_: Текст диалога.
    @param Min_: Минимальное значение.
    @param Max_: Максимальное занчение.
    @param Style_: Стиль диалога.
    @param Win_: Ссылка на окно.
    @return: Объект диалога.
    """
    try:
        global _PROGRESS_DLG
        if _PROGRESS_DLG:
            closeProgressDlg()
        _PROGRESS_DLG=icProgressDlg(Win_,Title_,Msg_,Min_,Max_,Style_)
    except:
        print(u'ERROR: Ошибка открытия прогресс бара')
        _PROGRESS_DLG=None
    return _PROGRESS_DLG

def updateProgressDlg(Value_=-1,NewMsg_=u''):
    """
    Обновить данные програсс бара.
    @param Value_: Значение.
    @param NewMsg_: Текст диалога.
    @return: Возвращает результат выполнения операции True/False.
    """
    try:
        global _PROGRESS_DLG
        if _PROGRESS_DLG is not None:
            _PROGRESS_DLG.UpdateDlg(Value_,NewMsg_)
            return True
        return False
    except:
        print(u'ERROR: Ошибка обновления прогресс бара')
        return False

def incProgressDlg(NewMsg_=u''):
    """
    Увеличить данные програсс бара на 1.
    @param NewMsg_: Текст диалога.
    @return: Возвращает результат выполнения операции True/False.
    """
    try:
        global _PROGRESS_DLG
        if _PROGRESS_DLG is not None:
            _PROGRESS_DLG.IncDlg(NewMsg_)
            return True
        return False
    except:
        print(u'ERROR: Ошибка увеличения прогресс бара')
        return False

def decProgressDlg(NewMsg_=u''):
    """
    Уменьшить данные програсс бара на 1.
    @param NewMsg_: Текст диалога.
    @return: Возвращает результат выполнения операции True/False.
    """
    try:
        global _PROGRESS_DLG
        if _PROGRESS_DLG is not None:
            _PROGRESS_DLG.DecDlg(NewMsg_)
            return True
        return False
    except:
        print(u'ERROR: Ошибка уменьшения прогресс бара')
        return False

def closeProgressDlg():
    """
    Закрыть прогресс бар.
    """
    try:
        global _PROGRESS_DLG
        if _PROGRESS_DLG is not None:
            #_PROGRESS_DLG.CloseDlg()
            #_PROGRESS_DLG.Close()
            _PROGRESS_DLG.Destroy()
            _PROGRESS_DLG=None
            return True
        else:
            print(u'WARNING! _PROGRESS_DLG is None')
        return False
    except:
        print(u'ERROR: Ошибка закрытия прогресс бара')
        return False

def test_progress():
    """
    """
    import time   
    openProgressDlg(u'Тест прогресс диалога',u'Значение',0,200)

    for i in range(200):
        updateProgressDlg(i,u'Значение: %d'%i)
        time.sleep(0.1)

    closeProgressDlg()

def test_inc():
    """
    """
    import time   
    openProgressDlg(u'Тест прогресс диалога',u'Значение',0,100)

    for i in range(200):
        incProgressDlg(u'Значение: %d'%i)
        time.sleep(0.1)

    closeProgressDlg()

def test_dec():
    """
    """
    import time   
    openProgressDlg(u'Тест прогресс диалога',u'Значение',0,100)

    for i in range(200):
        decProgressDlg(u'Значение: %d'%i)
        time.sleep(0.1)

    closeProgressDlg()

def test():
    """
    """
    app=wx.PySimpleApp()
    frm=wx.Frame(None)
    
    test_progress()
    test_inc()
    test_dec()

    #frm.Close()


if __name__=='__main__':
    test()

