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
from mne.stats import f_threshold_mway_rm, f_mway_rm, fdr_correction
from mne.datasets import sample

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

            
words = ['TAR', 'CON']

power_dict = dict()
itc_dict = dict()
decim = 2
freqs = np.logspace(*np.log10([4, 25]), num=12)
n_cycles = freqs / 2
n_freqs = len(freqs)

epochs_power = np.empty(shape = (n_subj,0,n_freqs,601))
epochs_itc = np.empty(shape = (n_subj,0,n_freqs,601))
for word in words:
    for j in range(n_sesh):
        sesh = session_list[j]
        epoch_power = list()
        epoch_itc = list()
        for i in range(n_subj):
            ch_name = ['FZ']###change this to PZ or CZ or FZ
            subj = subj_list[i]
            import warnings
            warnings.filterwarnings('ignore')
            fname = word_epoch_dir + "%s_%s_%s_word-epo.fif" %(subj, sesh, fname_suffix)
            this_epoch = mne.read_epochs(fname, preload = True)
            this_epoch.pick_channels(ch_name)  
            this_epoch = this_epoch[word]
            power, itc = tfr_morlet(this_epoch, freqs=freqs, decim = decim, n_cycles=n_cycles, use_fft=True,
                    return_itc=True)
            power.apply_baseline(mode='ratio', baseline=(-0.2, 0))
            itc.apply_baseline(mode='ratio', baseline=(-0.2, 0))
            epoch_power.append(power.data)
            print np.shape(epoch_power)
            epoch_itc.append(itc.data)
        epochs_power = np.append(epochs_power, epoch_power, axis = 1)
        epochs_itc = np.append(epochs_itc, epoch_itc, axis = 1)
        print "epochs_power", np.shape(epochs_power)
        
n_conditions = 4 #number of conditions
n_replications = n_subj

factor_levels = [2, 2]  # number of levels in each factor
effects = 'A*B' 

n_freqs = len(freqs)
times = 1e3 * this_epoch.times[::decim]
n_times = len(times)

data = np.swapaxes(np.asarray(epochs_itc), 1, 0)
data = data.reshape(n_replications, n_conditions, n_freqs*n_times)
np.shape(data)


###f-map for intertrial coherence.
fvals, pvals = f_mway_rm(data, factor_levels, effects=effects)
effect_labels = ['word', 'session', 'word by session']

for effect, sig, effect_label in zip(fvals, pvals, effect_labels):
    plt.figure()
    # show naive F-values in gray
    plt.imshow(effect.reshape(n_freqs, 601), cmap=plt.cm.gray, extent=[times[0],
               times[-1], freqs[0], freqs[-1]], aspect='auto',
               origin='lower')
    # create mask for significant Time-frequency locations
    effect = np.ma.masked_array(effect, [sig > .05])
    plt.imshow(effect.reshape(n_freqs, 601), cmap='RdBu_r', extent=[times[0],
               times[-1], freqs[0], freqs[-1]], aspect='auto',
               origin='lower')
    plt.colorbar()
    plt.xlabel('Time (ms)')
    plt.ylabel('Frequency (Hz)')
    plt.title(r"Intertrial coherence for '%s' (%s)" % (effect_label, ch_name))
    plt.show()

effects = 'A:B'
def stat_fun(*args):
    return f_mway_rm(np.swapaxes(args, 1, 0), factor_levels=factor_levels,
                     effects=effects, return_pvals=False)[0]


# The ANOVA returns a tuple f-values and p-values, we will pick the former.
pthresh = 0.00001  # set threshold rather high to save some time
f_thresh = f_threshold_mway_rm(n_replications, factor_levels, effects,
                               pthresh)
tail = 1  # f-test, so tail > 0
n_permutations = 256  # Save some time (the test won't be too sensitive ...)
T_obs, clusters, cluster_p_values, h0 = mne.stats.permutation_cluster_test(
    epochs_itc, stat_fun=stat_fun, threshold=f_thresh, tail=tail, n_jobs=1,
    n_permutations=n_permutations, buffer_size=None)

good_clusters = np.where(cluster_p_values < .05)[0]
T_obs_plot = np.ma.masked_array(T_obs,
                                np.invert(clusters[np.squeeze(good_clusters)]))

plt.figure()
for f_image, cmap in zip([T_obs, T_obs_plot], [plt.cm.gray, 'RdBu_r']):
    plt.imshow(f_image, cmap=cmap, extent=[times[0], times[-1],
               freqs[0], freqs[-1]], aspect='auto',
               origin='lower')
plt.xlabel('Time (ms)')
plt.ylabel('Frequency (Hz)')
plt.title("Time-locked response for 'modality by location' (%s)\n"
          " cluster-level corrected (p <= 0.05)" % ch_name)
plt.show()