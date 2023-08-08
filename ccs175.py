# -*- coding: utf-8 -*-
"""
Created on Wed May 10 16:22:41 2023

@author: rchaw
"""

import os
import time
import matplotlib.pyplot as plt
import math
from ctypes import *
import sys
class spectrometer:
    def __init__(self, address = b"USB0::0x1313::0x8087::M00335005::RAW", library = "TLCCS_64.dll"):
        self.add = address
        self.lib = cdll.LoadLibrary(library)
        self.address = address
        self.ccs_handle=c_int(0)
        self.integration_time=c_double(0)
        
        self.wavelengths=(c_double*3648)()
        self.lib.tlccs_init(self.add, 1, 1, byref(self.ccs_handle)) 
    def set_integration_time(self,time):
        try:
            #For convenience the integration time is entered here in ms.
            #But please note that tlccs_setIntegrationTime has seconds as input, hence the factor of 0.001.
            self.integration_time = c_double(time)#c_double(0.001 * float(input("Please enter the integration time of the spectrometer in ms (allowed range is 0.01 - 60000 ms): ")))
            if  self.integration_time.value < 1e-5:
                print("Entered integration time is too small. Integration time will be set to 0.01 ms.")
                self.integration_time = c_double(1e-5)     
            elif self.integration_time.value > 6e1:
                print("Entered integration time is too high. Integration time will be set to 60000 ms.")
                self.integration_time = c_double(6e1)
        except:
            print("Error: Incorrect input. Please do not use letters, only use numbers.")
            print("Code will be stopped.")
            sys.exit()

        #Set integration time in  seconds, ranging from 1e-5 to 6e1
        self.lib.tlccs_setIntegrationTime(self.ccs_handle, self.integration_time)
    def get_spectrum(self):
        #input("Press ENTER to start measurement of spectrum.")
        self.lib.tlccs_startScan(self.ccs_handle)
        data_array_ref=(c_double*3648)()
        status = c_int(0)

        while (status.value & 0x0010) == 0:
            self.lib.tlccs_getDeviceStatus(self.ccs_handle, byref(status))
            print(status)

        self.lib.tlccs_getScanData(self.ccs_handle, byref(data_array_ref))
        print("spectrum recorded.")
        print()
        return data_array_ref
    def get_wavelengths(self):
    
        self.lib.tlccs_getWavelengthData(self.ccs_handle, 0, byref(self.wavelengths), c_void_p(None), c_void_p(None))
        return self.wavelengths
    def close(self):
        self.lib.tlccs_close(self.ccs_handle)
        print('Spectrometer Object closed')
'''spec = spectrometer()
spec.set_integration_time(2e-3) # 2 mss
for i in range(5):
    time.sleep(.5)
    intensity = spec.get_spectrum()
    wav = spec.get_wavelengths()
intensity = spec.get_spectrum()
wav = spec.get_wavelengths()
plt.plot(wav, intensity)
plt.xlabel('Wavelength [nm]')
plt.ylabel('Intensity [a.u.]')
plt.ylim(-0.1, .1)
plt.grid(True)
spec.close()'''
