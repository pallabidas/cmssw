
'''
crab submit -c cragConfig.py

crab status -d <dir name>
'''

import CRABClient
from CRABClient.UserUtilities import config

config = config()

#config.General.requestName = 
config.General.workArea = 'crab/AWB_test_v1'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'test/HIG-RunIISummer20UL18NanoAODv9-02146_addHto4bPlus_cfg.py'
#config.JobType.inputFiles = '/afs/cern.ch/work/a/abrinke1/public/HiggsToAA/NanoAOD/crab/2018/CMSSW_10_6_26/src/RecoBTag/Combined/data/ParticleNetAK8/'
#config.JobType.pyCfgParams = ['maxEvt=-1', 'prtEvt=10000', 'nVtxMin=50', 'HCALPFA=%s' % (scheme)] 
#config.JobType.outputFiles = ['L1Ntuple_HCAL.root']

# config.Data.inputDataset = '/SUSY_GluGluH_01J_HToAATo4B_Pt150_M-20_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1/MINIAODSIM'
config.Data.userInputFiles = ['/eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/MC/SUSY_GluGluH_01J_HToAATo4B_Pt150_M-20_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL18/83EF2569-DC5F-1D4C-9B28-712F9751D75D.root']

# config.General.requestName = config.Data.inputDataset.split('/')[1]
config.General.requestName = 'SUSY_GluGluH_01J_HToAATo4B_Pt150_M-20_TuneCP5_13TeV_madgraph_pythia8'
config.Data.outputDatasetTag = '%s_%s' % (config.General.workArea, config.General.requestName)
config.Data.publication = False

config.Data.ignoreLocality = False
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased' # 'Automatic' #'LumiBased' 'FileBased'
# config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_355100_362760_Golden.json'
# config.Data.runRange = '362433-362760'
config.Data.unitsPerJob = 1
config.Site.storageSite = 'T2_CH_CERN' # Choose your site
config.Data.outLFNDirBase = '/store/group/phys_susy/HToaaTo4b/NanoAOD/2018/MC/custom_PNet_v1_2023_08_30_AWB_test_v1/'
