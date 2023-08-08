# -*- coding: utf-8 -*-
"""
Created on Wed May 10 14:29:20 2023

@author: rchaw
"""

# -*- coding: utf-8 -*-
"""
Example of C Libraries for CCS Spectrometers in Python with CTypes

"""
import os
import time
import matplotlib.pyplot as plt
from ctypes import *

#os.chdir(r"C:\Program Files\IVI Foundation\VISA\Win64\Bin")
lib = cdll.LoadLibrary("TLCCS_64.dll")

ccs_handle=c_int(0)

#documentation: C:\Program Files\IVI Foundation\VISA\Win64\TLCCS\Manual

#Start Scan- Resource name will need to be adjusted
#windows device manager -> NI-VISA USB Device -> Spectrometer -> Properties -> Details -> Device Instance ID
lib.tlccs_init(b"USB\VID_1313&PID_8087\M00335005", 1, 1, byref(ccs_handle))   

#set integration time in  seconds, ranging from 1e-5 to 6e1
integration_time=c_double(1)
lib.tlccs_setIntegrationTime(ccs_handle, integration_time)


#start scan
lib.tlccs_startScan(ccs_handle)
# Let's look into the below and see if this is a pointer then let's populate this with wavelength valuess
wavelengths=(c_double*3648)()
wav = 1e-9
for i in range(3648):
    wavelengths[i] = wav
    wav+=1e-9
lib.tlccs_getWavelengthData(ccs_handle, 0, byref(wavelengths), c_void_p(None), c_void_p(None))

#retrieve data
data_array=(c_double*3648)()
lib.tlccs_getScanData(ccs_handle, byref(data_array))
print(wavelengths)
print(data_array)
#plot data
plt.plot(wavelengths, data_array)
plt.xlabel("Wavelength [nm]")
plt.ylabel("Intensity [a.u.]")
plt.grid(True)
plt.show()

#close
lib.tlccs_close (ccs_handle)

