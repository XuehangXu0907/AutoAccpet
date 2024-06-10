@echo off
REM Remove the shortcut from the Startup folder
set SHORTCUT_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\autoAccept.lnk

if exist "%SHORTCUT_PATH%" (
    del "%SHORTCUT_PATH%"
    echo Startup shortcut removed successfully.
) else (
    echo No startup shortcut found.
)
pause
