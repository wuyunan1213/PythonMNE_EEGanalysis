###This script uses python 3.7
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
            
diff_FZ = []
diff_CZ = []
diff_PZ = []
for word in words:
    print(word)
    evoked_PRE = []
    evoked_POST = []
    for sesh in session_list:
        for i in range(n_subj):
            subj = subj_list[i]
            fname = word_epoch_dir + "%s_%s_%s_word-epo.fif" %(subj, sesh, fname_suffix)
            epochs = mne.read_epochs(fname, preload = True)
            
            evoked = epochs[word].crop(-0.1,0.3).average().data
            if sesh == 'PRE':
                evoked_PRE.append(evoked)
            else:
                evoked_POST.append(evoked)
    FZ = epochs['S6/ZHUO4/TAR'].ch_names.index('FZ')
    CZ = epochs['S6/ZHUO4/TAR'].ch_names.index('CZ')
    PZ = epochs['S6/ZHUO4/TAR'].ch_names.index('PZ')
    evoked_PRE  = np.array(evoked_PRE)
    evoked_POST = np.array(evoked_POST)
    sub_FZ = np.subtract(evoked_POST[:,FZ,:],evoked_PRE[:,FZ,:])
    sub_CZ = np.subtract(evoked_POST[:,CZ,:],evoked_PRE[:,CZ,:])
    sub_PZ = np.subtract(evoked_POST[:,PZ,:],evoked_PRE[:,PZ,:])
    diff_FZ.append(sub_FZ)
    diff_CZ.append(sub_CZ)
    diff_PZ.append(sub_PZ)
    
#threshold = 6.0
T_obs, clusters, cluster_p_values, H0 = \
    permutation_cluster_test([diff_FZ[0], diff_FZ[1]], n_permutations=1000,
                             tail=1, n_jobs=1)
channel = 'FZ'
times = np.arange(-0.1,0.301,0.001)
plt.close('all')
plt.subplot(211)
plt.title('Channel : ' + channel)
plt.plot(times, diff_FZ[0].mean(axis=0) - diff_FZ[1].mean(axis=0),
         label="ERP Contrast (Target Diff - Control Diff)")
plt.ylabel("Amplitude difference")
plt.legend()
plt.subplot(212)
for i_c, c in enumerate(clusters):
    c = c[0]
    if cluster_p_values[i_c] <= 0.05:
        h = plt.axvspan(times[c.start], times[c.stop - 1],
                        color='r', alpha=0.3)
    else:
        plt.axvspan(times[c.start], times[c.stop - 1], color=(0.3, 0.3, 0.3),
                    alpha=0.3)
hf = plt.plot(times, T_obs, 'g')
plt.legend((h, ), ('cluster p-value < 0.05', ))
plt.xlabel("time (ms)")
plt.ylabel("f-values")
plt.show()


T_obs, clusters, cluster_p_values, H0 = \
    permutation_cluster_test([diff_CZ[0], diff_CZ[1]], n_permutations=1000,
                             tail=1, n_jobs=1)
channel = 'CZ'
times = np.arange(-0.1,0.301,0.001)
plt.close('all')
plt.subplot(211)
plt.title('Channel : ' + channel)
plt.plot(times, diff_CZ[0].mean(axis=0) - diff_CZ[1].mean(axis=0),
         label="ERP Contrast (Target Diff - Control Diff)")
plt.ylabel("Amplitude difference")
plt.legend()
plt.subplot(212)
for i_c, c in enumerate(clusters):
    c = c[0]
    if cluster_p_values[i_c] <= 0.05:
        h = plt.axvspan(times[c.start], times[c.stop - 1],
                        color='r', alpha=0.3)
    else:
        plt.axvspan(times[c.start], times[c.stop - 1], color=(0.3, 0.3, 0.3),
                    alpha=0.3)
hf = plt.plot(times, T_obs, 'g')
plt.legend((h, ), ('cluster p-value < 0.05', ))
plt.xlabel("time (ms)")
plt.ylabel("f-values")
plt.show()


T_obs, clusters, cluster_p_values, H0 = \
    permutation_cluster_test([diff_PZ[0], diff_PZ[1]], n_permutations=1000,
                             tail=1, n_jobs=1)
channel = 'PZ'
times = np.arange(-0.1,0.301,0.001)
plt.close('all')
plt.subplot(211)
plt.title('Channel : ' + channel)
plt.plot(times, diff_PZ[0].mean(axis=0) - diff_PZ[1].mean(axis=0),
         label="ERP Contrast (Target Diff - Control Diff)")
plt.ylabel("Amplitude difference")
plt.legend()
plt.subplot(212)
for i_c, c in enumerate(clusters):
    c = c[0]
    if cluster_p_values[i_c] <= 0.05:
        h = plt.axvspan(times[c.start], times[c.stop - 1],
                        color='r', alpha=0.3)
    else:
        plt.axvspan(times[c.start], times[c.stop - 1], color=(0.3, 0.3, 0.3),
                    alpha=0.3)
hf = plt.plot(times, T_obs, 'g')
plt.legend((h, ), ('cluster p-value < 0.05', ))
plt.xlabel("time (ms)")
plt.ylabel("f-values")
plt.show()
#sesh = 'POST'
#word = 'TAR'
#for i in range(n_subj):
#    subj = subj_list[i]
#    fname = word_epoch_dir + "%s_%s_%s_word-epo.fif" %(subj, sesh, fname_suffix)
#    epochs = mne.read_epochs(fname, preload = True)
#    if i == 0:
#        evoked_PostTar = [epochs[word].average().data]
#    else: 
#        evoked_PostTar.append(epochs[word].average().data)
#        
#FZ = epochs['S6/ZHUO4/TAR'].ch_names.index('FZ')
#
#            
#        
#sesh = 'POST'