@echo off
cd /d "%~dp0"

REM 仮想環境のPythonを探して実行
if exist "venv\Scripts\python.exe" (
    echo Starting Chatbot with local venv...
    echo ブラウザを自動で開きます...
    start /B venv\Scripts\python.exe app.py
    timeout /t 3 /nobreak >nul
    start http://localhost:3000
    goto :success
)

if exist "..\venv\Scripts\python.exe" (
    echo Starting Chatbot with parent venv...
    echo ブラウザを自動で開きます...
    start /B ..\venv\Scripts\python.exe app.py
    timeout /t 3 /nobreak >nul
    start http://localhost:3000
    goto :success
)

echo [ERROR] Virtual environment (venv) not found.
echo Please make sure you have set up the environment.
pause
exit /b 1

:success
echo.
echo アプリが起動しました！
echo ブラウザで http://localhost:3000 にアクセスしています...
echo.
echo 終了するには、このウィンドウを閉じてください。
pause
