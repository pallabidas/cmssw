# cmsDriver.py --python_filename HIG-RunIISummer20UL18NanoAODv9-02146_1_cfg.py --eventcontent NANOAODSIM --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02146.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n 100

TOPDIR = '/eos/cms/store/group/phys_susy/HToaaTo4b/NanoAOD/2018/MC/'

# JOBID  = '1-18'
# INFILE = 'file:/eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/MC/SUSY_GluGluH_01J_HToAATo4B_Pt150_M-40_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL18/05B17C49-301F-F04C-943A-5C262AB6C17E.root'
# OUTFILE = TOPDIR+'PNet_v1_2023_10_06/SUSY_GluGluH_01J_HToAATo4B_Pt150_M-40_TuneCP5_13TeV_madgraph_pythia8/r1/231007_083639/0000/PNet_v1_'+JOBID

# # JOBID = '1-4a'
# JOBID = '1-4b'
# # INFILE = 'file:/eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/MC/SUSY_GluGluH_01J_HToAATo4B_Pt150_M-15_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL18/CCD7A5EE-0B03-9B45-AEDF-9691C006D471.root'
# INFILE = 'file:/eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/MC/SUSY_GluGluH_01J_HToAATo4B_Pt150_M-15_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL18/8D9FA65C-81CA-1E41-A551-D3CBDD414B49.root'
# OUTFILE = TOPDIR+'PNet_v1_2023_10_06/SUSY_GluGluH_01J_HToAATo4B_Pt150_M-15_TuneCP5_13TeV_madgraph_pythia8/r1/231007_085007/0000/PNet_v1_'+JOBID

# JOBID  = '3-15'
# INFILE = 'file:/eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/MC/QCD_HT700to1000_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18/04193046-685A-9541-881A-AF38A95F79BA.root'
# OUTFILE = TOPDIR+'custom_PNet_v1_2023_08_30_AWB_test_v8/QCD_HT700to1000_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/AWBTagTestV8/231006_215119/0000/HtoAA_PNet_Prod_v1_'+JOBID

JOBID   = '466'
INFILES = ['file:/eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/MC/ZJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18/F8B681AA-1188-4D4F-A497-75AEF34D91F8.root']
LUMIS   = ["1:1602-1:1602", "1:1867-1:1867", "1:4830-1:4830", "1:8459-1:8459", "1:8630-1:8630", "1:8764-1:8764", "1:8863-1:8863", "1:17925-1:17925", "1:20914-1:20914", "1:24964-1:24964"]
OUTFILE = TOPDIR+'PNet_v1_2023_10_06/ZJetsToQQ_HT-800toInf_TuneCP5_13TeV-madgraphMLM-pythia8/r1/231010_132027/0000/PNet_v1_'+JOBID


## ----------------------------------------------------------------------------- ##

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
process.load('PhysicsTools.NanoAOD.nano_addHto4bPlus_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)
process.MessageLogger.cerr.FwkReport.reportEvery = 10

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(FILE for FILE in INFILES),
    lumisToProcess = cms.untracked.VLuminosityBlockRange(LUMI for LUMI in LUMIS),
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
    skimFatJet = cms.untracked.bool(True),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string(OUTFILE+'.root'),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v16_L1v1', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_addHto4bPlus_cff
from PhysicsTools.NanoAOD.nano_addHto4bPlus_cff import nanoAOD_customizeMC 

#call to customisation function nanoAOD_customizeMC imported from PhysicsTools.NanoAOD.nano_addHto4bPlus_cff
process = nanoAOD_customizeMC(process, True)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
