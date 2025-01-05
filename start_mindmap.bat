REM filepath: /e:/工作/脚本/思维导图/start_mindmap.bat
@echo off
chcp 65001
setlocal enabledelayedexpansion

REM 检查Python环境
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python未安装或未添加到环境变量！
    pause
    exit /b 1
)

REM 检查必要的Python库
python -c "import xmind,markdown,bs4" 2>nul
if %errorlevel% neq 0 (
    echo 正在安装必要的Python库...
    pip install xmind-sdk-python markdown beautifulsoup4
)

REM 处理文件
if "%~1"=="" (
    if exist "input.md" (
        echo 找到input.md，开始处理...
        python mind.py "input.md" "output.xmind"
    ) else (
        echo 使用方法：
        echo 1. 直接拖拽markdown文件到本脚本上
        echo 2. 将markdown文件命名为input.md放在同目录下
        pause
        exit /b 1
    )
) else (
    echo 正在处理文件：%~1
    python mind.py "%~1" "%~dpn1.xmind"
)

if %errorlevel% neq 0 (
    echo 处理失败！
    pause
    exit /b 1
)

echo 处理完成！
timeout /t 3