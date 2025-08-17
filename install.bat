@echo off
chcp 65001 >nul
echo JSON格式化工具安装程序
echo.

set "INSTALL_DIR=%USERPROFILE%\Desktop\JSON格式化工具"
set "EXE_FILE=JSON格式化工具.exe"

echo 正在安装到: %INSTALL_DIR%
echo.

if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

copy "%EXE_FILE%" "%INSTALL_DIR%\" >nul
if %errorlevel% equ 0 (
    echo [OK] 安装成功！
    echo.
    echo [INFO] 程序已安装到: %INSTALL_DIR%
    echo [TIP] 您可以在桌面文件夹中找到"JSON格式化工具"文件夹
    echo.
    
    echo 是否现在运行程序？ (Y/N)
    set /p choice=
    if /i "%choice%"=="Y" (
        start "" "%INSTALL_DIR%\%EXE_FILE%"
    )
) else (
    echo [ERROR] 安装失败！请检查权限或联系管理员。
)

echo.
pause
