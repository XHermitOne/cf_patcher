#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Logging functions.
"""
import os
import time

DEFAULT_LOG_FILENAME='./log.txt'
DEFAULT_LOG_DATETIME_FMT='%Y.%m.%d %H:%M:%S'

def log_to_file(txt,filename=DEFAULT_LOG_FILENAME,datetime_fmt=DEFAULT_LOG_DATETIME_FMT):
    """
    Log text to file.
    """
    f=None
    try:
        f=open(filename,'a')
        now_time=time.strftime(datetime_fmt,time.localtime(time.time()))
        now_time+=':\n'
        f.write(now_time)

        if type(txt)==type(u''):
            import sys
            txt=txt.encode(sys.getfilesystemencoding())

        f.write(txt)
        f.write('\n')
        f.close()
    except:
        if f:
            f.close()
            f=None
        raise
        
def log_cmd(cmd,txt_ctrl=None):
    """
    Run and logging command result.
    @param cmd: Command.
    @param txt_ctrl: wxTextCtrl object for logging.
    """
    try:
        if type(cmd)==type(u''):
            import sys
            cmd=cmd.encode(sys.getfilesystemencoding())
        result=os.popen3(cmd)
        if txt_ctrl:
            log_to_ctrl(txt_ctrl,result)
        else:
            log_to_file(cmd2Txt(result))
    except:
        print(('ERROR! Run command:',cmd))
        raise

def cmd2Txt(cmd):
    """
    Convert popen result to text.
    """
    result=''
    if cmd:
        if type(cmd)<>type(()):
            #Обработка результат popen
            txt=cmd.readline().strip()
            while txt:
                result+=txt+'\n'
                txt=cmd.readline().strip()                
        elif type(cmd)==type(()) and len(cmd)==3:
            #Обработка результат popen3
            out=cmd[1].readline() #.strip()
            err=cmd[2].readline() #.strip()                

            while out or err:
                if out:
                    result+=out+'\n'
                if err:
                    start=len(result)
                    result+=err+'\n'
                        
                out=cmd[1].readline() #.strip()
                err=cmd[2].readline() #.strip()                
    return result

def log_to_ctrl(txt_ctrl,cmd=None):
    """
    Logging cmd to TextCtrl.
    @param txt_ctrl: wxTextCtrl object for logging.
    @param cmd: Command.
    """
    if cmd:
        if type(cmd)<>type(()):
            #Обработка результат popen
            txt=cmd.readline().strip()
            while txt:
                txt_ctrl.AppendText(txt)
                txt=cmd.readline().strip()                
        elif type(cmd)==type(()) and len(cmd)==3:
            #Обработка результат popen3
            out=cmd[1].readline() #.strip()
            err=cmd[2].readline() #.strip()                

            while out or err:
                if out:
                    txt_ctrl.AppendText(out)
                if err:
                    start=len(txt_ctrl.GetValue())
                    txt_ctrl.AppendText(err)
                    #Закрасить в красный цвет ошибки
                    end=len(txt_ctrl.GetValue())
                    txt_ctrl.SetStyle(start,end,wx.TextAttr('RED',wx.NullColour))
                        
                out=cmd[1].readline() #.strip()
                err=cmd[2].readline() #.strip()                

