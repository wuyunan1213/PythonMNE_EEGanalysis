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
from mne.stats import f_threshold_mway_rm, f_mway_rm, fdr_correction

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
            
cond = []
for word in words:
    print(word)
    for sesh in session_list:
        evoked_cond= []
        for i in range(n_subj):
            subj = subj_list[i]
            fname = word_epoch_dir + "%s_%s_%s_word-epo.fif" %(subj, sesh, fname_suffix)
            epochs = mne.read_epochs(fname, preload = True)
            
            evoked = epochs[word].crop(-0.1,0.3).average().data
            evoked_cond.append(evoked)
        cond.append(np.array(evoked_cond))

cond = np.array(cond)
n_conditions = cond.shape[0] ##in this case there are 4 conditions
n_replications = cond.shape[1] ## we already get the averaged data for each participants so the 
##replication number is 13
#threshold = 6.0
n_channels = cond.shape[2]
times = np.arange(-100,301)
n_times =  len(times)
effects = 'A*B'
factor_levels = [2,2]

data = np.swapaxes(cond, 1, 0)
data = data.reshape(n_replications, n_conditions, n_channels * n_times)

###the order for the conditions is:
###tar/pre, tar/post, con/pre, con/post
fvals, pvals = f_mway_rm(data, factor_levels, effects=effects)

effect_labels = ['word', 'session', 'word by session']

for effect, sig, effect_label in zip(fvals, pvals, effect_labels):
    plt.figure()
    # show naive F-values in gray
    plt.imshow(effect.reshape(n_channels, n_times), cmap=plt.cm.gray, extent=None, aspect='auto',
               origin='lower')
    # create mask for significant Time-frequency locations
    effect = np.ma.masked_array(effect, [sig > .05])
    plt.imshow(effect.reshape(n_channels, n_times), cmap='RdBu_r', extent=None, aspect='auto',
               origin='lower')
    plt.colorbar()
    plt.xlabel('Time (ms)')
    plt.ylabel('Channel')
    plt.title(r"Time-locked response for '%s' " % (effect_label))
    plt.show()


effects = 'A:B'

def stat_fun(*args):
    return f_mway_rm(np.swapaxes(args, 1, 0), factor_levels=factor_levels,
                     effects=effects, return_pvals=False)[0]


# The ANOVA returns a tuple f-values and p-values, we will pick the former.
pthresh = 0.001  # set threshold rather high to save some time
f_thresh = f_threshold_mway_rm(13, factor_levels, effects,
                               pthresh)
tail = 1  # f-test, so tail > 0
n_permutations = 10000  # Save some time (the test won't be too sensitive ...)
T_obs, clusters, cluster_p_values, h0 = mne.stats.permutation_cluster_test(
    cond, stat_fun=stat_fun, threshold=f_thresh, tail=tail, n_jobs=1,
    n_permutations=n_permutations, buffer_size=None)

good_clusters = np.where(cluster_p_values < .05)[0]
T_obs_plot = np.ma.masked_array(T_obs,
                                np.invert(clusters[np.squeeze(good_clusters)]))

plt.figure()
for f_image, cmap in zip([T_obs, T_obs_plot], [plt.cm.gray, 'RdBu_r']):
    plt.imshow(f_image, cmap=cmap, extent=None, aspect='auto',
               origin='lower')
plt.xlabel('Time (ms)')
plt.ylabel('Channel')
plt.title("ERP F-test for 'word by session'\n"
          " cluster-level corrected (p <= 0.05)")
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