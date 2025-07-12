import argparse
import csv
from tabulate import tabulate
from colorama import init, Fore

init(autoreset=True)


def load_csv(file_path):
    """Загрузка CSV-файла в список словарей."""
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)


def parse_condition(condition):
    """Разбор условия фильтрации вида 'price>500'."""
    operators = ['>', '<', '=']
    for op in operators:
        if op in condition:
            parts = condition.split(op, 1)
            if len(parts) == 2:
                return parts[0].strip(), op, parts[1].strip()
    raise ValueError(f"Неверный формат условия фильтрации: {condition}")


def apply_filter(data, condition):
    """Применение фильтрации к данным."""
    if not condition:
        return data

    column, operator, value = parse_condition(condition)

    filtered_data = []
    for row in data:
        if column not in row:
            raise ValueError(f"В данных нет колонки '{column}'")
        row_value = row[column]

        try:
            row_value_num = float(row_value)
            value_num = float(value)
            if operator == '>' and row_value_num > value_num:
                filtered_data.append(row)
            elif operator == '<' and row_value_num < value_num:
                filtered_data.append(row)
            elif operator == '=' and row_value_num == value_num:
                filtered_data.append(row)
        except ValueError:
            if operator == '=' and row_value == value:
                filtered_data.append(row)

    return filtered_data


def apply_aggregation(data, condition):
    """
    Применение агрегации к данным.
    Поддерживаемые функции: avg, min, max, sum, count.
    """
    if not condition:
        return None

    if '=' not in condition:
        raise ValueError(f"Неверный формат агрегации: {condition}")

    column, func = condition.split('=', 1)
    column = column.strip()
    func = func.strip().lower()

    if func == 'count':
        return {'function': func, 'column': column, 'value': len(data)}

    if not data:
        print(Fore.YELLOW + "Нет данных для агрегации")
        return None

    try:
        values = [float(row[column]) for row in data if column in row]
    except ValueError:
        raise ValueError(f"Невозможно агрегировать нечисловую колонку: {column}")

    if not values:
        print(Fore.YELLOW + f"В колонке '{column}' нет числовых данных")
        return None

    if func == 'avg':
        result = sum(values) / len(values)
    elif func == 'min':
        result = min(values)
    elif func == 'max':
        result = max(values)
    elif func == 'sum':
        result = sum(values)
    else:
        raise ValueError(f"Неизвестная функция агрегации: {func}")

    return {'function': func, 'column': column, 'value': result}


def display_results(data, aggregation=None):
    """Вывод результатов в виде таблицы."""
    if aggregation:
        headers = ["Функция", "Колонка", "Значение"]
        rows = [[aggregation['function'], aggregation['column'], aggregation['value']]]
        print(Fore.CYAN + tabulate(rows, headers=headers, tablefmt="grid"))
    elif data:
        headers = data[0].keys()
        rows = [list(row.values()) for row in data]
        print(Fore.GREEN + tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print(Fore.YELLOW + "Нет данных для отображения")


def main():
    parser = argparse.ArgumentParser(
        description='Обработка CSV-файла с фильтрацией и агрегацией.'
    )
    parser.add_argument(
        '--file', required=True,
        help='Путь к CSV-файлу'
    )
    parser.add_argument(
        '--where',
        help='Условие фильтрации, например "price>500" или "name=John"'
    )
    parser.add_argument(
        '--aggregate',
        help='Агрегация, например "price=avg". Поддерживает: avg, min, max, sum, count'
    )

    args = parser.parse_args()

    try:
        data = load_csv(args.file)

        if not data:
            print(Fore.YELLOW + "CSV-файл пустой")
            return

        filtered_data = apply_filter(data, args.where) if args.where else data
        aggregation_result = apply_aggregation(filtered_data, args.aggregate) if args.aggregate else None

        if args.aggregate:
            display_results(None, aggregation_result)
        else:
            display_results(filtered_data)

    except Exception as e:
        print(Fore.RED + f"Ошибка: {str(e)}")


if __name__ == '__main__':
    main()
