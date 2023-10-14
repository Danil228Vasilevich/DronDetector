from flask import Flask, render_template, request, jsonify
from flask_htmx import HTMX

# Создание экземпляра Flask-приложения
app = Flask(__name__)

# Инициализация Flask-HTMX
htmx = HTMX(app)

# Глобальные переменные для хранения данных
data_global = ""
data_globalOld = ""

# Маршрут для отображения главной страницы
@app.route("/")
def home():
    return render_template("index.html", data=data_global)

# Маршрут для обновления данных
@app.route('/update_data', methods=['GET'])
def update_data():
    global data_global
    global data_globalOld

    if data_global == data_globalOld:
        # Если данные не изменились, возвращаем "pass"
        return jsonify(data="pass")
    else:
        # Если данные изменились, обновляем data_globalOld и возвращаем текущие данные
        data_globalOld = data_global
        return jsonify(data=data_global)

# Маршрут для обработки запросов
@app.route('/', methods=['GET', 'POST'])
def index():
    global data_global

    if request.method == 'POST':
        # Если получен POST-запрос
        print(request.json)
        data_global = request.json
        return f'{request.method} Запрос отправлен'
    return f'{request.method} Запрос отклонен'

# Запуск приложения при запуске этого файла
if __name__ == "__main__":
    app.run(debug=True)
