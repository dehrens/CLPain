# Loading the libraries needed
import tdt # These are the functions for tdt
import pandas as pd 
import os
import numpy as np
import scipy.signal as ss
import matplotlib.pyplot as plt # this is used for plotting
import matplotlib.colors as colors


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
#Plot stimulation signal

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


# Declare the size of the time-lock window before and after
prestim_winsize = round( fs_lfp * 0.1) # this is for 100 msec 
postim_winsize = round( fs_lfp * 0.4 )# this is for 400 msec
tlock_wsize = prestim_winsize+postim_winsize
# Transform peak location in stim signal to location in lfp signal
lfp_locs = peak_locs*fs_lfp//fs_stim
pulse_period = (lfp_locs[2]-lfp_locs[1])/ fs_lfp
# Select the time-lock window size 
time_vect = np.arange(tlock_wsize)/fs_lfp - .1 # create time vector
time_msvect = np.round(time_vect*1000) # Vector of time in miliseconds

# This is the matrix that stacks all the evoked responses. 
# dim [LFP instances x #stimulations]
stacked_responses = np.empty((tlock_wsize,NumberStims))

# For now is only one channel but here you would create a matrix for more channels
lfp_data = LFP_signal_ch1* 1000
path = os.path.normpath(exp_path)
split_path = path.split(os.sep)
expid = split_path[-1]

print('Stimuliation nb=',str(NumberStims),' amp=',str(StimAmp),'  period=',str(pulse_period))

plt.figure(0)
plt.plot(Stim_signal_ch1)
plt.show
#plt.savefig(exp_path+'/FIG_'+expid+'_StimSignal.png')
#plt.close()
plt.figure(1)
plt.plot(LFP_signal_ch1)
plt.show
#plt.savefig(exp_path+'/FIG_'+expid+'_LFPsignal.png')
#plt.close()





# Trial figure

spacing_trials = 0.3
fig = plt.figure(2)
ax = plt.axes()

plt.style.use('_classic_test_patch')

for pulse in range(0,NumberStims):
    start_idx = int(lfp_locs[pulse] - prestim_winsize)
    end_idx = int(lfp_locs[pulse] + postim_winsize)
    stacked_responses[:,pulse] = lfp_data[start_idx:end_idx]
    plt.plot(time_msvect,stacked_responses[:,pulse]+spacing_trials*pulse,)  # comment for stacked response
    #plt.plot(time_msvect,stacked_responses[:,pulse],) # UNcomment for stacked response

Amplitude_limit = 0.5;    
ylabs = [str(x+1) for x in range(NumberStims )]
ax.set_yticks([ x*spacing_trials for x in range(NumberStims)]) # comment for stacked response
ax.set_yticklabels(ylabs) # comment for stacked response
plt.xlim(time_msvect[0],time_msvect[-1])
plt.ylim(-0.7,NumberStims*spacing_trials+0.2)

#plt.ylim(-Amplitude_limit,Amplitude_limit) # UNcomment for stacked response


plt.xlabel('Time [msec]')
plt.ylabel('Trial #')
plt.title('Response over trials')
plt.show

path = os.path.normpath(exp_path)
split_path = path.split(os.sep)
expid = split_path[-1]

#plt.savefig(exp_path+'/FIG_'+expid+'_TrialsResponse.png')
#plt.close()



avg_response = np.mean(stacked_responses,axis=1)
std_dev_response = np.std(stacked_responses,axis=1)


# AVG response
Amplitude_limit = 0.7;# window amplitude limit for the response

figavg = plt.figure(3)
plt.plot(time_msvect,avg_response,color='b')
plt.plot(time_msvect,avg_response+std_dev_response,linestyle='dotted',color='k')
plt.plot(time_msvect,avg_response-std_dev_response,linestyle='dotted',color='k')
plt.ylim(-Amplitude_limit,Amplitude_limit)
plt.xlim(time_msvect[0],time_msvect[-1])
plt.xlabel('Time [msec]')
plt.ylabel('Amplitude [mV]')
plt.title('Averaged Response')
plt.show()

#plt.savefig(exp_path+'/FIG_'+expid+'_AvgResponse.png')
#plt.close()

# Spectral Analysis
#______________________________________________________________________________
# Get the power of the signal using Welch's method of the FFT
#f, PSD = ss.welch(lfp_data, fs_lfp)


# Do a loop for the different frequencies
#f, t, Sxx = scipy.signal.spectrogram(lfp_data[1,:],fs_lfp,window=('hamming'),nperseg=600,noverlap=200)
#Sxx_altered = 10e15*Sxx




#plt.figure(1)
#plt.pcolormesh(t[0:100],f[0:30],Sxx_altered[0:30,0:100],vmin=30,vmax=6000000)
#plt.xlabel('Time [s]')
#plt.ylabel('Frequency [Hz]')
#plt.show()




