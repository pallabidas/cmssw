
'''
crab submit -c crab/crabConfigData.py

crab status -d <dir name>
'''

import CRABClient
from CRABClient.UserUtilities import config

config = config()

config.General.workArea = 'crab/r1'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'test/Nano_Data_addHto4bPlus_crab_cfg.py'
config.JobType.maxMemoryMB = 4000
# config.JobType.priority = 100  ## High priority for small test

# config.Data.inputDataset = '/JetHT/Run2018C-UL2018_MiniAODv2_GT36-v1/MINIAOD'
config.Data.inputDataset = 'DUMMY'

# config.General.requestName = config.Data.inputDataset.split('/')[1]+'_'+config.Data.inputDataset.split('/')[2]
config.General.requestName = 'DUMMY'
config.Data.outputDatasetTag = 'r1'
config.Data.publication = False

config.Data.ignoreLocality = False
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased' # 'Automatic' #'LumiBased' 'FileBased'
config.Data.unitsPerJob = 5
# config.Data.totalUnits = 50  ## Perform a small test
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
config.Site.storageSite = 'T2_CH_CERN' # Choose your site
# config.Data.outLFNDirBase = '/store/group/phys_susy/HToaaTo4b/NanoAOD/2018/data/PNet_v1_2023_10_06/'+config.Data.inputDataset.split('/')[2]+'/'
config.Data.outLFNDirBase = 'DUMMY'
