import pytest
from main import parse_condition, apply_filter, apply_aggregation

# Фиктивные данные, соответствующие products.csv
TEST_DATA = [
    {"name": "iphone 15 pro", "brand": "apple", "price": "999", "rating": "4.9"},
    {"name": "galaxy s23 ultra", "brand": "samsung", "price": "1199", "rating": "4.8"},
    {"name": "redmi note 12", "brand": "xiaomi", "price": "199", "rating": "4.6"},
    {"name": "poco x5 pro", "brand": "xiaomi", "price": "299", "rating": "4.4"},
]

# parse_condition

def test_parse_condition_greater():
    col, op, val = parse_condition("price>500")
    assert col == "price"
    assert op == ">"
    assert val == "500"

def test_parse_condition_less():
    col, op, val = parse_condition("price<300")
    assert col == "price"
    assert op == "<"
    assert val == "300"

def test_parse_condition_equal():
    col, op, val = parse_condition("brand=xiaomi")
    assert col == "brand"
    assert op == "="
    assert val == "xiaomi"

def test_parse_condition_invalid():
    with pytest.raises(ValueError):
        parse_condition("price>>500")

# apply_filter

def test_apply_filter_price_gt():
    filtered = apply_filter(TEST_DATA, "price>500")
    assert len(filtered) == 2
    for row in filtered:
        assert float(row["price"]) > 500

def test_apply_filter_price_lt():
    filtered = apply_filter(TEST_DATA, "price<300")
    assert len(filtered) == 2
    for row in filtered:
        assert float(row["price"]) < 300

def test_apply_filter_brand_eq():
    filtered = apply_filter(TEST_DATA, "brand=xiaomi")
    assert len(filtered) == 2
    for row in filtered:
        assert row["brand"] == "xiaomi"

def test_apply_filter_name_eq():
    filtered = apply_filter(TEST_DATA, "name=iphone 15 pro")
    assert len(filtered) == 1
    assert filtered[0]["name"] == "iphone 15 pro"

def test_apply_filter_no_condition_returns_all():
    result = apply_filter(TEST_DATA, None)
    assert result == TEST_DATA

# apply_aggregation

def test_apply_aggregation_avg_price():
    result = apply_aggregation(TEST_DATA, "price=avg")
    assert result["function"] == "avg"
    assert result["column"] == "price"
    expected_avg = (999 + 1199 + 199 + 299) / 4
    assert abs(result["value"] - expected_avg) < 1e-6

def test_apply_aggregation_min_price():
    result = apply_aggregation(TEST_DATA, "price=min")
    assert result["function"] == "min"
    assert result["value"] == 199

def test_apply_aggregation_max_price():
    result = apply_aggregation(TEST_DATA, "price=max")
    assert result["function"] == "max"
    assert result["value"] == 1199

def test_apply_aggregation_sum_price():
    result = apply_aggregation(TEST_DATA, "price=sum")
    assert result["function"] == "sum"
    assert result["value"] == (999 + 1199 + 199 + 299)

def test_apply_aggregation_count_price():
    result = apply_aggregation(TEST_DATA, "price=count")
    assert result["function"] == "count"
    assert result["value"] == 4

def test_apply_aggregation_invalid_function():
    with pytest.raises(ValueError):
        apply_aggregation(TEST_DATA, "price=unknown")