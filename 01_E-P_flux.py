# %%
import numpy as np
import math

Fy = np.zeros((145,37),dtype=np.float64)*np.nan
Fz = np.zeros((145,37),dtype=np.float64)*np.nan

namelist = ['hgt','tmp','ugrd','vgrd']

def hensa(name,day):
    file = f'D:/気象データ/{name}/anl_p_{name}.2020.bin'
    f = open(file, 'rb')
    print(f'{name} 読み込み中')
    array = np.fromfile(f,dtype='>f').reshape(366,37,145,288)
    print(f'{name} 読み込み完了')
    f.close()
    data = array[day,:,:,::-1]
    zonal = np.mean(data,axis=2)
    # dev = data - zonal[..., np.newaxis]
    dev = (data.T - zonal.T).T
    return data, zonal, dev

# ----------------------------
day = 30*8+20
# ---------------------------


for name in namelist:
    globals()['data'+ name], globals()['zonal'+ name], globals()['dev'+ name]= hensa(name,day)
#%%
pcord = np.array([1000,975,950,925,900,875,850,825,800,775,750,700,
        650,600,550,500,450,400,350,300,250,225,200,175,150,125,100,70,
        50,30,20,10,7,5,3,2,1])

phicord = np.arange(-90,91,1.25)

a = 6.37e+6
R = 284
Cp = 1004
K = R/Cp
g0 = 9.80
ps = 1.00e+5
omega = 7.29e-5
Ts =  240
H = R*Ts/g0
rhos = ps/R/Ts

f = 2*omega*np.sin(phicord)
# print(np.sin(phicord))
vu_hensa = np.mean(devvgrd*devugrd,axis=2)
rho = rhos*(pcord/ps)
Fy = ((-1*a*vu_hensa*np.cos(phicord)).T*rho).T

theta = (datatmp.T*(ps/pcord)**K).T # 3次元
theta_z_dev = theta*K/H

vtheta_hensa = np.mean(devvgrd*theta,axis=2)
Fz = ((a*np.cos(phicord)*f*vtheta_hensa/np.mean(theta_z_dev,axis=2)).T*rho).T

# print(Fy)
print(np.mean(Fy,axis=1))
# print(Fy.shape)
# print(Fz)
print(np.mean(Fz,axis=1))
# T = datatmp[day,k,j,i]
# z = -1*H*math.log(p/ps)
# rho = rhos*math.e**((-1)*z/H)



# %%
# import time
# import numpy as np
# fileHGT = f'D:/気象データ/HGT/anl_p_hgt.2020.bin'
# print('open')
# s = time.time()
# fHGT = open(fileHGT, 'rb')
# print(time.time()-s)
# print('読み込み')
# s = time.time()
# dataHGT = np.fromfile(fHGT,dtype='>f').reshape(366,37,145,288)
# print(time.time()-s)
# print('ソート')
# s = time.time()
# HGT4 = dataHGT[:,:,::-1]
# print(time.time()-s)
# print('平均')
# s = time.time()
# zonalHGT = np.mean(HGT4,axis=3)
# print(time.time()-s)
# # test = HGT4
# # test2 = zonalHGT
# print('転置　帯状偏差')
# start1 = time.time()
# devHGT1 = (HGT4.T - zonalHGT.T).T
# print(time.time()-start1)
# print('次元追加　帯状偏差')
# start2 = time.time()
# devHGT2 = HGT4 - zonalHGT[..., np.newaxis]
# print(time.time()-start2)