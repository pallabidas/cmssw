# cmsDriver.py --python_filename test/JetHT_cfg.py --eventcontent NANOAOD --datatier NANOAOD --fileout file:JetHT.root --conditions 106X_dataRun2_v36 --step NANO --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --data -n 100

MAX_EVT  = 100   ## Maximum number of events to process
PRT_EVT  = 1     ## Print every Nth event
SKIM_FAT = True  ## Skim requiring at least 1 AK8 fatJet
SAMP     = 'JetHT_2018C'  ## Sample to process
## JetHT_2018A, JetHT_2018B, JetHT_2018C, JetHT_2018C

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
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(MAX_EVT)
)
process.MessageLogger.cerr.FwkReport.reportEvery = PRT_EVT

top_dir = '/eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/data/'
if SAMP == 'JetHT_2018C':
    in_dir = top_dir+'JetHT/Run2018C-UL2018_MiniAODv2_GT36-v1/'
    in_files = ['file:'+in_dir+'00286796-4A86-AD46-B017-149AEB39EC10.root',
                'file:'+in_dir+'004F56C4-E18E-324B-A918-6BEF1BE6C2EF.root']

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(in_files[0]),
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

# Output file name
out_file = 'file:output/HtoAA_default_'+SAMP
if SKIM_FAT: out_file += '_skim'
if MAX_EVT > 0: out_file += '_%dk' % (MAX_EVT / 1000)
out_file += '.root'

# Output definition
process.NANOAODoutput = cms.OutputModule("NanoAODOutputModule",
    skimFatJet = cms.untracked.bool(SKIM_FAT),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string(out_file),
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

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeData 

#call to customisation function nanoAOD_customizeData imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeData(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
