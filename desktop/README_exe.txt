🖥 七号技师桌面版启动说明（打包用）

将 main_app.py 打包成 .exe 可执行程序：
推荐使用 pyinstaller：

pyinstaller --noconsole --onefile main_app.py

或者通过 launch.bat 启动：

@echo off
python app.py
