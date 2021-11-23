import geojson
from descartes import PolygonPatch
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.colors
import numpy as np; np.random.seed(0)
import pandas as pd
import csv
import matplotlib as mpl
from colour import Color
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
from shapely.geometry import Point, MultiPoint, MultiPolygon
from random import shuffle, randint

def colorFader(c1,c2,mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

def readcsv(filename):
    with open(filename, 'r') as dest_f:
        data_iter = csv.reader(dest_f, delimiter=',', quotechar='"')
        data = [data for data in data_iter]
    data_array = np.asarray(data)
    return data_array

basin = '/Users/sarah/Documents/AAA_burnSnow/data5_4km_monthly/Basins/Basin_shpefile.geojson'
with open(basin) as json_file:
    json_data = geojson.load(json_file)

# c1='#1f77b4' #blue
# c2='green' #green
# len = np.shape(patches)[0]
# colors = []
# for i in range(len+1):
#     temp_color = colorFader(c1,c2,i/len)
#     temp_color = np.array(mpl.colors.to_rgb(temp_color))
#     colors.append(temp_color)
#
# rgb1 = [255/255,0/255,0/255]
# rgb2 = [0,0,255/255]
# steps=5
# output = []
# r1, g1, b1 = rgb1
# r2, g2, b2 = rgb2
# output.append((r1, g1, b1))
# rdelta, gdelta, bdelta = (r2-r1)/(steps-1), (g2-g1)/(steps-1), (b2-b1)/(steps-1)
# for step in range(steps-1):
#     r1 += rdelta
#     g1 += gdelta
#     b1 += bdelta
#     output.append((r1, g1, b1))
#
# colors = output

# cmap = mpl.cm.get_cmap('Spectral')
# cmap_2 = plt.cm.Spectral
# colors = []
# for i in range(5):
#     colors.append(cmap(i/5))


x = np.arange(4)
y = np.random.rand(4)*51
c = y
df = pd.DataFrame({"x":x,"y":y,"c":c})

cmap = plt.cm.rainbow
norm = matplotlib.colors.Normalize(vmin=np.nanmin(c), vmax=np.nanmax(c))
colors=cmap(norm(df.c.values))

plt.clf()
fig, ax = plt.subplots()  # fig.gca()
m = Basemap(projection='robin', lon_0=0, resolution='c')
m.drawmapboundary(fill_color='white', zorder=-1)
m.drawparallels(np.arange(-90., 91., 30.), labels=[1, 0, 0, 1], dashes=[1, 1], linewidth=0.25, color='0.5',
                fontsize=14)
m.drawmeridians(np.arange(0., 360., 60.), labels=[1, 0, 0, 1], dashes=[1, 1], linewidth=0.25, color='0.5',
                fontsize=14)
# m.drawcoastlines(color='0.6', linewidth=1)

patches = []

# for i in [6,7,10,14,15,16,18,22,25,28,29,31,32,35,38,43]:
for i in range(0, 4):
    print(i)

    coordlist = json_data.features[i]['geometry']['coordinates'][0]
    shape = np.shape(coordlist)
    print(shape)


    if shape[0]>1:
        len = shape[0]
        coordlist_new = np.zeros((1, len, 2))
        # for j in range(0, 1):
        #     for k in range(0, len):
        #         coordlist_new[j, k, 0] = coordlist[k][0]
        #         coordlist_new[j, k, 1] = coordlist[k][1]

        for j in range(0, 1):
            for k in range(0, len):
                temp = coordlist[k][0]
                if temp>180:
                    temp =180
                if temp<-180:
                    temp =-180

                coordlist_new[j][k][0], coordlist_new[j][k][1] = m(temp, coordlist[k][1])

        poly = {"type": "Polygon", "coordinates": coordlist_new}
        # polygon = PolygonPatch(poly, fc = colors[i], ec=[0,0,0])
        # patches.append(polygon)
        ax.add_patch(PolygonPatch(poly, fc = colors[i], ec=[0,0,0], zorder=0.2))

    if shape[0]==1:
        coordlist = json_data.features[i]['geometry']['coordinates']
        shape_2 = np.shape(coordlist)
        for j in range(0, shape_2[0]):
        # for j in range(2, 3):
            item = coordlist[j]
            shape_3 = np.shape(item)
            if shape_3[0]==1:
                coordlist_new = np.zeros((1, shape_3[1], 2))
                for k in range(0, 1):
                    for l in range(0, shape_3[1]):
                        temp = item[k][l][0]
                        if temp > 180:
                            temp = 180
                        if temp < -180:
                            temp = -180
                        coordlist_new[k][l][0], coordlist_new[k][l][1] = m(temp, item[k][l][1])
                poly = {"type": "Polygon", "coordinates": coordlist_new}
                # polygon = PolygonPatch(poly, fc = colors[i], ec=[0,0,0])
                # patches.append(polygon)
                ax.add_patch(PolygonPatch(poly, fc = colors[i], ec=[0,0,0], zorder=0.2))
            else:
                for p in range(0, shape_3[0]):
                    item_2 = item[p]
                    shape_4 = np.shape(item_2)
                    coordlist_new = np.zeros((1, shape_4[0], 2))
                    for k in range(0, 1):
                        for l in range(0, shape_4[0]):
                            temp = item_2[l][0]
                            if temp > 180:
                                temp = 180
                            if temp < -180:
                                temp = -180
                            coordlist_new[k][l][0], coordlist_new[k][l][1] = m(temp, item_2[l][1])
                    poly = {"type": "Polygon", "coordinates": coordlist_new}
                    # polygon = PolygonPatch(poly, fc = colors[i], ec=[0,0,0])
                    # patches.append(polygon)
                    ax.add_patch(PolygonPatch(poly, fc = colors[i], ec=[0,0,0],  zorder=0.2))




# red = Color("red")
# colors = list(red.range_to(Color("blue"),len))
# colors = 100*np.random.rand(np.shape(patches)[0])
# p = PatchCollection(patches,cmap=plt.get_cmap('RdYlBu_r'), alpha=0.4)
# p.set_array(colors)
# p.set_clim([np.ma.min(colors),np.ma.max(colors)])
# ax.add_collection(p)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # only needed for matplotlib < 3.1
fig.colorbar(sm)
#
# ax.axis('scaled')
# cb = plt.colorbar(ax, orientation="horizontal")
# plt.title(str(i), fontsize=20)
plt.draw()
# output = '/Users/sarah/Documents/AAA_burnSnow/results3_basin/NH/' + 'ID_' + str(i)  + '.png'
output = '/Users/sarah/Documents/AAA_burnSnow/results3_basin/whole/' + 'ID_all'  + '.png'
# plt.savefig(output, dpi=500)
plt.show()

plt.close()
print('ok')

