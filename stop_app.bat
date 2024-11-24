@echo off
rem Stop PostgreSQL service
start "" "C:\Program Files\PostgreSQL\13\bin\pg_ctl.exe" -D "C:\Program Files\PostgreSQL\13\data" stop

rem Stop the Flask backend
taskkill /F /IM python.exe

rem Stop React frontend
taskkill /F /IM node.exe
