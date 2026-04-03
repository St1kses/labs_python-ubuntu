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
    total = sum(finance_storage.get(year, {}).values())
    return f"Суммарные траты за {year} год: {total}"
@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    if month < 1 or month > 12:
        return "Ошибка: месяц должен быть от 1 до 12", 400
    month_total = finance_storage.get(year, {}).get(month, 0)
    return f"Суммарные траты за {month:02d}.{year}: {month_total}"
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
