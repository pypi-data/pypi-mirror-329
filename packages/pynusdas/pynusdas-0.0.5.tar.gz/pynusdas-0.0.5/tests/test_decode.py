import logging
from pynus import decode_nusdas

# set up the logger (probably unnecessary)
logger = logging.getLogger(__name__)

# showin DEBUG level messages 
logging.basicConfig(level=logging.DEBUG) #, format='%(levelname)s - %(name)s - %(asctime)s - %(message)s')

# showing messages in and above the INFO level in pynus.decode
logging.getLogger('pynus.decode').setLevel(logging.DEBUG)



for dd in [2009100701 + hh for hh in range(0, 1)]:
    mdls, surfs = decode_nusdas(f"./data/fcst_mdl.nus/ZSSTD1/{dd:10d}00", variables=['RU'])

    mdls.to_netcdf(f"./tmp/MF10km_MDLL_{dd:10d}00.nc")
    surfs.to_netcdf(f"./tmp/MF10km_SURF_{dd:10d}00.nc")
