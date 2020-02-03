# -*- coding: utf-8 -*-
from .class_git import gitApi
from getpass import getpass

# ----------------------------------------------------------------------------------------------------------------------
#                                             Второстепенные функции
# ----------------------------------------------------------------------------------------------------------------------
def validInputNum(text_for_num, start_num = None, end_num = None, list_allowed = None):
    '''
        Функция для проверки ввода числа с определенными ограничениями, если в этом есть необходимость
        :param text_for_num: текст, который выводится пользователю
        :param start_num: с какого числа должно начинаться, иначе с любого
        :param end_num: каким числом должно заканчиваться, иначе заканчивается любым
        :param list_allowed: список дозволенных чисел, иначе любое
        :return: введенное число пользователем
    '''
    # Зацикливаем, до тех пор пока не введут число в нужном диапазоне
    while True:
        # Считываем в текст
        num = input(text_for_num)
        # Проверяем является ли целое число
        if not num.replace("-", "").isdigit() or num.find("-") > 0:
            print("Необходимсо ввести целое число")
            continue
        # Проверяем задан ли диапазон
        if not start_num is None or not end_num is None:
            if not start_num is None and not end_num is None:
                # Проверяем чтобы попадало в диапазон
                if (int(num) < int(start_num) or int(num) > int(end_num)):
                    print("Число должно соответствовать диапазону от %s до %s" % (start_num, end_num))
                    continue
            elif not end_num is None:
                # Проверяем чтобы попадало в диапазон
                if (int(num) > int(end_num)):
                    print("Число должно соответствовать диапазону до %s" % (end_num))
                    continue
            else:
                # Проверяем чтобы попадало в диапазон
                if (int(num) < int(start_num)):
                    print("Число должно соответствовать диапазону от %s " % (start_num))
                    continue
        # Проверяем заданы значения в массиве
        if not list_allowed is None:
            if not int(num) in list_allowed:
                print("Данного числа нет в допустимых вариантах. ")
                continue
        #Если все хорошо, возвращаем переменную в типе int
        return int(num)


if __name__ == "__main__":
    ga = gitApi()

    print("-" * 10)
    print('Урок 1')
    print("-" * 10)
    print("В качетсве работы с api для 1-го и 2-го задания был выбран github")
    print("-" * 10)
    while(True):
        print("""1. Вывести список репозиториев для конкретного пользователя.\n2. Сохранить список репозиториев в формате json.""")
        if ga.isAuth():
            print("""3. Вывести список своих репозиториев.\n4. Сохранить список своих репозиториев.\n5. Создать репозиторий.\n6. Удалить репозиторий .\n7.Выход""")
            end_num = 7
        else:
            print("3. Авторизироваться в github с помощью логин/пароль.\n4.Выход")
            end_num = 4

        punkt = validInputNum("Ваш выбор: ", start_num=1, end_num=end_num)

        if punkt == 7 and ga.isAuth() or punkt == 4 and ga.isAuth():
            break

        if punkt == 1:
            username = input("Введите имя пользователя: ")
            ga.print_repos(username)

        if punkt == 2:
            username = input("Введите имя пользователя: ")
            ga.export_repos(username)

        if not ga.isAuth() and punkt == 3:
            username = input('Login: ')
            passwd = getpass(prompt='Password: ')
            ga.set_auth(username, passwd)

        if ga.isAuth() and punkt == 3:
            ga.print_repos(ga._username)

        if ga.isAuth() and punkt == 4:
            ga.export_repos(ga._username)

        if ga.isAuth() and punkt == 5:
            name_repos = input("Введите наименование репозитория")
            ga.create_repos(name_repos)

        if ga.isAuth() and punkt == 6:
            name_repos = input("Введите наименование репозитория")
            ga.delete_repos(name_repos)