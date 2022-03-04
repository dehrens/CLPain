import tdt
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
data = tdt.read_block('C:\TDT\Synapse\Tanks\Rec_StimJHU-210915-132412\sub-10-211028-105951')
plt.figure(0)
plt.plot(data.streams.eS1r.data[0,:])
plt.show

fs_lfp = data.streams.TET1.fs
fs_stim = data.streams.eS1r.fs
peaks = scipy.signal.find_peaks(data.streams.eS1r.data[0,:],height=100,distance=8)
peak_locs = peaks[0]
lfp_locs = peak_locs*fs_lfp//fs_stim
time_vect = np.arange(305+3052)/fs_lfp - .1
stacked_responses = np.empty((4,305+3052,np.size(peak_locs)))
lfp_data = data.streams.TET1.data

f, t, Sxx = scipy.signal.spectrogram(lfp_data[1,:],fs_lfp,window=('hamming'),nperseg=600,noverlap=200)
Sxx_altered = 10e15*Sxx
plt.figure(1)
plt.pcolormesh(t[0:100],f[0:30],Sxx_altered[0:30,0:100],vmin=30,vmax=6000000)
plt.xlabel('Time [s]')
plt.ylabel('Frequency [Hz]')
plt.show()

plt.figure(2)
for pulse in range(0,np.size(peak_locs)):
    start_idx = int(lfp_locs[pulse]-305)
    end_idx = int(lfp_locs[pulse]+3052)
    stacked_responses[:,:,pulse] = lfp_data[:,start_idx:end_idx]
    plt.plot(time_vect,stacked_responses[0,:,pulse]+.0003*pulse)

plt.show

plt.figure(3)
avg_response = np.mean(stacked_responses,axis=2)
std_dev_response = np.std(stacked_responses,axis=2)
plt.plot(time_vect,avg_response[0,:],color='b')
#plt.plot(time_vect,avg_response[0,:]+std_dev_response[0,:],linestyle=':',color='b')
#plt.plot(time_vect,avg_response[0,:]-std_dev_response[0,:],linestyle=':',color='b')
plt.ylim(-0.0004,0.0004)
plt.show()
