@echo off
REM ================================================================
REM SQLite Backup Script for KeToan SME
REM Schedule via Windows Task Scheduler:
REM   schtasks /Create /TN "KeToanSME_Backup" /TR "E:\gl\deploy\backup.bat" /SC DAILY /ST 23:00
REM ================================================================

setlocal

REM Configuration
set PROJECT_DIR=E:\gl
set DB_FILE=%PROJECT_DIR%\db.sqlite3
set BACKUP_DIR=%PROJECT_DIR%\backups
set DATE_STAMP=%DATE:~-4%%DATE:~3,2%%DATE:~0,2%
set TIME_STAMP=%TIME:~0,2%%TIME:~3,2%
set TIME_STAMP=%TIME_STAMP: =0%
set BACKUP_FILE=%BACKUP_DIR%\db_backup_%DATE_STAMP%_%TIME_STAMP%.sqlite3

REM Create backup directory if not exists
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Check if database exists
if not exist "%DB_FILE%" (
    echo [ERROR] Database file not found: %DB_FILE%
    exit /b 1
)

REM Copy database file
echo [INFO] Backing up database to %BACKUP_FILE%...
copy /Y "%DB_FILE%" "%BACKUP_FILE%" >nul

if %ERRORLEVEL% EQU 0 (
    echo [OK] Backup successful: %BACKUP_FILE%
    
    REM Keep only last 30 days of backups
    forfiles /P "%BACKUP_DIR%" /S /M *.sqlite3 /D -30 /C "cmd /c del @path" 2>nul
    
    echo [OK] Old backups cleaned (>30 days)
) else (
    echo [ERROR] Backup failed!
    exit /b 1
)

endlocal
