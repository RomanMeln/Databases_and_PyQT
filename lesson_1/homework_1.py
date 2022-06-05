"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping
будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел
должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять
их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес
сетевого узла должен создаваться с помощью функции ip_address().
"""

import os
import platform
import subprocess
from ipaddress import ip_address
from pprint import pprint

result = {'Доступные узлы': "", "Недоступные узлы": ""}

DNULL = open(os.devnull, 'w')  # заглушка, чтобы поток не выводился на экран
# https://stackoverflow.com/questions/52435965/difference-between-os-devnull-and-subprocess-pipe


def check_is_ipaddress(value):
    """
    Проверка является ли введённое значение IP адресом
    :param value: присланные значения,
    :return ipv4: полученный ip адрес из переданного значения
        Exception ошибка при невозможности получения ip адреса из значения
    """
    try:
        ipv4 = ip_address(value)
    except ValueError:
        raise Exception('Некорректный ip адрес')
    return ipv4


def host_ping(hosts_list, get_list=False):
    """
    Проверка доступности хостов
    :param hosts_list: список хостов
    :param get_list: признак нужно ли отдать результат в виде словаря (для задания #3)
    :return словарь результатов проверки, если требуется
    """
    print("Начинаю проверку доступности адресов...")
    for host in hosts_list:  # проверяем, является ли значение ip-адресом
        try:
            ipv4 = check_is_ipaddress(host)
        except Exception as e:
            print(f'{host} - {e} воспринимаю как доменное имя')
            ipv4 = host

        param = '-n' if platform.system().lower() == 'windows' else '-c'
        response = subprocess.Popen(["ping", param, '1', '-w', '1', str(ipv4)],
                                    stdout=subprocess.PIPE)
        if response.wait() == 0:
            result["Доступные узлы"] += f"{ipv4}\n"
            res_string = f"{ipv4} - Узел доступен"
        else:
            result["Недоступные узлы"] += f"{ipv4}\n"
            res_string = f"{ipv4} - Узел недоступен"
        if not get_list:  # если результаты не надо добавлять в словарь, значит отображаем
            print(res_string)
    if get_list:        # если требуется вернуть словарь (для задачи №3), то возвращаем
        return result


if __name__ == '__main__':
    # список проверяемых узлов
    hosts_list = ['192.168.8.1', '8.8.8.8', 'yandex.ru', 'google.com', 'test.test',
                  '127.0.0.1', '127.0.0.2', '127.0.0.3', '127.0.0.4', '127.0.0.5',
                  '127.0.0.6', '127.0.0.7', '127.0.0.8', '127.0.0.9', '127.0.1.0']

    host_ping(hosts_list)
    pprint(result)
