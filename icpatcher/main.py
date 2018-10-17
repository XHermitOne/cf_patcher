# !/usr/bin/env python
#  -*- coding: utf-8 -*-
""" 
Основная запускаемая функция.
"""

import sys
import os,os.path

import icWizard

def main():
    """
    Основная запускаемая функция.
    """
    argv=sys.argv[1:]
    
    pkg_path=os.path.dirname(icWizard.__file__)
    print(('ADD PACKAGE PATH:',pkg_path))
    sys.path.append(pkg_path)

    if '--wizard' in argv:
        return main_wizard(*argv)
    elif '--form' in argv:
        return main_form(*argv)
    else:
        return main_console(*argv)
    
def main_wizard(*args,**kwargs):
    """
    Запуск визарда.
    """
    return icWizard.run(*args,**kwargs)

def main_console(*args,**kwargs):
    """
    Запуск консольного варианта исполнения патчера.
    """
    if '--help' in args:
        print(__doc__)
        return
    
    elif '--cf_file' in args:
        cf_file=args[args.index('--cf_file')]
    elif '--scripts' in args:
        scripts=args[args.index('--scripts')].split(',')        
    elif '--out' in args:
        result_cf_file=args[args.index('--out')]
    
    import patch_cmd
    
    return patch_cmd.do_patch(cf_file,scripts,result_cf_file)
    
def main_form(*args,**kwargs):
    """
    Запуск варианта исполнения патчера с одной формой.
    """
    import iccfpatcherform
    return iccfpatcherform.run()
    
if __name__=='__main__':
    main()