from __future__ import division
import math
from statsmodels.distributions.empirical_distribution import ECDF
import pandas as pd
from eca import eca
import scipy
import matplotlib.ticker
import csv
import numpy as np
import matplotlib.pyplot as plt
# from basemap_toolbox import Basemap
# from mpl_toolkits.basemap import Basemap
import mpl_toolkits
mpl_toolkits.__path__.append('/usr/lib/python3.6/dist-packages/mpl_toolkits/')
from mpl_toolkits.basemap import Basemap

import matplotlib.ticker

def autolabel(rects,y_std):
    len = np.shape(y_std)[0]
    index=0
    for rect in rects:
        std = y_std[index]
        height = rect.get_height()
        ax.annotate(str(r'$\pm$') + str("{:.2}".format(std)),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
        index+=1
def createList(r1, r2):
    # Testing if range r1 and r2
    # are equal
    if (r1 == r2):
        return r1

    else:

        # Create empty list
        res = []

        # loop to append successors to
        # list until r2 is reached.
        while (r1 < r2 + 1):
            res.append(r1)
            r1 += 1
        return res
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


def binarize(x, thres, inverted=False):
    upper = 1 if not inverted else 0
    lower = 0 if not inverted else 1
    binarized = x.copy()
    binarized.loc[x > thres] = upper
    binarized.loc[x < thres] = lower
    binarized.loc[x == thres] = upper if inverted else lower
    return binarized


def binarize_quantile(x, quantile=0.9, **kwargs):
    q = x.dropna().quantile(quantile)
    return binarize(x, thres=q, **kwargs)


def roll_back(array, shift):
    return np.concatenate((array[shift:], np.zeros(shift)))


def roll_in(array, shift):
    if shift < 0:
        return roll_back(array, abs(shift))
    return array if shift == 0 else np.concatenate((np.zeros(shift), array[:-shift]))


def precursor_coincidence_rate(seriesA, seriesB, deltaT=0, tau=0, no_nan_length = 1, sym=False,  **kwagrs):
    a_events = seriesA[seriesA == 1].count()
    if sym:
        coincidence_interval = range(0 + tau - deltaT, 0 + tau + deltaT + 1)
    else:
        coincidence_interval = range(0 + tau - deltaT, 0 + tau + 1)
    shifted_values = [(seriesA.values == roll_in(seriesB, shift)) for shift in coincidence_interval]
    precursor_coincidences = np.shape(seriesA[np.all([seriesA.values == 1, np.any(shifted_values, axis=0)], axis=0)])[0]
    pcr = 0 if a_events == 0 else precursor_coincidences / no_nan_length
    return a_events, precursor_coincidences, pcr


def trigger_coincidence_rate(seriesA, seriesB, deltaT=0, tau=0, no_nan_length=1, sym=False,**kwagrs):
    b_events = seriesB[seriesB == 1].count()
    if sym:
        coincidence_interval = range(tau + 0 - deltaT, tau + deltaT + 1)
    else:
        coincidence_interval = range(tau + 0, tau + deltaT + 1)
    ## shifted_values ##
    # type: matrix
    # shape: (b_events, deltaT)
    # contains: [time,shift] := Is there an coincidence of seriesB[time] and seriesA[time+shift]
    shifted_values = [(seriesB.values == roll_in(seriesA, shift)) for shift in coincidence_interval]
    trigger_coincidences = np.shape(seriesB[np.all([seriesB.values == 1, np.any(shifted_values, axis=0)], axis=0)])[0]
    tcr = 0 if b_events == 0 else trigger_coincidences / no_nan_length
    return b_events, trigger_coincidences, tcr
    # return {'trigger_coincidence_rate': tcr,
    #         'b_events': b_events,
    #         'trigger_coincidences': trigger_coincidences}


def binomial_of(K_p, N_a, N_b, TOL, T, tau):

    return (scipy.special.comb(N=N_a, k=K_p, exact=True)
            * math.pow(1 - math.pow(1 - (TOL / (T - tau)), N_b), K_p)
            * math.pow(math.pow(1 - (TOL / (T - tau)), N_b), N_a - K_p))


def poisson_test(a_events, b_events, tau, deltaT, precursor_coincidences, trigger_coincidences, sym,
                 alpha, no_nan_length,
                 **kwgars):
    if not sym:
        # Note: nan values are not considered in analytical significance test
        T = no_nan_length
        TOL = deltaT + 1
    else:
        T = no_nan_length
        TOL = 2 * deltaT + 1
    # Calculation for Precursor Coincidence
    analytic_precursor_coincidence = 0
    analytic_trigger_coincidence = 0
    for k_p in range(precursor_coincidences, a_events + 1):
        analytic_precursor_coincidence += binomial_of(k_p, a_events, b_events, TOL, T, tau)

    for k_p in range(trigger_coincidences, b_events + 1):
        analytic_trigger_coincidence += binomial_of(k_p, b_events, a_events, TOL, T, tau)

    if analytic_precursor_coincidence >= alpha:
        true_precursor =1
    else:
        true_precursor=0
    if analytic_trigger_coincidence >= alpha:
        true_trigger =1
    else:
        true_trigger =0

    return analytic_precursor_coincidence, analytic_trigger_coincidence, true_precursor, true_trigger





# # *********************************************  Burn - Unburn  ****************************************************************
Data_Burn_2003 = np.load('/Users/sarah/Documents/AAA_burnSnow/data7_10km_monthly/Burn_fireYear_2003_GDPpop.npy')
Data_Burn_2004 = np.load('/Users/sarah/Documents/AAA_burnSnow/data7_10km_monthly/Burn_fireYear_2004_GDPpop.npy')
Data_Burn_2005 = np.load('/Users/sarah/Documents/AAA_burnSnow/data7_10km_monthly/Burn_fireYear_2005_GDPpop.npy')
Data_Unburn_basin = np.load('/Users/sarah/Documents/AAA_burnSnow/data7_10km_monthly/Unbn_forEachBasin_GDPpop.npy')

var_index = [0, 4, 5, 9, 10, 11, 12, 13, 15, 19, 20, 21, 23, 24, 14]
var_Name = ['Albedo',
            'ET',
            'EVI',
            'LST',
            'LAI',
            'NDSI',
            'NDVI',
            'PET',
            'SA',
            'Radiative forcing',
            'CWD',
            'CWB',
            'GDP',
            'POP',
            'Precip'
            ]



len_YearAF = 17
Data_fireYear = np.zeros((3, len_YearAF, 12, 25))
basin_ID = [3020024310, 4020050210, 4020050220, 1020040190, 4020050290, 4020050470, 7020000010, 6020000010, 3020000010, 1020000010, 8020000010, 4020000010, 5020000010, 2020000010, 9020000010, 7020014250, 6020006540, 3020003790, 8020008900, 4020006940, 5020015660, 2020003440, 7020021430, 3020005240, 1020018110, 8020010700, 4020015090, 5020037270, 2020018240, 7020024600, 3020008670, 1020021940, 8020020760, 4020024190, 2020024230, 7020038340, 3020009320, 1020027430, 8020022890, 4020034510, 5020054880, 2020033490, 1020034170, 8020032840, 2020041390, 7020046750, 7020047840, 6020029280, 8020044560, 2020057170, 7020065090, 2020065840, 2020071190]
#
# # For each latitude ****************************************************************************************************
for i in range(0, 3):
    if i==0:
        Data = Data_Burn_2003[i:i+len_YearAF,:,:,:]
        shape = np.shape(Data)
        len_1 = shape[2]
    if i==1:
        Data = Data_Burn_2004[i:i+len_YearAF,:,:,:]
        shape = np.shape(Data)
        len_2 = shape[2]
    if i==2:
        Data = Data_Burn_2005[i:i+len_YearAF,:,:,:]
        shape = np.shape(Data)
        len_3 = shape[2]


    shape = np.shape(Data)
    Data_dif = np.copy(Data)
    Data_dif[:] = np.nan
    num = 0
    for basin in range(0, 53):
        count = np.count_nonzero(Data[:, :, :,  6] == basin_ID[basin])
        index = np.where(Data[:,:,:,6] == basin_ID[basin])
        index_x = index[0]
        index_y = index[1]
        index_z = index[2]
        rows = int(count / len_YearAF / 12)
        item_biomeType = np.zeros((len_YearAF, 12, rows, 25))
        item_biomeType[:] = np.nan
        for j in range(0, count):
            item_biomeType[index_x[j], index_y[j], j % rows, :] = Data[index_x[j], index_y[j], index_z[j], :]
        Data_dif[:, :, num:num+rows, :] = item_biomeType - Data_Unburn_basin[0, i:i+len_YearAF, :, basin, :].reshape(len_YearAF, 12,1, 25)
        Data_dif[:, :, num:num + rows, 17:19] = item_biomeType[:,:,:,17:19]
        num+=rows

    if i==0:
        Data_2003 = np.zeros((np.shape(Data_dif)[0]*np.shape(Data_dif)[1],np.shape(Data_dif)[2],np.shape(Data_dif)[3]))
        for j in range(0, len_YearAF):
            for k in range(0, 12):
                index_month = j * 12 + k
                Data_2003[index_month, :, :] = Data_dif[j, k, :, :]

    if i==1:
        Data_2004 = np.zeros((np.shape(Data_dif)[0]*np.shape(Data_dif)[1],np.shape(Data_dif)[2],np.shape(Data_dif)[3]))
        for j in range(0, len_YearAF):
            for k in range(0, 12):
                index_month = j * 12 + k
                Data_2004[index_month, :, :] = Data_dif[j, k, :, :]

    if i==2:
        Data_2005 = np.zeros((np.shape(Data_dif)[0]*np.shape(Data_dif)[1],np.shape(Data_dif)[2],np.shape(Data_dif)[3]))
        for j in range(0, len_YearAF):
            for k in range(0, 12):
                index_month = j * 12 + k
                Data_2005[index_month, :, :] = Data_dif[j, k, :, :]


len = np.shape(Data_2003)[1]+np.shape(Data_2004)[1]+np.shape(Data_2005)[1]
Data_long = np.zeros((np.shape(Data_2003)[0], len, 25))
Data_long[:,0:np.shape(Data_2003)[1]] = Data_2003
Data_long[:,np.shape(Data_2003)[1]:np.shape(Data_2003)[1]+np.shape(Data_2004)[1]] = Data_2004
Data_long[:,np.shape(Data_2003)[1]+np.shape(Data_2004)[1]:np.shape(Data_2003)[1]+np.shape(Data_2004)[1]+np.shape(Data_2005)[1]] = Data_2005

# output = '/Users/sarah/Documents/AAA_burnSnow/data7_10km_monthly/' + 'Dif'  + '_forEachEcoID_GDPpop.npy'
# # np.save(output, Data_long)
# Data_long = np.load(output)

# *********** plot Seasonly time series *************
Data_long = Data_long[0:12,:,:]
Data_long_winter = Data_long[0:6, :, :]
Data_long_summer = Data_long[6:12, :, :]

for i in range(0, 3):
    if i==0:
        data = np.nanmean(Data_long, axis=0)
        seasonName = 'yearly'
    if i==1:
        data = np.nanmean(Data_long_winter, axis=0)
        seasonName = 'winter'
    if i==2:
        data = np.nanmean(Data_long_summer, axis=0)
        seasonName = 'summer'

    for l in range(0, 15):
        index = var_index[l]
        data_y = data[:, index]
        data_x = data[:, 17]
        index_lat = np.argsort(data_x)

        x = data_x[index_lat]
        y = data_y[index_lat]


        if l == 9:
            y = -y

        data_xy = np.zeros((np.shape(x)[0], 2))
        data_xy[:, 0] = np.copy(x)
        data_xy[:, 1] = np.copy(y)

        data_xy[:, ~np.isnan(data_xy).any(axis=0)]

        x = np.copy(data_xy[:, 0])
        y = np.copy(data_xy[:, 1])


        # ***************** by latitude *****************

        font_size = 50
        plt.rc('font', family='serif', size=font_size)
        fig, ax = plt.subplots(figsize = (20,10))
        cmap = plt.cm.jet
        norm = matplotlib.colors.Normalize(vmin=np.nanmin(y), vmax=np.nanmax(y))
        plt.bar(x, y, color=cmap(norm(y)),width=0.1)
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])  # only needed for matplotlib < 3.1
        cb = fig.colorbar(sm, shrink=0.6, pad=0.02)
        cb.ax.tick_params(labelsize=font_size)

        plt.xlabel('Latitude', fontsize=font_size + 2, fontweight='bold', labelpad=5)
        plt.ylabel('\u0394' + var_Name[l], fontsize=font_size + 2, fontweight='bold', labelpad=5)
        if l == 9:
            plt.ylabel(var_Name[l], fontsize=font_size + 2, fontweight='bold', labelpad=5)
        # plt.legend()
        # ax.set_xticks()
        # ax.set_xticklabels(np.arange(0-12, np.shape(data)[0]-12, 12))
        ax.spines['top'].set_linewidth(1)
        ax.spines['bottom'].set_linewidth(1)
        ax.spines['left'].set_linewidth(1)
        ax.spines['right'].set_linewidth(1)
        fig.tight_layout()

        output = '/Users/sarah/Documents/AAA_burnSnow/results5_10km_burn/dif/scatter_byLatitude/' + var_Name[l] +'_' + seasonName + '.png'
        plt.savefig(output, dpi=200, transparent = 'true')
        # plt.show()
        plt.close()

        # # ***************** by each latitude *****************
        font_size = 50
        y_0 = 0
        y_25 = 0
        y_50 = 0

        num_0 = 0
        num_25 = 0
        num_50 = 0

        for j in range(0, np.shape(x)[0]):
            if x[j]<25:
                if np.isnan(y[j]):
                    a=1
                else:
                    y_0 += y[j]
                    num_0+=1
            if x[j] >= 25 and x[j]<50:
                if np.isnan(y[j]):
                    a=1
                else:
                    y_25 += y[j]
                    num_25 += 1
            if x[j] >= 50:
                if np.isnan(y[j]):
                    a=1
                else:
                    y_50 += y[j]
                    num_50 += 1

        y_0 = y_0/num_0
        y_25 = y_25 / num_25
        y_50 = y_50 / num_50
        y_all = np.nansum(y)/(num_0+num_25+num_50)

        x_ticks_labels = ['0-25','25-50','50-70','0-70']
        plt.rc('font', family='serif', size=font_size)
        fig, ax = plt.subplots(figsize = (20, 10))
        cmap = plt.cm.jet
        norm = matplotlib.colors.Normalize(vmin=np.nanmin([y_0,y_25,y_50,y_all]), vmax=np.nanmax([y_0,y_25,y_50,y_all]))
        ax.bar(np.arange(0,4), [y_0,y_25,y_50,y_all], color=cmap(norm([y_0,y_25,y_50,y_all])))
        ax.bar(3, y_all, HATCH = '/', alpha = 0)

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])  # only needed for matplotlib < 3.1
        cb = fig.colorbar(sm, shrink=0.6, pad=0.02)
        cb.ax.tick_params(labelsize=font_size)

        plt.xlabel('Latitude', fontsize=font_size + 2, fontweight='bold', labelpad=5)
        plt.ylabel('\u0394' + var_Name[l], fontsize=font_size + 2, fontweight='bold', labelpad=5)
        if l == 9:
            plt.ylabel(var_Name[l], fontsize=font_size + 2, fontweight='bold', labelpad=5)
        # plt.legend()
        # Set number of ticks for x-axis
        ax.set_xticks(np.arange(0,4))
        ax.set_xticklabels(x_ticks_labels, fontsize=font_size)
        ax.spines['top'].set_linewidth(1)
        ax.spines['bottom'].set_linewidth(1)
        ax.spines['left'].set_linewidth(1)
        ax.spines['right'].set_linewidth(1)
        fig.tight_layout()

        output = '/Users/sarah/Documents/AAA_burnSnow/results5_10km_burn/dif/scatter_byLatitude/' + var_Name[l] +'_' + seasonName + '_2'+ '.png'
        plt.savefig(output, dpi=200, transparent = 'true')
        # plt.show()
        plt.close()


# For each continent ****************************************************************************************************
len_YearAF = 17
Data_fireYear = np.zeros((3, len_YearAF, 12, 25))
basin_ID = [3020024310, 4020050210, 4020050220, 1020040190, 4020050290, 4020050470, 7020000010, 6020000010, 3020000010,
            1020000010, 8020000010, 4020000010, 5020000010, 2020000010, 9020000010, 7020014250, 6020006540, 3020003790,
            8020008900, 4020006940, 5020015660, 2020003440, 7020021430, 3020005240, 1020018110, 8020010700, 4020015090,
            5020037270, 2020018240, 7020024600, 3020008670, 1020021940, 8020020760, 4020024190, 2020024230, 7020038340,
            3020009320, 1020027430, 8020022890, 4020034510, 5020054880, 2020033490, 1020034170, 8020032840, 2020041390,
            7020046750, 7020047840, 6020029280, 8020044560, 2020057170, 7020065090, 2020065840, 2020071190]
continent_ID = [1, 2, 3, 4, 5, 6, 7, 8, 9]
continent_list = ['Africa', 'Europe', 'Siberia', 'Asia', 'Australia', 'Northern South America', 'North America',
                  'Arctic(North America)', 'Greenland']
seasons = ['Boreal fall-winter', 'Boreal spring-summer']
season_index = [[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11]]

for i in range(0, 3):
    if i == 0:
        Data = Data_Burn_2003[i:i + len_YearAF, :, :, :]
        shape = np.shape(Data)
        len_1 = shape[2]
    if i == 1:
        Data = Data_Burn_2004[i:i + len_YearAF, :, :, :]
        shape = np.shape(Data)
        len_2 = shape[2]
    if i == 2:
        Data = Data_Burn_2005[i:i + len_YearAF, :, :, :]
        shape = np.shape(Data)
        len_3 = shape[2]

    shape = np.shape(Data)
    Data_dif = np.copy(Data)
    Data_dif[:] = np.nan
    num = 0
    for basin in range(0, 53):
        count = np.count_nonzero(Data[:, :, :, 6] == basin_ID[basin])
        index = np.where(Data[:, :, :, 6] == basin_ID[basin])
        index_x = index[0]
        index_y = index[1]
        index_z = index[2]
        rows = int(count / len_YearAF / 12)
        item_biomeType = np.zeros((len_YearAF, 12, rows, 25))
        item_biomeType[:] = np.nan
        for j in range(0, count):
            item_biomeType[index_x[j], index_y[j], j % rows, :] = Data[index_x[j], index_y[j], index_z[j], :]
        Data_dif[:, :, num:num + rows, :] = item_biomeType - Data_Unburn_basin[0, i:i + len_YearAF, :, basin,
                                                             :].reshape(len_YearAF, 12, 1, 25)
        Data_dif[:, :, num:num + rows, 6] = item_biomeType[:, :, :, 6]
        Data_dif[:, :, num:num + rows, 17] = item_biomeType[:, :, :, 17]
        Data_dif[:, :, num:num + rows, 18] = item_biomeType[:, :, :, 18]
        num += rows

    if i == 0:
        Data_2003 = np.zeros(
            (np.shape(Data_dif)[0] * np.shape(Data_dif)[1], np.shape(Data_dif)[2], np.shape(Data_dif)[3]))
        for j in range(0, len_YearAF):
            for k in range(0, 12):
                index_month = j * 12 + k
                Data_2003[index_month, :, :] = Data_dif[j, k, :, :]

    if i == 1:
        Data_2004 = np.zeros(
            (np.shape(Data_dif)[0] * np.shape(Data_dif)[1], np.shape(Data_dif)[2], np.shape(Data_dif)[3]))
        for j in range(0, len_YearAF):
            for k in range(0, 12):
                index_month = j * 12 + k
                Data_2004[index_month, :, :] = Data_dif[j, k, :, :]

    if i == 2:
        Data_2005 = np.zeros(
            (np.shape(Data_dif)[0] * np.shape(Data_dif)[1], np.shape(Data_dif)[2], np.shape(Data_dif)[3]))
        for j in range(0, len_YearAF):
            for k in range(0, 12):
                index_month = j * 12 + k
                Data_2005[index_month, :, :] = Data_dif[j, k, :, :]

len = np.shape(Data_2003)[1] + np.shape(Data_2004)[1] + np.shape(Data_2005)[1]
Data_long = np.zeros((np.shape(Data_2003)[0], len, 25))
Data_long[:, 0:np.shape(Data_2003)[1]] = Data_2003
Data_long[:, np.shape(Data_2003)[1]:np.shape(Data_2003)[1] + np.shape(Data_2004)[1]] = Data_2004
Data_long[:,
np.shape(Data_2003)[1] + np.shape(Data_2004)[1]:np.shape(Data_2003)[1] + np.shape(Data_2004)[1] + np.shape(Data_2005)[
    1]] = Data_2005

Data_mean_continent = np.zeros((len_YearAF * 12, 9, 25))
for continent in range(0, 9):
    basin = Data_long[:, :, 6]
    count = np.count_nonzero(np.floor(basin / 1000000000) == continent_ID[continent])
    index = np.where(np.floor(basin / 1000000000) == continent_ID[continent])
    index_x = index[0]
    index_y = index[1]

    rows = int(count / np.shape(Data_long)[0])
    item_biomeType = np.zeros((204, rows, 25))
    item_biomeType[:] = np.nan
    for j in range(0, count):
        item_biomeType[index_x[j], j % rows, :] = Data_long[index_x[j], index_y[j], :]
    Data_mean_continent[:, continent, :] = np.nanmean(item_biomeType, axis=1)

Data_mean = np.nanmean(Data_mean_continent, axis=1)

Data_mean_winter = np.zeros((len_YearAF, 25))
Data_mean_continent_winter = np.zeros((len_YearAF, 9, 25))
Data_mean_summer = np.zeros((len_YearAF, 25))
Data_mean_continent_summer = np.zeros((len_YearAF, 9, 25))
Data_mean_year = np.zeros((len_YearAF, 25))
Data_mean_continent_year = np.zeros((len_YearAF, 9, 25))

for i in range(0, len_YearAF):
    Data_mean_winter[i, :] = np.nanmean(Data_mean[i*12:i*12+6,:], axis=0)
    Data_mean_summer[i, :] = np.nanmean(Data_mean[i * 12+6:i * 12 + 12, :], axis=0)
    Data_mean_year[i, :] = np.nanmean(Data_mean[i * 12 :i * 12 + 12, :], axis=0)

    Data_mean_continent_winter[i, :,:] = np.nanmean(Data_mean_continent[i*12:i*12+6,:,:], axis=0)
    Data_mean_continent_summer[i, :, :] = np.nanmean(Data_mean_continent[i * 12+6:i * 12 + 12, :, :], axis=0)
    Data_mean_continent_year[i, :, :] = np.nanmean(Data_mean_continent[i * 12 :i * 12 + 12, :, :], axis=0)


Data_mean_winter = Data_mean_winter[0,:]
Data_mean_continent_winter= Data_mean_continent_winter[0,:,:]
Data_mean_summer= Data_mean_summer[0,:]
Data_mean_continent_summer = Data_mean_continent_summer[0,:,:]
Data_mean_year = Data_mean_year[0,:]
Data_mean_continent_year = Data_mean_continent_year[0,:,:]

#  ***************** plot *****************

for i in range(0, 3):
    if i==0:
        data = Data_mean_continent_winter
        seasonName = 'winter'
    if i==1:
        data = Data_mean_continent_summer
        seasonName = 'summer'
    if i==2:
        data = Data_mean_continent_year
        seasonName = 'year'
    for l in range(0, 15):
        index = var_index[l]
        data_plot = data[:, index]
        x = np.arange(0, 7)
        y=np.zeros(7)
        y[0] = data_plot[2]
        y[1] = data_plot[7]
        y[2] = data_plot[1]
        y[3] = data_plot[6]
        y[4] = data_plot[3]
        y[5] = data_plot[0]
        y[6] = data_plot[5]


        lengend1 = 'Siberia'
        lengend2 = 'Arctic'
        lengend3 = 'Europe'
        lengend4 = 'N. America'
        lengend5 = 'Asia'
        lengend6 = 'Africa'
        lengend7 = 'S. America'


        font_size = 50
        x_ticks_labels = [lengend1, lengend2, lengend3, lengend4, lengend5, lengend6, lengend7]
        plt.rc('font', family='serif', size=font_size)
        fig, ax = plt.subplots(figsize = (20, 10))
        cmap = plt.cm.jet
        norm = matplotlib.colors.Normalize(vmin=np.nanmin(y), vmax=np.nanmax(y))
        ax.bar(x, y, color=cmap(norm(y)))
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])  # only needed for matplotlib < 3.1
        cb = fig.colorbar(sm, shrink=0.6, pad=0.02)
        cb.ax.tick_params(labelsize=font_size)

        plt.xlabel('Continent', fontsize=font_size + 2, fontweight='bold', labelpad=5)
        plt.ylabel('\u0394' +var_Name[l], fontsize=font_size + 2, fontweight='bold', labelpad=5)
        if l == 9:
            plt.ylabel(var_Name[l], fontsize=font_size + 2, fontweight='bold', labelpad=5)
        # plt.legend()
        # Set number of ticks for x-axis
        ax.set_xticks(x)
        ax.set_xticklabels(x_ticks_labels, fontsize=font_size,rotation = 45)
        ax.spines['top'].set_linewidth(1)
        ax.spines['bottom'].set_linewidth(1)
        ax.spines['left'].set_linewidth(1)
        ax.spines['right'].set_linewidth(1)
        fig.tight_layout()

        output =  '/Users/sarah/Documents/AAA_burnSnow/results5_10km_burn/dif/scatter_byContinent/' + var_Name[l] +'_' + seasonName + '_2'+ '.png'
        plt.savefig(output, dpi=200, transparent = 'true')
        # plt.show()
        plt.close()