# %%
import numpy as np

Fy = np.zeros((180,37),dtype=np.float64)*np.nan
Fz = np.zeros((180,37),dtype=np.float64)*np.nan
rho = np.zeros((37),dtype=np.float64)*np.nan
H = np.zeros((37),dtype=np.float64)*np.nan
a = 6.37e+6

# %%
import numpy as np
file = f'C:/Users/riku satake/Documents/data/anl_p_hgt.2020.bin'

f = open(file, 'rb')

data = np.fromfile(f,dtype='>f').reshape(366,37,145,288)
data = data[:,:,::-1]
print(data[0,10])


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

T =250
H = R*T/g0
rhos = ps/R/Ts
rho = rhos*math.e**((-1)*z/H)

theta = T*(ps/p)**K