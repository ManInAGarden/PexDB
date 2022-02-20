rem batch to build the distributable version for ms-windows
echo off
call conda activate PexDb
rem pyinstaller -w --name PexViewerWin --distpath ./dist/win --workpath ./build/win PexViewerMain.py
pyinstaller -w --noconfirm --name PexViewerWin ^
    --hidden-import "sklearn.utils._typedefs" ^
    --add-data ./PexDbWINDIST.conf;. ^
    --add-data ./PexSeeds;./PexSeeds ^
    --add-data ./ressources;./ressources ^
    --icon ./ressources/application.ico ^
    PexViewerMain.py
call conda deactivate
pause
