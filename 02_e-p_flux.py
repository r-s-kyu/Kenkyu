
# %%
import numpy as np
import math

namelist = ['temp','ugrd','vgrd']
kindlist = ['data','zonal','dev']

for kind in kindlist:
    for name in namelist:
        savefile = f'../../dataJRA55/{name}/{name}_one_day_{kind}.npy'
        globals()[kind + name] = np.load(savefile)

pcord = np.array([1000,975,950,925,900,875,850,825,800,775,750,700,
        650,600,550,500,450,400,350,300,250,225,200,175,150,125,100,70,
        50,30,20,10,7,5,3,2,1])*100

phicord = np.arange(-90,91,1.25)*(2.*math.pi/180.)

a = 6.37e+6
R = 287
Cp = 1004
K = R/Cp
g0 = 9.80665
ps = 1.00e+5
omega = 7.29e-5
Ts =  240
H = R*Ts/g0
# print(H)
rhos = ps/R/Ts
# print(rhos)
Fy = np.zeros((145,37),dtype=np.float64)*np.nan
Fz = np.zeros((145,37),dtype=np.float64)*np.nan
N_2 = 4.0e-4
f = 2*omega*np.sin(phicord)
# print(np.sin(phicord))

vudev_mean = np.mean(devvgrd*devugrd,axis=2)
rho = rhos*(pcord/ps)
Fy = (((-1)*a*vudev_mean*np.cos(phicord)).T*rho).T

vTdev_mean = np.mean(devvgrd*devtemp,axis=2)
# Fz = ((a*np.cos(phicord)*f*R*vTdev_mean/(N**2*H)).T*rho).T
Fz = ((a*np.cos(phicord)*f*R*vTdev_mean/(N_2*H)).T*rho).T


# theta = (datatmp.T*(ps/pcord)**K).T # 3次元
# thetadev = (theta.T - np.mean(theta).T).T
# vthetadev_mean = np.mean(devvgrd*thetadev,axis=2)
# theta_z_dev = theta*K/H
# Fz = ((a*np.cos(phicord)*f*vthetadev_mean/np.mean(theta_z_dev,axis=2)).T*rho).T
# vector_scale = 1.0e+6
vector_scale = 5.0e+4
lim = 50
# print(Fy)
# print(np.mean(Fy,axis=1))
# print(Fy.shape)
# print(Fz.shape)
# print(Fy[-11:,:])
# print(Fz[-11:,:])
test1 = np.mean(Fy[-11:,:],axis=1)
# print(test1)
# print(len(test1))
test2 = np.mean(Fz[-11:,:],axis=1)
# print(test2)
# print(len(test2))
i = 5
j = 20
print((Fy[-1*i,2::7]**2+(Fz[-1*i,2::7]*100)**2)**0.5/vector_scale)
print((Fy[-1*j,2::7]**2+(Fz[-1*j,2::7]*100)**2)**0.5/vector_scale)
# print(Fy[-9,2::7],(Fz[-9,2::7]*100))

# print(np.mean(Fz,axis=1))
# T = datatmp[day,k,j,i]
# z = -1*H*math.log(p/ps)
# rho = rhos*math.e**((-1)*z/H)

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 10),facecolor='white')
# fig = plt.figure(facecolor='white')


pcord = np.array([1000,975,950,925,900,875,850,825,800,775,750,700,
        650,600,550,500,450,400,350,300,250,225,200,175,150,125,100,70,
        50,30,20,10,7,5,3,2,1])
ycord = np.arange(-90, 90.1, 1.25)
ylon=([ 50, 10, 5, 1])
chei=([ "50", "10", "5", "1"])
ax.set_ylim(lim,1.0e-1)
ax.set_xlim(30,80)
ax.set_yscale('log')
ax.set_yticks(ylon)
ax.set_yticklabels(chei)

for a in range(len(pcord)):
    if pcord[a] == lim:
        num = a


# print(pcord)
X,Y=np.meshgrid(ycord,pcord)

q = plt.quiver(X[num:,2::7], Y[num:,2::7], Fy[num:,2::7], Fz[num:,2::7]*100,pivot='middle',
                scale_units='xy', headwidth=5,scale=vector_scale, color='green',width=0.005)
# ylon=([1000, 500, 100, 50, 10, 5, 1])
# chei=(["1000", "500", "100", "50", "10", "5", "1"])
plt.savefig('./warota.png')

# %%

aa = np.arange(30)

print(aa)
print(aa[2::3])