@echo off
set numpackages=2

rem make sure the working folder is the one containing this file.
cd /D "%~dp0"

echo current directory: %cd%

rem run this to fill the pycmd environment variable
call findpython.bat 1
if %errorlevel% NEQ 0 goto error

echo.
echo Checking for pip...
%pycmd% -m pip --version 2>NUL
if %errorlevel% NEQ 0 set errormessage=Could not find pip & goto error
echo.

echo Attempting to install pillow...
%pycmd% -m pip install pillow
if %errorlevel% NEQ 0 echo Could not install Pillow
echo Attempting to install numpy...
%pycmd% -m pip install numpy
if %errorlevel% NEQ 0 echo Could not install NumPy


rem set up variables
set /a counter=0
set pip=
set numpy=
set Pillow=

echo.
echo -- Summary -----------------------------
set name=
for /f "tokens=1,2 delims= " %%A in ('pip list') do ^
if "%%A"=="pip" (set %%A=%%B) else ^
if "%%A"=="numpy" (set %%A=%%B) else ^
if "%%A"=="Pillow" (set %%A=%%B) else ^
rem

if %pip%x neq x (echo pip %pip% & set /a counter=%counter%+0) else echo pip [not installed]
echo.
if %numpy%x neq x (echo numpy %numpy% & set /a counter=%counter%+1) else echo numpy [not installed]
if %Pillow%x neq x (echo Pillow %Pillow% & set /a counter=%counter%+1) else echo Pillow [not installed]
echo.

echo %counter%/%numpackages% required packages were installed.
echo ----------------------------------------
if %counter% neq %numpackages% set errormessage=Some packages not installed.&goto error

goto success

:error
echo.
echo Did NOT complete successfully.
echo.ERROR: %errormessage%
echo.
echo.
echo                      No longer do the dance of joy Numfar.
echo.
echo.
pause
goto theend

:success
echo.
echo Done.
echo.
echo.
echo                           Numfar, do the dance of joy!
echo.
echo.
pause

:theend