from ctypes import *
import ctypes 
import numpy as np
import xarray as xr

# set the in and out arrays ...
# Instead of appending rows, allocate a suitably sized array, and then assign to it row-by-row:

nsweeps = 4   

nazs = 4
azs = np.zeros(nazs, dtype=np.float32)
azs[0] = 0
azs[0] = 90
azs[0] = 180
azs[0] = 270

slice_delta_azimuth = 90

nGates = 5  
startRangeKm = 1.0  
gateSpacingKm = 0.1
radarLatitudeDeg = 30  # np.float64(dt_horizontal['/sweep_0'].latitude)
radarLongitudeDeg = 30 # np.float64(dt_horizontal['/sweep_0'].longitude)
radarAltitude = 1      # np.float64(dt_horizontal['/sweep_0'].altitude)
nyquist = 0.0

nrays = 4              #  nrays is number of rays per sweep
print("nrays = ", nrays)

isweep = 0
sweep_index = np.empty([nsweeps])
a = np.empty((nsweeps*nrays,nGates), dtype=np.float32)          # velocity data: [all_rays, nGates] =  [nsweeps*nrays, nGates]
# a = np.empty([nrays,nGates])                                  # velocity data: [all_rays, nGates] =  [nsweeps*nrays, nGates]
nAz = azs.size

print("rays shape = ", a.shape)
elevs = np.ones(4, dtype=np.float32)   
elevs[0] = 5.0
elevs[1] = 10.0
elevs[2] = 15.0
elevs[3] = 20.0

a[0,:]   = np.zeros(5, dtype=np.float32)
a[1,:]  = np.ones(5, dtype=np.float32)
a[2,:] = np.zeros(5, dtype=np.float32)
a[3,:] = np.ones(5, dtype=np.float32) * -1.0

a[4,:]   = np.zeros(5, dtype=np.float32)
a[5,:]  = np.ones(5, dtype=np.float32)
a[6,:] = np.zeros(5, dtype=np.float32)
a[7,:] = np.ones(5, dtype=np.float32) * -1.0

a[8,:]   = np.zeros(5, dtype=np.float32)
a[9,:]  = np.ones(5, dtype=np.float32)
a[10,:] = np.zeros(5, dtype=np.float32)
a[11,:] = np.ones(5, dtype=np.float32) * -1.0

a[12,:]   = np.zeros(5, dtype=np.float32)
a[13,:]  = np.ones(5, dtype=np.float32)
a[14,:] = np.zeros(5, dtype=np.float32)
a[15,:] = np.ones(5, dtype=np.float32) * -1.0

 # index of last ray for sweep
sweep_index[0] = 3
sweep_index[1] = 7
sweep_index[2] = 11
sweep_index[3] = 15

# really, rays is better named velocity, because it is the velocity data for all sweeps, for all azimuths/rays, for all gates/ranges
# rays = a  # need a flat structure of all the rays for all the sweeps for all the ranges/gates

# subsitute missing value for nans
rays = np.nan_to_num(a, copy=False, nan=-9999.0)

# use default for these ...
profile_max_height = 20.0
profile_min_height = 0.5
profile_height_interval = 0.5

nZ = (int) ((profile_max_height - profile_min_height) / profile_height_interval) + 1


#  uu,vv are calculated for each elevation and one elevation per sweep
ht = np.zeros(nZ, dtype=np.float32) # initialize to all zeros
uu = np.zeros(nZ, dtype=np.float32) # initialize to all zeros
vv = np.zeros(nZ, dtype=np.float32) # initialize to all zeros
ww = np.zeros(nZ, dtype=np.float32) # initialize to all zeros
div = np.zeros(nZ, dtype=np.float32) # initialize to all zeros

# create a pointer type ...
c_float_p = ctypes.POINTER(ctypes.c_float)
c_size_t_p = ctypes.POINTER(ctypes.c_size_t)

# make sure the in and out arrays are of the correct type ...
# x = x.astype(np.float32)
# y = y.astype(np.float32)
sweep_index = sweep_index.astype(np.uintp)
 
#  
## load the library ...
cdll.LoadLibrary("lroselite.dylib")
## <CDLL 'lroselite.dylib', handle 760e4eb0 at 0x1058fefd0>
lroselite = CDLL("lroselite.dylib")
lroselite.RadxEvad
## <_FuncPtr object at 0x105998790>
#
#
## set the in and out arrays ...
#
## call the C++ library ...
lroselite.RadxEvad(sweep_index.ctypes.data_as(c_size_t_p),  
    c_size_t(nsweeps),
    rays.ctypes.data_as(c_float_p), 
    c_size_t(nrays),
    elevs.ctypes.data_as(c_float_p), 
    azs.ctypes.data_as(c_float_p), 
    c_size_t(nGates),
    c_float(startRangeKm),
    c_float(gateSpacingKm),
    c_float(radarLatitudeDeg),
    c_float(radarLongitudeDeg),
    c_float(radarAltitude),
    c_float(nyquist),
    ht.ctypes.data_as(c_float_p),
    uu.ctypes.data_as(c_float_p),
    vv.ctypes.data_as(c_float_p),
    ww.ctypes.data_as(c_float_p),
    div.ctypes.data_as(c_float_p),
    c_float(profile_max_height),
    c_float(profile_min_height),
    c_float(profile_height_interval),
    c_int(slice_delta_azimuth),
    )
### 55625936

###
#### notice the changed output array ...
###ht
#### array([4., 4., 4., 1.], dtype=float32)
###uu
#### array([12., 13., 11.,  1.], dtype=float32)
###
###
