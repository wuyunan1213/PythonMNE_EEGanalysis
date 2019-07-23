import warnings
warnings.filterwarnings('ignore')
import mne
import numpy as np
import scipy, time
import scipy.io
import scipy.stats
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from mne import io
from mne.stats import permutation_cluster_test
from mne.datasets import sample
from mne.time_frequency import tfr_morlet

import sys

###this is only to visualize TFR for the post-training session to see if we can see any difference
##between target and control words. 

tmp_rootdir = '/Users/charleswu/Desktop/MNE/'
raw_dir = tmp_rootdir + "raw_data/"
filtered_dir = tmp_rootdir + "filtered_raw_data/"
ica_dir = tmp_rootdir + "ica_raw_data/" 
word_epoch_dir = tmp_rootdir + "word_epoch_raw_data/"
evoked_dir = tmp_rootdir + "evoked/"
analysis_dir = tmp_rootdir + "analysis/"
event_dir = tmp_rootdir + "event_files/"

Mastoids = ['M1','M2']
EOG_list = ['HEOG', 'VEOG']
n_eeg_channels = 32

trigger_list = ['STI 014']
l_freq = 0.1
h_freq = 110.0
notch_freq = [60.0,120.0]
fname_suffix = "filter_%d_%dHz_notch_raw" %(l_freq, h_freq)

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE','POST']
n_subj = len(subj_list) 
n_sesh = len(session_list)

event_id = {'English': 1, 
            'S1/MU2/CON': 120,
            'S1/MU2/TAR': 121,
            'S1/ZHUO2/CON': 140, 
            'S1/ZHUO2/TAR': 141, 
            'S3/MU7/CON': 320,
            'S3/MU7/TAR': 321,
            'S3/ZHUO7/CON': 340, 
            'S3/ZHUO7/TAR': 341,
            'S5/MU5/CON': 520,
            'S5/MU5/TAR': 521, 
            'S5/ZHUO5/CON':540,
            'S5/ZHUO5/TAR':541,
            'S6/MU4/CON':620,
            'S6/MU4/TAR':621,
            'S6/ZHUO4/CON':640,
            'S6/ZHUO4/TAR':641}

            
#ch_names = ['FZ', 'CZ', 'PZ']
#for j in range(n_sesh):
sesh = 'POST'
evoked_itcDIFF = []
for i in range(n_subj):
    subj = subj_list[i]
    fname = word_epoch_dir + "%s_%s_%s_word-epo.fif" %(subj, sesh, fname_suffix)
    epochs = mne.read_epochs(fname,  preload = True)
    epochs.drop_channels(['M2'])
    decim = 2
    freqs = np.logspace(*np.log10([2, 25]), num=12)
    n_cycles = freqs / 2
    
    all_itcTAR = []
    all_itcCON = []
    for word in event_id:
        if 'TAR' in word:
            print word
            evokedTAR = epochs[word]
            powerTAR, itcTAR = tfr_morlet(evokedTAR, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                            return_itc=True) 
            all_itcTAR.append(itcTAR)   
        elif 'CON' in word:
            evokedCON = epochs['CON']
            powerCON, itcCON = tfr_morlet(evokedCON, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                            return_itc=True)  
            all_itcCON.append(itcCON)
    #    print 'itcTAR before', itcTAR
    #    print 'average across electrodes', np.mean(itcTAR.data, axis = 0)
    #    itcTAR.data = np.mean(itcTAR.data, axis = 0)
    #    itcCON.data = np.mean(itcCON.data, axis = 0)
    #    print 'itcTAR afterwards', itcTAR
    all_itcTAR_ave = mne.grand_average(all_itcTAR)
    all_itcCON_ave = mne.grand_average(all_itcCON)
    
    itcDIFF = all_itcTAR_ave - all_itcCON_ave
#    if i == 0:
#        evoked_itcDIFF = [itcDIFF]
#    else:
#        evoked_itcDIFF.append(itcDIFF)
    evoked_itcDIFF.append(itcDIFF)
ave_itcDIFF = mne.grand_average(evoked_itcDIFF)
#ave_itcDIFF.plot(ave_itcDIFF.data, baseline=(-0.2, 0), mode='logratio', title='TargetControlItcDifference_%s' %(sesh))
ave_itcDIFF.plot_topo(title='Inter-Trial coherence_post', tmin = -0.2, tmax = 0.3, vmin=0., vmax=0.1)

sesh = 'PRE'
evoked_itcDIFF_PRE = []
for i in range(n_subj):
    subj = subj_list[i]
    fname = word_epoch_dir + "%s_%s_%s_word-epo.fif" %(subj, sesh, fname_suffix)
    epochs = mne.read_epochs(fname,  preload = True)
    epochs.drop_channels(['M2'])
    decim = 2
    freqs = np.logspace(*np.log10([2, 25]), num=12)
    n_cycles = freqs / 2
    
    all_itcTAR_PRE = []
    all_itcCON_PRE = []
    for word in event_id:
        if 'TAR' in word:
            print word
            evokedTAR_PRE = epochs[word]
            powerTAR_PRE, itcTAR_PRE = tfr_morlet(evokedTAR_PRE, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                            return_itc=True) 
            all_itcTAR_PRE.append(itcTAR_PRE)   
        elif 'CON' in word:
            evokedCON_PRE = epochs['CON']
            powerCON_PRE, itcCON_PRE = tfr_morlet(evokedCON_PRE, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                            return_itc=True)  
            all_itcCON_PRE.append(itcCON_PRE)
    #    print 'itcTAR before', itcTAR
    #    print 'average across electrodes', np.mean(itcTAR.data, axis = 0)
    #    itcTAR.data = np.mean(itcTAR.data, axis = 0)
    #    itcCON.data = np.mean(itcCON.data, axis = 0)
    #    print 'itcTAR afterwards', itcTAR
    all_itcTAR_PRE_ave = mne.grand_average(all_itcTAR_PRE)
    all_itcCON_PRE_ave = mne.grand_average(all_itcCON_PRE)
    
    itcDIFF_PRE = all_itcTAR_PRE_ave - all_itcCON_PRE_ave
#    if i == 0:
#        evoked_itcDIFF = [itcDIFF]
#    else:
#        evoked_itcDIFF.append(itcDIFF)
    evoked_itcDIFF_PRE.append(itcDIFF_PRE)
ave_itcDIFF_PRE = mne.grand_average(evoked_itcDIFF_PRE)
#ave_itcDIFF.plot(ave_itcDIFF.data, baseline=(-0.2, 0), mode='logratio', title='TargetControlItcDifference_%s' %(sesh))
ave_itcDIFF_PRE.plot_topo(title='Inter-Trial coherence_pre', tmin = -0.2, tmax = 0.3, vmin=0., vmax=0.1)