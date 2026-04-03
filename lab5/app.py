import subprocess
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField
from wtforms.validators import InputRequired, NumberRange, ValidationError
from port_utils import ensure_port_free
app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"
app.config["WTF_CSRF_ENABLED"] = False
def _no_shell_injection_chars(form, field):
    code = field.data or ""
    if '"' in code or "\n" in code or ";" in code:
        raise ValidationError("Недопустимые символы в коде для безопасного запуска без shell")
class ExecuteForm(FlaskForm):
    code = TextAreaField(
        validators=[
            InputRequired(message="code is required"),
            _no_shell_injection_chars,
        ]
    )
    timeout = IntegerField(
        validators=[
            InputRequired(message="timeout is required"),
            NumberRange(min=1, max=30, message="timeout must be 1..30"),
        ]
    )
@app.route("/execute", methods=["POST"])
def execute_code():
    form = ExecuteForm()
    if not form.validate_on_submit():
        return form.errors, 400
    code = form.code.data
    timeout_sec = form.timeout.data
    cmd = [
        "prlimit",
        "--nproc=1:1",
        "python3",
        "-c",
        code,
    ]
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        out, err = proc.communicate(timeout=timeout_sec)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        return "Исполнение не уложилось в отведённое время", 408
    output = (out or "") + (err or "")
    return output or "", 200
if __name__ == "__main__":
    PORT = 5000
    ensure_port_free(PORT)
    app.run(host="127.0.0.1", port=PORT, debug=False)
