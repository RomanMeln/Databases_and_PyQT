"""
2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.
"""


import platform
import subprocess
from ipaddress import ip_address

result = {'Доступные узлы': "", "Недоступные узлы": ""}  # словарь с результатами


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
    :param get_list: признак нужно ли отдать результат в виде словаря
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


def host_range_ping(get_list=False):
    """
    Функция запрашивает первоначальный адрес и количество адресов,
    и далее, если в последнем октете есть возможность увеличивать адрес,
    функция возвращает список возможных адресов.
    Затем проверяет доступность этих адресов с пом ф-ции host_ping()
    :param get_list:
    :return:
    """

    while True:
        start_ip = input("Введите первоначальный адрес: ")
        try:
            ipv4_start = check_is_ipaddress(start_ip)
            last_oct = int(start_ip.split('.')[3])       # смотрим чему равен последний октет
            break
        except Exception as e:
            print(e)
    while True:
        end_ip = input("Сколько адресов проверить?: ")
        if not end_ip.isnumeric():
            print("Необходимо ввести число")
        else:
            if (last_oct + int(end_ip)) > 255+1:  # По условию меняется только последний октет
                print(f"Можем менять только последний октет, "
                      f"т.е. максимальное число хостов {255+1 - last_oct}")
            else:
                break
    host_list = []
    [host_list.append(str(ipv4_start + x)) for x in range(int(end_ip))]  # формируем список ip
    if not get_list:   # передаём список в функцию для проверки
        host_ping(host_list)
    else:
        return host_ping(host_list, True)


if __name__ == "__main__":
    host_range_ping()
