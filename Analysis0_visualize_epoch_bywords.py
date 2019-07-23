###this script is slightly different than the other analysis0 script
##because given the ERP responses in the target/control words, we suspect
##that there might be some intrinsic differences between the different target/control
##words. Therefore, we want to examine these target vs. control words individually
#rather than grouping all of them together. 

##the ERP figures for each individual speaker identity (sentence frame or control word used)
##are stored in the evoked_word_fig dir.
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
fig_dir = tmp_rootdir + "evoked_word_fig/"

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
speakers = ['S1/MU2','S1/ZHUO2','S3/MU7', 'S3/ZHUO7', 'S5/MU5','S5/ZHUO5','S6/MU4','S6/ZHUO4']
words = ['TAR','CON']
warnings.simplefilter("ignore", DeprecationWarning)
##read the events from the event files instead of the stim channels in the data.
colors = dict()

for speaker in speakers:
    evoked_dict = dict()
    for word in words:
        condition = "%s/%s"%(speaker, word)
        print condition
        for j in range(n_sesh):
            sesh = session_list[j]
            for i in range(n_subj):
                subj = subj_list[i]
                fname = word_epoch_dir + "%s_%s_%s_word-epo.fif" %(subj, sesh, fname_suffix)
                epochs = mne.read_epochs(fname, preload = False)
                if i == 0:
                    evoked = [epochs[condition].average()]
                else:
                    evoked.append(epochs[condition].average())
            condition_sesh = mne.grand_average(evoked).crop(-0.2,0.5)
            evoked_dict["%s/%s" %(condition, sesh)] = condition_sesh

    colors = dict(TAR="Crimson", CON="CornFlowerBlue")
    linestyles = dict(PRE='--', POST='-')
    pick_FZ = epochs['S6/ZHUO4/TAR'].ch_names.index('FZ')
    pick_CZ = epochs['S6/ZHUO4/TAR'].ch_names.index('CZ')
    pick_PZ = epochs['S6/ZHUO4/TAR'].ch_names.index('PZ')
##note that the speaker identity S1, S3, S5 and S6 are not to be confused with subject ID--all
##subjects are averaged so there is no subject ID anymore. The speaker identify indicate
##which speaker generated the stimuli and in fact, the speaker identify also indicates the sentence frame
##and therefore the control word being used in that sentence frame. So the files in the evoked dir do not
##indicate subject ID.
    fig1, ax = plt.subplots()
    mne.viz.plot_compare_evokeds(evoked_dict, picks=pick_CZ, colors=colors, 
                                 linestyles = linestyles, 
                                 show_sensors = False,
                                 truncate_xaxis=False, axes = ax)
    ax.set_xticklabels([-0.3,-0.2,0.1,0,0.1,0.2,0.3,0.4,0.5])
    
    tmp_fig_name1 = fig_dir  + "%.2s_%s_CZ.png" %(speaker, speaker[3:-1])
    fig1.savefig(tmp_fig_name1)

    fig2, ax = plt.subplots()
    mne.viz.plot_compare_evokeds(evoked_dict, picks=pick_PZ, colors=colors, 
                                 linestyles = linestyles, 
                                 show_sensors = False,
                                 truncate_xaxis=False, axes = ax)
    ax.set_xticklabels([-0.3,-0.2,0.1,0,0.1,0.2,0.3,0.4,0.5])
    
    tmp_fig_name2 = fig_dir  + "%.2s_%s_PZ.png" %(speaker, speaker[3:-1])
    fig2.savefig(tmp_fig_name2)

    fig3, ax = plt.subplots()
    mne.viz.plot_compare_evokeds(evoked_dict, picks=pick_FZ, colors=colors, 
                                 linestyles = linestyles, 
                                 show_sensors = False,
                                 truncate_xaxis=False, axes = ax)
    ax.set_xticklabels([-0.3,-0.2,0.1,0,0.1,0.2,0.3,0.4,0.5])
    
    tmp_fig_name3 = fig_dir  + "%.2s_%s_FZ.png" %(speaker, speaker[3:-1])
    fig3.savefig(tmp_fig_name3)
    ###change axis and the ylim
