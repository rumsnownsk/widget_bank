def filter_by_state(data:list, state:str = "EXECUTED") -> list:
    new_list = []

    for item in data:
        if item['state'] == state:
            new_list.append(item)

    return new_list