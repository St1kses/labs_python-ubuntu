# Найденные ошибки в классе Person
## 1. get_age
- Проблема: возраст считался как `self.yob - now.year`.
- Исправление: `now.year - self.yob`.
## 2. set_name
- Проблема: `self.name = self.name`.
- Исправление: `self.name = name`.
## 3. set_address
- Проблема: использовалось `==` вместо присваивания.
- Исправление: `self.address = address`.
## 4. is_homeless
- Проблема: использовалась несуществующая переменная `address`.
- Исправление: проверка `self.address in ("", None)`.
