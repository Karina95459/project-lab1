@echo off
echo === Запуск тестів ===
pytest tests/ --html=report.html --self-contained-html

echo === Перевірка стилю коду ===
flake8 . --max-line-length=120

echo === Готово ===
pause