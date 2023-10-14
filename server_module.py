# Импорт необходимых библиотек
import requests  # Для выполнения HTTP-запросов
import json  # Для работы с данными в формате JSON

# Определение класса Server
class Server:
    def __init__(self, ip="localhost", port=5000) -> None:
        """
        Конструктор класса Server.

        Args:
            ip (str): IP-адрес сервера (по умолчанию "localhost").
            port (int): Порт сервера (по умолчанию 5000).
        """
        self.ip = ip
        self.port = port

    def send(self, freq=None, power=None):
        """
        Метод для отправки данных на сервер.

        Args:
            freq (list): Список значений частоты.
            power (list): Список значений мощности.

        Описание:
        - Создает базовый URL для отправки данных, используя IP-адрес и порт.
        - Подготавливает данные для отправки, формируя JSON-структуру.
        - Преобразует данные в формат JSON.
        - Устанавливает заголовок Content-Type как application/json.
        - Отправляет POST-запрос на сервер.
        - Проверяет успешность запроса и выводит соответствующие сообщения.
        
        Важно:
        - Метод ожидает, что `freq` и `power` - это списки с одинаковым количеством элементов.
        - Если запрос выполнен успешно, ответ сервера и код состояния выводятся на консоль.
        - В случае ошибки при выполнении запроса, выводится сообщение об ошибке и код ошибки.

        """
        base_url = f'http://{self.ip}:{self.port}/'
        data_to_send = [{"freq": str(f), "power": str(p)} for f, p in zip(freq, power)]
        data_to_send = {"datas": data_to_send}
        json_data = json.dumps(data_to_send)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(base_url, data=json_data, headers=headers)
        if response.status_code == 200:
            print('Запрос успешно выполнен')
            print('Ответ от сервера:')
            print(response.text)
        else:
            print('Ошибка при выполнении запроса. Код ошибки:', response.status_code)
  
  
            
# Пример запроса            
        
# # main.py
# from server_module import Server

# if __name__ == "__main__":
#     server = Server()
#     server.send(freq=[11133,123], power=[1322211331,1111])

