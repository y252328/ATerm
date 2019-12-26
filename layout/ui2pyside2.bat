@ECHO OFF
call  F:\Program_Files\Miniconda3\Scripts\activate.bat py36
call pyside2-uic Ui_MainWindow.ui > Ui_MainWindow.py
ECHO "Ui_MainWindow.ui -> Ui_MainWindow.py"
rem call pyside2-uic Ui_SettingDialog.ui > Ui_SettingDialog.py
rem ECHO "Ui_SettingDialog.ui -> Ui_SettingDialog.py"
rem call D:\Program_Files\Anaconda3\Scripts\deactivate.bat
pause
