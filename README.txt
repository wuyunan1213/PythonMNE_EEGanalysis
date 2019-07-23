###This folder contains scripts for analyzing EEG data collected from a learning study investigating learning Mandarin categories from continuous speech through videogame play. Once the paper is published, a link to the paper will be provided here for a reference. All data and results are stored in a separate folder

###the raw EEG data were collected using NeuroScan system and the experiment stimuli were presented in Eprime. 

#######################################Preprocessing######################################
#######################################Step 0######################################
EEG0_filter_visualize.py

Band-pass filter of 0.1Hz-110Hz

Notch filter of 60Hz

Both ends of the continuous data were cropped such that it starts from 3 seconds before the first event and 3 seconds after the last event.

DC shift was removed by normalizing the data by the mean.

Data re-referenced to the average of M1 and M2. 

Save filtered data into directory ./filtered_raw_data/

Run this file so you can look at visualize the raw data through raw.plot(). You can mark the bad channels in these plots. 

#######################################Step 1######################################
EEG1_filter_visualize.py

Read the filtered data and compute the IC components

Data were down-sampled 10 times for ICA computation, which should not affect the original data resolution or component detection but could speed up computation

EOG epochs were identified to correlate with the components for better artifact detection. 

in ica.fit function, random_state should be set to a particular integer so that the results are guaranteed to be the same every time we run them

The ICA components as well as the EOG components are saved in the ica_raw_data folder

You could run the file twice by changing the EOG channel to correlate the data with (first time using VEOG second time using HEOG, and saving the files with different names) so we have more information and more EOG channels to find eye blink components in ICA.

Therefore, in this folder, you will see 3 .mat files. One called '_HEOG', one called '_VEOG' and another one called '_manual_check'. The first two are the components we get from running the automatic EOG component detection. The last one is the final decision I made after visualizing the components. 

#######################################Step 2######################################
Since this step is computationally expensive and takes a long time, I separated it out from the ICA analysis. Therefore, there are 3 steps, Step 2-4 that are all related to ICA
In this step, I’m plotting all of the components in the 2-D scalp. This can help us visualize all of the components from all participants in both sessions. Then I’m saving these plots automatically in the ica_fig directory for later examination. 
#######################################Step 3######################################
This step is the only manual step in the preprocessing pipeline and takes the longest time. In this step, I can’t automate everything in a loop because I have to inspect every component for every subject and decide which component to reject so the components to be rejected are different for everyone. 

So for each subject in each session, I visually inspect every component and decide which ones are possible eye blink, heart and muscle components. Put these component numbers in “picks” and then plot them using the plot_overlay function to see if we rejected the component what the data would look like. This is a great function that tells you basically how noisy this component is. Usually muscle components don’t matter that much after rejection so I didn’t reject a lot of muscle components. But eye blinks are clearly noisier. Heart components are a little hard to identify sometimes but they are clearly visible in some subjects. Therefore, I also used the plot_sources function to look at the raw data for the suspected heart component.

In the previous step we did some automatic artifact detection. These are usually very accurate but I wanted to double check the components that it identified, particularly the correlation scores. So I print these scores after loading the Ica data. 

For component identification, it helps to do some practice on the website: http://labeling.ucsd.edu/tutorial/labels. Please note that during component labeling, I try to be as conservative as possible and label as muscle as possible. All of the components to be rejected are labeled only when I’m extremely sure that this component is noise and not signal. It’s better to reject less than more because random noise will eventually fade out after averaging. 

After identifying all the components to be rejected, I save them in lists e.g. new_eog/ecg/muscle_inds and save these lists in manual_check.mat
#######################################Step 4######################################
In this step, I just load both the Ica and raw data, and then load the manual_check.mat matrix where we get the bad components identified in the previous step. After loading these, I use the function ica.apply to apply these components back to the raw data and reject these components from the raw data. Finally, saved the cleaned data into a file in the Ica_raw_data directory called after_ica_raw.fif
#######################################Step 5######################################
This is one of the last steps of the pre-processing pipeline. This tile takes events from the sentence event file and read them and label the EEG data with the event types. Please note  that these are only sentence events, word events will come in the next step. In this step, I used -600ms to 600ms as my epoch length with a baseline correct from -200ms to 0. The long epoch period is considering the later time-frequency analysis that I will look into—these analyses usually require longer time periods before the stimuli onset. In this step, I also used a trial/epoch rejection method where epochs that are 15 standard deviations from the average would be rejected. Usually for each subject in each session, there are around 4-5 epochs being rejected, which is not a lot. These sentence epochs are then saved to the directory sentence_epoch_raw_data.
#######################################Step 6######################################
This is the last step of the pre-processing pipeline. This step is essentially identical from the last step except the event files that we read for this step are word event files.  The same trial rejection procedure is applied and the data are saved to wordd_epoch_raw_data
#######################################Analysis######################################
#######################################Step 0######################################