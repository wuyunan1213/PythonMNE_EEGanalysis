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
words = ['TAR','CON']

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
            
sesh ='POST'
ch_names = ['FZ', 'CZ', 'PZ']
for i in range(n_subj):
    word = 'TAR'
    subj = subj_list[i]
    import warnings
    warnings.filterwarnings('ignore')
    fname = word_epoch_dir + "%s_%s_%s_word-epo.fif" %(subj, sesh, fname_suffix)
    epochs = mne.read_epochs(fname, preload = True)
    epochs.pick_channels(ch_names)
    decim = 2
    freqs = np.arange(4, 36, 2)  # define frequencies of interest
    n_cycles = 1.5
    evoked = epochs[word]
    powerTAR, itcTAR = tfr_morlet(evoked, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                    return_itc=True)  
    if i == 0:
        evoked_powerTAR = [powerTAR]
        evoked_itcTAR = [itcTAR]
    else:
        evoked_powerTAR.append(powerTAR)
        evoked_itcTAR.append(itcTAR)
    
ave_powerTAR = mne.grand_average(evoked_powerTAR)
ave_itcTAR = mne.grand_average(evoked_itcTAR)
                       
ave_powerTAR.plot([0], baseline=(-0.2, 0), mode='logratio', title='POST_Target_%s_Induced_power' %(ave_powerTAR.ch_names[0]))
ave_itcTAR.plot([0], baseline=(-0.2, 0), mode='logratio', title='POST_Target_%s_itc' %(ave_itcTAR.ch_names[0]))

ave_powerTAR.plot([1], baseline=(-0.2, 0), mode='logratio', title='POST_Target_%s_Induced_power' %(ave_powerTAR.ch_names[1]))
ave_itcTAR.plot([1], baseline=(-0.2, 0), mode='logratio', title='POST_Target_%s_itc' %(ave_itcTAR.ch_names[1]))


for i in range(n_subj):
    word = 'CON'
    subj = subj_list[i]
    import warnings
    warnings.filterwarnings('ignore')
    fname = word_epoch_dir + "%s_%s_%s_word-epo.fif" %(subj, sesh, fname_suffix)
    epochs = mne.read_epochs(fname, preload = True)
    epochs.pick_channels(ch_names)
    decim = 2
    freqs = np.arange(4, 36, 2)  # define frequencies of interest
    n_cycles = 1.5
    evoked = epochs[word]
    powerCON, itcCON = tfr_morlet(evoked, freqs=freqs, n_cycles=n_cycles, use_fft=True,
                    return_itc=True)  
    if i == 0:
        evoked_powerCON = [powerCON]
        evoked_itcCON = [itcCON]
    else:
        evoked_powerCON.append(powerCON)
        evoked_itcCON.append(itcCON)
    
ave_powerCON = mne.grand_average(evoked_powerCON)
ave_itcCON = mne.grand_average(evoked_itcCON)
                       
ave_powerCON.plot([2], baseline=(-0.2, 0), mode='logratio', title='POST_Control_Induced_power%s' %(ave_powerCON.ch_names[1]))
ave_itcCON.plot([2], baseline=(-0.2, 0), mode='logratio', title='POST_Control_%s_itc' %(ave_itcCON.ch_names[1]))

#            EpochsTFR = EpochsTFR(info = condition.info, data = condition.get_data(), 
#                                  times = times, freqs = frequencies)
# =============================================================================
#             if i == 0:
#                 evoked = [epochs[word].average()]
#             else:
#                 evoked.append(epochs[word].average())
# =============================================================================
