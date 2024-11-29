#!/usr/bin/env python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
from matplotlib.gridspec import GridSpec
import cartopy
import cartopy.crs as ccrs
import seaborn as sns

import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Read in data from CSV
filename = 'data/TOAR_Table_2.csv'
readcsv = pd.read_csv(filename, skiprows=1, header=0)


temp = readcsv.P_since_1995
ozone_trend = readcsv.Trend_since_1995.abs()
ozone_trend_direction = readcsv['Trend_since_1995']*30+90
ozone_p = readcsv.P_since_1995

lat = readcsv.Lat
lon = readcsv.Lon

def OC_colors(row):
    trend = row.Trend_since_1995
    p = row.P_since_1995
    if p<=0.05 and trend>0.:
        return '#980000'
    elif p<=0.05 and trend<0.:
        return '#010198'

    elif p>0.05 and p<=0.10 and trend>0.:
        return '#FF9933'
    elif p>0.05 and p<=0.10 and trend<0.:
        return '#0080FF'

    elif p>0.10 and p<=0.34 and trend>0.:
        return '#FFB266'
    elif p>0.10 and p<=0.34 and trend<0.:
        return '#99CCFF'
    else:
        return '#66CC00'

readcsv['plot_color'] = readcsv.apply(OC_colors, axis=1)





plt.figure(dpi=300)
# extract U and V components
WG_wind_U =   np.sin((ozone_trend_direction)*np.pi/180)
WG_wind_V = - np.cos((ozone_trend_direction)*np.pi/180)
plt.clf()
# m = Basemap(projection='cyl',lon_0=0.)

# Grid the co-ordinates
X,Y = np.meshgrid(lon,lat)
lons,lats = m(X,Y) # convert the co-ordinates to fit on the map

fig = plt.figure(figsize=[12, 4], dpi=300)
ax1 = fig.add_subplot(111, projection=ccrs.PlateCarree())
ax1.coastlines()
ax1.gridlines()
ax1.set_global()
ax1.add_feature(cartopy.feature.LAND,zorder=0, color='#E0E0E0', edgecolor='#808080')
gl = ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='#E0E0E0', alpha=0.4, linestyle='--')
gl.top_labels = False
gl.right_labels = False
ax1.quiver(lons[0,:],lats[:,0],WG_wind_U,WG_wind_V,color=readcsv['plot_color'], headlength=2.5, headaxislength=3)
# gl.left_labels=True
#('Longitude / degrees')
#ax1.set_ylabel('Latitude / degrees')
plt.title('Ozone trend since 1995 / ppb per year') 
ax1.text(-0.07, 0.55, 'latitude', va='bottom', ha='center',
        rotation='vertical', rotation_mode='anchor',
        transform=ax.transAxes)
ax1.text(0.5, -0.2, 'longitude', va='bottom', ha='center',
        rotation='horizontal', rotation_mode='anchor',
        transform=ax.transAxes)

# upper panel
data = pd.read_csv('data/diurnal_data.csv', index_col=0)
anndata = pd.read_csv('data/annual_cycle.csv', index_col=0)
trenddata = pd.read_csv('data/trends.csv', index_col=0)

fig = plt.figure(figsize=[7, 2.7], dpi=300)


ax3 = fig.add_subplot(131)
data['MLO'].plot(ax=ax3, label='MLO, US')
data['MNM'].plot(ax=ax3, label='MNM, JP')
data['UKA00315'].plot(ax=ax3, label='LMA, UK')
data['DENW073'].plot(ax=ax3, label='BK, BK')
#plt.legend(ncols=2, loc='lower center', fontsize=6.5)
ax3.set_ylim([0,55])
ax3.tick_params(axis='both', labelsize=8)
ax3.set_xlim([-0.5,23.5])


ax3.grid(True, linestyle='--')
ax3.set_xlabel("Local time / hrs", fontsize=10)
ax3.set_ylabel("Ozone / ppb", fontsize=10)
ax3.set_title('Ozone diurnal cycle')
ax3.yaxis.set_label_position("left")
ax3.legend(ncols=2, loc='lower center', fontsize=7)


ax1 = fig.add_subplot(132)
anndata['MLO'].plot(ax=ax1, label='MLO, US')
anndata['MNM'].plot(ax=ax1, label='MNM, JP')
anndata['UKA00315'].plot(ax=ax1, label='LMA, UK')
anndata['DENW073'].plot(ax=ax1, label='BK, BK')
ax1.set_ylim([0,55])
ax1.tick_params(axis='both', labelsize=8)
#ax2.set_xlim([-0.5,23.5])

ax1.set_xticks([1,2,3,4,5,6,7,8,9,10,11,12])
ax1.set_xticklabels(['J','F','M','A','M','J','J','A','S','O','N','D'], fontsize=10)

ax1.grid(True, linestyle='--')
ax1.set_xlabel("Month of year", fontsize=10)
ax1.set_title('Ozone annual cycle')
ax1.axes.yaxis.set_ticklabels([])
#ax1.yaxis.tick_right()
ax1.legend(ncols=2, loc='lower center', fontsize=7)

ax2 = fig.add_subplot(133)
trenddata['MLO'].plot(ax=ax2, label='MLO, US')
trenddata['MNM'].plot(ax=ax2, label='MNM, JP')
trenddata['UKA00315'].plot(ax=ax2, label='LMA, UK')
trenddata['DENW0073'].plot(ax=ax2, label='BK, BK')
ax2.set_ylim([0,55])
ax2.tick_params(axis='both', labelsize=8)
ax2.grid(True, linestyle='--')
ax2.set_xlabel("Year", fontsize=10)
ax2.set_title('Ozone trend')
ax2.yaxis.set_label_position("right")
ax2.set_ylabel("Ozone / ppb", fontsize=10, rotation =-90,labelpad=15)
ax2.yaxis.tick_right()
ax2.legend(ncols=2, loc='lower center', fontsize=7)

plt.tight_layout()
