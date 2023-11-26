@echo off
cd %~dp0

REM
for %%i in (*.mp3) do (
    del "%%i"
)

cd temp
for %%i in (*.mp4) do (
    del "%%i"
)

REM
pause