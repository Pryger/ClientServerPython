import socket
import json


class Client:  # Класс с методами организующими сетевое взаимодействие
    # Конструктор self = this
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port

    # Установка соединения
    def startConnect(self):
        # Создаём сокет. По умолчанию socket.AF_INET, socket.SOCK_STREAM
        self.sock = socket.socket()
        try:
            self.sock.connect((self.addr, self.port))
        except socket.error:  # В случае ошибки не отсанавливаем программу, а возвращаем False
            return False
        else:
            return True

    # Получение любого ответа и вывод его на экран
    def getRecv(self):
        data = self.sock.recv(256).decode(
            'utf-8')  # Принимаем у сервера строку
        request = json.loads(data)  # Превращаем её в json
        return print(request['data'])  # Выводим на экран информацию из пакета

    # Отправка стартового пакета в формате json
    def sendPackageStart(self, name):
        Data = dict()  # Формируем объект
        Data['header'] = 'start'
        Data['name'] = name
        package = str(json.dumps(Data)).encode(
            'utf-8')  # Превращаем объект в json
        self.sock.send(package)  # Отправляем через сокет
        self.getRecv()  # Ждёт ответ и выводим на экран

    # Отправка информации в файле пакетами
    def sendData(self, data):
        # Отправка всех данных пакетами по 1024 байта
        self.sock.sendall(data.encode('utf-8'))
        # Когда всё отправленно, в конце отправляем нулевой байт
        self.sock.send(b'\x00')

    # Отправка пакета завершающего соединение по принципу sendPackageStart
    def sendPackageClose(self):
        Data = dict()
        Data['header'] = 'close'
        package = str(json.dumps(Data)).encode('utf-8')
        self.sock.send(package)

    # Отправка завершающего пакета и закрытие сокета
    def closeConnect(self):
        self.sendPackageClose()
        self.sock.close()
