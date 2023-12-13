import pytest
from utils import *
import os

abs_path_geojson_test = r'C:\Users\User\OneDrive\Pulpit\Marcysia\github\visualisation_geographic_data\tests\test_examples\pollution_coordinates_test_copy.geojson'
abs_path_geojson_init_test = r'C:\Users\User\OneDrive\Pulpit\Marcysia\github\visualisation_geographic_data\data\wojewodztwa-min.geojson'
abs_path_excel_test = r'C:\Users\User\OneDrive\Pulpit\Marcysia\github\visualisation_geographic_data\data\pollution_data.xlsx'


@pytest.fixture()
def add_area_init():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = pd.ExcelFile(abs_path_excel_test)
    add_area(test_data_geojson, test_data_excel)

    return test_data_geojson


def test_add_area_pass(add_area_init):
    assert ("area" in add_area_init['features'][0]['properties']) is True


@pytest.fixture()
def add_area_invalid_excel_path():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = r'data/pollution_data.xlsx'
    return test_data_geojson, test_data_excel


def test_add_area_invalid_excel_path(add_area_invalid_excel_path):
    with pytest.raises(TypeError):
        add_area(add_area_invalid_excel_path[0], add_area_invalid_excel_path[1])


@pytest.fixture()
def add_area_invalid_excel_field():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = r'test_examples/pollution_data_test_1.xlsx'
    return test_data_geojson, test_data_excel


def test_add_area_invalid_excel_field(add_area_invalid_excel_field):
    with pytest.raises(ValueError):
        add_area(add_area_invalid_excel_field[0], add_area_invalid_excel_field[1])


@pytest.fixture()
def add_area_invalid_geojson_field():
    with open(r'test_examples/wojewodztwa_test_1.geojson', 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = abs_path_excel_test
    return test_data_geojson, test_data_excel


def test_add_area_invalid_geojson_field(add_area_invalid_geojson_field):
    with pytest.raises(ValueError):
        add_area(add_area_invalid_geojson_field[0], add_area_invalid_geojson_field[1])


@pytest.fixture()
def add_data_per_km2_init():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = pd.ExcelFile(abs_path_excel_test)
    add_data_per_km2(test_data_geojson, test_data_excel)

    return test_data_geojson


def test_add_data_per_km2_pass(add_data_per_km2_init):
    assert ("co2_2020_per_km_sq" in add_data_per_km2_init['features'][0]['properties']) is True


@pytest.fixture()
def add_data_per_km2_invalid_excel_path():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = r'data/pollution_data.xlsx'
    return test_data_geojson, test_data_excel


def test_add_data_per_km2_invalid_excel_path(add_data_per_km2_invalid_excel_path):
    with pytest.raises(TypeError):
        add_data_per_km2(add_data_per_km2_invalid_excel_path[0], add_data_per_km2_invalid_excel_path[1])


@pytest.fixture()
def add_data_per_km2_invalid_excel_sheets():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = r'test_examples/pollution_data_test_2.xlsx'
    return test_data_geojson, test_data_excel


def test_add_data_per_km2_invalid_excel_sheets(add_data_per_km2_invalid_excel_sheets):
    with pytest.raises(TypeError):
        add_data_per_km2(add_data_per_km2_invalid_excel_sheets[0], add_data_per_km2_invalid_excel_sheets[1])


@pytest.fixture()
def add_data_per_km2_invalid_excel_field():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = r'test_examples/pollution_data_test_1.xlsx'
    return test_data_geojson, test_data_excel


def test_add_data_per_km2_invalid_excel_field(add_data_per_km2_invalid_excel_field):
    with pytest.raises(ValueError):
        add_data_per_km2(add_data_per_km2_invalid_excel_field[0], add_data_per_km2_invalid_excel_field[1])


@pytest.fixture()
def add_data_per_km2_invalid_geojson_field():
    with open(r'test_examples/wojewodztwa_test_1.geojson', 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = abs_path_excel_test
    return test_data_geojson, test_data_excel


def test_add_data_per_km2_invalid_geojson_field(add_data_per_km2_invalid_geojson_field):
    with pytest.raises(ValueError):
        add_data_per_km2(add_data_per_km2_invalid_geojson_field[0], add_data_per_km2_invalid_geojson_field[1])


@pytest.fixture()
def add_data_per_km2_divide_by_zero():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = r'test_examples/pollution_data_test_3.xlsx'
    return test_data_geojson, test_data_excel


def test_add_data_per_km2_divide_by_zero(add_data_per_km2_divide_by_zero):
    with pytest.raises(ZeroDivisionError):
        add_data_per_km2(add_data_per_km2_divide_by_zero[0], add_data_per_km2_divide_by_zero[1])


@pytest.fixture
def save_data_init():
    data_geojson = {"key": "value"}
    path = r'test_examples/test_save_data_result.json'
    return path, data_geojson


def test_save_data_pass(save_data_init):
    save_data(save_data_init[0], save_data_init[1])

    assert os.path.exists(save_data_init[0])

    with open(save_data_init[0], 'r') as f:
        saved_data = json.load(f)
        assert saved_data == save_data_init[1]


@pytest.fixture
def save_data_fail():
    class TestClass:
        def __init__(self, field):
            self.field = field

    data_geojson = TestClass("field")
    path = r'test_examples/test_save_data_result_fail.json'
    return path, data_geojson


def test_save_data_fail(save_data_fail):
    with pytest.raises(TypeError):
        save_data(save_data_fail[0], save_data_fail[1])


@pytest.fixture()
def add_data_absolute_init():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = pd.ExcelFile(abs_path_excel_test)
    add_data_absolute(test_data_geojson, test_data_excel)

    return test_data_geojson


def test_add_data_absolute_pass(add_data_absolute_init):
    assert ("co2_2020" in add_data_absolute_init['features'][0]['properties']) is True


@pytest.fixture()
def add_data_absolute_invalid_excel_path():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = r'data/pollution_data.xlsx'
    return test_data_geojson, test_data_excel


def test_add_data_absolute_invalid_excel_path(add_data_absolute_invalid_excel_path):
    with pytest.raises(TypeError):
        add_data_absolute(add_data_absolute_invalid_excel_path[0], add_data_absolute_invalid_excel_path[1])


@pytest.fixture()
def add_data_absolute_invalid_excel_sheets():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = r'test_examples/pollution_data_test_2.xlsx'
    return test_data_geojson, test_data_excel


def test_add_data_absolute_invalid_excel_sheets(add_data_absolute_invalid_excel_sheets):
    with pytest.raises(TypeError):
        add_data_absolute(add_data_absolute_invalid_excel_sheets[0], add_data_absolute_invalid_excel_sheets[1])


@pytest.fixture()
def add_data_absolute_invalid_excel_field():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = r'test_examples/pollution_data_test_1.xlsx'
    return test_data_geojson, test_data_excel


def test_add_data_absolute_invalid_excel_field(add_data_absolute_invalid_excel_field):
    with pytest.raises(ValueError):
        add_data_absolute(add_data_absolute_invalid_excel_field[0], add_data_absolute_invalid_excel_field[1])


@pytest.fixture()
def add_data_absolute_invalid_geojson_field():
    with open(r'test_examples/wojewodztwa_test_1.geojson', 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = abs_path_excel_test
    return test_data_geojson, test_data_excel


def test_add_data_absolute_invalid_geojson_field(add_data_absolute_invalid_geojson_field):
    with pytest.raises(ValueError):
        add_data_absolute(add_data_absolute_invalid_geojson_field[0], add_data_absolute_invalid_geojson_field[1])


def test_init_data_json_decode_error():
    with pytest.raises(json.JSONDecodeError):
        init_data(r'test_examples/test_init_data.json', abs_path_geojson_test, abs_path_excel_test)


def test_init_data_invalid_init_file():
    with pytest.raises(TypeError):
        init_data(r'\data\wojewodztwa-min.geojson', abs_path_geojson_test, abs_path_excel_test)
