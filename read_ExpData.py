
import tdt # These are the functions for tdt
import pandas as pd 
import numpy as np
import scipy.signal as ss
import matplotlib.pyplot as plt # this is used for plotting
import holoviews as hv
hv.extension('bokeh')

# Select folder to import data
from tkinter import Tk, filedialog
root = Tk() # pointing root to Tk() to use it as Tk() in program.
root.withdraw() # Hides small tkinter window.
root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
exp_path = filedialog.askdirectory(parent=root, initialdir='A:/ExpData_Tank',title= 'Hello! Please select the experiment to load!') # Returns opened path as str
print(exp_path)

# Read data
data = tdt.read_block(exp_path)
# Declare variables for stim signal and lfp signal
Stim_signal_ch1 = data.streams.eS1r.data[0,:]
LFP_signal_ch1 = data.streams.LFP1.data[0,:]
# Get the stimulation amplitude
StimAmp = max(Stim_signal_ch1)

# Find stimulation peaks location and amplitude
fs_lfp = data.streams.LFP1.fs
fs_stim = data.streams.eS1r.fs
peaks = ss.find_peaks(Stim_signal_ch1,height=StimAmp,distance=8)

# This can be done more efficiently I dont know enough about python
peak_locs = peaks[0]
peak_ampst = peaks[1]
peak_amps = peak_ampst['peak_heights']
# Get number of stimulations
NumberStims = len(peak_amps) # Can also be done with np.size(peak_locs)

print('Stimuliation nb=',str(NumberStims),' amp=',str(StimAmp))

# Declare the size of the time-lock window before and after
prestim_winsize = round( fs_lfp * 0.1) # this is for 100 msec 
postim_winsize = round( fs_lfp * 0.4 )# this is for 100 msec
tlock_wsize = prestim_winsize+postim_winsize
# Transform peak location in stim signal to location in lfp signal
lfp_locs = peak_locs*fs_lfp//fs_stim
# Select the time-lock window size 
time_vect = np.arange(tlock_wsize)/fs_lfp - .1 # create time vector
time_msvect = np.round(time_vect*1000) # Vector of time in miliseconds

# This is the matrix that stacks all the evoked responses. 
# dim [LFP instances x #stimulations]
stacked_responses = np.empty((tlock_wsize,NumberStims))

# For now is only one channel but here you would create a matrix for more channels
lfp_data = LFP_signal_ch1* 1000

# Plot stimulation signal
#plt.figure(0)
#plt.plot(Stim_signal_ch1)
# plt.show


fig = plt.figure(0)
ax = plt.axes()

for pulse in range(0,NumberStims):
    start_idx = int(lfp_locs[pulse] - prestim_winsize)
    end_idx = int(lfp_locs[pulse] + postim_winsize)
    stacked_responses[:,pulse] = lfp_data[start_idx:end_idx]
    plt.plot(time_msvect,stacked_responses[:,pulse]+.3*pulse)

ylabs = [str(x+1) for x in range(NumberStims )]
ax.set_yticks([ x*0.3 for x in range(NumberStims)])
ax.set_yticklabels(ylabs)
plt.xlim(time_msvect[0],time_msvect[-1])
plt.xlabel('Time [msec]')
plt.ylabel('Trial #')
plt.show
# fix ticks y labels  
avg_response = np.mean(stacked_responses,axis=1)
std_dev_response = np.std(stacked_responses,axis=1)



figavg = plt.figure(1)
plt.plot(time_msvect,avg_response,color='b')
plt.plot(time_msvect,avg_response+std_dev_response,linestyle='dotted',color='k')
plt.plot(time_msvect,avg_response-std_dev_response,linestyle='dotted',color='k')
plt.ylim(-0.5,0.5)
plt.xlim(time_msvect[0],time_msvect[-1])
plt.xlabel('Time [msec]')
plt.ylabel('Amplitude [mV]')
plt.show()


# Spectral Analysis
#______________________________________________________________________________
# Get the power of the signal using Welch's method of the FFT
f, PSD = ss.welch(lfp_data, fs_lfp)


# Do a loop for the different frequencies
#f, t, Sxx = scipy.signal.spectrogram(lfp_data[1,:],fs_lfp,window=('hamming'),nperseg=600,noverlap=200)
#Sxx_altered = 10e15*Sxx




#plt.figure(1)
#plt.pcolormesh(t[0:100],f[0:30],Sxx_altered[0:30,0:100],vmin=30,vmax=6000000)
#plt.xlabel('Time [s]')
#plt.ylabel('Frequency [Hz]')
#plt.show()




