import csv
import argparse
from typing import List, Dict, Tuple, Optional
from tabulate import tabulate


def parse_where(condition: str) -> Tuple[str, str, object]:
    """
    Разбирает строку условия фильтрации.

    Примеры:
        "rating>4.5" → ("rating", ">", 4.5)

    :param condition: строка с условием
    :return: кортеж (column, operator, value)
    :raises ValueError: если формат некорректен
    """
    if '>' in condition:
        column, value = condition.split('>')
        return column.strip(), '>', float(value.strip())
    elif '<' in condition:
        column, value = condition.split('<')
        return column.strip(), '<', float(value.strip())
    elif '=' in condition:
        column, value = condition.split('=')
        return column.strip(), '=', value.strip()
    else:
        raise ValueError("Поддерживаются только операторы >, < и =")


def matches(
        row: Dict[str, str],
        column: str,
        op: str,
        value: object
) -> bool:
    """
    Проверяет, соответствует ли строка условию фильтрации.
    Поддерживает числовые и строковые сравнения.
    """
    cell_value = row[column]
    try:
        cell_value = float(cell_value)
        value = float(value)
    except ValueError:
        # Сравнение строк
        pass

    if op == '>':
        return cell_value > value
    elif op == '<':
        return cell_value < value
    elif op == '=':
        return str(cell_value) == str(value)
    return False


def parse_aggregate(condition: str) -> Tuple[str, str]:
    """
    Разбирает строку агрегации в формате "column=operation".

    Примеры:
        "rating=min" → ("min", "rating")

    :param condition: строка с условием агрегации
    :return: кортеж (operation, column)
    :raises ValueError: если формат некорректен
    """
    if '=' not in condition:
        raise ValueError("Агрегация должна иметь формат column=operation")
    column, operation = condition.split('=')
    operation = operation.strip().lower()
    column = column.strip()

    if operation not in ('avg', 'min', 'max'):
        raise ValueError("Поддерживаются только операции: avg, min, max")
    return operation, column


def aggregate_rows(
        rows: List[Dict[str, str]],
        operation: str,
        column: str
) -> Optional[float]:
    """
    Выполняет агрегирующую операцию по колонке.

    :param rows: список словарей с данными
    :param operation: 'avg', 'min' или 'max'
    :param column: колонка для агрегации
    :return: результат агрегирования или None, если данных нет
    """
    values = [float(row[column]) for row in rows]
    if not values:
        return None
    if operation == 'avg':
        return sum(values) / len(values)
    elif operation == 'min':
        return min(values)
    elif operation == 'max':
        return max(values)


def read_csv(file_path: str) -> List[Dict[str, str]]:
    """Читает CSV файл и возвращает список словарей."""
    with open(file_path, newline='') as f:
        return list(csv.DictReader(f))


def apply_filter(
        rows: List[Dict[str, str]],
        condition: str
) -> List[Dict[str, str]]:
    """Фильтрует строки по условию."""
    column, op, value = parse_where(condition)
    return [row for row in rows if matches(row, column, op, value)]


def print_aggregation(
        rows: List[Dict[str, str]],
        aggregate_arg: str
) -> None:
    """Вычисляет и выводит результат агрегации."""
    operation, agg_column = parse_aggregate(aggregate_arg)
    result = aggregate_rows(rows, operation, agg_column)
    table = [{f"{operation}({agg_column})": result}]
    print(tabulate(table, headers="keys", tablefmt="fancy_grid"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help='CSV файл')
    parser.add_argument('--where', help='Фильтр, например: rating>4.5')
    parser.add_argument('--aggregate', help='Агрегация, например: rating=min')
    args = parser.parse_args()

    rows = read_csv(args.file)

    if args.where:
        rows = apply_filter(rows, args.where)

    if args.aggregate:
        print_aggregation(rows, args.aggregate)
    else:
        print(tabulate(rows, headers="keys", tablefmt="fancy_grid"))


if __name__ == '__main__':
    main()
