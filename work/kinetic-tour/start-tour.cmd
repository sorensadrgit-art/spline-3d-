@echo off
cd /d "%~dp0"
if not exist "node_modules\vite\bin\vite.js" (
  echo Run npm ci, then npm run build in this folder first.
  pause
  exit /b 1
)
echo Open http://127.0.0.1:4177/ in your browser.
echo If port 4177 is already in use, the current preview may still be running.
call npm run preview
