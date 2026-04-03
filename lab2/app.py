import os
from datetime import datetime
from flask import Flask
app = Flask(__name__)
WEEKDAYS_GENITIVE = (
    "понедельника",
    "вторника",
    "среды",
    "четверга",
    "пятницы",
    "субботы",
    "воскресенья",
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
finance_storage = {}
@app.route("/hello-world/<name>")
def hello_world_name(name: str):
    weekday_index = datetime.today().weekday()
    weekday_name = WEEKDAYS_GENITIVE[weekday_index]
    return f"Привет, {name}. Хорошей {weekday_name}!"
@app.route("/max_number/<path:numbers_path>")
def max_number(numbers_path: str):
    parts = [p for p in numbers_path.split("/") if p]
    if not parts:
        return "Ошибка: не переданы числа", 400
    numeric_values = []
    for item in parts:
        try:
            numeric_values.append(float(item))
        except ValueError:
            return f"Ошибка: '{item}' не является числом", 400
    max_value = max(numeric_values)
    return f"Максимальное число: <i>{max_value:g}</i>"
@app.route("/preview/<int:size>/<path:relative_path>")
def preview_file(size: int, relative_path: str):
    file_path = os.path.join(BASE_DIR, relative_path)
    abs_path = os.path.abspath(file_path)
    if size < 0:
        return "Ошибка: size должен быть >= 0", 400
    if not os.path.exists(abs_path):
        return "Ошибка: файл не найден", 404
    if not os.path.isfile(abs_path):
        return "Ошибка: путь не указывает на файл", 400
    try:
        with open(abs_path, "r", encoding="utf-8") as file:
            preview_text = file.read(size)
    except UnicodeDecodeError:
        return "Ошибка: файл не является текстовым UTF-8", 400
    preview_size = len(preview_text)
    return f"<b>{abs_path}</b> {preview_size}<br>{preview_text}"
@app.route("/add/<date>/<int:number>")
def add_expense(date: str, number: int):
    if len(date) != 8 or not date.isdigit():
        return "Ошибка: дата должна быть в формате YYYYMMDD", 400
    year = int(date[:4])
    month = int(date[4:6])
    if month < 1 or month > 12:
        return "Ошибка: месяц должен быть от 1 до 12", 400
    finance_storage.setdefault(year, {}).setdefault(month, 0)
    finance_storage[year][month] += number
    return f"Добавлено: {number} руб. за {date}"
@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    year_data = finance_storage.get(year, {})
    total = sum(year_data.values())
    return f"Суммарные траты за {year} год: {total}"
@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    if month < 1 or month > 12:
        return "Ошибка: месяц должен быть от 1 до 12", 400
    month_total = finance_storage.get(year, {}).get(month, 0)
    return f"Суммарные траты за {month:02d}.{year}: {month_total}"
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
