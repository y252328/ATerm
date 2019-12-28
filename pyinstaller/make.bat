call F:\Program_Files\Miniconda3\Scripts\activate.bat py36
call pyinstaller -w -F -n "ATerm" ../main.py
move dist\ATerm.exe ..\bin
pause