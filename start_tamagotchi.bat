

@echo off

cd /d C:\Users\conje\my_agent\feynman_tamagotchi

start "" frontend\index.html

C:\Users\conje\anaconda3\envs\google\python.exe -m uvicorn server:app --reload

pause