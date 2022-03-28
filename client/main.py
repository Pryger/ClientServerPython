from Client import Client
import os.path


cl = Client('127.0.0.1', 50043)  # Создание объекта класса клиент
selectPhrase = "1 - отправить файл на сервер \n2 - закрыть соединение\n"

# Реализация пользовательского интерфейса
command = input(selectPhrase)
while (command == '1'):
    if(command == '1'):
        curPath = input("Введите путь с названием файла\n")
        if(os.path.isfile(curPath)):  # Проверка файла на существование
            newPath = input(
                "Введите путь для сохранения на сервер с названием файла\n")
            if(cl.startConnect()):  # Открываем соединение если успешно true иначе false
                print('Соединение установлено')

                with open(curPath, 'r') as text:  # Открытие файла для чтения
                    data = text.read()  # Чтение данных из файла

                # Отпревка стартового пакета с названием файла и путём для сохранения
                cl.sendPackageStart(newPath)

                cl.sendData(data)  # Отправка данных

                cl.closeConnect()  # Закрываем соединение
            else:
                print('Ошибка соединения с сервером')
                break
        else:
            print('Файла не существует')
        command = input(selectPhrase)
    else:
        print('Соединение прервано')
print('Клиент выключен')
