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

event_id = {'S1/MU2/CON': 120,
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
list_itcDIFF_TAR = []
list_itcDIFF_CON = []
decim = 2
freqs = np.logspace(*np.log10([2, 25]), num=12)
n_cycles = freqs / 2
for i in range(n_subj):
    subj = subj_list[i]
    for sesh in session_list:
        fname = word_epoch_dir + "%s_%s_%s_word-epo.fif" %(subj, sesh, fname_suffix)
        epochs = mne.read_epochs(fname,  preload = True)
        epochs.drop_channels(['M2'])
        itcTAR = []
        itcCON = []
        for word in event_id:
            print word
            evoked = epochs[word]
            power, itc = tfr_morlet(evoked, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                                return_itc=True) 
            if 'TAR' in word:
                itcTAR.append(itc)
            elif 'CON' in word:
                itcCON.append(itc)
            print 'itcTAR', np.shape(itcTAR)
            print 'itcCON', np.shape(itcCON)
            
        if 'PRE' in sesh:
            PRE_TAR_ave = mne.grand_average(itcTAR)
            PRE_CON_ave = mne.grand_average(itcCON)
        elif 'POST' in sesh:
            POST_TAR_ave = mne.grand_average(itcTAR)
            POST_CON_ave = mne.grand_average(itcCON)
    itcDIFF_TAR = POST_TAR_ave - PRE_TAR_ave
    itcDIFF_CON = POST_CON_ave - PRE_CON_ave
        #    if i == 0:
        #        evoked_itcDIFF = [itcDIFF]
        #    else:
        #        evoked_itcDIFF.append(itcDIFF)
    list_itcDIFF_TAR.append(itcDIFF_TAR)
    list_itcDIFF_CON.append(itcDIFF_CON)
    print 'list_itcDIFF_TAR', np.shape(list_itcDIFF_TAR)
    print 'list_itcDIFF_CON', np.shape(list_itcDIFF_CON)
    
ave_itcDIFF_TAR = mne.grand_average(list_itcDIFF_TAR)
ave_itcDIFF_CON = mne.grand_average(list_itcDIFF_CON)
#ave_itcDIFF.plot(ave_itcDIFF.data, baseline=(-0.2, 0), mode='logratio', title='TargetControlItcDifference_%s' %(sesh))
ave_itcDIFF_TAR.plot_topo(title='Inter-Trial coherence_TAR', tmin = -0.2, tmax = 0.3, vmin=0., vmax=0.05)
ave_itcDIFF_CON.plot_topo(title='Inter-Trial coherence_CON', tmin = -0.2, tmax = 0.3, vmin=0., vmax=0.05)

itcDIFF_TAR.plot_topo(title='Inter-Trial coherence_TAR', tmin = -0.2, tmax = 0.3, vmin=0., vmax=0.2)
itcDIFF_CON.plot_topo(title='Inter-Trial coherence_TAR', tmin = -0.2, tmax = 0.3, vmin=0., vmax=0.1)

ave_itcDIFF_TAR.plot_topo(title='Inter-Trial coherence_TAR', vmin=0., vmax=0.1)
ave_itcDIFF_CON.plot_topo(title='Inter-Trial coherence_CON', vmin=0., vmax=0.1)