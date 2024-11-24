@echo off
rem Run Backend
start python backend/app.py
rem Run Frontend
start npm start --prefix frontend
