# cmsDriver.py --python_filename test/JetHT_cfg.py --eventcontent NANOAOD --datatier NANOAOD --fileout file:JetHT.root --conditions 106X_dataRun2_v36 --step NANO --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --data -n 100

TOPDIR = '/eos/cms/store/group/phys_susy/HToaaTo4b/NanoAOD/2018/data/'

JOBID   = '2535'
INFILES = ['file:/eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/data/JetHT/Run2018A-UL2018_MiniAODv2_GT36-v1/8CA8B24E-9764-3745-9086-C4826E038B13.root',
           'file:/eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/data/JetHT/Run2018A-UL2018_MiniAODv2_GT36-v1/1A05DD2B-73B0-BD4D-82C7-8028CC42F805.root']
LUMIS   = ["316187:57-316187:57", "316187:22-316187:22", "316187:16-316187:16", "316187:19-316187:19", "316187:52-316187:52", "316187:47-316187:47"]
OUTFILE = TOPDIR+'PNet_v1_2023_10_06/Run2018A-UL2018_MiniAODv2_GT36-v1/JetHT/r1/231009_211628/0002/PNet_v1_'+JOBID


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
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
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
process.NANOAODoutput = cms.OutputModule("NanoAODOutputModule",
    skimFatJet = cms.untracked.bool(True),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string(OUTFILE+'.root'),
    outputCommands = process.NANOAODEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v36', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequence)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODoutput_step = cms.EndPath(process.NANOAODoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_addHto4bPlus_cff
from PhysicsTools.NanoAOD.nano_addHto4bPlus_cff import nanoAOD_customizeData 

#call to customisation function nanoAOD_customizeData imported from PhysicsTools.NanoAOD.nano_addHto4bPlus_cff
process = nanoAOD_customizeData(process, True)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
