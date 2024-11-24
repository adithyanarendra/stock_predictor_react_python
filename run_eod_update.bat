@echo off
rem Run EOD update for all stocks
cd backend
call venv\Scripts\activate
start python app.py fetch_historic_data
