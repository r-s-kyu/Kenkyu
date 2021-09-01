# %%
import os

for year in range(2010,2020):
    oldname = f'D:/data/JRA55/tmp/anl_p_temp.{year}.bin'
    newname = f'D:/data/JRA55/tmp/anl_p_tmp.{year}.bin'
    os.rename(oldname,newname)

