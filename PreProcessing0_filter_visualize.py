import mne
import numpy as np
import scipy
import scipy.io

tmp_rootdir = '/Users/charleswu/Desktop/MNE/'
raw_dir = tmp_rootdir + "raw_data/"
filtered_dir = tmp_rootdir + "filtered_raw_data/"
ica_dir = tmp_rootdir + "ica_raw_data/" 
l_freq = 0.1 
h_freq = 110.0 ##the low and high-pass filters were selected based on other EEG studies. See Southwell, 
##Baumann, Gal, Barascud, Friston and Chait, 2017 
notch_freq = [60.0,120.0]

fname_suffix = "filter_%d_%dHz_notch_raw" %(l_freq, h_freq)
Mastoids = ['M1','M2']
#EOG_list = [u'LhEOG', u'RhEOG', u'LvEOG1', u'LvEOG2', u'RvEOG1']
EOG_list = ['HEOG', 'VEOG']
#ECG_list = [u'ECG']
#ECG_list = ['ECG']

# drop_names = []
# for i in range(7):
#     drop_names.append("misc%d"%(i+1))

trigger_list = ['STI 014']
#events = ['1','12','14','32','34','52','54','62','64']      
# the trigger is now status 
#exclude_list = Mastoids + EOG_list + drop_names + trigger_list #+ ECG_list

# subject
#============================================
#subj_id_seq = [1,2,3,4,5,6,7,8,10,11,12,13]    
#subj_list = ['Extra1','Extra2'] 
#for i in subj_id_seq:
#    subj_list.append('Subj%d' % i)
#subj_list = ['Subj14']  
#subj_list = ['Subj16', 'Subj18']  
#subj_list = ['SubjYY_100', 'SubjYY_500']

# additional EEG subjects 500 ms presentation
subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
      
n_subj = len(subj_list) 
n_sesh = len(session_list)
#============================================    
for i in range(n_subj):
    for j in range(n_sesh):
        subj = subj_list[i]
        sesh = session_list[j]
        print subj
        print sesh
        raw_fname = raw_dir + "%s_%s.cnt" %(subj, sesh)
        raw = mne.io.read_raw_cnt(raw_fname, montage = None, eog = 'auto', preload = True, verbose = None)
    
        events = mne.find_events(raw, stim_channel = trigger_list[0])

        # 
        # bad_channels were identified in Step1
        #bad_channel_list_name = raw_dir + "%s_EEG/%s_EEG_bad_channel_list.txt" %(subj,subj)
        # ignore comments #, the first line is always the emtpy room data
        #bad_channel_list = list()
        #f = open(bad_channel_list_name)
        #for line in f:
        #    if line[0]!= "#":
        #        print line.split()
        #        bad_channel_list.append(line.split())
        #f.close()
        # there will be only one line
        #raw.info['bads'] += bad_channel_list[0]
        #print "bad channels"
        #print raw.info['bads']
        # the Status channel has extremely large values
        # subtract the minium value there, so it is 0, 100, 200
        #raw.info['projs'] = []#
        start_time = max(raw._times[events[0,0]]-3.0,0.0)#
        end_time = raw._times[events[-1,0]] + 3.0#
        raw = raw.crop(tmin = start_time, tmax = end_time)#
        picks = mne.pick_channels(raw.info['ch_names'],include = raw.info['ch_names'],exclude = trigger_list+raw.info['bads'])#                       
        #raw._data[-1,:] -= np.min(raw._data[-1,:])#

            # ================remove the DC for each individual channel?================
        data = raw._data[picks,:]#
        data = (data.T- np.mean(data, axis = 1)).T#
        raw._data[picks,:] = data#

        #=================== do not reference to mastoids M1, M2==========================
        # if M1/M2 are very noisy, it will mess up all channels!!!
        raw, ref_data = mne.io.set_eeg_reference(raw, ref_channels=Mastoids, copy=True)
        # also remove the irrelevent channels, they should all be zero. 
        drop_picks = mne.pick_channels(raw.info['ch_names'],include =drop_names) ## for now just leave the
        ###drop_names because this funtion requires at least two arguments and leaving it there doesn't 
        ##affect the analysis anyways because the drop_picks would just be an empty list
        raw._data[drop_picks] = 0#
            
        raw.filter(l_freq, h_freq, picks = picks)
        raw.notch_filter(notch_freq)
        filtered_name = filtered_dir + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
        raw.save(filtered_name, overwrite = True)
        
        #raw.plot()
