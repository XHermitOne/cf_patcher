# !/usr/bin/env python
#  -*- coding: utf-8 -*-
""" 
Функции работы с файлами.
"""

import os,os.path
import util

def createTxtFile(FileName_,Txt_=None):
    """
    Создать текстовый файл.
    @param FileName_: Имя создаваемого файла.
    @param Txt_: Текст по умолчанию записываемый в файл.
    @return: True/False.
    """
    Txt_=util.encodeText(Txt_)
    f=None
    try:
        if os.path.exists(FileName_):
            os.remove(FileName_)
        f=open(FileName_,'w')
        if Txt_:
            f.write(Txt_)
        f.close()
        return True
    except:
        if f:
            f.close()
        f=None
        raise
    return False