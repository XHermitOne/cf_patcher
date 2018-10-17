# !/usr/bin/env python
#  -*- coding: utf-8 -*-
""" 
Функции-комманды управления процессом изменения конфигурации.
"""

#--- Imports ---
import os,os.path
import sys
import shutil

import wx

from utils import log
from utils import dlg

import config

#
DEFAULT_V8UNPACK_PATH='/V8Unpack20/bin/V8Unpack.exe'

CUR_CF_DIR=None

def gen_cf_dir(CFFileName_):
    """
    Генерация директории, в которую будет происходить парсинг.
    @param CFFileName_: Полное имя CF файла конфигурации 1c.
    """
    return os.path.normpath(os.path.dirname(CFFileName_)+'/'+os.path.basename(CFFileName_).replace('.','_'))

def parse_cf_file(CFFileName_,CFDir_=None):
    """
    Парсинг файла конфигурации 1с.
    @param CFFileName_: Полное имя CF файла конфигурации 1c.
    @param CFDir_: Директория, в которую будет происходить парсинг.
    """
    try:
        if not os.path.exists(CFFileName_):
            log.log_to_file('ERROR! CF file %s not exists!'%CFFileName_)
            dlg.MsgBox(u'ERROR!',u'CF file %s not exists!'%CFFileName_)
            return
        else:
            if CFDir_ is None:
                global CUR_CF_DIR
                #CUR_CF_DIR=os.path.dirname(CFFileName_)
                CUR_CF_DIR=gen_cf_dir(CFFileName_)
                CFDir_=CUR_CF_DIR            

        if os.path.exists(CFDir_):
            #Удалить папку конфигурации, если она существует
            #os.remove(CFDir_)
            print(('DELETE DIRECTORY:',CFDir_))
            shutil.rmtree(CFDir_,True)
            log.log_to_file('DELETE DIRECTORY: '+CFDir_)
                
        v8unpack_filename=os.path.dirname(os.path.dirname(__file__))+DEFAULT_V8UNPACK_PATH
        v8unpack_filename=os.path.abspath(v8unpack_filename)
        if not os.path.exists(v8unpack_filename):
            log.log_to_file('ERROR! V8Unpack.exe file(%s) not exists!'%v8unpack_filename)
            dlg.MsgBox(u'ERROR!',u'V8Unpack.exe file(%s) not exists!'%v8unpack_filename)
            return
        cmd='%s -PARSE "%s" "%s"'%(v8unpack_filename,CFFileName_,CFDir_)
            
        if wx.Platform=='__WXGTK__':
            cmd='wine '+cmd
            
        print(('RUN COMMAND:',cmd))
        log.log_to_file('RUN COMMAND: '+cmd)
        log.log_cmd(cmd)
    except:
        print('ERROR! Error in parse_cf_file function')
        raise       

def patch_cf_dir(CFDir_=None,CFPatcher_=None,Metaobjects_=None,Scripts_=None,Root_=None):
    """
    Пропатчить конфигурацию.
    @param CFDir_: Директория конфигурации 1с.
    """
    if CFDir_ is None:
        global CUR_CF_DIR
        CFDir_=CUR_CF_DIR
        
    patcher=CFPatcher_
    if patcher is None:
        import iccfpatcher
        patcher=iccfpatcher.icCFPatcher()
        
    import iccfanalyzer
    analyzer=iccfanalyzer.icCFAnalyzer()
    cf_obj_lst=analyzer.createCFList(CFDir_)
   
    metaobjects=Metaobjects_
    if metaobjects is None:
        #metaobjects=[]
        metaobjects=analyzer.getMetaobjects(cf_obj_lst)
        
    scripts=Scripts_
    if scripts is None:
        scripts=[]

    root=Root_
    if root is None:
        root=analyzer.getRootMetaobject()

    if config.DEBUG_MODE:
        log.log_to_file('''Patch run:
    CF DIRECTORY: %s
    SCRIPTS: %s
    ROOT: %s'''%(CFDir_,scripts,root))
        
    #return patcher.patch(CFDir_,metaobjects,scripts,root)
    return patcher.patch(CFDir_,None,scripts,root)
    
def build_cf_file(CFFileName_,CFDir_=None):
    """
    Построить CF файл конфигурации 1с.
    @param CFFileName_: Полное имя CF файла конфигурации 1c.
    @param CFDir_: Директория из которой будет происходить сборка.
    """
    if CFDir_ is None:
        global CUR_CF_DIR
        CFDir_=CUR_CF_DIR
        
    try:
        if not os.path.exists(CFDir_):
            log.log_to_file('ERROR! Directory %s not exists!'%CFDir_)
            dlg.MsgBox(u'ERROR!',u'Directory %s not exists!'%CFDir_)
            return
        
        if os.path.exists(CFFileName_):
            print(('DELETE CF FILE:',CFFileName_))
            os.remove(CFFileName_)
            log.log_to_file('DELETE CF FILE: '+CFFileName_)
                
        v8unpack_filename=os.path.dirname(os.path.dirname(__file__))+DEFAULT_V8UNPACK_PATH
        v8unpack_filename=os.path.abspath(v8unpack_filename)
        if not os.path.exists(v8unpack_filename):
            log.log_to_file('ERROR! V8Unpack.exe file(%s) not exists!'%v8unpack_filename)
            dlg.MsgBox(u'ERROR!',u'V8Unpack.exe file(%s) not exists!'%v8unpack_filename)
            return
        cmd='%s -BUILD "%s" "%s"'%(v8unpack_filename,CFDir_,CFFileName_)

        if wx.Platform=='__WXGTK__':
            cmd='wine '+cmd
                
        print(('RUN COMMAND:',cmd))
        log.log_to_file('RUN COMMAND: '+cmd)
        log.log_cmd(cmd)
    except:
        print('ERROR! Error in build_cf_file function')
        raise        


def do_patch(cf_file,scripts,result_cf_file):
    """
    Процедура комплексного выполнения патча.
    """             
    #Распарсить
    parse_cf_file(cf_file)
    #Пропатчить
    patch_cf_dir(Scripts_=scripts)
    #И собрать
    build_cf_file(CFFileName_=result_cf_file)

    return True
