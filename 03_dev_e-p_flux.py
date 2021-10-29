
# %%
import numpy as np
import math
from datetime import date
import os

year = 2020
month = 2
day = 3
fday = date(year,1,1)

dc = (date(year,month,day)-fday).days + 1

namelist = ['tmp','ugrd','vgrd']
# kindlist = ['zonal','dev']
kind = 'dev'

# for kind in kindlist:

for name in namelist:
    savefile = f'D:/data/JRA55/{name}/{year}/{year}d{str(dc).zfill(3)}_{name}_{kind}.npy'
    globals()[kind + name] = np.load(savefile)

pcord = np.array([1000,975,950,925,900,875,850,825,800,775,750,700,
        650,600,550,500,450,400,350,300,250,225,200,175,150,125,100,70,
        50,30,20,10,7,5,3,2,1])


phicord = np.arange(-90,91,1.25)*(math.pi/180.)

a = 6.37e+6
R = 287
Cp = 1004
K = R/Cp
g0 = 9.80665
ps = 100000
omega = 7.29e-5
Ts =  240
H = R*Ts/g0
rhos = ps/R/Ts
f = 2*omega*np.sin(phicord)
rho = rhos*(pcord*100/ps)
N_2 = 4.0e-4

# print(devvgrd[31,24])
# print(devugrd[31,24])
# print(devtmp[31,24])
# print(devhgt[31,24])
vudev_mean = np.mean(devvgrd*devugrd,axis=2)
# print(vudev_mean.shape)
Fy = (((-1)*a*vudev_mean*np.cos(phicord)).T*rho).T
devFy = np.gradient(Fy*np.cos(phicord), phicord,axis=1)

z = -H*np.log(pcord*100/ps)
vTdev_mean = np.mean(devvgrd*devtmp,axis=2)
# print(vTdev_mean)
Fz = ((a*np.cos(phicord)*f*R*vTdev_mean/(N_2*H)).T*rho).T
devFz = np.gradient(Fz,z,axis=0)
nablaF = devFy/(a*np.cos(phicord)) + devFz
fzmean = np.mean(np.mean(nablaF))

nablaF = ((nablaF/(a*np.cos(phicord))).T/rho).T
nablaF = nablaF*60*60*24
# print(nablaF)
# print(nablaF[31])
fmean = np.mean(np.mean(nablaF))
vector_scale = 8.0e+5
# vector_scale = 5.0e+4
lim = 100
mabiki = 4

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 6),facecolor='white')

pcord = np.array([1000,975,950,925,900,875,850,825,800,775,750,700,
        650,600,550,500,450,400,350,300,250,225,200,175,150,125,100,70,
        50,30,20,10,7,5,3,2,1])

ycord = np.arange(-90, 90.1, 1.25)
# ylon=([1000, 500, 100, 50, 10, 5, 1])
ylon=([100, 50, 10, 5, 1])
# chei=(["1000", "500", "100", "50", "10", "5", "1"])
chei=(["100", "50", "10", "5", "1"])
ax.set_ylim(lim,1.0)
ax.set_xlim(-90,90)
ax.set_yscale('log')
ax.set_yticks(ylon)
ax.set_yticklabels(chei)
ax.set_xlabel('LAT')
ax.set_ylabel('pressure')
# ax.imshow(vmin=1e-6,vmax=1e+6)

# num = 0
for a in range(len(pcord)):
    if pcord[a] == lim:
        num = a

min_value ,max_value = -100, 100
div=40      #図を描くのに何色用いるか
delta=(max_value-min_value)/div
interval=np.linspace(min_value,max_value,div+1)
# print(interval)
# interval=np.arange(min_value,abs(max_value)*2+delta,delta)[0:int(div)+1]
X,Y=np.meshgrid(ycord,pcord)
# cont = plt.contour(X,Y,zonalhgt,colors='black')
contf = plt.contourf(X,Y,nablaF,interval,cmap='bwr',extend='both') #cmap='bwr_r'で色反転, extend='both'で範囲外設定
q = plt.quiver(X[num:,2::mabiki], Y[num:,2::mabiki], Fy[num:,2::mabiki], Fz[num:,2::mabiki]*100,pivot='middle',
                scale_units='xy', headwidth=5,scale=vector_scale, color='green',width=0.005)
plt.title(f'{month}/{day}/{year} E-Pflux and ∇',fontsize=20)
plt.colorbar(contf)
file =  f'./picture/day/{year}/{year}{str(month).zfill(2)+str(day).zfill(2)}_E-Pflux.png'
if not os.path.exists(file[:13]+f'/{year}'):
    os.makedirs(file[:13]+f'/{year}')
plt.savefig(file)
