"""Модуль для работы пользователя с телефонным справочником.

Хранение данных реализовано с помощью csv-файла с разделителем в виде ";".
Данные в файле хранятся в следующем виде:
"Имя";"Отчество";"Фамилия";"Компания";"Моб. тел";"Рабочий тел."
Управление происходит при помощи аргументов командной строки.
Пользоваетлю доступны следующие команды:
- Вывод постранично записей из справочника - команда get
    параметр -pg: номер страницы. Одна страница вмещает 10 контактов.
- Добавление новой записи в справочник - команда add
    параметры -n, -p, -s, -c, -mp, -wp: имя, отчество, фамилия,
    компания, мобильный и рабочий телефон соответственно.
- Поиск записей в справочнике - команда search
    параметры -sn, ss, sp: имя, фамилия и телефон, соответственно,
    по которым нужно производить поиск.
- Редактирования записи в справочнике - команда edit
    параметры -sn, -ss, sp: имя, фамилия и телефон, соответственно,
    по которым нужно найти запись, которая будет отредактирована.
    параметры -n, -p, -s, -c, -mp, -wp: новые даныне - имя, отчество, фамилия,
    компания, мобильный и рабочий телефон соответственно.
"""
import csv

from configs import configure_argument_parser

FILE_NAME = "phonebook.csv"
PAGE_SIZE = 10


def get_contacts_by_page(page: str | None) -> None:
    """Печатает контакты с заданной странице.

    На одной странице 10 контактов.
    Если страница не передана в запросе, то печатает все контакты.
    """
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if not page:
            start, end = 0, len(lines)
        else:
            page = int(page)
            start = max((page - 1), 0) * PAGE_SIZE
            start = start if start < len(lines) else 0
            end = min(len(lines), start + 10)
        for line in lines[start:end]:
            print(*line.split(";"))


def add_new_contact(
    name: str | None,
    patronimic: str | None,
    surname: str | None,
    company: str | None,
    mobile_phone: str | None,
    work_phone: str | None,
) -> None:
    """Добавляет новый контакт."""
    with open(FILE_NAME, "a", encoding="utf-8") as file:
        writer = csv.writer(file, dialect="unix", delimiter=";")
        writer.writerow(
            (name, patronimic, surname, company, mobile_phone, work_phone))
    print(f"Контакт {name} {surname} успешно добавлен")


def remove_extra_char_from_phone(phone_number: str) -> str:
    """Удаляет лишние символы из номера телефона контакт."""
    if not phone_number:
        return phone_number
    if phone_number[:2] == "+7":
        phone_number = "8" + phone_number[2:]
    correct_phone = "".join([i for i in phone_number if i.isdigit()])
    return correct_phone


def get_searching_contacts(
    search_name: str | None,
    search_surname: str | None,
    search_phone: str | None
) -> list:
    """Возвращает контакты, отвечающие поисковому запросу."""
    searching_results = []
    not_none_arguments_count = 3 - [
        search_name, search_surname, search_phone].count(None)
    search_phone = remove_extra_char_from_phone(search_phone)
    search_name = search_name.lower() if search_name else None
    search_surname = search_surname.lower() if search_surname else None

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        for line in file.readlines():
            result_list = []
            name, _, surname, _, mobile_phone, work_phone = line.split(";")
            name = name.replace('"', "")
            surname = surname.replace('"', "")
            result_list.append(
                search_name and name.lower().startswith(search_name))
            result_list.append(
                search_surname and surname.lower().startswith(search_surname)
            )
            if search_phone:
                mobile_phone = remove_extra_char_from_phone(mobile_phone)
                work_phone = remove_extra_char_from_phone(work_phone)
                result_list.append(
                    mobile_phone.startswith(search_phone)
                    or work_phone.startswith(search_phone)
                )
            if result_list.count(True) == not_none_arguments_count:
                searching_results.append(line)
    return searching_results


def search_contact(
        search_name: str | None,
        search_surname: str | None,
        search_phone: str | None
) -> None:
    """Печатает список найденных контактов."""
    contacts = get_searching_contacts(
        search_name, search_surname, search_phone)
    if not contacts:
        print("Контакты по запросу отсутствуют в справочнике")
        return
    for line in contacts:
        print(*line.split(";"))


def edit_contact(
        data: dict,
        search_name: str | None,
        search_surname: str | None,
        search_phone: str | None
) -> None:
    """Изменяет данные контакта."""
    contacts = get_searching_contacts(
        search_name, search_surname, search_phone)
    if not contacts:
        print("Контакты по запросу отсутствуют в справочнике")
        return
    if len(contacts) > 1:
        print(
            'Найдено несколько контактов, удовлетворяющих запросу.'
            'Уточните запрос, чтобы остался один, который вы хотите изменить'
        )
        for contact in contacts:
            print(*contact.split(";"))
        return
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        old_phonebook = file.read()
    old_contact_data = contacts[0].strip().replace('"', '')
    name, patronimic, surname, company, mobile_phone, work_phone = old_contact_data.split(';')

    new_name = data["name"] if data["name"] else name
    new_patronimic = data["patronimic"] if data["patronimic"] else patronimic
    new_surname = data["surname"] if data["surname"] else surname
    new_company = data["company"] if data["company"] else company
    new_mobile_phone = data[
        "mobile_phone"] if data["mobile_phone"] else mobile_phone
    new_work_phone = data["work_phone"] if data["work_phone"] else work_phone

    new_contact_data = [
        new_name,
        new_patronimic,
        new_surname,
        new_company,
        new_mobile_phone,
        new_work_phone,
    ]
    new_contact = ";".join([f'"{param}"' for param in new_contact_data]) + "\n"
    new_phonebook = old_phonebook.replace(contacts[0], new_contact)
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        file.write(new_phonebook)


def get_function(
        parser_command: str,
        pages_count: int,
        search_fields: dict,
        data_fields: dict
):
    """Возвращает результат работы функции в зависимости от режима работы."""
    if parser_command == "get":
        return get_contacts_by_page(pages_count)
    if parser_command == "add":
        return add_new_contact(**data_fields)
    if parser_command == "search":
        return search_contact(**search_fields)
    if parser_command == "edit":
        return edit_contact(data_fields, **search_fields)


def main() -> None:
    arg_parser = configure_argument_parser()
    args = arg_parser.parse_args()
    parser_command = args.command
    if args.pages is not None:
        if not args.pages.isdigit():
            print('Номер страницы должен быть числом большим нуля')
            return
    pages_count = args.pages
    search_fields = {
        "search_name": args.searchname,
        "search_surname": args.searchsurname,
        "search_phone": args.searchphone,
    }
    data_fields = {
        "name": args.name,
        "patronimic": args.patronimic,
        "surname": args.surname,
        "company": args.company,
        "mobile_phone": args.mobilephone,
        "work_phone": args.workphone,
    }
    get_function(parser_command, pages_count, search_fields, data_fields)


if __name__ == "__main__":
    main()
