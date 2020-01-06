call F:\Program_Files\Miniconda3\Scripts\activate.bat py36
call pyinstaller -w -F -i "..\layout\icon.ico" -n "ATerm" ../main.py
mkdir ..\bin
move dist\ATerm.exe ..\bin
pause