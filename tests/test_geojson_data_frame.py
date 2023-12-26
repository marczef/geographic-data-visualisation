import pytest
from src.utils import *
from contextlib import nullcontext as does_not_raise
import os

abs_path_geojson_test = r'C:\Users\User\OneDrive\Pulpit\Marcysia\github\geographic-data-visualisation\tests\test_examples\pollution_coordinates_test_copy.geojson'
abs_path_geojson_init_test = r'C:\Users\User\OneDrive\Pulpit\Marcysia\github\geographic-data-visualisation\tests\test_examples\wojewodztwa-min_test_copy.geojson'
abs_path_excel_test = r'C:\Users\User\OneDrive\Pulpit\Marcysia\github\geographic-data-visualisation\tests\test_examples\pollution_data_test.xlsx'

@pytest.fixture()
def add_area_init():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = pd.ExcelFile(abs_path_excel_test)
    add_area(test_data_geojson, read_from_excel(test_data_excel))

    return test_data_geojson


def test_add_area_pass(add_area_init):
    assert ("area" in add_area_init['features'][0]['properties']) is True


@pytest.fixture()
def add_area_invalid_excel_field():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = r'test_examples/pollution_data_test_1.xlsx'
    return test_data_geojson, read_from_excel(test_data_excel)


def test_add_area_invalid_excel_field(add_area_invalid_excel_field):
    with pytest.raises(ValueError):
        add_area(add_area_invalid_excel_field[0], add_area_invalid_excel_field[1])


@pytest.fixture()
def add_area_invalid_geojson_field():
    with open(r'test_examples/wojewodztwa_test_1.geojson', 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = abs_path_excel_test
    return test_data_geojson, read_from_excel(test_data_excel)


def test_add_area_invalid_geojson_field(add_area_invalid_geojson_field):
    with pytest.raises(ValueError):
        add_area(add_area_invalid_geojson_field[0], add_area_invalid_geojson_field[1])


@pytest.fixture()
def add_area_invalid_dictionary_key():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = read_from_excel(abs_path_excel_test)
    test_data_excel['test2020'] = test_data_excel['2021']
    del test_data_excel['2021']
    return test_data_geojson, test_data_excel


def test_add_area_invalid_dictionary_key(add_area_invalid_dictionary_key):
    with pytest.raises(KeyError):
        add_area(add_area_invalid_dictionary_key[0], add_area_invalid_dictionary_key[1])


@pytest.fixture()
def add_area_invalid_dictionary_types():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = {1: "not data frame", 2: "for sure not data frame"}
    return test_data_geojson, test_data_excel


def test_add_area_invalid_dictionary_types(add_area_invalid_dictionary_types):
    with pytest.raises(ValueError):
        add_area(add_area_invalid_dictionary_types[0], add_area_invalid_dictionary_types[1])


@pytest.fixture()
def add_data_per_km2_init():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = pd.ExcelFile(abs_path_excel_test)
    add_data_per_km2(test_data_geojson, read_from_excel(test_data_excel))

    return test_data_geojson


def test_add_data_per_km2_pass(add_data_per_km2_init):
    assert ("co2_2020_per_km_sq" in add_data_per_km2_init['features'][0]['properties']) is True


@pytest.fixture()
def add_data_per_km2_invalid_excel_field():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = r'test_examples/pollution_data_test_1.xlsx'
    return test_data_geojson, read_from_excel(test_data_excel)


def test_add_data_per_km2_invalid_excel_field(add_data_per_km2_invalid_excel_field):
    with pytest.raises(ValueError):
        add_data_per_km2(add_data_per_km2_invalid_excel_field[0], add_data_per_km2_invalid_excel_field[1])


@pytest.fixture()
def add_data_per_km2_invalid_geojson_field():
    with open(r'test_examples/wojewodztwa_test_1.geojson', 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = abs_path_excel_test
    return test_data_geojson, read_from_excel(test_data_excel)


def test_add_data_per_km2_invalid_geojson_field(add_data_per_km2_invalid_geojson_field):
    with pytest.raises(ValueError):
        add_data_per_km2(add_data_per_km2_invalid_geojson_field[0], add_data_per_km2_invalid_geojson_field[1])


@pytest.fixture()
def add_data_per_km2_divide_by_zero():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = {year: pd.DataFrame(pd.read_excel(r'test_examples/pollution_data_test_3.xlsx', 'data' + year))
                       for year in ['2021', '2020', '2019', '2018', '2017', '2016']}
    return test_data_geojson, test_data_excel


def test_add_data_per_km2_divide_by_zero(add_data_per_km2_divide_by_zero):
    with pytest.raises(ZeroDivisionError):
        add_data_per_km2(add_data_per_km2_divide_by_zero[0], add_data_per_km2_divide_by_zero[1])


@pytest.fixture()
def add_data_per_km2_invalid_dictionary_key():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = read_from_excel(abs_path_excel_test)
    test_data_excel['test2020'] = test_data_excel['2021']
    del test_data_excel['2021']
    return test_data_geojson, test_data_excel


def test_add_data_per_km2_invalid_dictionary_key(add_data_per_km2_invalid_dictionary_key):
    with pytest.raises(KeyError):
        add_data_per_km2(add_data_per_km2_invalid_dictionary_key[0], add_data_per_km2_invalid_dictionary_key[1])


@pytest.fixture()
def add_data_per_km2_invalid_dictionary_types():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = {1: "not data frame", 2: "for sure not data frame"}
    return test_data_geojson, test_data_excel


def test_add_data_per_km2_area_invalid_dictionary_types(add_data_per_km2_invalid_dictionary_types):
    with pytest.raises(ValueError):
        add_data_per_km2(add_data_per_km2_invalid_dictionary_types[0], add_data_per_km2_invalid_dictionary_types[1])


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
    test_data_excel = read_from_excel(pd.ExcelFile(abs_path_excel_test))
    add_data_absolute(test_data_geojson, test_data_excel)

    return test_data_geojson


def test_add_data_absolute_pass(add_data_absolute_init):
    assert ("co2_2020" in add_data_absolute_init['features'][0]['properties']) is True


@pytest.fixture()
def add_data_absolute_invalid_excel_field():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = r'test_examples/pollution_data_test_1.xlsx'
    return test_data_geojson, read_from_excel(test_data_excel)


def test_add_data_absolute_invalid_excel_field(add_data_absolute_invalid_excel_field):
    with pytest.raises(ValueError):
        add_data_absolute(add_data_absolute_invalid_excel_field[0], add_data_absolute_invalid_excel_field[1])


@pytest.fixture()
def add_data_absolute_invalid_geojson_field():
    with open(r'test_examples/wojewodztwa_test_1.geojson', 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = abs_path_excel_test
    return test_data_geojson, read_from_excel(test_data_excel)


def test_add_data_absolute_invalid_geojson_field(add_data_absolute_invalid_geojson_field):
    with pytest.raises(ValueError):
        add_data_absolute(add_data_absolute_invalid_geojson_field[0], add_data_absolute_invalid_geojson_field[1])


@pytest.fixture()
def add_data_absolute_invalid_dictionary_key():
    with open(abs_path_geojson_init_test, 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = read_from_excel(abs_path_excel_test)
    test_data_excel['test20219'] = test_data_excel['2019']
    test_data_excel.pop('2019')
    return test_data_geojson, test_data_excel


def test_add_data_absolute_invalid_dictionary_key(add_data_absolute_invalid_dictionary_key):
    with pytest.raises(KeyError):
        add_data_absolute(add_data_absolute_invalid_dictionary_key[0], add_data_absolute_invalid_dictionary_key[1])


@pytest.fixture()
def add_data_absolute_invalid_dictionary_types():
    with open(r'test_examples/wojewodztwa_test_1.geojson', 'r') as f:
        test_data_geojson = json.load(f)
    test_data_excel = {1: "not data frame", 2: "for sure not data frame"}
    return test_data_geojson, test_data_excel


def test_add_data_absolute_area_invalid_dictionary_types(add_data_absolute_invalid_dictionary_types):
    with pytest.raises(ValueError):
        add_data_absolute(add_data_absolute_invalid_dictionary_types[0], add_data_absolute_invalid_dictionary_types[1])


def test_init_data_json_decode_error():
    with pytest.raises(json.JSONDecodeError):
        init_data(r'test_examples/test_init_data.json', abs_path_geojson_test, abs_path_excel_test)


def test_init_data_invalid_init_file():
    with pytest.raises(TypeError):
        init_data(r'\data\wojewodztwa-min.geojson', abs_path_geojson_test, abs_path_excel_test)


def test_read_from_excel_pass():
    with does_not_raise():
        read_from_excel(abs_path_excel_test)


def test_read_from_excel_invalid_path():
    with pytest.raises(ValueError) as e:
        read_from_excel(r'\data\pollution_data.xlsx')
    assert str(e.value) == "Didn't find file or sheet"


def test_read_from_excel_invalid_sheet():
    with pytest.raises(ValueError) as e:
        read_from_excel(r'test_examples/pollution_data_test_2.xlsx')
    assert str(e.value) == "Didn't find file or sheet"


def test_read_from_excel_zero_values():
    with pytest.raises(ValueError) as e:
        read_from_excel(r'test_examples/pollution_data_test_3.xlsx')
    assert str(e.value) == "Pollution cannot be less/equal to 0"


def test_read_from_excel_strings_in_excel():
    with pytest.raises(ValueError) as e:
        read_from_excel(r'test_examples/pollution_data_test_4.xlsx')
    assert str(e.value) == "Invalid type"


def test_read_from_excel_zeroes_and_negative_numbers_in_excel():
    with pytest.raises(ValueError) as e:
        read_from_excel(r'test_examples/pollution_data_test_5.xlsx')
    assert str(e.value) == "Pollution cannot be less/equal to 0"
