@echo off
c:\python25\python.exe C:\Python25\Lib\site-packages\asciidoc\asciidoc.py -a icons -a iconsdir="./images/icons" cf_patcher.txt
start cf_patcher.html
