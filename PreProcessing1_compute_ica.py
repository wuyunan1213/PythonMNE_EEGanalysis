import mne
import numpy as np
import scipy
from mne.preprocessing import ICA, create_eog_epochs, create_ecg_epochs
import scipy.io

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

drop_names = []
for i in range(7):
    drop_names.append("misc%d"%(i+1))

trigger_list = ['STI 014']    
#events = ['1','12','14','32','34','52','54','62','64']   
# the trigger is now status 
exclude_list = Mastoids + EOG_list + drop_names + trigger_list
decim = 10
print decim
 

#=================================================
#subj_id_seq = [1,2,3,4,5,6,7,8,10,11,12,13]    
##subj_list = ['Extra1','Extra2'] 
#subj_list = list()
#for i in subj_id_seq:
#    subj_list.append('Subj%d' % i)
#subj_list = ['Subj14'] 
#subj_list = ['Subj16', 'Subj18']  
#subj_list = ['SubjYY_100', 'SubjYY_500']

# additional EEG subjects 500 ms presentation
subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']

# Subj_additional_2_500 can not go through ICA?
#subj_list = ["Subj_additional_3_500"]

#========================       
n_subj = len(subj_list) 
n_sesh = len(session_list)

# Note Extra1 and 2 have different EOG and ECG channel names, I need to do it seperately
for i in range(n_subj):
    for j in range(n_sesh):
        subj = subj_list[i]
        sesh = session_list[j]
        print subj
        print sesh
        filtered_fname = filtered_dir + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
        raw = mne.io.Raw(filtered_fname, preload = True)
        
        # bad_channel_list_name =raw_dir + "%s_EEG/%s_EEG_bad_channel_list.txt" %(subj, subj) 
        # bad_channel_list = list()
        # f = open(bad_channel_list_name)
        # for line in f:
        #     if line[0]!= "#":
        #         print line.split()
        #         bad_channel_list.append(line.split())
        # f.close()
        # raw.info['bads'] = bad_channel_list[0]
        # do not interpolate the bad channel here, once ica is done, do the interpolation
        picks = mne.pick_channels(raw.info['ch_names'],include = raw.info['ch_names'],
                                exclude = drop_names + trigger_list+raw.info['bads'])

        # compute the ica components, if the number of IC components are smaller than the full rank
        # ICA works much better
        ica = ICA(n_components = None, max_iter = 10000, random_state = 10)
        # which sensors to use
        ch_names = raw.info['ch_names']
        eeg_picks = mne.pick_channels(ch_names, include = [], exclude = exclude_list + raw.info['bads'])     
        # compute the ica components ( slow ), no rejection was applied
        # decim : downsample the data a bit to compute the ica, reduce computational burden.
        #reject = dict(eeg = 00e-6) 
        ica.fit(raw, picks = eeg_picks, decim = decim, reject = dict(eeg = 1E-3))
        ica_out_fname = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
        ica.save(ica_out_fname)
        	
        #if subj[0:4] == "Subj":
        #===== EOG ======
        # create EOG epochs to improve detection by correlation
        EOG_picks = mne.pick_channels(ch_names,include = EOG_list)
        eog_epochs = create_eog_epochs(raw, ch_name =EOG_list[0]) ##run this file with both vertical and 
        ##horizontal EOG to see if the correlated components are different. 
        eog_inds, eog_scores = ica.find_bads_eog(eog_epochs, ch_name =EOG_list[0])   
        #====== ECG ======
        #ecg_epochs = create_ecg_epochs(raw,ch_name = "ECG",picks= np.hstack([eeg_picks,ECG_picks]))
        # weirdly somehow I have to pick all channels here, otherwise, ECG is gone
        #ecg_inds, ecg_scores = ica.find_bads_ecg(ecg_epochs[0:len(ecg_epochs)//5], ch_name = "ECG")
        # picks_EEG = mne.pick_types(raw.info, eeg=True, ecg=True)
        # ecg_epochs = create_ecg_epochs(raw, picks=picks)
        # ecg_inds, ecg_scores = ica.find_bads_ecg(ecg_epochs[0:len(ecg_epochs)//5], ch_name = "ECG") 
        
        # =================== save the results =====================================
        mat_name = ica_dir + "%s_%s_%s_HEOG.mat" %(subj, sesh, fname_suffix)
        mat_dict = dict(eog_inds = eog_inds, eog_scores = eog_scores)
                        #(ecg_inds = ecg_inds, ecg_scores = ecg_scores)
        scipy.io.savemat(mat_name, mat_dict)
        del(raw)
        del(ica)
        del(mat_dict)
     

