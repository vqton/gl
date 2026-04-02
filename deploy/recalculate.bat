@echo off
REM ================================================================
REM Nightly Inventory Recalculation
REM Schedule via Windows Task Scheduler:
REM   schtasks /Create /TN "KeToanSME_Recalculate" /TR "E:\gl\deploy\recalculate.bat" /SC DAILY /ST 23:30
REM ================================================================

setlocal

set PROJECT_DIR=E:\gl
set PYTHON=%PROJECT_DIR%\venv\Scripts\python.exe

echo [INFO] Starting inventory recalculation...
cd /d %PROJECT_DIR%
%PYTHON% manage.py recalculate_inventory

if %ERRORLEVEL% EQU 0 (
    echo [OK] Recalculation completed successfully
) else (
    echo [ERROR] Recalculation failed with code %ERRORLEVEL%
)

endlocal
