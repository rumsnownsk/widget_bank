def filter_by_state(data:list, state:str = "EXECUTED") -> list:
    return [item for item in data if item['state'] == state]