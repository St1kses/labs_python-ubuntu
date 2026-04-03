import re
import subprocess
from datetime import datetime
from typing import Optional
from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import Email, InputRequired, Optional as OptionalValidator, ValidationError
app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"
app.config["WTF_CSRF_ENABLED"] = False
WEEKDAYS_GENITIVE = (
    "понедельника",
    "вторника",
    "среды",
    "четверга",
    "пятницы",
    "субботы",
    "воскресенья",
)
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
def number_length(min_len: int, max_len: int, message: Optional[str] = None):
    def _number_length(form: FlaskForm, field: IntegerField):
        value = field.data
        if value is None:
            return
        length = len(str(value))
        if length < min_len or length > max_len:
            raise ValidationError(message or f"Number length must be between {min_len} and {max_len}")
    return _number_length
class NumberLength:
    def __init__(self, min_len: int, max_len: int, message: Optional[str] = None):
        self.min_len = min_len
        self.max_len = max_len
        self.message = message
    def __call__(self, form: FlaskForm, field: IntegerField):
        value = field.data
        if value is None:
            return
        length = len(str(value))
        if length < self.min_len or length > self.max_len:
            raise ValidationError(self.message or f"Number length must be between {self.min_len} and {self.max_len}")
def validate_positive_phone(form: FlaskForm, field: IntegerField):
    if field.data is not None and field.data <= 0:
        raise ValidationError("phone must be positive")
class RegistrationForm(FlaskForm):
    email = StringField(validators=[InputRequired(message="email is required"), Email(message="invalid email format")])
    phone = IntegerField(
        validators=[
            InputRequired(message="phone is required"),
            number_length(10, 10, message="phone must contain exactly 10 digits"),
        ]
    )
    name = StringField(validators=[InputRequired(message="name is required")])
    address = StringField(validators=[InputRequired(message="address is required")])
    index = IntegerField(validators=[InputRequired(message="index is required")])
    comment = StringField(validators=[OptionalValidator()])
class RegistrationFormWithClassValidator(RegistrationForm):
    phone = IntegerField(
        validators=[
            InputRequired(message="phone is required"),
            NumberLength(10, 10, message="phone must contain exactly 10 digits"),
            validate_positive_phone,
        ]
    )
@app.route("/registration", methods=["GET", "POST"])
def registration():
    form = RegistrationFormWithClassValidator()
    if request.method == "GET":
        return "Send POST request to /registration"
    if form.validate_on_submit():
        return "Registration data is valid"
    return form.errors, 400
@app.route("/uptime", methods=["GET"])
def uptime():
    result = subprocess.run(["uptime", "-p"], capture_output=True, text=True, check=False)
    return f"Current uptime is {result.stdout.strip()}"
@app.route("/ps", methods=["GET"])
def ps_endpoint():
    args: list[str] = request.args.getlist("arg")
    safe_args = []
    for arg in args:
        if not re.fullmatch(r"[A-Za-z]+", arg):
            return {"error": f"invalid arg: {arg}"}, 400
        safe_args.append(f"-{arg}")
    result = subprocess.run(["ps"] + safe_args, capture_output=True, text=True, check=False)
    return f"<pre>{result.stdout}</pre>"
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
