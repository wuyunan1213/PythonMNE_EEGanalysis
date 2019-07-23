
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
import mne
import numpy as np
import scipy, time
import scipy.io
import scipy.stats
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import sys



tmp_rootdir = '/Users/charleswu/Desktop/MNE/'
raw_dir = tmp_rootdir + "raw_data/"
filtered_dir = tmp_rootdir + "filtered_raw_data/"
ica_dir = tmp_rootdir + "ica_raw_data/" 
word_epoch_dir = tmp_rootdir + "word_epoch_raw_data/"
evoked_dir = tmp_rootdir + "evoked/"
fig_dir = tmp_rootdir + "evoked_word_fig/"
analysis_dir = tmp_rootdir + "analysis/"

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

for speaker in speakers:
    for word in words:
        condition = "%s/%s"%(speaker, word)
        for j in range(n_sesh):
            sesh = session_list[j]
            evoked_data = np.empty(shape = (0,0,0))
            for i in range(n_subj):
                print condition
                ch_names = ['FZ', 'CZ', 'PZ']
                subj = subj_list[i]
                fname = word_epoch_dir + "%s_%s_%s_word-epo.fif" %(subj, sesh, fname_suffix)
                this_epoch = mne.read_epochs(fname, preload = True)
                this_epoch.pick_channels(ch_names)
                print "this_epoch", np.shape(this_epoch.get_data())
                epoch_data = this_epoch[condition].crop(-0.2, 0.6)
                FZ_ave = epoch_data.data[0]
                CZ_ave = epoch_data.data[1]
                PZ_ave = epoch_data.data[2]
                
                dataframe = pd.DataFrame(np.repeat([[subj],[sesh],[word],[condition]],np.shape(FZ_ave)[0], axis=1).T)
                dataframe['TimePoint'] = range(-200,501)
                dataframe['FZ'] = FZ_ave
                dataframe['CZ'] = CZ_ave
                dataframe['PZ'] = PZ_ave
                dataframe.to_csv(path_or_buf = analysis_dir+'AveAmplitude_byWord.csv', mode = 'a',header = False, 
                             index = False)###for extracting the average amplitude

