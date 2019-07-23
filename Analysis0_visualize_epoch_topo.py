###here we want to group the conditions by target and control words so we can compare their ERPs.
##in this script, we group all of the target and control words whereas in the other script, we look
##at every target and control word individually.
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
# for cond in event_id:
#     evoked = epochs[cond].average()
#     evoked.plot_joint(title = cond)

session_list = ['PRE','POST']
words = ['TAR','CON']
##read the events from the event files instead of the stim channels in the data.
evoked_dict = dict()

for word in words:
    for sesh in session_list:
        fname = evoked_dir + "evoked%s_%s_%s-ave.fif" %(word, sesh, fname_suffix)
        evoked = mne.read_evokeds(fname)
        evoked_dict["%s/%s" %(word, sesh)] = evoked[0].crop(-0.1,0.3)

from mne.channels.layout import find_layout
layout = find_layout(evoked[0].info)
pos = layout.pos.copy()
left = 0.05
right = 0.05
down = 0.08
up = 0.08

pos[13,0]=pos[13,0] + right ##have to mannually change the position of 
##the elctrodes for plotting

pos[0,1] = pos[0,1] - down
pos[1,1] = pos[1,1] - down
pos[2,1] = pos[2,1] - down

f = plt.figure()
f.set_size_inches(10,50)

ylims = (-1,1)
ymax = np.min(np.abs(np.array(ylims)))

colors = {"TAR": "crimson", "CON": 'steelblue'}
linestyles = {"POST": '-', "PRE": '--'}

for pick, (pos_, ch_name) in enumerate(zip(pos, evoked[0].ch_names)):
    ax = plt.axes(pos_)
    mne.viz.plot_compare_evokeds(evoked_dict, picks = pick, axes=ax,
                         ylim=dict(eeg=ylims),
                         show=False,
                         colors = colors,
                         linestyles = linestyles,
                         show_sensors=False,
                        show_legend=False,
                         title='');
    ax.set_xticklabels(())
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.set_yticks((-ymax, ymax))
    ax.set_xticks((0,0.1, 0.2))
    ax.spines["left"].set_bounds(-ymax, ymax)
    ax.set_ylim(ylims)
    ax.set_yticklabels('')
    ax.text(-.1, 1, ch_name, transform=ax.transAxes)

ax.legend(loc='right', bbox_to_anchor=(6, 10))
    




