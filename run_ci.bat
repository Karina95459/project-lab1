@echo off
chcp 65001 > nul

for /f "delims=" %%i in ('where python') do set PY_PATH="%%i" & goto :found
:found

if not defined PY_PATH set PY_PATH=python

echo === Запуск тестів ===
%PY_PATH% -m pytest tests/ --html=report.html --self-contained-html

echo === Перевірка стилю коду ===
%PY_PATH% -m flake8 . --max-line-length=120

echo === Готово ===
pause