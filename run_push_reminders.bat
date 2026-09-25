@echo off

cd /d D:\PetCare_Portal

D:\PetCare_Portal\venv\Scripts\python.exe manage.py send_reminder_pushes >> D:\PetCare_Portal\push_scheduler.log 2>&1