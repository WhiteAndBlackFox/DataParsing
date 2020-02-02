# -*- coding: utf-8 -*-

import requests
import json
import os
from time import gmtime, strftime

class gitApi:

    #-------------------------------------------------------------------------------------------------------------------
    # Params for class
    # -------------------------------------------------------------------------------------------------------------------

    # Dicts urls for generate template requests
    __urls = {
      'repos':'https://api.github.com/users/{}/repos',
    }

    __toSaveDumps = 'dumps'

    # Parametrs for auth
    __username = None
    __token = None

    def __init__(self, username = None, token = None):
        self.__username = username
        self.__token = token
        super().__init__()

    def print_repos(self, username):
        data = self.get_repos(username)
        if data['isData']:
            print("%-60s%30s%30s%10s%-100s" % ("Наименование проекта", "Дата создания репозитория", "Последняя дата изменения", '', "Ссылка на git_clone"))
            for project in data['response']:
                print("%-60s%30s%30s%10s%-100s" % (project['name'], project['created_at'], project['updated_at'], '', project['clone_url']))
        else:
            print(f"В репозитории пользователя {username} не найдено проектов")

    def export_repos(self, username):
        data = self.get_repos(username)
        if data['isData']:
            if not os.path.exists(self.__toSaveDumps):
                try:
                    os.makedirs(self.__toSaveDumps)
                except OSError as err:
                    print(err)
            date_now = strftime('%Y%m%d_%H%M%S', gmtime())
            with open(f"{self.__toSaveDumps}/dump_{username}_{date_now}.json", 'w+') as f:
                json.dump(data['response'], f)
        else:
            print(f"В репозитории пользователя {username} не найдено проектов")

    def get_repos(self, username):
        try:
            response = requests.get(self.__urls['repos'].format(username))
            return {'isData': True if response.ok else False, 'response': json.loads(response.text)}
        except Exception as e:
            print(e)
