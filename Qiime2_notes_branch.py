#!/usr/bin/env python
# coding: utf-8

# In[2]:


conda install -c conda-forge jupyterthemes


# In[9]:


get_ipython().system('jt -t monokai -f fira -fs 10 -nf ptsans -nfs 11 -N -kl -cursw 2 -cursc r -cellw 95% -T')


# # Qiime2 
# 
# Microbiome analysis package with focus on data and analysis transparency. Starts with an analysis with raw DNA sequence data and finish with publication-quality figures and statistical results.
# 
# ## Glosary: core concepts
# 
# ### Artifacts
# Data produces by Qiime2 exits as artifacts (.qza); contains data and metadata. 
# Visualizations 
# Any combination of visual data representations, such as: statistical results table, static images, etc. (.qzv)
# For observe .qza and .qzv use the following link:
# https://view.qiime2.org/
# ### Semantic type
# Type of data that ensure the data that is passed to an action is meaningful for the operation that will be performed. https://docs.qiime2.org/2021.2/semantic-types/. Define the type of data such as value in python.
# #### Plugins
# Correspond to a small code complementary to the program written to carry out a specified task.  Available plugins can be observed at https://docs.qiime2.org/2021.2/plugins/available/ 
# ### Methods 
# Type of action that takes one or more artifacts or parameters as input and produce one or more artifacts as terminal or intermediate outputs.
# ### Visualizers
# Type of action that takes one or more artifacts as inputs and produce ONE visualization as terminal output.
# * For more information go to https://docs.qiime2.org/2021.2/glossary/ 
# 
# ## Instaling by Windows Subsystem Linux (WSL)
# 
# ### 1. For install Qiime2 in Windows it is necesary to enable the subsytem for Linux and install Ubuntu:
# 
# 1. Open Start Menu at Windows
# 2. Click on Settings
# 3. Click on Apps
# 4. Scroll down and click on Related settings > Programs and Features
# 5. Go to the left menu and click on Turn Windows features on or off
# 6. Scroll down and enable Windows Subsystem for Linux clicking on the left checkbox
# 
# After WSL is enable, download Ubuntu terminal
# *Recomended to dowload version 16.04
# g. Open Power Shell at the Start Menu
# h. Download Ubunto by executing:
# 

# In[ ]:


curl.exe -L -o ubuntu-1604.appx https://aka.ms/wsl-ubuntu-1604


# i. Install Ubunto by executing:

# In[ ]:


Add-AppxPackage .\ubuntu-1604.appx


# you can find the instructions at: http://mmb.irbbarcelona.org/webdev/slim/molywood/public/tutorials/windows_sub and https://docs.microsoft.com/en-us/windows/wsl/install-manual
# 
# ### 2. Open Ubuntu and dowload miniconda
# 
# 1. Open Ubuntu terminal from Start Menu at Windows
# 2. Download miniconda installer for Linux (Python 3.8) Miniconda3 Linux 64-Bit at https://docs.conda.io/en/latest/miniconda.html#linux-installers 
# 3. At Ubuntu terminal execute:
# 

# In[ ]:


cd /mnt/c/Users/patir/Downloads 
## Users/patir/Downloads serves as an example where the miniconda installer was downloaded, change it acording to your needs!


# ### 3. Install miniconda and update it
# Execute the instalation command

# In[ ]:


bash Miniconda3-latest-Linux-x86_64.sh 


# Press yes to install and when the final message (For activation) appers press no and execute the command for activate conda's environment in the current shell session and update it.

# In[ ]:


eval "$(/home/patirais/miniconda3/bin/conda shell.bash hook)" 
conda update conda


# ### 4. Install Qiime2
# 
# a. Install wget command to eneble conda access and downlod files from the internet and dowload Qiime2 internet installer file 

# In[ ]:


conda install wget
wget https://data.qiime2.org/distro/core/qiime2-2021.2-py36-linux-conda.yml 


# If the command deny access do it manually as follows:
# 1. Copy-paste https://data.qiime2.org/distro/core/qiime2-2021.2-py36-linux-conda.yml on the web browser.
# 2. Copy-paste all text found into a text file in notes. 
# 3. Save the file in the Downloads folder as qiime2-2021.2-py36-linux-conda.yml
# 
# Execute the following commands, if everything works fine the help menu from Qiime2 will appear. 
# 

# In[ ]:


conda env create -n qiime2-2021.2 --file qiime2-2021.2-py36-linux-conda.yml


# In[ ]:


conda activate qiime2-2021.2 


# In[ ]:


qiime --help 


# # Open Qiime2
# To open qiime 2 in the WSL 
# 1. Open Ubuntu 
# 2. Acivate qiime environment and activate the tab completion by executing

# In[10]:


conda activate qiime2-2021.2 


# In[ ]:


source tab-qiime 
# To know which environments you have in Ubunto (For example if you save qiime environment with other name and you do not remember it) use comand:
# conda info --envs


# 3. For new data create a new folder for save all obtained data by executing 

# In[ ]:


mkdir ./qiime2/newfoldername


# Else, enter to the folder with your data by executing:

# In[ ]:


cd ./ qiime2/newfoldername/
# If you do not know where is your folder you can use pwd and ls command following the cd ./ to enter to the folder


# # Check DATA!
# Before starting to import data is very important to know the type of data we are working with FOR KNOWN HOW TO IMPORT THE DATA, for example in the project ‘Fístulas anastomóticas en pacientes con cancer de colon’ the sequenciation was performed in Illumina as **Paired-end-sequencing** of the variable regions V3 and V4 (460 pb) of the 16s rRNA gene. * Illumina can sequence regions of 300 pb maximum, therefore, the F and R files must be overlapped in qiime2 to obtain the 460 pb sequenced amplicon. Additionally, sequence data is already demultiplex by Illumina (barcode file is not provided), therefore, only we only have two Fastq.qz files per sample (Forward and Reverse raw sequences). The data must be saved in the same folder that we create, to open the folder in WSL execute:

# In[ ]:


explorer.exe  .


# In[ ]:



# Paste the raw sequences folder, if any Zone.identifier file is created delated by executing
cd ~ && find . -name "*:Zone.Identifier" -type f -delete  


# # Importing data 
# In this section it will be explained how to import data manually for **Paired-end-sequencing demultiplexed**, we only have two files per sample (Forward raw sequence: sample1_R1.fastq.gz and Reverse sequence: sample1_R2.fastq.gz).
# 
# ## Manifest
# A text file must be created containgin in the first row the sample-id, the forward-absolute-filepath and the reverse-absolute-filepath (filepath makes reference to the directory where the fastq file are located). The tsv file can be created in python with the following script * Change the 4 paths accordig to your needs:

# In[12]:


import os
import pandas as pd

path = '/home/patirais/qiime2/prueba1/'
path_raw = path + 'Raw Sequences 16s rRNA/'
path_W = '//wsl$/Ubuntu-16.04' + path
path_W_raw = path_W + 'Raw Sequences 16s rRNA/'

data = pd.DataFrame()
data['file'] = os.listdir(path_W_raw)
data['absolute-filepath'] = [path_raw+x for x in os.listdir(path_W_raw)]
data['sample-id'] = data['file'].apply(lambda x: x.split('_')[0])
data['sample-id'] = data['sample-id'].apply(lambda x: '0'+x if len(x)==1 else x)
data['direction'] = data['file'].apply(lambda x: x.split('_')[1].split('.')[0])
data = data.sort_values(['sample-id','direction'])
data['direction'] = data['direction'].apply(lambda x: 'forward' if x=='R1' else 'reverse')
data = data[['sample-id','absolute-filepath','direction']]
df1 = data.loc[data['direction'] == 'forward'].set_index('sample-id').drop(columns= 'direction')
df1 = df1.rename(columns = {'absolute-filepath' : 'forward-absolute-filepath'})
df2 = data.loc[data['direction'] == 'reverse'].set_index('sample-id')
df1['reverse-absolute-filepath'] =  df2['absolute-filepath']

df1.to_csv(path_W+'manifest.tsv',sep ='\t', encoding = 'utf-8', index_label = 'sample-id')


# In[23]:


#After you open the file create it must look similar to this one:
from IPython.display import Image
Image('C:/Users/patir/Desktop/qiime2/Captura_manifest.png')


# ## Importing 
# Once the manifest is created , import it to qiime executing:
# **Important to know the queality score that Ilummina work with (normally 33)**
# 
# 

# In[ ]:


qiime tools import   --type 'SampleData[PairedEndSequencesWithQuality]'   --input-path /home/patirais/qiime2/prueba1/manifest.tsv  --output-path paired-end-demux.qza   --input-format PairedEndFastqManifestPhred33V2
qiime tools peek paired-end-demux.qza
# last command to check the format, UUIC, and type


# Summarize the data and create a visualization, check the interactive quility plot to observed where to cut the sequences asuring of good quality.

# In[ ]:


qiime demux summarize --i-data paired-end-demux.qza --o-visualization demux-paired-summary.qzv


# If your environment can run the qiime tools view run the comand 
# qiime tools view demux-paired-summary.qzv
# **ELSE** go to https://view.qiime2.org/ and drag the .qzv file 

# In[25]:


from IPython.display import Image
Image('C:/Users/patir/Desktop/qiime2/demux_seq.png')


# # Sequence qulity control and feature table construction with DADA2
# 
# The Divisive Amplicon Denoising Algorithm (DADA) is an open software for modeling and corection of amplicon sequences by Illumina. DADA introduced a model-based approach for correcting amplicon errors without constructing OTUs. DADA identified fien-scale variation in 454-sequenced amplicon data while outputting few false positives. 

# Three DADA2 constructions will be performed (with diferent trunc sections) in order of choosing the best aligmnent (higher reteined features in the summarize table qzv file ). Therfore, we will create 3 folders with trunqued sequence lenght chosed.

# In[ ]:


mkidir results-dada2-271-219


# In[ ]:


qiime dada2 denoise-paired --i-demultiplexed-seqs paired-end-demux.qza --p-trunc-len-f 273 --p-trunc-len-r 219 --p-trim-left-f 19 --p-trim-left-r 22 --p-n-threads 0 --o-table results-dada2-271-219/table.qza --o-representative-sequences results-dada2-271-219/rep-seqs.qza --o-denoising-stats results-dada2-271-219/stats-dada2.qza


# Generate the vizualition file for denoising stats

# In[ ]:


qiime metadata tabulate --m-input-file results-dada2-271-219/stats-dada2.qza --o-visualization results-dada2-271-219/stats-dada2.qzv


# # FeatureTable and FeatureData summaries
# Generate the **feature data summaries** (Gives information on how many sequences are associated with each sample with each feature,histogramsof those distributions, and some relaed summary statistics) and the **feature table** (Provide a mapping feature IDs to sequences, and provide links to easily BLAST each sequence at NCBI database)

# In[ ]:


qiime feature-table summarize --i-table results-dada2-271-219/table.qza --o-visualization results-dada2-271-219/table.qzv --m-sample-metadata-file metadata.tsv


# In[ ]:


qiime feature-table tabulate-seqs --i-data results-dada2-271-219/rep-seqs.qza --o-visualization results-dada2-271-219/rep-seqs.qzv


# Do the same for the two other sequences (280-210 and 290-219)

# In this example the 271-219 sequence was chosen due to qiime vizualitation of table.qzv has teh higher retained features (51.79% at sampling depth of 42594). Notice the % is quite low, this is due to the small sampling we are using (15 samples with one control).

# In[ ]:




