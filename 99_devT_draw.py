# %%
import numpy as np
import math
from datetime import date
import os
import matplotlib.pyplot as plt


year = 2020
month = 10
day = 1
fday = date(year,1,1)
name = 'tmp'
kind = 'dev'

# ====================描画値===================
vector_scale = 8.0e+5
lim = 100
mabiki = 5
yticks=([100, 50, 10, 5, 1])
ylabel=(["100", "50", "10", "5", "1"])
latrange = [-80,-30]
Fztimes = 500

dc = (date(year,month,day)-fday).days + 1

savefile = f'D:/data/JRA55/{name}/{year}/{year}d{str(dc).zfill(3)}_{name}_{kind}.npy'
devT = np.load(savefile)
# devT = devT[:,:,0]

print(devT)
print(devT.shape)
print(np.where(devT!=0.))

pcord = np.array([1000,975,950,925,900,875,850,825,800,775,750,700,
        650,600,550,500,450,400,350,300,250,225,200,175,150,125,100,70,
        50,30,20,10,7,5,3,2,1])
phicord = np.arange(-90,91,1.25)*(math.pi/180.)
ycord = np.arange(-90, 90.1, 1.25)


def draw():
    fig, ax = plt.subplots(facecolor='grey')
    ax.set_ylim(lim,1.0)
    ax.set_xlim(latrange[0],latrange[1])
    ax.set_yscale('log')
    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabel)
    ax.set_xlabel('LAT')
    ax.set_ylabel('pressure')

    # for prsnum in range(len(pcord)):
    #     if pcord[prsnum] == lim:
    #         num = prsnum

    min_value ,max_value = 150, 300
    div=40      #図を描くのに何色用いるか
    interval=np.linspace(min_value,max_value,div+1)
    X,Y=np.meshgrid(ycord,pcord)
    # for y in range(syear, eyear+1):
    #     Fy, Fz, nablaF = makeEPflux(y)
    #     axnum = y - syear
        # cont = ax[axnum].contour(X,Y,zonalhgt,colors='black')
    contf = ax.contourf(X,Y,devT,interval,cmap='jet',extend='both') #cmap='bwr_r'で色反転, extend='both'で範囲外設定
        # q = ax[axnum].quiver(X[num:,2::mabiki], Y[num:,2::mabiki], Fy[num:,2::mabiki], Fz[num:,2::mabiki]*Fztimes,pivot='middle',
        #             scale_units='xy', headwidth=5,scale=vector_scale, color='green',width=0.005)
        # ax[axnum].set_title(f'{y}',fontsize=15)
    fig.suptitle(f'{month}/{day}/{year} T',fontsize=20)
    axpos = ax.get_position()
    cbar_ax = fig.add_axes([0.87, axpos.y0, 0.02, axpos.height])
    fig.colorbar(contf,cax=cbar_ax)
    plt.subplots_adjust(right=0.85)
    plt.subplots_adjust(wspace=0.15)
    plt.savefig(f'./picture/test/devT/{str(month).zfill(2)+str(day).zfill(2)}_T.png')

def main():
    # draw()
    print('finish')

if __name__ == '__main__':
    main()