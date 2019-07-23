###here we want to group the conditions by target and control words so we can compare their ERPs.
##in this script, we group all of the target and control words whereas in the other script, we look
##at every target and control word individually.
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
import mne
import numpy as np
import scipy, time
import scipy.io
import scipy.stats
import matplotlib
import matplotlib.pyplot as plt

import sys



tmp_rootdir = '/Users/charleswu/Desktop/MNE/'
raw_dir = tmp_rootdir + "raw_data/"
filtered_dir = tmp_rootdir + "filtered_raw_data/"
ica_dir = tmp_rootdir + "ica_raw_data/" 
word_epoch_dir = tmp_rootdir + "word_epoch_raw_data/"
evoked_dir = tmp_rootdir + "evoked/"

Mastoids = ['M1','M2']
EOG_list = ['HEOG', 'VEOG']
n_eeg_channels = 32

trigger_list = ['STI 014']
l_freq = 0.1
h_freq = 110.0
notch_freq = [60.0,120.0]
fname_suffix = "filter_%d_%dHz_notch_raw" %(l_freq, h_freq)
alpha = 15
event_dir = tmp_rootdir + "event_files/"
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

# for cond in event_id:
#     evoked = epochs[cond].average()
#     evoked.plot_joint(title = cond)

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE','POST']
n_subj = len(subj_list) 
n_sesh = len(session_list)
words = ['TAR','CON']
warnings.simplefilter("ignore", DeprecationWarning)
##read the events from the event files instead of the stim channels in the data.
evoked_dict = dict()

for word in words:
    for j in range(n_sesh):
        sesh = session_list[j]
        for i in range(n_subj):
            subj = subj_list[i]
            fname = word_epoch_dir + "%s_%s_%s_word-epo.fif" %(subj, sesh, fname_suffix)
            epochs = mne.read_epochs(fname, preload = False)
            if i == 0:
                evoked = [epochs[word].average()]
            else:
                evoked.append(epochs[word].average())
        word_sesh = mne.grand_average(evoked).crop(-0.2,0.5)
        write_name = evoked_dir + "%s_%s_%s-ave.fif" %(word, sesh, fname_suffix)
        mne.write_evokeds(write_name, word_sesh)
        evoked_dict["%s/%s" %(word, sesh)] = word_sesh


colors = dict(TAR="Crimson", CON="CornFlowerBlue")
linestyles = dict(PRE='--', POST='-')
pick_FZ = epochs['S6/ZHUO4/TAR'].ch_names.index('FZ')
pick_CZ = epochs['S6/ZHUO4/TAR'].ch_names.index('CZ')
pick_PZ = epochs['S6/ZHUO4/TAR'].ch_names.index('PZ')

fig, ax = plt.subplots()
mne.viz.plot_compare_evokeds(evoked_dict, picks=pick_CZ, colors=colors, 
                             linestyles = linestyles, 
                             truncate_xaxis=False, axes = ax)
ax.set_xticklabels([-0.3,-0.2,0.1,0,0.1,0.2,0.3,0.4,0.5])
###change axis and the ylim

mne.viz.plot_compare_evokeds(evoked_dict, picks=pick_CZ, colors=colors, linestyles = linestyles, truncate_xaxis=False)
mne.viz.plot_compare_evokeds(evoked_dict, picks=pick_PZ, colors=colors, linestyles = linestyles, truncate_xaxis=False)
mne.viz.plot_compare_evokeds(evoked_dict, picks=pick_FZ, colors=colors, linestyles = linestyles, truncate_xaxis=False)

