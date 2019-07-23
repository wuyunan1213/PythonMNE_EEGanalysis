# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 21:49:35 2014
ICA Step (2)
We need to inspect the independent components and decide which are bad.
# ===================
July 9, 2014, All subjects except s4 were preprocessed with ICA. 
Most of the blocks had 64 to 68 components, and only 1 ECG and 1-2 EOG components were removed. 
# ===================

@author: Charles Wu
"""
import warnings
warnings.simplefilter("ignore", DeprecationWarning)
###There are some warning messages that are annoying. Get rid of them with these two lines above.
import mne
import numpy as np
import scipy.io, time

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
n_eeg_channels = 32

#subj_id_seq = [1,2,3,4,5,6,7,8,10,11,12,13,14, 16, 18]    
###subj_list = ['Extra1','Extra2'] 
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

#========================= get ICA data===========================================
import warnings
warnings.simplefilter("ignore", DeprecationWarning)

for i in range(n_subj):
    for j in range(n_sesh):
        subj = subj_list[i]
        sesh = session_list[j]
        fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
        raw = mne.io.Raw(fif_name,preload = True)
        # ============= load ICA =========================================================
        ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
        ica = mne.preprocessing.read_ica(ica_name)
        new_mat_name = ica_dir  + "%s_%s_%s_manual_check.mat" %(subj, sesh, fname_suffix)
        new_mat = scipy.io.loadmat(new_mat_name)

        if len(new_mat['new_eog_inds'])>0:
            new_eog_inds = new_mat['new_eog_inds'][0].astype(np.int)
        else:
            new_eog_inds = []
        if len(new_mat['new_ecg_inds'])>0:
            new_ecg_inds = new_mat['new_ecg_inds'][0].astype(np.int)
        else:
            new_ecg_inds = []
        if len(new_mat['muscle_inds'])>0:
            muscle_inds = new_mat['muscle_inds'][0].astype(np.int)
        else:
            muscle_inds = []    
        
        union = np.union1d(muscle_inds, np.union1d(new_eog_inds, new_ecg_inds))
        exclude = union.astype(np.int).tolist()
        print exclude
        ica.exclude = exclude

        tmp_t = time.time()
        raw_after_ica = ica.apply(raw,exclude = ica.exclude)  
                    
        # since I didn't have bad channels in my data I will not interpolate the bad channels. 
            
        ica_raw_name = ica_dir  + "%s_%s_%s_after_ica_raw.fif" %(subj, sesh, fname_suffix)
        raw_after_ica.save(ica_raw_name, overwrite = True)  
        print time.time()-tmp_t
        
        # =============== clean the objects to release memory ======================
        del(raw)
        del(ica)
        del(raw_after_ica)

    
#================================================================================
# reference
# I do not need rereferencing, by default, the referencing will altomatically be applied to the data
#if False:
#    print "=============== re-reference======================================="
#    Masteroids = ['M1','M2']
#    EOG_list = ['EOG_LO1','EOG_LO2','EOG_IO1','EOG_SO1','EOG_IO2']
#    ECG_list = ['ECG']
#    drop_names = []
#    for i in range(7):
#        drop_names.append("misc%d"%(i+1))
#        trigger_list = ['STI101']      
#    # the trigger is now status 
#    exclude_list = Masteroids + EOG_list + ECG_list + drop_names + trigger_list
#         
#    for i in range(n_subj):
#        subj = "Subj%d_EEG" %subj_list[i]
#        ica_raw_name = ica_dir  + "%s/%s_%s_ica_raw.fif" %(subj,subj,fname_suffix)
#        ica_raw_name_save = ica_dir  + "%s/%s_%s_ica_raw_reref.fif" %(subj,subj,fname_suffix)
#        raw = mne.io.Raw(ica_raw_name, preload = True)  
#        
#        #=============================================
#        picks = mne.pick_channels(raw.info['ch_names'],include = [], exclude = exclude_list + raw.info['bads'])
#        print len(picks)
#        data = raw._data[picks,:]
#        data = (data- np.mean(data, axis = 0))
#        raw._data[picks,:] = data
#        # This can be wrong referencing
#        #=============================================
#        # the mne default re-referencing.  I have not verified it the same as rereferencing for each time point, 
#        # or across time points. it seems to be across all time points, not at each time point
#        raw1, ref_data = mne.io.set_eeg_reference(raw,ref_channels = None, copy = True)
#        raw.save(ica_raw_name_save, overwrite = False)
#        # =============== clean the objects to release memory ======================
#        del(raw)
#        
