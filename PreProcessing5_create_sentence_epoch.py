import warnings
warnings.simplefilter("ignore", DeprecationWarning)
import mne
import numpy as np
import scipy, time
import scipy.io
import scipy.stats

import sys



tmp_rootdir = '/Users/charleswu/Desktop/MNE/'
raw_dir = tmp_rootdir + "raw_data/"
filtered_dir = tmp_rootdir + "filtered_raw_data/"
ica_dir = tmp_rootdir + "ica_raw_data/" 
sentence_epoch_dir = tmp_rootdir + "sentence_epoch_raw_data/"
event_dir = tmp_rootdir + "event_files/"

Mastoids = ['M1','M2']
#EOG_list = [u'LhEOG', u'RhEOG', u'LvEOG1', u'LvEOG2', u'RvEOG1']
EOG_list = ['HEOG', 'VEOG']
n_eeg_channels = 32

trigger_list = ['STI 014']
l_freq = 0.1
h_freq = 110.0
notch_freq = [60.0,120.0]
fname_suffix = "filter_%d_%dHz_notch_raw" %(l_freq, h_freq)
alpha = 15
#events = ['1','12','14','32','34','52','54','62','64']      
#The following code visualizes the ERPs
# subj = "S01"
# sesh = 'PRE'

# ica_raw_name = ica_dir  + "%s_%s_%s_after_ica_raw.fif" %(subj, sesh, fname_suffix)
# raw = mne.io.Raw(ica_raw_name,preload = True)

# event_id = {'English': 1, 'S1_MU2': 12,
#             'S1_ZHUO2': 14, 'S3_MU7': 32,
#             'S3_ZHUO7': 34, 'S5_MU5': 52, 'S5_ZHUO5':54, 'S6_MU4':62, 'S6_ZHUO4':64}
# color = {1: 'green', 12: 'yellow', 14: 'red', 32: 'orange', 34: 'black', 52: 'blue', 54: 'pink', 62: 'gray', 64: 'purple'}
# events = mne.find_events(raw, stim_channel = trigger_list[0])
# mne.viz.plot_events(events, raw.info['sfreq'], raw.first_samp, color=color,
#                     event_id=event_id)

# order = np.arange(raw.info['nchan'])
# order[9] = 35  # We exchange the plotting order of two channels
# order[35] = 9  # to show the trigger channel as the 10th channel.
# raw.plot(events=events, n_channels=10, order=order)

# tmin, tmax = -0.2, 0.5
# reject = dict(eeg = 1E-3)
# baseline = (None, 0.0)
# epochs = mne.Epochs(raw, events=events, event_id=event_id, tmin=tmin,
#                     tmax=tmax, reject=reject)
# epochs.plot(block = True)
# epochs.plot_drop_log()

# picks = mne.pick_types(epochs.info, eeg = True, eog = True)
# evoked_12 = epochs['S1_ZHUO2'].average(picks=picks)
# evoked_12.plot()

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
n_subj = len(subj_list) 
n_sesh = len(session_list)

for i in range(n_subj):
    for j in range(n_sesh):
        subj = subj_list[i]
        sesh = session_list[j]
        warnings.simplefilter("ignore", DeprecationWarning)
        ica_raw_name = ica_dir  + "%s_%s_%s_after_ica_raw.fif" %(subj, sesh, fname_suffix)
        raw = mne.io.Raw(ica_raw_name,preload = True)

        event_id = {'English': 1, 'S1/MU2': 12,
                    'S1/ZHUO2': 14, 'S3/MU7': 32,
                    'S3/ZHUO7': 34, 'S5/MU5': 52, 'S5/ZHUO5':54, 'S6/MU4':62, 'S6/ZHUO4':64}
        color = {1: 'green', 12: 'yellow', 14: 'red', 32: 'orange', 34: 'black', 52: 'blue', 54: 'pink', 62: 'gray', 64: 'purple'}
        fname = event_dir + "%s_%s_SENTENCE.eve"%(subj,sesh)
        events = mne.read_events(fname)

        tmin, tmax = -0.6, 0.6
        baseline = (-0.2, 0.0)
        ##the baseline period is set to equal to the length of the epoch. The epoch is set to be longer
        ##than usual because of the potential time-frequency analysis that comes later. 
        epochs = mne.Epochs(raw, events=events, baseline = baseline, event_id=event_id, tmin=tmin,
                            tmax=tmax)
        ##In this step, we will also reject the bad trials that have 3 standard deviations
        ##from the average
        picks = mne.pick_types(epochs.info, eeg = True, stim = False, eog = False)
        epoch_mat = epochs.get_data()[:,picks,:]
        ##epoch_mat is 3-D where 0 is n_events, 1 is n_channels and 2 is n_time points
        #The following code rejects epochs that are alpha std beyong the average. Serves as an 
        #Automatic trial rejection step
        ranges_each_trial = np.max(epoch_mat, axis = 2) - np.min(epoch_mat, axis = 2)
        ranges_zscore = scipy.stats.zscore(ranges_each_trial, axis = 0)
        bad_trials = np.any(ranges_zscore > alpha, axis = 1)
        print "# bad_trials %d" %bad_trials.sum()
        epochs.drop(np.where(bad_trials == 1)[0])
        epoch_fname = sentence_epoch_dir + "%s_%s_%s_sentence-epo.fif" %(subj, sesh, fname_suffix)
        epochs.save(epoch_fname)

