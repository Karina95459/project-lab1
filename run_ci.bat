@echo off
echo === Запуск тестів ===
C:\Users\risen\AppData\Local\Programs\Python\Python313\Scripts\pytest tests/ --html=report.html --self-contained-html

echo === Перевірка стилю коду ===
C:\Users\risen\AppData\Local\Programs\Python\Python313\Scripts\flake8 . --max-line-length=120

echo === Готово ===
pause