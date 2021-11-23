import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
# import xlrd
from matplotlib import colors as c
import numpy as np
import matplotlib.pyplot as plt
# from basemap_toolbox import Basemap
# import xlrd
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


Burn = np.load('/Volumes/Star/burnSnow/data_25km_monthly/Alb_RF2_25kmbyFireYear/Burn.npy')
Unburn = np.load('/Volumes/Star/burnSnow/data_25km_monthly/Alb_RF2_25kmbyFireYear/Unbn.npy')

lon_burn = []
lat_burn = []
lon_unburn = []
lat_unburn = []
for f in range(0, 2):
    if f==0:
        # print('Burn')
        Data = np.copy(Burn)
        del Burn
        BurnName = 'Burned Area'
        BurnFld = 'Burn'
    if f==1:
        # print('Unburn')
        Data = np.copy(Unburn)
        del Unburn
        BurnName = 'Unburned Area'
        BurnFld = 'Unburn'

    for i in range(1, 18):
        fireYear = i + 2000 + 1
        Data_fireYear = Data[i, :, :, :, :]
        Biome = Data_fireYear[:, :, :, 2]
        biome = np.unique(Biome, return_counts=True)
        biome_value = biome[0][~np.isnan(biome[0])]
        biome_count = biome[1][0:len(biome_value)]
        # print(biome_value)
        # print(biome_count)
        biome_types = np.size(biome_value)
        Data_biome = np.zeros((19, 12, biome_types, 19))
        Data_biome[:] = np.nan
        Data_biome_std = np.zeros((19, 12, biome_types, 19))
        Data_biome_std[:] = np.nan
        for k in range(0, biome_types):
            count = biome_count[k]
            index = np.where(Biome == biome_value[k])
            index_x = index[0]
            index_y = index[1]
            index_z = index[2]
            rows = int(count/19/12)
            item_biomeType = np.zeros((19, 12, rows, 19))
            for j in range(0, count):
                item_biomeType[index_x[j], index_y[j], j%rows, :] = Data_fireYear[index_x[j], index_y[j], index_z[j], :]
            Data_biome[:, :, k, :] = np.nanmean(item_biomeType, axis=2)

            if biome_value[k] == 6:
                biomeName = 'Boreal forests'
                biomeNumber = '06'

                Data_lon = item_biomeType[:, :, :, 13]
                Data_lat = item_biomeType[:, :, :, 12]
                if f == 0:
                    lon_burn.append(Data_lon[0, 0, :])
                    lat_burn.append(Data_lat[0, 0, :])
                if f == 1:
                    lon_unburn.append(Data_lon[0, 0, :])
                    lat_unburn.append(Data_lat[0, 0, :])

lon_burn = np.concatenate(lon_burn).ravel()
lat_burn = np.concatenate(lat_burn).ravel()
lon_unburn = np.concatenate(lon_unburn).ravel()
lat_unburn = np.concatenate(lat_unburn).ravel()


fig = plt.gcf()
fig.set_size_inches(13, 6.5)
font_size = 20
m = Basemap(projection='robin', lon_0 = 0)
# m.shadedrelief()
m.drawcoastlines(color='grey', linewidth=0.2)
m.drawparallels(np.arange(-90.,120.,30.), labels=[1, 0, 0, 0],linewidth=0.3 ,dashes=[1, 4], fontsize= font_size)
m.drawmeridians(np.arange(0.,360.,60.),linewidth=0.3, dashes=[1, 4], fontsize = font_size )
clevs = np.linspace(22.42, 81.84, 7, endpoint=True)

x_burn, y_burn = m(lon_burn, lat_burn)
x_unburn, y_unburn = m(lon_unburn, lat_unburn)

cm2 = plt.scatter(x_burn, y_burn, c='red', cmap='BuPu', marker='.', edgecolors='k', linewidths=0, s=8,label='Burned boreal forest')
cm1 = plt.scatter(x_unburn, y_unburn, c='black', cmap='BuPu', marker='.', edgecolors='k', linewidths=0, s=8,label='Neighboring unburned boreal forest')

lgnd = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, ncol=5,markerscale=8,
           scatterpoints=1, fontsize=10).get_frame().set_edgecolor("black")

output = '/Volumes/Star/burnSnow/results_7_25km_0.25thrld_monthly/' + 'Location_burnUnburn.png'
# plt.savefig(output, dpi=500)
plt.show()









