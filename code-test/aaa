import numpy as np
import matplotlib.pyplot as plt
from basemap_toolbox import Basemap
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

class FormatScalarFormatter(matplotlib.ticker.ScalarFormatter):
    def __init__(self, fformat="%1.1f", offset=True, mathText=True):
        self.fformat = fformat
        matplotlib.ticker.ScalarFormatter.__init__(self,useOffset=offset,
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

folder_unburn = glob.glob("/Volumes/Star/burnSnow/data/snowAlbedoLst2_NoFirstLastCol/snow_lst_albedo_Unburn/20071001-20081001/*.csv")
folder_burn = glob.glob("/Volumes/Star/burnSnow/data/snowAlbedoLst2_NoFirstLastCol/snow_lst_albedoBurn/20071001-20081001/*.csv")
date = np.ones((1,19))
for k in range (0, 19):
    date[0, k] = 2001+k

for n in range(0, len(folder_burn)):
    file = folder_burn[n]
    data = readcsv(file)
    shape = np.shape(data)
    for i in range(0, shape[0]):

        snowCover_burn = np.ones((1,19))
        albedo_burn = np.ones((1,19))
        lst_burn = np.ones((1,19))
        firstSnow_burn = np.ones((1,19))
        lastSnow_burn = np.ones((1,19))
        lat = np.ones((1,19))
        lon = np.ones((1,19))
        snowPeriod_burn = np.ones((1,19))

        snowCover_unburn = np.ones((1,19))
        albedo_unburn = np.ones((1,19))
        lst_unburn = np.ones((1,19))
        firstSnow_unburn = np.ones((1,19))
        lastSnow_unburn = np.ones((1,19))
        snowPeriod_unburn = np.ones((1,19))

        snowCover_dif = np.ones((1,19))
        albedo_dif = np.ones((1,19))
        lst_dif = np.ones((1,19))
        firstSnow_dif= np.ones((1,19))
        lastSnow_dif = np.ones((1,19))
        snowPeriod_dif = np.ones((1,19))

        for j in range(0,19):
            file_burn = folder_burn[n+j]
            data_burn = readcsv(file_burn)
            snowCover_burn[0,j] = data_burn[i, 1]
            albedo_burn[0,j] = data_burn[i, 3]
            lst_burn[0,j] = data_burn[i, 4]
            firstSnow_burn[0,j] = data_burn[i, 5]
            lastSnow_burn[0,j] = data_burn[i, 7]
            lat[0,j] = data_burn[i, 8]
            lon[0,j] = data_burn[i, 9]
            snowPeriod_burn[0, j] = lastSnow_burn[0,j] - firstSnow_burn[0,j]
        plt.scatter(date, firstSnow_burn, marker='o', c = 'red')
        plt.scatter(date, lastSnow_burn, marker='o', c = 'green')
        plt.scatter(date, snowPeriod_burn, marker='o', c = 'blue')

        for j in range(0,19):
            file_unburn = folder_unburn[n+j]
            data_unburn = readcsv(file_unburn)
            snowCover_unburn[0,j] = data_unburn[i, 1]
            albedo_unburn[0,j] = data_unburn[i, 3]
            lst_unburn[0,j] = data_unburn[i, 4]
            firstSnow_unburn[0,j] = data_unburn[i, 5]
            lastSnow_unburn[0,j] = data_unburn[i, 7]
            snowPeriod_unburn[0, j] = lastSnow_unburn[0,j] - firstSnow_unburn[0,j]
        plt.scatter(date, firstSnow_unburn, marker='^', c = 'red')
        plt.scatter(date, lastSnow_unburn, marker='^', c = 'green')
        plt.scatter(date, snowPeriod_unburn, marker='^', c = 'blue')

        for j in range(0,19):
            snowCover_dif[0,j] = snowCover_unburn[0,j] - snowCover_burn[0,j]
            albedo_dif[0,j] = albedo_unburn[0,j] - albedo_burn[0,j]
            lst_dif[0,j] = lst_unburn[0,j] - lst_burn[0,j]
            firstSnow_dif[0,j] = firstSnow_unburn[0,j] - firstSnow_burn[0,j]
            lastSnow_dif[0,j] = lastSnow_unburn[0,j] - lastSnow_burn[0,j]
            snowPeriod_dif[0, j] = snowPeriod_unburn[0,j] - snowPeriod_burn[0,j]
        plt.scatter(date, firstSnow_dif, marker='*', c = 'red')
        plt.scatter(date, lastSnow_dif, marker='*', c = 'green')
        plt.scatter(date, snowPeriod_dif, marker='*', c = 'blue')


        plt.show()








