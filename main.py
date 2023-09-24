import geopandas as gpd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    url = 'data/wojewodztwa-medium.geojson'

    districts = gpd.read_file(url)
    # print(districts)
    ax1=districts.plot(column="carbon_dioxide", cmap='RdYlGn_r')
    ax1.set_title("carbon dioxide per voivodeship")
    ax1.set_axis_off()
    plt.get_current_fig_manager().set_window_title('pora na ')

    ax2 = districts.plot(column="carbon_dioxide_tons_by_sq_km", cmap='RdYlGn_r')
    ax2.set_axis_off()
    ax2.set_title("carbon dioxide (tons/km^2)")
    plt.get_current_fig_manager().set_window_title('z csa ')
    plt.show()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
