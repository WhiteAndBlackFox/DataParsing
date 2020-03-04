# -*- coding: utf-8 -*-

import requests
import json
import os
from time import gmtime, strftime
import logging

class gitApi:

    #-------------------------------------------------------------------------------------------------------------------
    # Params for class
    # -------------------------------------------------------------------------------------------------------------------

    # Dicts urls for generate template requests
    __urls = {
        'list_repos': 'https://api.github.com/users/{}/repos',
        'create_repos': 'https://api.github.com/user/repos',
        'delete_repos': 'https://api.github.com/repos/{}/{}',
        'auth' : 'https://api.github.com/user'
    }

    __toSaveDumps = 'dumps'
    logger = None
    __logging_filename = 'lessons1.log'
    __isAuth = False

    # Parametrs for auth
    _username = None
    __passwd = None
    __sessions = None

    def __init__(self, username = None, passwd = None):

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler(self.__logging_filename)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        if username and passwd:
            self._username = username
            self.__passwd = passwd
            self.__check_auth()
        super().__init__()

    def __del__(self):
        self._username = None
        self.__passwd = None

    def set_auth(self, username, passwd):
        self._username = username
        self.__passwd = passwd
        self.__check_auth()

    def __get_sessions(self):
        if not self._username or not self.__passwd:
            self.logger.error('Не заполнен логин или пароль')
            Exception('Не заполнен логин или пароль')

        session = None

        try:
            session = requests.Session()
            session.auth = (self._username, self.__passwd)
        except Exception as e:
            self.logger.error(f'Ошибка: {e}')
            print(e)

        return session

    def __check_auth(self):
        session = self.__get_sessions()
        response = session.get(self.__urls['auth'])
        if response.ok:
            self.logger.info(
                f'Авторизация пользователя {self._username} прошла успешно! Склонировать можно: git clone {json.loads(response.text)}')
            self.__isAuth = True
        else:
            self.logger.error(
                f'Авторизация пользователя {self._username} не удалась! Ошибка: {json.loads(response.text)["message"]}')
            self.__isAuth = False
            print(f'Авторизация пользователя {self._username} не удалась!')

    def create_repos(self, name):
        session = self.__get_sessions()
        issue = {
                "name": name,
                "description": "This is your first repository",
                "homepage": "https://github.com",
                "private": False,
                "has_issues": True,
                "has_wiki": True
        }

        response = session.post(self.__urls['create_repos'], json.dumps(issue))

        if response.ok:
            self.logger.info(f'Репозиторий успешно создан! Склонировать можно: git clone {json.loads(response.text)["clone_url"]}')
            return {'create': True, 'msg': json.loads(response.text)['clone_url']}
        else:
            self.logger.error(f'Ошибка создания репозитория! Ошибка: {json.loads(response.text)["message"]}')
            return {'create': False, 'msg': json.loads(response.text)['message']}

    def delete_repos(self, name):
        session = self.__get_sessions()

        urls = self.__urls['delete_repos'].format(self._username, name)
        response = session.delete(urls)
        if response.ok:
            self.logger.info(f'Репозиторий успешно удален! URL: {urls}')
            return {'delete': True, 'msg': 'Репозиторий успешно удален!'}
        else:
            self.logger.error(f'Ошибка удаления: {json.loads(response.text)["message"]}')
            return {'delete': False, 'msg': json.loads(response.text)['message']}

    def print_repos(self, username):
        data = self.get_repos(username)
        if data['isData']:
            self.logger.info(f"В репозитории найдено {len(data['response'])} проект(ов)")
            print("%-60s%30s%30s%10s%-100s" % ("Наименование проекта", "Дата создания репозитория", "Последняя дата изменения", '', "Ссылка на git_clone"))
            for project in data['response']:
                print("%-60s%30s%30s%10s%-100s" % (project['name'], project['created_at'], project['updated_at'], '', project['clone_url']))
        else:
            self.logger.error(f"В репозитории пользователя {username} не найдено проектов")
            print(f"В репозитории пользователя {username} не найдено проектов")

    def export_repos(self, username):
        data = self.get_repos(username)
        if data['isData']:
            self.logger.info(f"В репозитории найдено {len(data['response'])} проект(ов)")
            if not os.path.exists(self.__toSaveDumps):
                try:
                    os.makedirs(self.__toSaveDumps)
                except OSError as err:
                    self.logger.error(f'Ошибка удаления: {err}')
                    print(err)
            date_now = strftime('%Y%m%d_%H%M%S', gmtime())
            with open(f"{self.__toSaveDumps}/dump_{username}_{date_now}.json", 'w+') as f:
                json.dump(data['response'], f)
            print(f"Данные выгружены в {self.__toSaveDumps}/dump_{username}_{date_now}.json")
        else:
            self.logger.error(f"В репозитории пользователя {username} не найдено проектов")
            print(f"В репозитории пользователя {username} не найдено проектов")

    def get_repos(self, username):
        try:
            response = requests.get(self.__urls['list_repos'].format(username))
            return {'isData': True if response.ok else False, 'response': json.loads(response.text)}
        except Exception as e:
            self.logger.error(f'Ошибка получения репозиториев: {e}')
            print(e)

    def isAuth(self):
        return self.__isAuth