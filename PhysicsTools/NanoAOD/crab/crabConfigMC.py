
'''
crab submit -c crab/crabConfigMC.py

crab status -d <dir name>
'''

import CRABClient
from CRABClient.UserUtilities import config

config = config()

config.General.workArea = 'crab/r1'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'test/Nano_MC_addHto4bPlus_crab_cfg.py'
config.JobType.maxMemoryMB = 4000
# config.JobType.priority = 100  ## High priority for small test

# config.Data.inputDataset = '/SUSY_GluGluH_01J_HToAATo4B_Pt150_M-12_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM'
config.Data.inputDataset = 'DUMMY'

# config.General.requestName = config.Data.inputDataset.split('/')[1]
config.General.requestName = 'DUMMY'
config.Data.outputDatasetTag = 'r1'
config.Data.publication = False

config.Data.ignoreLocality = False
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased' # 'Automatic' #'LumiBased' 'FileBased'
config.Data.unitsPerJob = 10
# config.Data.totalUnits = 100  ## Perform a small test
config.Site.storageSite = 'T2_CH_CERN' # Choose your site
config.Data.outLFNDirBase = '/store/group/phys_susy/HToaaTo4b/NanoAOD/2018/MC/PNet_v1_2023_10_06/'
