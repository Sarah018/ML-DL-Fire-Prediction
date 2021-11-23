from __future__ import division

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker
import csv
import numpy as np
import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
import xlrd
from matplotlib import colors as c
import numpy as np
import matplotlib.pyplot as plt
from basemap_toolbox import Basemap

import xlrd
import matplotlib.ticker
from matplotlib import colors as c
import glob
import csv


def fmt(x, pos):
    a, b = '{:.2e}'.format(x).split('e')
    b = int(b)
    return r'${} \times 10^{{{}}}$'.format(a, b)


def nans(shape, dtype=float):
    a = np.empty(shape, dtype)
    a.fill(np.nan)
    return a


class FormatScalarFormatter(matplotlib.ticker.ScalarFormatter):
    def __init__(self, fformat="%1.1f", offset=True, mathText=True):
        self.fformat = fformat
        matplotlib.ticker.ScalarFormatter.__init__(self, useOffset=offset,
                                                   useMathText=mathText)

    def _set_format(self, vmin, vmax):
        self.format = self.fformat
        if self._useMathText:
            self.format = '$%s$' % matplotlib.ticker._mathdefault(self.format)


def readcsv(filename):
    with open(filename, 'r') as dest_f:
        data_iter = csv.reader(dest_f, delimiter=',', quotechar='"')
        data = [data for data in data_iter]
    data_array = np.asarray(data)
    return data_array

class OOMFormatter(matplotlib.ticker.ScalarFormatter):
    def __init__(self, order=0, fformat="%1.1f", offset=True, mathText=True):
        self.oom = order
        self.fformat = fformat
        matplotlib.ticker.ScalarFormatter.__init__(self,useOffset=offset,useMathText=mathText)
    def _set_order_of_magnitude(self):
        self.orderOfMagnitude = self.oom
    def _set_format(self, vmin=None, vmax=None):
        self.format = self.fformat
        if self._useMathText:
            self.format = r'$\mathdefault{%s}$' % self.format

Burn = np.load('/Users/sarah/Documents/AAA_burnSnow/data3_25km_monthly/Burn_byFireYear.npy')
# Unburn = np.load('/Volumes/Star/burnSnow/data2_25km_monthly/Alb_RF2_25kmbyFireYear/Unbn.npy')
# Dif = np.load('/Volumes/Star/burnSnow/data2_25km_monthly/Alb_RF2_25kmbyFireYear/Difc.npy')


var_index = [2, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 25, 26]
var_Name = ['Albedo',
            'Monthly Evapotranspiration',
            'Land Surface Temperature',
            'Leaf Area Index',
            'NDSI Snow Cover',
            'Specific Humidity',
            'Monthly Snow Melt',
            'Carbon Mass Flux Into Atmosphere Based on RCP45',
            'Carbon Mass Flux Into Atmosphere Based on RCP85',
            'Radiative Forcing by Snow Albedo Change',
            'Radiative Forcing by Albedo Change',
            'Snow depth water equivalent',
            'Downward short-wave radiation flux',
            'Snow Albedo',
            'Air temperature',
            'Wind speed',
            'Carbon Mass Based on RCP45',
            'Carbon Mass Based on RCP85']
months = ['Oct.', 'Nov.', 'Dec.', 'Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.']
MONTHS = ['10', '11', '12', '1', '2', '3', '4', '5', '6', '7', '8', '9']
seasons = ['Spring', 'Summer', 'Fall', 'Winter']

x_Label = ['Albedo', 'Monthly Evapotranspiration (kg/$m^2$)', 'Land Surface Temperature (°C)',
           'Leaf Area Index ($m^2$/$m^2$)', 'NDSI Snow Cover', 'Specific Humidity (kg/kg)',
           'Monthly Snow Melt (kg/$m^2$)', 'Carbon Mass Flux Based on RCP45 (kgc/$m^2$/s)',
           'Carbon Mass Flux Based on RCP85 (kgc/$m^2$/s)',
           'Radiative Forcing by Snow Albedo Change (W/$m^2$)', 'Radiative Forcing by Albedo Change (W/$m^2$)',
           'Snow depth water equivalent (kg/$m^2$)',
           'Downward short-wave radiation flux (W/$m^2$)', 'Snow Albedo', 'Air temperature (°C)',
           'Wind speed: m/s', 'Carbon Mass Based on RCP45 (kg/$m^2$)', 'Carbon Mass Based on RCP85 (kg/$m^2$)']


Data_Burn = np.copy(Burn)
del Burn


for yearOfAverage in range(3, 4):
    begin_fireYear = 3
    len_fireYear = 12
    FireYear_Burn = np.empty((len_fireYear, 4, 48))

    FireYear_Burn_std = np.empty((len_fireYear, 4, 48))



    fireYear_start = begin_fireYear + 2000 + 1
    fireYear_end = begin_fireYear + len_fireYear + 2000 + 1

    for i in range(begin_fireYear, len_fireYear + begin_fireYear):
        fireYear = i + 2000 + 1
        # print('fireYear:')
        # print(fireYear)

        fire_year = i
        Data_fireYear = Data_Burn[i,:,:,:,:]
        Biome = Data_fireYear[:, :, :, 23]
        biome = np.unique(Biome, return_counts=True)
        biome_value = biome[0][~np.isnan(biome[0])]
        biome_count = biome[1][0:len(biome_value)]
        # print(biome_value)
        # print(biome_count)
        biome_types = np.size(biome_value)
        Data_biome = np.zeros((19, 12, biome_types, 48))
        Data_biome[:] = np.nan
        Data_biome_std = np.zeros((19, 12, biome_types, 48))
        Data_biome_std[:] = np.nan
        for k in range(0, biome_types):
            count = biome_count[k]
            index = np.where(Biome == biome_value[k])
            index_x = index[0]
            index_y = index[1]
            index_z = index[2]
            rows = int(count/19/12)
            item_biomeType = np.zeros((19, 12, rows, 48))
            for j in range(0, count):
                item_biomeType[index_x[j], index_y[j], j%rows, :] = Data_fireYear[index_x[j], index_y[j], index_z[j], :]
            Data_biome[:, :, k, :] = np.nanmean(item_biomeType, axis=2)

            if biome_value[k] == 6:
                biomeName = 'Boreal forests'
                biomeNumber = '06'


                # index = np.argwhere(item_biomeType[i + 1, :, :, 15] < item_biomeType[i - 1, :, :, 15])
                # index_x = index[:, 0]
                # index_y = index[:, 1]
                # rows = int(len(index_x)/12)
                # item_biomeType2 = np.zeros((19, 12, rows, 29))
                # for m in range(0, int(len(index_x))):
                #     item_biomeType2[:, index_x[m], m % rows, :] = item_biomeType[:, index_x[m], index_y[m], :]

                Data_Burn_LC = item_biomeType

                for s in range(0, 4):

                    season_index = [[2, 3, 4], [5, 6, 7], [8, 9, 10], [11, 0, 1]]
                    plot_Burn_LC = np.nanmean(Data_Burn_LC[i + 1:i + 1 + yearOfAverage, :, :, :], axis=0) - np.nanmean(Data_Burn_LC[i - 3:i, :, :, :], axis=0)
                    seasonlyMean_Burn_LC = np.nanmean(plot_Burn_LC[season_index[s], :, :], axis=0)


                    for index in range(0, 18):
                        Data_afFireYear_lst_lat = Data_Burn_LC[0, 0, :, 21]
                        Data_afFireYear_lst_lon = Data_Burn_LC[0, 0, :, 22]
                        Data_afFireYear_lst = seasonlyMean_Burn_LC[:, var_index[index]]


                        fig = plt.gcf()
                        fig.set_size_inches(13, 6.5)
                        font_size = 20
                        m = Basemap(projection='robin', lon_0=0)
                        # m.shadedrelief()
                        m.drawcoastlines(color='grey', linewidth=0.2)
                        m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0], linewidth=0.3, dashes=[1, 4],
                                        fontsize=font_size)
                        m.drawmeridians(np.arange(0., 360., 60.), linewidth=0.3, dashes=[1, 4], fontsize=font_size)
                        clevs = np.linspace(22.42, 81.84, 7, endpoint=True)

                        x_burn, y_burn = m(Data_afFireYear_lst_lon, Data_afFireYear_lst_lat)


                        cm2 = plt.scatter(x_burn, y_burn, c=Data_afFireYear_lst, cmap='jet', marker='.', edgecolors='k', linewidths=0, s=80)
                        plt.colorbar(cm2)

                        # lgnd = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, ncol=5, markerscale=8,
                        #                   scatterpoints=1, fontsize=10).get_frame().set_edgecolor("black")


                        output = '/Users/sarah/Documents/AAA_burnSnow/results1_ByFireYear_burn/Burn/bySeason/Burn_Season_3yearAverage_map/' + var_Name[index] + ' of FireYear ' + str(fireYear) + '_' + ' in ' + seasons[s]  + '.png'
                        plt.savefig(output, dpi=500)
                        # plt.show()
                        plt.close()