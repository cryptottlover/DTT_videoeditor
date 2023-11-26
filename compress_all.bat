@echo off
setlocal enabledelayedexpansion

set "script_dir=%~dp0"

for %%F in ("%script_dir%\*.mp4") do (
    set "working_file=%%~nF_working.mp4"
    ffmpeg -i "%%~fF" -vcodec libx265 -crf 28 "!working_file!"
    move "!working_file!" "%%~nxF"
)

echo Compression completed.
pause
