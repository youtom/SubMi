@echo off
REM runas administrator
REM -l is for language in ISO three charactar format
REM replace USERNAME and PASSWORD with your OpenSubtitles credentials
REM for example hebrew installation commandline
REM %~dp0bin\FindSubs.exe -u USERNAME -p PASSWORD -i -l heb
%~dp0bin\FindSubs.exe -u USERNAME -p PASSWORD -i
exit