# !/usr/bin/env python
#  -*- coding: utf-8 -*-
""" 
Патчер для конфигурации 1с.
"""
import about
__version__ =about.__version__
__date__=about.__date__

#--- Imports ---
import os,os.path
import copy

import wx
import wx.wizard

#import util

#import icUninstallManager

#--- Classes ---
class icCFWizard(wx.wizard.Wizard):
    """
    Визард патчера конфигурации 1с.
    """
    def __init__(self,CFFileName_=None):
        """
        Конструктор.
        @param CFFileName_: Полное имя CF файла конфигурации.
        """
        if __file__:
            dirname=os.path.dirname(__file__)
            if dirname:
                path=os.path.dirname(__file__)
            else:
                path=os.getcwd()
        else:
            path=os.getcwd()
        img_file_name=path+'/img/1c_wiz.png'
        #print '>>>',os.getcwd(),__file__,img_file_name
        self.wizard_img=wx.Image(img_file_name,wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        
        title=u'Изменение конфигурации 1с: '
        if title:
            title+=' '+CFFileName_
        wx.wizard.Wizard.__init__(self,None,-1,title,self.wizard_img)
        #self.SetSize(wx.Size(700,500))       
        
        #Список порядка следования страниц
        self.page_order=[]
        
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED,self.on_changed)
        self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING,self.on_changing)
        
        #Внутренне окружение визарда инсталяции
        self.environment={}
        self._init_env(cf_filename=CFFileName_)
        
    def getPage(self,Idx_):
        """
        Получить страницу по индексу.
        """
        return self.page_order[Idx_]
        
    def getFinishPage(self):
        """
        Последняя финишная страница.
        """
        return self.getPage(-1)
        
    def appendPage(self,Page_):
        """
        Установка следующей страницы.
        """
        if Page_:
            if self.page_order:
                #Установить связи между страницами
                Page_.SetPrev(self.page_order[-1])
                self.page_order[-1].SetNext(Page_)
            self.page_order.append(Page_)

    def getNextPage(self,Page_):
        """
        Получить следующую страницу за указанной.
        """
        if Page_:
            if self.page_order:
                i=self.page_order.index(Page_)
                if i<len(self.page_order)-1:
                    return self.page_order[i+1]
                else:
                    return None
                
    def on_changed(self,event):
        """
        Обработчик смены страницы инсталляции.
        Это обработчик срабатывает перед 
        появлением страницы на экране. См. демку.
        """
        page=event.GetPage()
        if hasattr(page,'on_changed'):
            return page.on_changed(event)
        event.Skip()

    def on_changing(self,event):
        """
        Обработчик смены страницы инсталляции.
        Это обработчик срабатывает после 
        нажатия на кнопку Next.
        """
        page=event.GetPage()
        if hasattr(page,'on_changing'):
            return page.on_changing(event)
        event.Skip()
        
    def runFirstPage(self):
        """
        Запуск первой страницы.
        """
        if self.page_order:
            first_page=self.page_order[0]
            if first_page:
                self.RunWizard(first_page)
                
    def _init_env(self,**kwargs):
        """
        Инициализация внутреннего окружения визарда.
        """
        import iccfanalyzer
        import iccfpatcher
        
        self.environment=copy.deepcopy(kwargs)
        
        #self.environment['cf_filename']=os.path.dirname(os.getcwd())+'/tst_doc.cf'
        #self.environment['cf_dir']=os.path.dirname(os.getcwd())+'/tst_doc'
        self.environment['cf_analyzer']=iccfanalyzer.icCFAnalyzer()
        self.environment['cf_patcher']=iccfpatcher.icCFPatcher()
        
    def getCFAnalyzer(self):
        """
        Объект анализатора конфигурации.
        """
        return self.environment['cf_analyzer']
                
def run(*args,**kwargs):
    """
    Основная функция запуска визарда.
    @param InstallScript_: Функция инсталляционного скрипта.
    В качестве аргумента функция должна принимать объект визарда.
    """
    import icWizardPages
    
    app=wx.PySimpleApp()
    wizard=icCFWizard(u'Версия %s от %s'%('.'.join([str(i) for i in __version__]),__date__))
    #print 'WIZARD:',dir(wizard)
    
    page1=icWizardPages.icCFParsePage(wizard,u'''Парсинг 
конфигурации 1с''')
    wizard.appendPage(page1)
    #print 'WIZARD PAGE:',dir(page1)

    page2=icWizardPages.icCFChoicePage(wizard,u'''Выбор объектов 
конфигурации''')
    wizard.appendPage(page2)
    #page2.createPages()

    page3=icWizardPages.icCFScriptPage(wizard,
        u'''Выбор сценариев 
изменения 
конфигурации''')
    wizard.appendPage(page3)

    page4=icWizardPages.icCFPatchPage(wizard,
        u'''Запуск изменений 1с 
конфигурации по 
заданным сценариям''')
    wizard.appendPage(page4)
    
    page5=icWizardPages.icCFBuildPage(wizard,
        u'''Построение CF файла 
конфигурации 1с''')
    wizard.appendPage(page5)
    
    page_end=icWizardPages.icCFEndPage(wizard,u'Окончание',
        u'''Изменение конфигурации 
1с успешно завершено''')
    wizard.appendPage(page_end)

    wizard.FitToPage(page1)
    
    wizard.RunWizard(page1)
    
def test():
    """
    Функция тестирования визарда инсталятора.
    """
    run()
        
if __name__=='__main__':
    test()