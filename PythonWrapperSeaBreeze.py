
#David Dolt Testing
#Wrapper file in python to find spectrometer
#We need these ctypes to pass to functions
import ctypes
import sys
#Opening the dynamic library
myLib=ctypes.cdll.LoadLibrary('libseabreeze.dylib')
#Print test
print("hello")
#Setting some variables commonly used in every dll call
i=ctypes.c_int32(0)
error=ctypes.c_int32()



 #   this->usbEndpoint_primary_in = 0x81;
 #   this->usbEndpoint_secondary_out = 0;
 #   this->usbEndpoint_secondary_in = 0x82;
 #   this->usbEndpoint_secondary_in2 = 0x86;
#Can use this for size of
#ctypes.sizeof()

#opening the spectrometer
print(myLib.seabreeze_open_spectrometer(i, ctypes.byref(error)))
#Setting the integration time
second = 1000
print(myLib.seabreeze_set_integration_time_microsec(i,ctypes.byref(error), ctypes.c_int(100 * second)))
#Setting the trigger mode to the default mode
myLib.seabreeze_set_trigger_mode(i,ctypes.byref(error), ctypes.c_int(0))
#Finding the length of the formatted spectrum
FormattedLength= myLib.seabreeze_get_formatted_spectrum_length(i,ctypes.byref(error))
print(FormattedLength)
#Getting the length of the unformatted spectrum
raw_length=myLib.seabreeze_get_unformatted_spectrum_length(i,ctypes.byref(error))
print(raw_length)
#Finding the number of pixels
pixels=raw_length/2

#Getting the wavelengths
wave12 = ctypes.c_double * pixels
wavelengths = wave12()
WavePTR = ctypes.cast(wavelengths,ctypes.POINTER(ctypes.c_float))
#Here we get the wavelengths out in an array ?
#Or just ctypes.c_int(pixels)
seabreeze_get_wavelengths(i , ctypes.byref(error), WavePTR, ctypes.c_size_t(sys.getsizeof(waveDs))  );

temp = ctypes.c_double * pixels
Spectrum = temp()
SpectrumPTR = ctypes.cast(Spectrum,ctypes.POINTER(ctypes.c_float))
#Now we want to get the formatted spectrum
myLib.seabreeze_get_formatted_spectrum(i , ctypes.byref(error), SpectrumPTR,   ctypes.c_size_t(sys.getsizeof(Spectrum))    );


ctypes.POINTER(ctypes.c_float)
