
# %%
import numpy as np

namelist = ['hgt','tmp','ugrd','vgrd']
kindlist = ['data','zonal','dev']

for kind in kindlist:
    for name in namelist:
        savefile = f'{name}_one_day_{kind}.npy'
        globals()[kind + name] = np.load(savefile)

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
Fy = np.zeros((145,37),dtype=np.float64)*np.nan
Fz = np.zeros((145,37),dtype=np.float64)*np.nan

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
print(Fy.shape)
print(Fz.shape)
print(Fz)
print(np.mean(Fz,axis=1))
# T = datatmp[day,k,j,i]
# z = -1*H*math.log(p/ps)
# rho = rhos*math.e**((-1)*z/H)


# %%
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(10, 10),facecolor='white')
# fig = plt.figure(facecolor='white')


pcord = np.array([1000,975,950,925,900,875,850,825,800,775,750,700,
        650,600,550,500,450,400,350,300,250,225,200,175,150,125,100,70,
        50,30,20,10,7,5,3,2,1])
ycord = np.arange(-90, 90.1, 1.25)
print(pcord)
X,Y=np.meshgrid(ycord,pcord)
q = plt.quiver(X, Y, Fy, Fz*100,pivot='middle', scale_units='xy', headwidth=5,scale=10000)
# ylon=([1000, 500, 100, 50, 10, 5, 1])
ylon=([100, 50, 10, 5, 1])
# chei=(["1000", "500", "100", "50", "10", "5", "1"])
chei=(["100", "50", "10", "5", "1"])
ax.set_ylim(100,1)
ax.set_xlim(30,80)
ax.set_yscale('log')
ax.set_yticks(ylon)
ax.set_yticklabels(chei)
plt.savefig('./warota.png')