# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: --python_filename HIG-RunIISummer20UL18NanoAODv9-02146_1_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02146.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein file:/eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/MC/SUSY_GluGluH_01J_HToAATo4B_Pt350_mH-70_mA-12_wH-70_wA-70_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL18/10300/MiniAODv2_10312.root --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n 100
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_2018_cff import Run2_2018
from Configuration.Eras.Modifier_run2_nanoAOD_106Xv2_cff import run2_nanoAOD_106Xv2

process = cms.Process('NANO',Run2_2018,run2_nanoAOD_106Xv2)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.nano_fatJetsHto4b_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)
process.MessageLogger.cerr.FwkReport.reportEvery = 10

top_dir = '/eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/MC/'
# ## HtoAA WH-70
# in_dir = top_dir+'SUSY_GluGluH_01J_HToAATo4B_Pt350_mH-70_mA-12_wH-70_wA-70_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL18/'
## HtoAA MH-125 MA-20
in_dir = top_dir+'SUSY_GluGluH_01J_HToAATo4B_Pt150_M-20_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL18/'
# ## QCD BGen HT700to1000
# in_dir = top_dir+'QCD_HT700to1000_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18/'
# ## QCD bEnr HT700to1000
# in_dir = top_dir+'QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18/'
# ## ZtoQQ HT-400to600
# in_dir = top_dir+'ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18/'
# ## ZtoQQ HT-600to800
# in_dir = top_dir+'ZJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18/'

# Input source
process.source = cms.Source("PoolSource",
    # ## HtoAA WH-70
    # ## Small file (4.6 MB)
    # fileNames = cms.untracked.vstring('file:'+in_dir+'10300/MiniAODv2_10312.root'),
    # ## Large file (8.2 MB)
    # fileNames = cms.untracked.vstring('file:'+in_dir+'10400/MiniAODv2_10413.root'),
    ## HtoAA MH-125 MA-20
    fileNames = cms.untracked.vstring('file:'+in_dir+'003A1234-0E1D-154A-9704-9406B61CB642.root',
                                      'file:'+in_dir+'0B5221FE-B9CF-A449-A523-33FFCAF65CD2.root',
                                      'file:'+in_dir+'0CBDE505-6EE4-B44D-97B2-7CA3AB7C9E5F.root',
                                      'file:'+in_dir+'0E2F71F8-7E51-BC4B-A159-7CD4E2732F60.root'),
    # ## QCD BGen HT700to1000
    # fileNames = cms.untracked.vstring('file:'+in_dir+'04193046-685A-9541-881A-AF38A95F79BA.root',
    #                                   'file:'+in_dir+'0678A9F0-E3E7-3244-8FBF-9EFBF044B66B.root',
    #                                   'file:'+in_dir+'0C6DD58D-403B-6D40-BD6A-6A8C598A2DA0.root'),
    # ## QCD bEnr HT700to1000
    # fileNames = cms.untracked.vstring('file:'+in_dir+'26DB15A1-158E-B24A-84C7-7CD85D760D02.root',
    #                                   'file:'+in_dir+'2789F3AB-BCBC-DE47-BA4E-9365E2C9673C.root',
    #                                   'file:'+in_dir+'27DAB083-09A0-934D-BDE5-A4AF7F7697A0.root'),
    # ## ZtoQQ HT-400to600
    # fileNames = cms.untracked.vstring('file:'+in_dir+'033D8320-E6B6-C448-99C7-CE64AAE1ED99.root',
    #                                   'file:'+in_dir+'038F73DA-DAFD-7946-BF55-BBB30C8B7F42.root',
    #                                   'file:'+in_dir+'03C3FE24-D062-1040-8117-C6386F05EFCD.root'),
    # ## ZtoQQ HT-600to800
    # fileNames = cms.untracked.vstring('file:'+in_dir+'0226D148-735C-CE48-A726-59B6B6DF5CCD.root',
    #                                   'file:'+in_dir+'07570633-3AE3-4149-93CB-8721448B3FDF.root',
    #                                   'file:'+in_dir+'09C0E916-F1A3-0749-96A0-7A15E8EE6D6B.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('--python_filename nevts:100'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition
process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    writeTriggerBranches = cms.untracked.bool(False),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    # fileName = cms.untracked.string('file:output/HIG-RunIISummer20UL18NanoAODv9-02146_fatJetsHto4b.root'),
    fileName = cms.untracked.string('file:output/HtoAA_fatJetsHto4b_HtoAA_MH-125_MA-20_0_test.root'),
    # fileName = cms.untracked.string('file:output/HtoAA_fatJetsHto4b_QCD_BGen_HT700to1000_0_20k.root'),
    # fileName = cms.untracked.string('file:output/HtoAA_fatJetsHto4b_QCD_bEnr_HT700to1000_2_20k.root'),
    # fileName = cms.untracked.string('file:output/HtoAA_fatJetsHto4b_ZJetsToQQ_HT-400to600_03_10k.root'),
    # fileName = cms.untracked.string('file:output/HtoAA_fatJetsHto4b_ZJetsToQQ_HT-600to800_0_100k.root'),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v16_L1v1', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequenceCommon)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_fatJetsHto4b_cff
from PhysicsTools.NanoAOD.nano_fatJetsHto4b_cff import nanoAOD_customizeCommon 

#call to customisation function nanoAOD_customizeCommon imported from PhysicsTools.NanoAOD.nano_fatJetsHto4b_cff
process = nanoAOD_customizeCommon(process)

# # Automatic addition of the customisation function from Configuration.DataProcessing.Utils
# from Configuration.DataProcessing.Utils import addMonitoring 

# #call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
# process = addMonitoring(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
