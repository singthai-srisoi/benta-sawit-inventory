@echo off
start /B cmd /c "python manage.py runserver"
ping 127.0.0.1 -n 5 > nul
start http://127.0.0.1:8000
exit