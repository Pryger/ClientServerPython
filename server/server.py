import threading  # Потоки
import socket
import json
import re  # Регулярки

IP = '127.0.0.1'
PORT = 50043
MAX_CLIENTS = 3

conn = socket.socket()  # Создаём сокет
conn.bind((IP, PORT))  # Биндим на IP PORT
conn.listen(MAX_CLIENTS)  # Слушаем максимум MAX_CLIENTS клиентов
clients = []  # Массив для клиентских сокетов


# Формирует факет для отправки информации
def createPackage(header, data):
    Data = dict()  # Объект
    Data['header'] = header
    Data['data'] = data
    package = str(json.dumps(Data)).encode('utf-8')  # Объект превращаем в json
    return package


# Отправляет пакет информации
def sendResponse(client, data, header='text'):
    package = createPackage(header, data)
    print(data)
    client.send(package)


# Функция работающая в потоке с одним клиентом
def client(client):
    while True:
        # Получаем строку и превращаем её в json
        data = client.recv(256).decode('utf-8')
        request = json.loads(data)

        # Если заголовок start начинаем загрузку файла
        if(request['header'] == 'start'):
            # Получаем имя и проверяем на корректность допустимые символы [a-zA-Z0-9] . [a-z]
            name = request['name']
            test_name = re.search(r'[a-zA-Z0-9]+\.+[a-z]*', name)
            if(test_name == None or test_name != None and name != test_name.group(0)):
                # Если имя файла недопустимое, выходим из функции с отправкой клиенту сообщения об ошибке и убираем сокет из массива
                # Отправка клиенту сообщения
                sendResponse(client, "Не допустимое имя файла")
                # Удаление сокета клиента из массива
                clients.pop(clients.index(client))
                break
            else:
                # Отправка сообщения клиенту
                sendResponse(client, f"Загрузка файла {name}")

            with open(name, '+ab') as cont:  # Открываем файл на запись в конец
                while True:
                    text = client.recv(4096)  # Получаем пакеты по 4096
                    # Если в пакете есть нулевой бакт
                    if b'\x00' in text:
                        # Записываем в файл всё кроме последнего байта
                        cont.write(text[:-1])
                        break
                    elif not text:
                        break
                    # Если нулевого байта в пакете нет просто записываем их в файл
                    cont.write(text)
            sendResponse(
                client, f"Файл {name} успешно загружен на сервер. Клиент отключен.")

            # Удаляем сокет клиента из массива
            clients.pop(clients.index(client))
            break

        # Если заголовок не start удаляем сокет клиента и выходим из функции
        else:
            sendResponse(client, "Клиент отключен от серера")
            clients.pop(clients.index(client))
            break


# Запуск сервера
# Если текущий файл был запущен черз коммандную строку ...
if __name__ == '__main__':
    while True:
        try:
            client_sock, addr = conn.accept()  # Блокирующая функция. Ожидает подключений
        except KeyboardInterrupt:  # Если ctrl + c
            print('\nСервер отключен')
            break
        else:
            if(len(clients) < MAX_CLIENTS):  # Если число клиентв не максимально, создаём нового
                clients.append(client_sock)  # Добавляем сокет клиента в массив
                print(f"Соединение с {addr[0]} установлено")

                # Запускаем отдельный поток с этим клиентом через функцию client
                client_thread = threading.Thread(
                    target=client, args=(client_sock,))
                client_thread.start()
            else:
                print(f"Соединение с {addr[0]} отклонено!")
