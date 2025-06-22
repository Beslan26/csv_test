import pytest
from app.main import (
    parse_where,
    matches,
    parse_aggregate,
    aggregate_rows,
    apply_filter,
)


def test_parse_where_greater():
    """Парсинг условия с оператором '>'"""
    assert parse_where("rating>4.5") == ("rating", ">", 4.5)


def test_parse_where_less():
    """Парсинг условия с оператором '<'"""
    assert parse_where("rating<4.0") == ("rating", "<", 4.0)


def test_parse_where_equal():
    """Парсинг условия с оператором '=' (строковое значение)"""
    assert parse_where("brand=apple") == ("brand", "=", "apple")


def test_parse_where_invalid():
    """Должен вызвать ошибку при отсутствии допустимого оператора"""
    with pytest.raises(ValueError):
        parse_where("invalid")


def test_matches_numeric():
    """Проверка числовых сравнений"""
    row = {"price": "100"}
    assert matches(row, "price", ">", 50)
    assert matches(row, "price", "<", 200)
    assert matches(row, "price", "=", 100)


def test_matches_string():
    """Проверка строкового сравнения"""
    row = {"brand": "apple"}
    assert matches(row, "brand", "=", "apple")
    assert not matches(row, "brand", "=", "samsung")


def test_parse_aggregate_valid():
    """Корректный парсинг агрегации"""
    assert parse_aggregate("rating=min") == ("min", "rating")
    assert parse_aggregate("price=avg") == ("avg", "price")


def test_parse_aggregate_invalid_format():
    """Ошибка при неправильном формате агрегации"""
    with pytest.raises(ValueError):
        parse_aggregate("invalid_format")


def test_parse_aggregate_unsupported_op():
    """Ошибка при неподдерживаемой операции агрегации"""
    with pytest.raises(ValueError):
        parse_aggregate("rating=median")


def test_aggregate_avg():
    """Проверка среднего значения"""
    rows = [{"price": "100"}, {"price": "200"}, {"price": "300"}]
    assert aggregate_rows(rows, "avg", "price") == 200.0


def test_aggregate_min():
    """Проверка минимального значения"""
    rows = [{"rating": "4.9"}, {"rating": "4.5"}, {"rating": "4.8"}]
    assert aggregate_rows(rows, "min", "rating") == 4.5


def test_aggregate_max():
    """Проверка максимального значения"""
    rows = [{"rating": "4.1"}, {"rating": "4.6"}, {"rating": "4.2"}]
    assert aggregate_rows(rows, "max", "rating") == 4.6


def test_aggregate_empty():
    """Проверка агрегации пустого списка"""
    assert aggregate_rows([], "avg", "price") is None


def test_apply_filter():
    """Проверка фильтрации по условию"""
    rows = [
        {"price": "100", "brand": "apple"},
        {"price": "200", "brand": "samsung"},
        {"price": "50", "brand": "apple"},
    ]
    filtered = apply_filter(rows, "price>99")
    assert len(filtered) == 2
    assert all(float(row["price"]) > 99 for row in filtered)

    filtered_eq = apply_filter(rows, "brand=apple")
    assert len(filtered_eq) == 2
    assert all(row["brand"] == "apple" for row in filtered_eq)
