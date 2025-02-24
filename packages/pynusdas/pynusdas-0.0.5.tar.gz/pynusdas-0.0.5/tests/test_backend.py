import logging
import xarray as xr

# set up the logger (probably unnecessary)
logger = logging.getLogger(__name__)

# showin DEBUG level messages 
logging.basicConfig(level=logging.DEBUG) #, format='%(levelname)s - %(name)s - %(asctime)s - %(message)s')

# showing messages in and above the INFO level in pynus.decode
logging.getLogger('pynus.backend').setLevel(logging.INFO)


const=xr.open_dataset('/project/meteo/work/Takumi.Matsunobu/PRE/data/MF10km_MSM_M000/REF/fcst_const.nus/LYSTD1/200910061800', engine='pynus')
print(const)

for dd in [2009100701 + hh for hh in range(0, 1)]:
    mdls = xr.open_dataset(f"./data/fcst_mdl.nus/ZSSTD1/{dd:10d}00",
                          engine="pynus", chunks={"x": 19, "y": 17},)

    print(mdls)
