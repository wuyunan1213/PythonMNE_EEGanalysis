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
subj_list = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S09", "S10", "S11", "S12", "S14", "S15"]
session_list = ['PRE', 'POST']
n_subj = len(subj_list) 
n_sesh = len(session_list)

##it would be a much better idea to fun the following in an ide or jupyter.
for i in range(n_subj):
    for j in range(n_sesh):         
        subj = subj_list[i]
        sesh = session_list[j]
        print subj
        print sesh
        fif_name = filtered_dir  + "%s_%s_%s.fif" %(subj, sesh, fname_suffix)
        raw = mne.io.Raw(fif_name,preload = True)

        # ============= load ICA =========================================================
        ica_name = ica_dir + "%s_%s_%s_ica.fif" %(subj, sesh, fname_suffix)
        ica = mne.preprocessing.read_ica(ica_name)

        ##check and see what the automatically detected components are
        fig = ica.plot_components()
        figure1 = fig[0]
        figure2 = fig[1]
        ##what we have here is a list of figures because they are broken into two subfigures
        tmp_fig_name1 = fig_dir  + "%s_%s_component_plot0-19.png" %(subj, sesh)
        tmp_fig_name2 = fig_dir  + "%s_%s_component_plot20-31.png" %(subj, sesh)
        figure1.savefig(tmp_fig_name1)
        figure2.savefig(tmp_fig_name2)