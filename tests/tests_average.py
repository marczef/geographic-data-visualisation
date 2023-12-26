import pytest
from src.utils import *
from contextlib import nullcontext as does_not_raise


@pytest.mark.parametrize('years, gas, type_of_ploting, ids, expected', [
    (["2017"], 'co2', "square", [1, 5, 6], 0.97851),
    (["2016", "2020"], 'so2', "overall", [1, 2, 3, 10, 11], 26.39979),
    (["2016", "2017", "2018", "2019", "2020", "2021"], 'metan', "square", [], 0.00669),
])
def test_avg_by_year_pass(years, gas, type_of_ploting, ids, expected):
    assert count_avg_by_year(years, gas, type_of_ploting, ids) == expected


@pytest.mark.parametrize('years, gas, type_of_ploting, ids, expected', [
    ([], 'co2', "square", [1, 2, 3], None),
    (["2016", "2020"], 'co2', "square", [1, 2, 17], None),
    (["2016", "2021"], '', "overall", [1, 2, 3], None),
    (["2016", "2017"], 'metan', "", [1, 2, 3], None),
    ([2016], 'metan', "overall", [1, 2, 3], None),
    (["2016", "2017"], 'metan_or_co2', 1, [1, 2, 3], None),
    (["2016", "2021"], 'metan', "overall", ["string", 2, 3], None)
])
def test_avg_by_year_fail(years, gas, type_of_ploting, ids, expected):
    assert count_avg_by_year(years, gas, type_of_ploting, ids) == expected


@pytest.mark.parametrize('ids, gas, expected', [
    ([1, 2, 3], "co2_2020_per_km_sq", 1.03223),
    ([1, 2, 6, 7, 8, 9, 10], "n2o_2016", 3.89816)
])
def test_avg_by_voiv_pass(ids, gas, expected):
    assert count_avg_by_voivodeship(ids, gas) == expected


@pytest.mark.parametrize('ids, gas, expected', [
    ([], "co2_2020", None),
    ([1, 2, 6, 7, 8, 9, 18], "n2o_2021", None),
    (["string", 1, 2, 3], "so2_2020_per_km_sq", None),
    ([0, 1, 2, 3, 4, 5], "co2", None)
])
def test_avg_by_voiv_pass(ids, gas, expected):
    assert count_avg_by_voivodeship(ids, gas) == expected


@pytest.fixture()
def return_clicked_list_pass():
    return {'points': [{'curveNumber': 0, 'pointNumber': 10, 'pointIndex': 10, 'location': 10, 'z': 0.740832959272279,
                        'hovertext': 'pomorskie',
                        'bbox': {'x0': 364.7527982234803, 'x1': 364.7527982234803, 'y0': 80.74700334428648,
                                 'y1': 80.74700334428648}, 'customdata': [0.740832959272279, 10]}]}


def test_return_clicked_list_pass(return_clicked_list_pass):
    with does_not_raise():
        return_clicked_list(return_clicked_list_pass)
        assert clicked_locations == [10]


@pytest.fixture()
def return_clicked_list_clear():
    clicked_locations.append(5)
    clicked_locations.append(12)
    clicked_locations.append(1)


def test_return_clicked_list_clear(return_clicked_list_clear):
    return_clicked_list(None)
    assert clicked_locations == []


def test_return_clicked_list_invalid_type():
    with pytest.raises(ValueError):
        return_clicked_list([10])


def test_return_clicked_list_invalid_dict_key():
    with pytest.raises(KeyError):
        return_clicked_list({'points': [
            {'curveNumber': 0, 'pointNumber': 10, 'pointIndex': 10, 'location_test': 10, 'z': 0.740832959272279,
             'hovertext': 'pomorskie',
             'bbox': {'x0': 364.7527982234803, 'x1': 364.7527982234803, 'y0': 80.74700334428648,
                      'y1': 80.74700334428648}, 'customdata': [0.740832959272279, 10]}]})
