@echo off
chcp 65001 >nul
echo.
echo ========================================
echo Windows图标缓存清理工具
echo ========================================
echo.

echo 正在清理图标缓存...

:: 结束Windows资源管理器进程
taskkill /f /im explorer.exe >nul 2>&1

:: 删除图标缓存文件
del /a /q "%localappdata%\IconCache.db" >nul 2>&1
del /a /f /q "%localappdata%\Microsoft\Windows\Explorer\iconcache*" >nul 2>&1

:: 重启Windows资源管理器
start explorer.exe

echo.
echo ✅ 图标缓存已清理
echo 💡 图标应该会在几秒钟内更新
echo.

timeout /t 3 >nul
echo 完成！
pause