@echo off
chcp 65001 >nul
cls
echo ==========================================================
echo    学生会人事管理系统 —— Windows 桌面端打包脚本
echo    使用 PyInstaller + build.spec 配置打包
echo ==========================================================
echo.

cd /d "%~dp0"

REM 检查 Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [错误] 未找到 Python，请先安装 Python 3.10~3.12
    echo 下载地址：https://www.python.org/downloads/windows/
    echo 注意：PySide6 暂不支持 Python 3.13/3.14，请选 3.11 或 3.12
    pause
    exit /b 1
)

echo [1/3] Python 版本：
python --version

echo.
echo [2/3] 正在安装依赖...
python -m pip install -r requirements.txt -q
python -m pip install pyinstaller -q

echo.
echo [3/3] 正在打包（使用 build.spec）...
echo 提示：首次打包需 5-10 分钟，PySide6 体积较大
python -m PyInstaller build.spec --noconfirm

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [错误] 打包失败，请检查上方错误信息。
    pause
    exit /b 1
)

echo.
echo ==========================================================
echo  打包完成！
echo  输出文件：%~dp0dist\学生会人事管理系统.exe
echo  双击即可运行，无需安装 Python 或浏览器
echo ==========================================================
pause
