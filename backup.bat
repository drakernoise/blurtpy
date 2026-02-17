@echo off
setlocal enabledelayedexpansion

:: Get timestamp using wmic for locale independence
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set TIMESTAMP=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2%_%datetime:~8,2%-%datetime:~10,2%-%datetime:~12,2%

set "SOURCE=%~dp0"
:: Remove trailing slash
if "%SOURCE:~-1%"=="\" set "SOURCE=%SOURCE:~0,-1%"

set "DEST=%SOURCE%\backups\%TIMESTAMP%"

echo Backing up to %DEST%...
if not exist "%DEST%" mkdir "%DEST%"

:: Robocopy options:
:: /E :: copy subdirectories, including Empty ones.
:: /XD :: eXclude Directories matching given names/paths.
:: /XF :: eXclude Files matching given names/paths.
:: /R:0 :: number of Retries on failed copies: default 1 million.
:: /W:0 :: Wait time between retries: default 30 seconds.
robocopy "%SOURCE%" "%DEST%" /E /XD backups .git .gemini __pycache__ build dist *.egg-info .agent /XF *.pyc repo.zip *.log /R:0 /W:0

:: Robocopy exit codes:
:: 0 - No errors, no copying occurred (source/dest same)
:: 1 - One or more files copied successfully
:: 4 - Mismatched files/directories detected
:: 8 - Some files could not be copied (retry limit exceeded)
:: 16 - Serious error (file access denied, etc)
if %ERRORLEVEL% LSS 8 (
    echo Backup successful.
    exit /b 0
) else (
    echo Backup completed with errors.
    exit /b %ERRORLEVEL%
)
