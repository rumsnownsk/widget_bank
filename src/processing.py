def filter_by_state(data:list, state:str = "EXECUTED") -> list:
    """Функция возвращает список словарей, у которых state соответствует"""
    return [item for item in data if item['state'] == state]

def sort_by_date(data:list, sort_by:str = "from_last") -> list:

    return sorted(data, key= lambda x: x['date'], reverse=sort_by == 'from_last')
