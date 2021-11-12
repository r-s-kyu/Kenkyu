
# %%
from matplotlib import animation
import numpy as np
import math
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import calendar

# ===========================初期値====================================
# year = 2020
startyear =2011
endyear =2012
startdate = [8, 10]
enddate = [11, 10]
# month = 8
# day = 20
# =====================================================================


# ===========================定数======================================


pcord = np.array([1000,975,950,925,900,875,850,825,800,775,750,700,
        650,600,550,500,450,400,350,300,250,225,200,175,150,125,100,70,
        50,30,20,10,7,5,3,2,1])
phicord = np.arange(-90,91,1.25)*(math.pi/180.)
ycord = np.arange(-90, 90.1, 1.25)
# ylon=([1000, 500, 100, 50, 10, 5, 1])
ylon=([100, 50, 10, 5, 1])
# chei=(["1000", "500", "100", "50", "10", "5", "1"])
chei=(["100", "50", "10", "5", "1"])
vector_scale = 8.0e+5
lim = 100
mabiki = 5
for a in range(len(pcord)):
    if pcord[a] == lim:
        num = a
min_value ,max_value = -100, 100
div=40      #図を描くのに何色用いるか
# delta=(max_value-min_value)/div
interval=np.linspace(min_value,max_value,div+1)
X,Y=np.meshgrid(ycord,pcord)



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

namelist = ['tmp','ugrd','vgrd', 'hgt']
kindlist = ['zonal','dev']
# =======================================================================


def allDayChangeToDate(year, day_count):
    month = 1
    sumDay2 = (date(year, month, calendar.monthrange(year, month)[1])-date(year, 1, 1)).days + 1
    while sumDay2<day_count:
        month +=1
        sumDay2 = (date(year, month, calendar.monthrange(year, month)[1])-date(year, 1, 1)).days + 1
    
    day = 1
    sumDay3 = (date(year, month, day)-date(year, month, 1)).days + 1
    while sumDay3 < day_count:
        day += 1
        sumDay3 = (date(year, month, day)-date(year, 1, 1)).days + 1
    return month, day


def epFlux(dc,year):
    for name in namelist:
        if name == 'hgt':
            kind = kindlist[0]
        else:
            kind = kindlist[1]
        savefile = f'D:/data/JRA55/{name}/{year}/{year}d{str(dc).zfill(3)}_{name}_{kind}.npy'
        globals()[kind + name] = np.load(savefile)

    dp = np.array([])
    for i in range(len(pcord)-1):
        dp = np.append(dp, pcord[i]-pcord[i+1])
    dp = np.append(dp,1)

    vudev_mean = np.mean(devvgrd*devugrd,axis=2)
    Fy = (((-1)*a*vudev_mean*np.cos(phicord)).T*rho).T
    devFy = np.gradient(Fy*np.cos(phicord), phicord,axis=1)
    z = -H*np.log(pcord*100/ps)
    vTdev_mean = np.mean(devvgrd*devtmp,axis=2)
    Fz = ((a*np.cos(phicord)*f*R*vTdev_mean/(N_2*H)).T*rho).T
    devFz = np.gradient(Fz,z,axis=0)
    nablaF = devFy/(a*np.cos(phicord)) + devFz
    # fzmean = np.mean(np.mean(nablaF))
    nablaF = ((nablaF/(a*np.cos(phicord))).T/rho).T
    nablaF = nablaF*60*60*24
    # fmean = np.mean(np.mean(nablaF))
    return Fy, Fz, nablaF


# year =2010


#アニメーションの各時間で図を作成
def update(frame, year):
    # if frame != 0:
    #     plt.cla()
    month, day = allDayChangeToDate(year, frame+1)
    # dc = (date(year,month,day)-fday).days + 1
    Fy, Fz, nablaF = epFlux(frame+1,year)

    # num = 0
 
    # print(interval)
    # interval=np.arange(min_value,abs(max_value)*2+delta,delta)[0:int(div)+1]
    # cont = plt.contour(X,Y,zonalhgt,colors='black')
    # plt.cla()
    contf = plt.contourf(X,Y,nablaF,interval,cmap='bwr',extend='both') #cmap='bwr_r'で色反転, extend='both'で範囲外設定
    q = plt.quiver(X[num:,2::mabiki], Y[num:,2::mabiki], Fy[num:,2::mabiki], Fz[num:,2::mabiki]*100,pivot='middle',
                    scale_units='xy', headwidth=5,scale=vector_scale, color='green',width=0.005)
    plt.title(f'{month}/{day}/{year} E-Pflux and ∇',fontsize=20)
    # plt.savefig('./warota.png')

def makeAnimation(year):

    fday = date(year,1,1)
    # eday = date(year,12,31)
    # yearallday = (fday-eday).days+1
    # yearallday = 10

    startcday = (date(year,startdate[0],startdate[1])-fday).days + 1
    endcday = (date(year,enddate[0],enddate[1])-fday).days + 1
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # vector_scale = 5.0e+4
    
    ax.set_yscale('log')
    ax.set_yticks(ylon)
    ax.set_yticklabels(chei)
    ax.set_xlabel('LAT')
    ax.set_ylabel('pressure')
    # ax.imshow(vmin=1e-6,vmax=1e+6)
    ax.set_ylim(lim,1.0)
    ax.set_xlim(-80,-30)

    # startdate = 222
    # enddate = 366
    anim = FuncAnimation(fig, update, fargs = [year], frames = np.arange(startcday,endcday+1), interval = 500)
    # ax.colorbar(contf)
    # plt.show()
    w = animation.PillowWriter(fps=100)
    startStr = f'{year}{str(startdate[0]).zfill(2)+str(startdate[1]).zfill(2)}'
    endStr = f'{year}{str(enddate[0]).zfill(2)+str(enddate[1]).zfill(2)}'
    filename = f'D:/picture/study/JRA55/animation/ani{startStr}_{endStr}.gif'
    anim.save(filename, writer = 'imagemagick')
    print(f'finish {year}')

def main():
    for year in range(startyear,endyear+1):
        makeAnimation(year)
    # makeAnimation(year)
    print(f'finish program!')


main()