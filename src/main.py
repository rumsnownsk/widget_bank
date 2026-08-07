import re
from typing import Dict

from src.processing import sort_by_date
from src.search_operations import get_all_available_states, process_bank_search
from src.utils.dataframe_to_json import dataframe_to_json
from src.utils.load_transactions import load_transactions
from src.widget import get_date, mask_account_card


def main() -> tuple[str, list[Dict]]:
    """
    Основной интерактивный цикл программы widget_bank для фильтрации и вывода транзакций.

    Функция запрашивает у пользователя:
      - тип файла (JSON/CSV/XLSX) — используется только для UI-сообщения,
        реальные данные передаются через аргумент `data`;
      - статус транзакции для фильтрации (по номеру или по названию);
      - необходимость сортировки по дате и её направление;
      - фильтрацию только по рублёвым операциям;
      - поиск по ключевому слову в описании транзакции.

    После применения всех фильтров и сортировок возвращает:
      1. выбранный статус (в нижнем регистре);
      2. итоговый список отфильтрованных и отсортированных транзакций.


    :param :
    :return:
    """
    print("\n")
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями\n")

    # 1. Предложение выбора типа файла для загрузки данных
    print("""Выберите необходимый пункт меню (указать номер пункта меню): \n
    1. Получить информацию о транзакциях из JSON-файла\n
    2. Получить информацию о транзакциях из CSV-файла\n
    3. Получить информацию о транзакциях из XLSX-файла
        """)

    user_input = input("Выбрать цифру и нажать Enter: ").strip()
    type_files = {"1": "JSON", "2": "CSV", "3": "XLSX"}

    if user_input in type_files:
        print(f"Для обработки выбран {type_files.get(user_input)}-файл")
    else:
        print("Ошибка при выборе пункта меню\n")
        print("По умолчанию для обработки выбран JSON-файл")

    # 2.1 Приведение данных из файлов csv и xlsx к JSON-формату
    if user_input == "2":
        transactions = dataframe_to_json("transactions.csv")
    elif user_input == "3":
        transactions = dataframe_to_json("transactions_excel.xlsx")
    else:
        transactions = load_transactions()

    # 2. Предложение выбора Статуса операции
    print("Доступные для фильтровки статусы операций: \n")
    dict_states = get_all_available_states(transactions)
    for key, value in dict_states.items():
        print(key, value)

    print("\nВведите статус, по которому необходимо выполнить фильтрацию, или укажите цифру: ")
    confirm_status = True
    select_state = ""
    while confirm_status:
        raw_select_state = input("Ваш выбор: ")

        if raw_select_state.isdigit() and int(raw_select_state) in list(dict_states.keys()):
            select_state = dict_states[int(raw_select_state)]
            print(f"Операции отфильтрованы по статусу '{select_state}'\n")
            confirm_status = False

        elif raw_select_state.lower() in dict_states.values():
            select_state = raw_select_state.lower()
            print(f"Операции отфильтрованы по статусу '{raw_select_state}'\n")
            confirm_status = False
        elif raw_select_state.lower() not in dict_states.values():
            print(f"Статус операции '{raw_select_state}' недоступен\n ")
            print("Введите статус, по которому необходимо выполнить фильтрацию")
            print("Доступные для фильтровки статусы операций: \n")

            for key, value in dict_states.items():
                print(key, value)

    print(f"\nДелать сортировку или фильтрацию по разным условиям?\n"
          f"1. Да, хочу отфильтровать (по умолчанию)\n"
          f"2. Нет (вывести транзакции по статусу \"{select_state}\")")

    user_input = input("> ").strip()

    if user_input == "": user_input = "1"

    if not user_input.isdigit() or int(user_input) not in (1, 2):
        print("Неверный ввод. Будем использовать вариант по умолчанию (1).")

    # Если выбрали «Нет» (2), сразу возвращаем без сортировки
    if user_input == "2":
        return select_state, transactions

    sorted_by_date = input("Отсортировать операции по дате (по умолчанию - Нет)? (Да/Нет): ").strip()

    direction_sorted = ""
    if sorted_by_date.lower() in ("да", "д", "yes", "y"):
        direction_sorted = input(
            "Отсортировать по возрастанию(по умолчанию) или по убыванию? (по возрастанию/по убыванию): "
        ).strip()

    filter_by_rub = input("Выводить только рублевые транзакции (по умолчанию - Нет)? (Да/Нет): ").strip()

    sorted_by_word = input("""
    Отфильтровать список транзакций по определенному слову в описании?
    Напишите слово (минимум 3 буквы) или оставьте поле пустым :
     """).strip()

    result_data = process_bank_search(transactions, select_state)

    # сортировка списка по дате возрастания или убывания
    if sorted_by_date.lower() == "да":
        if direction_sorted == "по возрастанию" or direction_sorted == "":
            sort_dir = "from_first"
        elif direction_sorted == "по убыванию":
            sort_dir = "from_last"
        result_data = sort_by_date(result_data, sort_dir)

    # фильтрация списка по валюте в Рублях
    if filter_by_rub.lower() == "да":
        result_data = [item for item in result_data if item["operationAmount"]["currency"]["code"] == "RUB"]

    if len(sorted_by_word) >= 3 and isinstance(sorted_by_word, str):
        sorted_by_word = sorted_by_word.lower()
        pattern = re.compile(re.escape(sorted_by_word))

        result_data = [
            item
            for item in result_data
            if (word := item.get("description")) is not None and isinstance(word, str) and pattern.search(word.lower())
        ]

    return select_state, result_data


if __name__ == "__main__":

    state, data = main()

    print("\n")

    if not data:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print("Распечатываю итоговый список транзакций...\n")
        for item in data:
            operationAmount = item.get("operationAmount")
            second_string = f"{mask_account_card(item.get('to', ''))}"

            desc = item.get("description") or ""
            if "перевод" in (desc.lower()):
                second_string = f"{mask_account_card(item.get('from', ''))} -> {mask_account_card(item.get('to', ''))}"

            print(f"""
            {get_date(item.get('date', ''))}  {item.get('description')}
            {second_string}
            Сумма: {operationAmount['amount']} {operationAmount['currency']['name']}
            """)

        print(f"Всего банковских операций в выборке (по операции '{state}'): {len(data)};\n")
