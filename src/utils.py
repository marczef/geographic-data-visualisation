import numpy as np
import plotly.express as px
import pandas as pd
from numpyencoder import NumpyEncoder
import json
import plotly.graph_objects as go
from plotly.graph_objs import *

absolute_path = r'../data/pollution_coordinates.geojson'
absolute_path_init = r'../data/wojewodztwa-min.geojson'
absolute_path_excel = r'../data/pollution_data.xlsx'

clicked_locations = []


def init_data(init_geojson_path, path_geojson, excel_path):
    """
        Initializes and updates geographic and pollution data based on specified paths.

        Args:
        - init_geojson_path (str): Path to the initial geojson file.
        - path_geojson (str): Path to save the updated geojson file.
        - excel_path (str): Path to the Excel file containing pollution data.

        Raises:
        - json.JSONDecodeError: If the initial geojson file has invalid JSON syntax.
        - TypeError: If there's an issue with the provided paths.

        This function attempts to read the initial geojson file and the Excel file containing pollution data.
        If successful, it proceeds to read data from the Excel file, adds area-related information to the geojson data,
        and calculates additional pollution-related data (absolute and per km²). The updated geojson data is then saved
        to the specified path.
        """

    try:
        with open(init_geojson_path, 'r') as f:
            data_geojson = json.load(f)
        data = pd.ExcelFile(excel_path)

    except json.JSONDecodeError as e:
        raise json.JSONDecodeError("Invalid JSON syntax", e.doc, e.pos)

    except:
        raise TypeError("Invalid path")

    years = read_from_excel(data)

    add_area(data_geojson, years)
    add_data_absolute(data_geojson, years)
    add_data_per_km2(data_geojson, years)

    save_data(path_geojson, data_geojson)


def read_from_excel(data):
    """
        Reads pollution data from different Excel sheets corresponding to specific years.

        Args:
        - data (pandas.ExcelFile): ExcelFile object containing pollution data.

        Raises: - ValueError: If there's an issue with file or sheet retrieval, invalid data types, or non-positive
        pollution values.

        This function reads pollution data from different Excel sheets for specific years.
        It iterates through the provided ExcelFile object and validates the data retrieved from each sheet.
        If any issues are encountered, it raises appropriate ValueErrors with descriptive messages.
        """

    years = {}
    for year in ['2021', '2020', '2019', '2018', '2017', '2016']:
        try:
            df1 = pd.read_excel(data, 'data' + year)
            df = pd.DataFrame(df1)
            years[year] = df
        except:
            raise ValueError("Didn't find file or sheet")

        for pol in list(df.columns)[1:]:
            if not all(isinstance(item, (np.floating, float, np.integer, int)) for item in df[pol]):
                raise ValueError("Invalid type")
            if any(item is None or item <= 0 for item in df[pol]):
                raise ValueError("Pollution cannot be less/equal to 0")

    return years


def save_data(path, data_geojson):
    """
        Saves geojson data to a specified file path.

        Args:
        - path (str): Path to save the geojson data.
        - data_geojson (dict): Geojson data to be saved.

        Raises:
        - TypeError: If there's an issue with serializing the object.

        This function attempts to save the provided geojson data to a specified file path.
        It utilizes the `json.dump` method to serialize the data_geojson dictionary into the specified file.
        If any issues occur during the serialization process, it raises a TypeError with a descriptive message.
        """

    try:
        with open(path, 'w') as f:
            json.dump(data_geojson, f, cls=NumpyEncoder)
    except:
        raise TypeError("Unable to serialize the object")


def add_area(data_geojson, years):
    """
        Adds area information to geojson features based on DataFrame values.

        Args:
        - data_geojson (dict): Geojson data containing features.
        - years (dict): Dictionary containing pollution data for specific years as DataFrames.

        Raises:
        - ValueError: If there are issues with the provided dictionary values or invalid fields.

        This function attempts to add area information to the geojson features based on DataFrame values.
        It checks the validity of dictionary values and extracts the DataFrame for the year 2021.
        Then, it iterates through the geojson features and matches voivodeship names with DataFrame values.
        If matches are found, it adds the 'area' field to the corresponding geojson feature properties.
        """

    try:
        for k, v in years.items():
            if isinstance(k, str) and isinstance(v, pd.DataFrame):
                df = years['2021']
            else:
                raise ValueError("Invalid dictionary values")
    except KeyError:
        raise KeyError("Key must be years from 2016 to 2021")

    try:
        for feat in data_geojson['features']:
            for woj in range(len(df["woj."])):
                if feat["properties"]["nazwa"] == df["woj."][woj]:
                    feat['properties']['area'] = df["area"][woj]
    except:
        raise ValueError("Invalid field")


def add_data_per_km2(data_geojson, years):
    """
    Adds pollution data per square kilometer to geojson features.

    Args:
    - data_geojson (dict): Geojson data containing features.
    - years (dict): Dictionary containing pollution data for specific years as DataFrames.

    Raises:
    - KeyError: If the key for year is not between 2016 and 2021 in the years dictionary.
    - ZeroDivisionError: If division by zero occurs while calculating pollution per square kilometer.
    - ValueError: If there are issues with the provided dictionary values or invalid fields.

    This function calculates and adds pollution data per square kilometer to geojson features. It iterates through
    the years dictionary and matches voivodeship names in geojson with DataFrame values. If matches are found,
    it computes pollution per square kilometer for each pollutant and adds new fields to geojson features.
    """
    for year in ['2021', '2020', '2019', '2018', '2017', '2016']:

        try:
            for k, v in years.items():
                if isinstance(k, str) and isinstance(v, pd.DataFrame):
                    df = years[year]
                else:
                    raise ValueError("Invalid dictionary values")
        except KeyError:
            raise KeyError("Key must be years from 2016 to 2021")

        try:
            for feat in data_geojson['features']:
                for woj in range(len(df["woj."])):
                    if feat["properties"]["nazwa"] == df["woj."][woj]:
                        for pol in list(df.columns)[2:]:
                            feat['properties'][str(pol) + "_" + year + "_per_km_sq"] = df[pol][woj].item() / df['area'][
                                woj].item()
        except ZeroDivisionError:
            raise ZeroDivisionError("Cannot divide by zero")
        except:
            raise ValueError("Invalid field")


def add_data_absolute(data_geojson, years):
    """
        Adds absolute pollution data to geojson features.

        Args:
        - data_geojson (dict): Geojson data containing features.
        - years (dict): Dictionary containing pollution data for specific years as DataFrames.

        Raises:
        - KeyError: If the key for year is not between 2016 and 2021 in the years dictionary.
        - ValueError: If there are issues with the provided dictionary values or invalid fields.

        This function adds absolute pollution data to geojson features.
        It iterates through the years dictionary and matches voivodeship names in geojson with DataFrame values.
        If matches are found, it adds absolute pollution values for each pollutant to the geojson properties.
        """

    for year in ['2021', '2020', '2019', '2018', '2017', '2016']:

        try:
            for k, v in years.items():
                if isinstance(k, str) and isinstance(v, pd.DataFrame):
                    df = years[year]
                else:
                    raise ValueError("Invalid dictionary values")

        except KeyError:
            raise KeyError("Key must be years from 2016 to 2021")

        try:
            for feat in data_geojson['features']:
                for woj in range(len(df["woj."])):
                    if feat["properties"]["nazwa"] == df["woj."][woj]:
                        for pol in list(df.columns)[2:]:
                            feat['properties'][str(pol) + "_" + year] = df[pol][woj]
        except:
            raise ValueError("Invalid field")


def blank_fig():
    """
        Generates a blank Plotly figure.

        Returns:
        - plotly.graph_objs.Figure: A blank Plotly figure with transparent background.

        This function creates a blank Plotly figure with a transparent background. It sets the paper_bgcolor and
        plot_bgcolor to transparent, removes gridlines, ticks, and zero lines from both x and y axes. The resulting
        figure is a placeholder for later shown graph.
    """

    layout = Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig = go.Figure(go.Scatter(x=[], y=[]), layout=layout)
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
    return fig


def count_avg_by_voivodeship(ids, gas):
    """
        Calculates the average pollution data for selected voivodeships.

        Args:
        - ids (list): List of voivodeship IDs.
        - gas (str): Type of pollution gas.

        Returns:
        - float or None: The average pollution level for the selected voivodeships or None.

        This function calculates the average pollution data for the specified voivodeships. It checks the validity of
        input arguments - ensures that 'ids' and 'gas' are provided and are of the correct types. If IDs are not
        within the expected range (0-15), it returns None. It reads geojson data from the specified absolute path and
        iterates through features. For each feature with a matching ID, it accumulates the pollution data based on
        the provided 'gas' type. Finally, it computes the average pollution level for the selected voivodeships and
        returns it rounded to 5 decimal places.
    """

    if not ids or not gas or not all(isinstance(i, int) for i in ids):
        return
    if not all(0 <= i <= 15 for i in ids):
        return
    with open(absolute_path, 'r') as f:
        data_geojson = json.load(f)
    try:
        avg = 0
        for feat in data_geojson['features']:
            if feat["id"] in ids:
                avg += feat["properties"][gas]

        return round(avg / len(ids), 5)

    except:
        return None


def count_avg_by_year(years, gas, type_of_ploting, ids):
    """
        Calculates the average pollution data for selected years.

        Args:
        - years (list): List of years.
        - gas (str): Type of pollution gas.
        - type_of_ploting (str): Type of plotting ("overall" or "square").
        - ids (list): List of voivodeship IDs.

        Returns:
        - float or None: The average pollution level for the selected years or None.

        This function calculates the average pollution data for the specified years. It checks the validity of input
        arguments - ensures that 'years', 'gas', 'type_of_ploting', and 'ids' are provided and are of the correct
        types. If IDs are not within the expected range (0-15) or if 'ids' is empty, it generates IDs from 0 to 15.
        It reads geojson data from the specified absolute path and iterates through features. For each year and
        matching ID, it accumulates the pollution data based on the provided 'gas' type and 'type_of_ploting'.
        Finally, it computes the average pollution level for the selected years and returns it rounded to 5 decimal
        places.
        """

    if not years or not gas or not type_of_ploting or not all(isinstance(i, int) for i in ids):
        return
    if not all(0 <= i <= 15 for i in ids):
        return
    if len(ids) == 0:
        ids = [i for i in range(0, 16)]
    with open(absolute_path, 'r') as f:
        data_geojson = json.load(f)

    try:
        avg = 0
        for year in years:
            if type_of_ploting == "overall":
                gas_now = (gas + "_" + year)
            elif type_of_ploting == "square":
                gas_now = (gas + "_" + year + "_per_km_sq")

            for feat in data_geojson['features']:
                if feat["id"] in ids:
                    avg += feat["properties"][gas_now]
        return round(avg / (len(ids) * len(years)), 5)

    except:
        return None


def return_clicked_list(click_data):
    """
        Manages a list of clicked locations on a graph.

        Args:
        - click_data (dict): Data associated with a click event on a graph.

        Raises:
        - KeyError: If there's an issue with the keys in the click_data dictionary.
        - ValueError: If the click_data is not of type dict.

        This function handles a list of clicked locations on a graph.
        It expects click_data to be a dictionary with specific keys.
        Upon receiving valid click_data, it extracts the location information.
        If the location is not present in clicked_locations, it appends it. Otherwise, it removes it.
        If click_data is None, it clears the clicked_locations list.
        """

    if click_data is not None:
        if isinstance(click_data, dict):

            try:
                location = click_data['points'][0]['location']
            except KeyError:
                raise KeyError("Invalid clicked_data keys")

            if location not in clicked_locations:
                clicked_locations.append(location)
            else:
                clicked_locations.remove(location)
            return
        else:
            raise ValueError("Invalid type")
    else:
        clicked_locations.clear()
