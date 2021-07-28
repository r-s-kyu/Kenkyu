import time
import numpy as np
fileHGT = f'D:/気象データ/HGT/anl_p_hgt.2020.bin'
print('open')
s = time.time()
fHGT = open(fileHGT, 'rb')
print(time.time()-s)
print('読み込み')
s = time.time()
dataHGT = np.fromfile(fHGT,dtype='>f').reshape(366,37,145,288)
print(time.time()-s)
print('ソート')
s = time.time()
HGT4 = dataHGT[:,:,::-1]
print(time.time()-s)
print('平均')
s = time.time()
zonalHGT = np.mean(HGT4,axis=3)
print(time.time()-s)
# test = HGT4
# test2 = zonalHGT



print('次元追加　帯状偏差')
start2 = time.time()
devHGT2 = HGT4 - zonalHGT[..., np.newaxis]
print(time.time()-start2)