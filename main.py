import geopandas as gpd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    url = 'data/wojewodztwa-medium.geojson'

    districts = gpd.read_file(url)

    districts.plot()

    plt.show()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
