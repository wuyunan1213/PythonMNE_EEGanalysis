# -*- coding: utf-8 -*-
"""
Manual scripts, to save the ica components to exclude. 

@author: Charles Wu
"""

import mne
import numpy as np
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mne.preprocessing import ICA
import scipy.io
import scipy.stats
import time



#====================================================================================
tmp_rootdir = '/Users/charleswu/Desktop/MNE/'
raw_dir = tmp_rootdir + "raw_data/"
filtered_dir = tmp_rootdir + "filtered_raw_data/"
ica_dir = tmp_rootdir + "ica_raw_data/" 
l_freq = 0.1
h_freq = 110.0
notch_freq = [60.0,120.0]
fname_suffix = "filter_%d_%dHz_notch_raw" %(l_freq, h_freq)
Mastoids = ['M1','M2']
#EOG_list = [u'LhEOG', u'RhEOG', u'LvEOG1', u'LvEOG2', u'RvEOG1']
EOG_list = ['HEOG', 'VEOG']
#ECG_list = [u'ECG']
#ECG_list = ['ECG']
fig_dir = tmp_rootdir + "ica_fig/"


# ====================for future, these should be written in a text file============
#subj_id_seq = [1,2,3,4,5,6,7,8,10,11,12,13]    
##subj_list = ['Extra1','Extra2'] 
#subj_list = list()
#for i in subj_id_seq:
#    subj_list.append('Subj%d' % i)
    
    
#subj_list = ["Subj14"] 
#subj_list = ["Subj16", "Subj18"]  
#subj_list = ['SubjYY_100', 'SubjYY_500']
    
subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
n_subj = len(subj_list) 
n_sesh = len(session_list)


# TO BE MODIFIED: mne-python 0.10
# Also check the ics for muscle contaminations
# for this step we can't do everything in a loop because we have to visualize each participants' component
# in each session. So we will have to do this one by one and check the components visually. 
# Label the components manually and store them in the file _EOG_Manual_Check.

###############################################################################################################
###############################################################################################################
################################################S01_PRE########################################################
###############################################################################################################
###############################################################################################################
subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[0]
sesh = session_list[0]
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)

if len(EXG_dict1['eog_inds'])>0:
    print EXG_dict1['eog_inds'][0]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print EXG_dict2['eog_inds'][0]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
ica.plot_components() ##from these components and the automatic detection results, we think 0,1,2,6 and 7 might be blinks. 8,20,22,23 might be muscle. 21 might be heart
ica.plot_properties(raw, picks = [0,1,2,6,7,8,20,21,22,23])
##after examining these visually, I decide that I will reject 0,1,2 as eye blinks, 20,22,23 as muscle
##note that muscle rejection is rather tricky so we want to conservative and reject as few components are possible
##when in doubt, always retain the component because muscle noise does not matter as much especially for ERP
ica.plot_overlay(raw, exclude= [0,1,2])#,6,7,8,20,21,22,23])
# I finally decided to only reject 0,1,2 as EOC components
10,20,22,23
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,1,2]
new_ecg_inds = []
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################S01_POST########################################################
###############################################################################################################
###############################################################################################################
subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[0]
sesh = session_list[1]
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)

if len(EXG_dict1['eog_inds'])>0:
    print EXG_dict1['eog_inds'][0]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print EXG_dict2['eog_inds'][0]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
##from the component plots and the automatic detection results, we think 0,2,4,22 might be eye blinks
## 3,5,6,15,17,18,23,24 might be muscle. 9 might be heart
ica.plot_properties(raw, picks = [0,2,3,4,5,6,9,15,17,18,22,23,24],psd_args={'fmax': 80})
##after examining these visually, I decide that I will reject 0,2,4 as eye blinks, 20,22,23 as muscle, 9 as heart
##note that muscle rejection is rather tricky so we want to conservative and reject as few components are possible
##when in doubt, always retain the component because muscle noise does not matter as much especially for ERP
##I also decided not to reject the heart component in this step
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
ica.plot_overlay(raw, exclude= [0,2,4])
##based on the overlay plots, I decided to only reject 0,2,4 as eye blinks
new_eog_inds = [0,2,4]
new_ecg_inds = []
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################S02_PRE########################################################
###############################################################################################################
###############################################################################################################
subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[1] #S02
sesh = session_list[0]#PRE
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)

if len(EXG_dict1['eog_inds'])>0:
    print EXG_dict1['eog_inds'][0]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print EXG_dict2['eog_inds'][0]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
ica.plot_properties(raw, picks = [0,1,2,11,18,20,25,28],psd_args={'fmax': 80})##after checking
##the automatic detection and the components, 0,1,2 look like eye blinks, 
##18,20,25,28 look like muscle
##and 11 looks like heart
ica.plot_overlay(raw, exclude= [0,1,2,11,18,20,25,28]) ##look at the overlay plot and make sure 
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,1,2 has very significant effects on
##on noise removal so we will leave the other components intact.
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,1,2]
new_ecg_inds = []
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################S02_POST########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[1] #S02
sesh = session_list[1]#POST
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)

if len(EXG_dict1['eog_inds'])>0:
    print EXG_dict1['eog_inds'][0]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print EXG_dict2['eog_inds'][0]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,1,2,13,20,22,26]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 0,1,2 look like eye blinks, 
##13,20,22,26 look like muscle

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= [0,1,2,13,20,22,26]) ##look at the overlay plot and make sure 
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,1,2 has very significant effects on
##on noise removal so we will leave the other components intact.
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,1,2]
new_ecg_inds = []
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)
###############################################################################################################
###############################################################################################################
################################################S03_PRE########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[2] #S03
sesh = session_list[0]#PRE
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,1,2,15,16,21]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 2 looks like eye blinks, 
##0,1,15, 16, 21look like muscle

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= [0,1,2,15,16,21]) ##look at the overlay plot and make sure 
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 2 has very significant effects on
##on noise removal so we will leave the other components intact.
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [2]
new_ecg_inds = []
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)
###############################################################################################################
###############################################################################################################
################################################S03_POST########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[2] #S03
sesh = session_list[1]#POST
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [4,7,8,12,13,14,16,17,22,25]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 4,7,8,13,25 looks like eye blinks, 
##12,14,16,17,22look like muscle

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 4,7,8,13 has very significant effects on
##on noise removal so we will leave the other components intact.
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [4,7,8,13]
new_ecg_inds = []
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)
###############################################################################################################
###############################################################################################################
################################################S04_PRE########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[3] #S04
sesh = session_list[0]#PRE
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,2,4,6,7,8,9,12,13,14,18,19,21,22,25]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 0,2,12,13 looks like eye blinks, 
##4,6,7,8,14,18,19,21,22,25look like muscle

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,2,4,6,13,14 has very significant effects on
##noise removal so we will leave the other components intact. 0,2 are eye blinks and 4,6,13,14 are muscle
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,2]
new_ecg_inds = []
muscle_inds = [4,6,13,14]
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)
###############################################################################################################
###############################################################################################################
################################################S04_POST########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[3] #S04
sesh = session_list[1]#POST
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,2,3,7,13,14,15,16,17,21,25]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 0,2,3 looks like eye blinks, 
##7,13,14,15,16,17,21,25look like muscle

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,2,3 has very significant effects on
##noise removal so we will leave the other components intact. 0,2 are eye blinks and 3 is muscle
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,2]
new_ecg_inds = []
muscle_inds = [3]
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)
###############################################################################################################
###############################################################################################################
################################################S05_PRE########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[4] #S05
sesh = session_list[0]#PRE
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [1,11,9,30,3,13,14,16,17,19,22,24,27]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 1,11,9,30 looks like eye blinks, 
##3,13,14,16,17,19,22,24,27look like muscle

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 1,11,22,27,30 has very significant effects on
##9 and 17 also contribute to the noise a lot but they dont seem to be very characteristic of muscle
##movements so i decided to keep them
##noise removal so we will leave the other components intact. 1 are eye blinks and 22,27,30 are muscle
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [1]
new_ecg_inds = []
muscle_inds = [22,27,30]
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################S05_POST########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[4] #S05
sesh = session_list[1]#POST
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,1,3,19,10,13,14,17,19,20,23]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 0,1,3,19 looks like eye blinks, 
##13,14,17,19,20,23look like muscle
##10 looks like heart

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,1,3,14 has very significant effects on
##noise removal so we will leave the other components intact. 0,1,3 are eye blinks and leave 14 intact
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [1,0,3]
new_ecg_inds = []
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)
###############################################################################################################
###############################################################################################################
################################################S06_PRE########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[5] #S06
sesh = session_list[0]#PRE
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,2,4,3,7,10,13,14,16,21,6]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 0,2,4 looks like eye blinks, 
##3,7,10,13,14,16,21look like muscle
##6 looks like heart

for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
ica.plot_sources(raw, picks = 6)
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,2,7,4,14 has very significant effects on
##noise removal so we will leave the other components intact. 0,2 are eye blinks and 4,7,14 is muscle
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,2]
new_ecg_inds = []
muscle_inds = [4]
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################S06_POST########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[5] #S06
sesh = session_list[1]#POST
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,3,6,9,12,13,16,21]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 
##0,3 are eye blinks and 9,12,13,16,21 are muscle
##6 might be heart
for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
ica.plot_sources(raw, picks = 6)
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,3,9,12has very significant effects on
##noise removal so we will leave the other components intact. 0,3 are eye blinks and 9,12 are muscle
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,3]
new_ecg_inds = []
muscle_inds = [12]
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)
###############################################################################################################
###############################################################################################################
################################################S07_PRE########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[6] #S07
sesh = session_list[0]#PRE
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,2,4,7,11,15,21,29]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 
##0,7 are eye blinks and 
##4,11,15,21,29 are muscle
##2 might be heart
for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
ica.plot_sources(raw, picks = 6)
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,2,7 has very significant effects on
##noise removal so we will leave the other components intact. 0,7 are eye blinks and 2 is heart
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,7]
new_ecg_inds = [2]
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################S07_POST########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[6] #S07
sesh = session_list[1]#POST
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,1,3,4,9,10,15,16,18,19,21]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 
##0,3,4 are eye blinks and 
##9,10,15,16,18,19,21 are muscle
##1 might be heart
for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
ica.plot_sources(raw, picks = 6)
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,2,7 has very significant effects on
##noise removal so we will leave the other components intact. 0,7 are eye blinks and 2 is heart
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,3,4]
new_ecg_inds = [1]
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)
###############################################################################################################
###############################################################################################################
################################################S09_PRE########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[7] #S09
sesh = session_list[0]#PRE
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,1,2,3,4,9,10,17,18]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 
##0,1,2 are eye blinks and 
##4,9,10,17,18 are muscle
##3 might be heart
for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
ica.plot_sources(raw, picks = 3)
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,1,2,3,4,17 has very significant effects on
##noise removal so we will leave the other components intact. 0,1,2 are eye blinks and 3 is suspicious
##but it has all the characteristics of a heart component. Therefore reject. I also reject 17 as muscle
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,1,2]
new_ecg_inds = [3]
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################S09_POST########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[7] #S09
sesh = session_list[1]#POST
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,1,2,3,8,10,11,12,13,19,23]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 
##0,2,3 are eye blinks and 
##8,10,11,12,13,19,23are muscle
##1 might be heart
for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
ica.plot_sources(raw, picks = 6)
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,2,3,19 has very significant effects on
##After looking at the graphs, I decided to only reject 0,2,3 as eye blinks.
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,2,3]
new_ecg_inds = []
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################S10_PRE########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[8] #S10
sesh = session_list[0]#PRE
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,1,2,3,4,9,12,5,6,15,18,20,21,7]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 
##0,1,2,3,4,9,12 are eye blinks and 
##5,6,15,18,20,21are muscle
##7 might be heart
for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
ica.plot_sources(raw, picks = [7])
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,1,2,4,9,12,5,6 has very significant effects on
##noise removal so we will leave the other components intact. 0,1,2,4,9,12 are eye blinks and 7 is heart
##5,6 are muscle
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,1,2,4,9,12]
new_ecg_inds = [7]
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)
###############################################################################################################
###############################################################################################################
################################################S10_POST########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[8] #S10
sesh = session_list[1]#POST
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,1,2,3,4,8,14,5,13,17,19,21,23,24,25,6]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 
##0,1,2,3,4,8,14 are eye blinks and 
##5,13,17,19,21,23,24,25are muscle
##6 might be heart
for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
ica.plot_sources(raw, picks = [6])
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,1,4,2,3,6,8,14 has very significant effects on
##noise removal so we will leave the other components intact. 0,1,2,3,4,8,14 are eye blinks and 6 is heart
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,1,2,3,4,8,14]
new_ecg_inds = [6]
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)
###############################################################################################################
###############################################################################################################
################################################S11_PRE########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[9] #S11
sesh = session_list[0]#PRE
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,2,4,5,1,8,9,21,23,7]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 
##0,2,4are eye blinks and 
##5,1,8,9,21,23,7 are muscle
for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,2,7 has very significant effects on
##noise removal so we will leave the other components intact. 0,7 are eye blinks and 2 is heart
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,2,4]
new_ecg_inds = []
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################S11_POST########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[9] #S11
sesh = session_list[1]#POST
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,1,2,3,4,5,7,16,23,9,13]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 
##0,1,2,3,4,5are eye blinks and 
##7,16,23 are muscle
##9,13 might be heart
for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
ica.plot_sources(raw, picks = 6)
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,1,2,4,7,16 has very significant effects on
##noise removal so we will leave the other components intact. 0,1,2 are eye blinks and 4,7,16 are muscle
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,1,2]
new_ecg_inds = []
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################S12_PRE########################################################
###############################################################################################################
###############################################################################################################
subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[10] #S12
sesh = session_list[0]#PRE
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,2,3,6,9,10,14,18,24,25]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 
##0,2,3 are eye blinks and 
##6,9,14,18,24,25 are muscle
##10 might be heart
for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
ica.plot_sources(raw, picks = 6)
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,2,7 has very significant effects on
##noise removal so we will leave the other components intact. 0,7 are eye blinks and 2 is heart
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,2,3]
new_ecg_inds = [10]
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################S12_POST########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[10] #S12
sesh = session_list[1]#POST
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,2,4,6,8,9,11,10,20,21,22]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 
##0,2are eye blinks and 
##4,8,9,11,10,20,21,22 are muscle
##6 might be heart
for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
ica.plot_sources(raw, picks = [6])
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,2,7 has very significant effects on
##noise removal so we will leave the other components intact. 0,7 are eye blinks and 2 is heart
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,2]
new_ecg_inds = []
muscle_inds = [21]
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################S14_PRE########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[11] #S14
sesh = session_list[0]#PRE
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,1,2,3,7,8,10,13,14,15,16,18,19,23,24]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 
##0,1,2,3 are eye blinks and 
##7,10,13,14,15,16,18,19,23,24 are muscle
##8 might be heart
for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
ica.plot_sources(raw, picks = 6)
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,1,2,3,15 has very significant effects on
##noise removal so we will leave the other components intact. 0,1,3 are eye blinks and 2, 15 are muscle
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,1,3]
new_ecg_inds = []
muscle_inds = [2]
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################S14_POST########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[11] #S14
sesh = session_list[1]#POST
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,1,4,12,5,10,11,13,14,19,20,22,23]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 
##0,1,4,12 are eye blinks and 
##5,10,11,12,13,14,19,20,22,23 are muscle
#8 might be heart
for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
ica.plot_sources(raw, picks = 6)
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,1,11,12has very significant effects on
##noise removal so we will leave the other components intact. 0,1,12 are eye blinks and 11 is heart
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,1,12]
new_ecg_inds = [11]
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################S15_PRE########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[12] #S15
sesh = session_list[0]#PRE
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [0,2,3,8,13,17,19,20,21,22,23,25,26,1,7]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 
##0,2,3 are eye blinks and 
##8,13,17,19,20,21,22,23,25,26 are muscle
#1,7 might be heart
for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
ica.plot_sources(raw, picks = 6)
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 0,2,3, has very significant effects on
##noise removal so we will leave the other components intact. 0,2,3 are eye blinks
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [0,2,3]
new_ecg_inds = []
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)

###############################################################################################################
###############################################################################################################
################################################S15_POST########################################################
###############################################################################################################
###############################################################################################################

subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
subj = subj_list[12] #S15
sesh = session_list[1]#POST
print subj
print sesh
fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
raw = mne.io.Raw(fif_name,preload = True)

# ============= load ICA =========================================================
ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
ica = mne.preprocessing.read_ica(ica_name)
mat_name1 = ica_dir  + "%s_%s_%s_VEOG.mat" %(subj, sesh, fname_suffix)
mat_name2 = ica_dir  + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
EXG_dict1 = scipy.io.loadmat(mat_name1)
EXG_dict2 = scipy.io.loadmat(mat_name2)
eog_scores1 = EXG_dict1['eog_scores'][0]
eog_scores2 = EXG_dict2['eog_scores'][0]

if len(EXG_dict1['eog_inds'])>0:
    print 'VEOG = ', EXG_dict1['eog_inds'][0]
    print 'Vscore = ', eog_scores1[EXG_dict1['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores1))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds

if len(EXG_dict2['eog_inds'])>0:
    print 'HEOG = ', EXG_dict2['eog_inds'][0]
    print 'Hscore = ', eog_scores2[EXG_dict2['eog_inds'][0]]
else: 
    # if no automatic EOG was detected, use the first 10 ICs that are mostly
    # correlated with EOG1
    eog_inds = np.argsort(np.abs(eog_scores2))[-1:-10:-1]
    print "empty EOG inds, automatically choose", eog_inds
##check and see what the automatically detected components are
picks = [2,3,4,5,6,10,8,12,15,18,20,29,30]
n_components = len(picks)
fig = ica.plot_properties(raw, picks = picks,psd_args={'fmax': 80})
##after checking
##the automatic detection and the components, 
##2,3,4,5,10 are eye blinks and 
##8,12,15,18,20,29,30 are muscle
#6 might be heart
for i in range(n_components):
    tmp_fig_name1 = fig_dir  + "%s_%s_component%s.png" %(subj, sesh, picks[i])
    fig[i].savefig(tmp_fig_name1)

ica.plot_overlay(raw, exclude= picks) ##look at the overlay plot and make sure 
ica.plot_sources(raw, picks = 6)
##we are rejecting the correct components.
##after looking at the overlay plot, it seems like removing 2,5,8,3,4,10 has very significant effects on
##noise removal so we will leave the other components intact. 2,5 are eye blinks and 6 is heart,
# ================ make manual selections =====================================
#new_eog_inds = eog_inds[1:2]
new_eog_inds = [2,5]
new_ecg_inds = [6]
muscle_inds = []
#new_eog_inds = eog_inds[0:2]
#new_ecg_inds = ecg_inds[0:3]
        
# it is too dangerous to remove the muscle components here.  
# They are reletively in a short range of frequency, 15 Hz ish
# But many components have it, it is too risky to remove them
print new_eog_inds, new_ecg_inds, muscle_inds
new_mat = dict(new_eog_inds = new_eog_inds, new_ecg_inds = new_ecg_inds, muscle_inds = muscle_inds)
new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
print new_mat_name
scipy.io.savemat(new_mat_name, new_mat)
