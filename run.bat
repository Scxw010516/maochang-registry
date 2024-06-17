cd /d %~dp0
# 启动后端
start "back-end" cmd /k call command-back.bat
# 启动前端
start "front-end" cmd /k  call command-front.bat
# 启动服务端
start "server-end" call command-server.bat