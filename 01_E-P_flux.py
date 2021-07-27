# %%
import numpy as np

Fy = np.zeros((180,37),dtype=np.float64)*np.nan
Fz = np.zeros((180,37),dtype=np.float64)*np.nan
rho = np.zeros((37),dtype=np.float64)*np.nan
H = np.zeros((37),dtype=np.float64)*np.nan
a = 6.37e+6

# %%
import numpy as np
fileHGT = f'C:/Users/riku satake/Documents/data/anl_p_hgt.2020.bin'
fileT = f'C:/Users/riku satake/Documents/data/anl_p_tmp.2020.bin'
fileU = f'C:/Users/riku satake/Documents/data/anl_p_ugrd.2020.bin'
fileV = f'C:/Users/riku satake/Documents/data/anl_p_vgrd.2020.bin'


fHGT = open(fileHGT, 'rb')
fT = open(fileT, 'rb')
fU = open(fileU, 'rb')
fV = open(fileV, 'rb')

dataHGT = np.fromfile(fHGT,dtype='>f').reshape(366,37,145,288)
dataT = np.fromfile(fT,dtype='>f').reshape(366,37,145,288)
dataU = np.fromfile(fU,dtype='>f').reshape(366,37,145,288)
dataV = np.fromfile(fV,dtype='>f').reshape(366,37,145,288)

HGT4 = dataHGT[:,:,::-1]
T4 = dataT[:,:,::-1]
U4 = dataU[:,:,::-1]
V4 = dataV[:,:,::-1]
# print(dataT[0,10])


# %%
import numpy as np
import math

a = 6.37e+6
R = 284
Cp = 1004
K = R/Cp
g0 = 9.80
ps = 1.00e+5
omega = 7.29e-5
Ts =  240

phi = 
f = 2*omega*math.sin(phi)

T = 250
H = R*T/g0
rhos = ps/R/Ts
rho = rhos*math.e**((-1)*z/H)

theta = T*(ps/p)**K