# -*- coding: utf-8 -*-
from class_git import gitApi
from getpass import getpass

ga = gitApi()

print("-" * 10)
print('Урок 1')
print("-" * 10)
print("В качетсве работы с api для 1-го и 2-го задания был выбран github")
print("-" * 10)
while(True):
    print("""1. Вывести список репозиториев для конкретного пользователя.\n2. Сохранить список репозиториев в формате json.""")
    if ga.isAuth():
        print("""3. Вывести список своих репозиториев.\n4. Вывести список своих репозиториев.\n5. Создать репозиторий.\n6. Удалить репозиторий .\n""")
    else:
        print("3. Авторизироваться в github с помощью логин/пароль")
    variable = input("Выбирите один из пунктов: " )
#
# username = input('Login: ')
# passwd = getpass(prompt='Password: ')
#
#
# # create repos
# create_resp = ga.create_repos('ttt')
# delete repos
# del_resp = ga.delete_repos('ttt')
# print my repos
# my_resp = ga.print_repos(ga.username)

# print random repos
# ga = gitApi()
# ga.print_repos('asoifdhuipsdhuifhashfeaiushdui')
# ga.print_repos('WhiteAndBlackFox')
