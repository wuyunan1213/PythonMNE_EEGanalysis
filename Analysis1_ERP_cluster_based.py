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

import sys



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
            

for word in words:
    for j in range(n_sesh):
        sesh = session_list[j]
        for i in range(n_subj):
            subj = subj_list[i]
            fname = word_epoch_dir + "%s_%s_%s_word-epo.fif" %(subj, sesh, fname_suffix)
            epochs = mne.read_epochs(fname, preload = True)

            FZ = epochs['S6/ZHUO4/TAR'].ch_names.index('FZ')
            CZ = epochs['S6/ZHUO4/TAR'].ch_names.index('CZ')
            PZ = epochs['S6/ZHUO4/TAR'].ch_names.index('PZ')
            
            find_peak = epochs[word].crop(-0.2,0.3)
            peak_data = find_peak.get_data()
            peak_amplitude_FZ = np.min(peak_data[:,FZ,:],axis = 1)
            peak_amplitude_CZ = np.min(peak_data[:,CZ,:],axis = 1)
            peak_amplitude_PZ = np.min(peak_data[:,PZ,:],axis = 1)
            print 'Number of trials = ', np.shape(peak_amplitude_FZ)
            dataframe_peak = pd.DataFrame(np.repeat([[subj],[sesh],[word]],np.shape(peak_amplitude_FZ)[0], axis=1).T)
            dataframe_peak['FZ'] = peak_amplitude_FZ
            dataframe_peak['CZ'] = peak_amplitude_CZ
            dataframe_peak['PZ'] = peak_amplitude_PZ 
            dataframe_peak.to_csv(path_or_buf = analysis_dir+'Peak_amplitude_50_250.csv', mode = 'a',header = False, 
                             index = False)

            evoked = epochs[word].average().crop(-0.2,0.5)         
            FZ_ave = evoked.data[FZ]
            CZ_ave = evoked.data[CZ]
            PZ_ave = evoked.data[PZ]            
        
            dataframe = pd.DataFrame(np.repeat([[subj],[sesh],[word]],np.shape(FZ_ave)[0], axis=1).T)
            dataframe['TimePoint'] = range(-200,501)
            dataframe['FZ'] = FZ_ave
            dataframe['CZ'] = CZ_ave
            dataframe['PZ'] = PZ_ave
            dataframe.to_csv(path_or_buf = analysis_dir+'AveAmplitude.csv', mode = 'a',header = False, 
                             index = False)###for extracting the average amplitude
