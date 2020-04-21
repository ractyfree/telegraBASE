rd /s /q dist
rd /s /q build
del main.spec
rd /s /q __pycache__
pyinstaller.exe main.py