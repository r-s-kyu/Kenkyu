
# %%
import numpy as np
import math
from datetime import date
import matplotlib.pyplot as plt
import os
# ====================初期値===================
meanstart = 2010
meanend = 2019
year = 2020
month = 11
day = 11

# ====================描画値===================
vector_scale = 8.0e+5
lim = 100
mabiki = 5
yticks=([100, 50, 10, 5, 1])
ylabel=(["100", "50", "10", "5", "1"])
latrange = [-80,-30]

# ====================定数=====================
meanyears = meanend - meanstart + 1
pcord = np.array([1000,975,950,925,900,875,850,825,800,775,750,700,
        650,600,550,500,450,400,350,300,250,225,200,175,150,125,100,70,
        50,30,20,10,7,5,3,2,1])
phicord = np.arange(-90,91,1.25)*(math.pi/180.)
ycord = np.arange(-90, 90.1, 1.25)
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
z = -H*np.log(pcord*100/ps)
namelist = ['tmp','ugrd','vgrd', 'hgt']
kindlist = ['zonal','dev']

def makeEPflux(year):
    fday = date(year,1,1)
    dc = (date(year,month,day)-fday).days + 1

    for name in namelist:
        if name == 'hgt':
            kind = kindlist[0]
        else:
            kind = kindlist[1]
        savefile = f'D:/data/JRA55/{name}/{year}/{year}d{str(dc).zfill(3)}_{name}_{kind}.npy'
        globals()[kind + name] = np.load(savefile)

    vudev_mean = np.mean(devvgrd*devugrd,axis=2)
    Fy = (((-1)*a*vudev_mean*np.cos(phicord)).T*rho).T
    devFy = np.gradient(Fy*np.cos(phicord), phicord,axis=1)

    vTdev_mean = np.mean(devvgrd*devtmp,axis=2)
    Fz = ((a*np.cos(phicord)*f*R*vTdev_mean/(N_2*H)).T*rho).T
    devFz = np.gradient(Fz,z,axis=0)
    nablaF = devFy/(a*np.cos(phicord)) + devFz
    nablaF = ((nablaF/(a*np.cos(phicord))).T/rho).T
    nF = nablaF*60*60*24    
    return Fy, Fz, nF

def meanYear(startYear,endYear):
    Fy, Fz, nF = makeEPflux(startYear)
    fy_3d, fz_3d, nf_3d = Fy[np.newaxis], Fz[np.newaxis], nF[np.newaxis]
    for year in range(startYear+1,endYear+1):
        Fy, Fz, nF = makeEPflux(year)
        fy_3d = np.append(fy_3d,Fy[np.newaxis],axis=0)
        fz_3d = np.append(fz_3d,Fz[np.newaxis],axis=0)
        nf_3d = np.append(nf_3d,nF[np.newaxis],axis=0)
    FyMean = np.mean(fy_3d,axis=0)
    FzMean = np.mean(fz_3d,axis=0)
    nFMean = np.mean(nf_3d,axis=0)
    return FyMean, FzMean, nFMean

def draw():
    fig, axes = plt.subplots(1,2,figsize=(7, 6),facecolor='grey',sharex=True,sharey=True)
    axes[0].set_ylim(lim,1.0)
    axes[0].set_xlim(latrange[0],latrange[1])
    axes[0].set_yscale('log')
    axes[0].set_yticks(yticks)
    axes[0].set_yticklabels(ylabel)
    axes[0].set_xlabel('LAT')
    axes[0].set_ylabel('pressure')

    for prsnum in range(len(pcord)):
        if pcord[prsnum] == lim:
            num = prsnum

    min_value ,max_value = -80, 80
    div=40      #図を描くのに何色用いるか
    interval=np.linspace(min_value,max_value,div+1)
    X,Y=np.meshgrid(ycord,pcord)
    for y in range(2):
        if y == 0:
            Fy, Fz, nablaF = meanYear(meanstart,meanend)
            title = '10years mean'
        else:
            Fy, Fz, nablaF = makeEPflux(year)
            title = str(year)
        # cont = axes[axnum].contour(X,Y,zonalhgt,colors='black')
        contf = axes[y].contourf(X,Y,nablaF,interval,cmap='bwr',extend='both') #cmap='bwr_r'で色反転, extend='both'で範囲外設定
        q = axes[y].quiver(X[num:,2::mabiki], Y[num:,2::mabiki], Fy[num:,2::mabiki], Fz[num:,2::mabiki]*100,pivot='middle',
                    scale_units='xy', headwidth=5,scale=vector_scale, color='green',width=0.005)
        axes[y].set_title(f'{title}',fontsize=15)
    fig.suptitle(f'{month}/{day} E-Pflux and ∇',fontsize=20)
    axpos = axes[0].get_position()
    cbar_ax = fig.add_axes([0.87, axpos.y0, 0.02, axpos.height])
    fig.colorbar(contf,cax=cbar_ax)
    plt.subplots_adjust(right=0.85)
    plt.subplots_adjust(wspace=0.15)
    if not os.path.exists(f'D:/picture/study/JRA55/yearsmean_2020/{month}'):
        os.makedirs(f'D:/picture/study/JRA55/yearsmean_2020/{month}')
    plt.savefig(f'D:/picture/study/JRA55/yearsmean_2020/{month}/{meanyears}yearsMeanTo{year}_{str(month).zfill(2)+str(day).zfill(2)}_E-Pflux.png')

def main():
    draw()

if __name__ == '__main__':
    main()
