rem batch to build the distributable version for ms-windows
echo off
call conda activate PexDb
echo writing external libst to cache fur use in about pexdb ...
python create_dependcydb.py
echo ... done
pyinstaller -w --noconfirm --name PexViewerWin ^
    --hidden-import "sklearn.utils._typedefs" ^
    --add-data ./PexDbWINDIST.conf;. ^
    --add-data ./PexSeeds;./PexSeeds ^
    --add-data ./ressources;./ressources ^
    --icon ./ressources/application.ico ^
    PexViewerMain.py
call conda deactivate
pause
