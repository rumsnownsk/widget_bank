from src.search_operations import get_all_available_states


def main():
    print('\n')
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями\n")

    print("""Выберите необходимый пункт меню: \n
        1. Получить информацию о транзакциях из JSON-файла\n
        2. Получить информацию о транзакциях из CSV-файла\n
        3. Получить информацию о транзакциях из XLSX-файла
        """)

    select_type_file = int(input("Выбрать цифру и нажать Enter: "))
    type_files = {
        "1": "JSON",
        "2": "CSV",
        "3": "XLSX"
    }

    if select_type_file in [1, 2, 3]:
        print(f"Для обработки выбран {type_files.get(str(select_type_file))}-файл")
    else:
        select_type_file = 1
        print("Ошибка при выборе пункта меню\n")
        print("По умолчанию для обработки выбран JSON-файл")

    print("Доступные для фильтровки статусы операций: \n")
    dict_states = get_all_available_states()
    for key, value in dict_states.items():
        print(key, value)

    print("\nВведите статус, по которому необходимо выполнить фильтрацию, \n или укажите цифру: ")


    confirm_status = True
    while confirm_status:
        raw_select_state = input("Ваш выбор: ")


        if raw_select_state.isdigit() and int(raw_select_state) in list(dict_states.keys()):
            select_state = int(raw_select_state)
            print(f"Операции отфильтрованы по статусу '{dict_states[select_state]}'")
            confirm_status = False

        elif raw_select_state.lower() in dict_states.values():
            print(f"Операции отфильтрованы по статусу '{raw_select_state}'")
            confirm_status = False
        elif raw_select_state.lower() not in dict_states.values():
            print(f"Статус операции '{raw_select_state}' недоступен\n " )
            print("Введите статус, по которому необходимо выполнить фильтрацию" )
            print(f"Доступные для фильтровки статусы операций: \n")

            for key, value in dict_states.items():
                print(key, value)


if __name__ == "__main__":
    main()
