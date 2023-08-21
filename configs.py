import argparse


def configure_argument_parser() -> argparse.ArgumentParser:
    """Возвращает парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Телефонный справочник")
    parser.add_argument(
        "command", help="Команда", choices=["get", "edit", "add", "search"]
    )
    parser.add_argument(
        "-pg", "--pages", help="Количество страниц вывода контактов")
    parser.add_argument("-n", "--name", help="Имя")
    parser.add_argument("-p", "--patronimic", help="Отчество")
    parser.add_argument("-s", "--surname", help="Фамилия")
    parser.add_argument("-c", "--company", help="Компания")
    parser.add_argument("-mp", "--mobilephone", help="Мобильный телефон")
    parser.add_argument("-wp", "--workphone", help="Домашний телефон")
    parser.add_argument("-sn", "--searchname", help="Имя для поиска")
    parser.add_argument("-ss", "--searchsurname", help="Фамилия для поиска")
    parser.add_argument("-sp", "--searchphone", help="Телефон для поиска")
    return parser
