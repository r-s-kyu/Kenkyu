
# %%
import numpy as np
import math
from datetime import date

year = 2020
month = 2
day = 1
fday = date(year,1,1)

dc = (date(year,month,day)-fday).days + 1

namelist = ['temp','ugrd','vgrd']
# kindlist = ['data','zonal','dev']
kindlist = ['dev']

for kind in kindlist:
    for name in namelist:
        savefile = f'../../data/JRA55/{name}/{year}/{year}d{str(dc).zfill(3)}_{name}_{kind}.npy'
        globals()[kind + name] = np.load(savefile)

pcord = np.array([1000,975,950,925,900,875,850,825,800,775,750,700,
        650,600,550,500,450,400,350,300,250,225,200,175,150,125,100,70,
        50,30,20,10,7,5,3,2,1])

dp = np.array([])
for i in range(len(pcord)-1):
    dp = np.append(dp, pcord[i]-pcord[i+1])
dp = np.append(dp,1)
# print(pcord)

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

vudev_mean = np.mean(devvgrd*devugrd,axis=2)
Fy = (((-1)*a*vudev_mean*np.cos(phicord)).T*rho).T
devFy = np.gradient(Fy*np.cos(phicord), phicord,axis=1)

z = -H*np.log(pcord*100/ps)
vTdev_mean = np.mean(devvgrd*devtemp,axis=2)
Fz = ((a*np.cos(phicord)*f*R*vTdev_mean/(N_2*H)).T*rho).T
devFz = np.gradient(Fz,z,axis=0)

nablaF = devFy/(a*np.cos(phicord)) + devFz

vector_scale = 1.0e+6
# vector_scale = 5.0e+4
lim = 100
mabiki = 5

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 8),facecolor='white')

pcord = np.array([1000,975,950,925,900,875,850,825,800,775,750,700,
        650,600,550,500,450,400,350,300,250,225,200,175,150,125,100,70,
        50,30,20,10,7,5,3,2,1])

ycord = np.arange(-90, 90.1, 1.25)
ylon=([1000, 500, 100, 50, 10, 5, 1])
chei=(["1000", "500", "100", "50", "10", "5", "1"])
ax.set_ylim(lim,1.0e-1)
ax.set_xlim(30,80)
ax.set_yscale('log')
ax.set_yticks(ylon)
ax.set_yticklabels(chei)
ax.set_xlabel('LAT')
ax.set_ylabel('pressure')

for a in range(len(pcord)):
    if pcord[a] == lim:
        num = a

X,Y=np.meshgrid(ycord,pcord)
cont = plt.contourf(X,Y,nablaF)
q = plt.quiver(X[num:,2::mabiki], Y[num:,2::mabiki], Fy[num:,2::mabiki], Fz[num:,2::mabiki]*100,pivot='middle',
                scale_units='xy', headwidth=5,scale=vector_scale, color='green',width=0.005)
plt.rcParams['image.cmap'] = 'bwr'
plt.colorbar(cont)
plt.savefig('./warota.png')