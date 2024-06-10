@echo off
REM Create a shortcut to the executable in the Startup folder
set TARGET_PATH=%~dp0autoAccept.exe
set SHORTCUT_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\autoAccept.lnk

REM Check if the shortcut already exists
if exist "%SHORTCUT_PATH%" (
    echo The startup shortcut already exists.
) else (
    REM Create the shortcut
    powershell $s=(New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath='%TARGET_PATH%'; $s.Save()
    echo Startup shortcut created successfully.
)
pause
