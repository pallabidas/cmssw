# cmsDriver.py --python_filename HIG-RunIISummer20UL18NanoAODv9-02146_1_cfg.py --eventcontent NANOAODSIM --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02146.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n 100

MAX_EVT  = 100   ## Maximum number of events to process
PRT_EVT  = 10    ## Print every Nth event
SKIM_FAT = True  ## Skim requiring at least 1 AK8 fatJet
SAMP     = 'ZJetsToQQ_HT-200to400'  ## Sample to process
## HToAA_Pt350_mH-70_mA-12, HtoAA_MH-125_MA-20
## QCD_BGen_HT700to1000, QCD_bEnr_HT700to1000
## ZJetsToQQ_HT-200to400, ZJetsToQQ_HT-400to600, ZJetsToQQ_HT-600to800

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
process.load('PhysicsTools.NanoAOD.nano_addHto4b_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(MAX_EVT)
)
process.MessageLogger.cerr.FwkReport.reportEvery = PRT_EVT

top_dir = '/eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/MC/'
if SAMP == 'HToAA_Pt350_mH-70_mA-12':
    in_dir = top_dir+'SUSY_GluGluH_01J_HToAATo4B_Pt350_mH-70_mA-12_wH-70_wA-70_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL18/'
    in_files = ['file:'+in_dir+'10300/MiniAODv2_10312.root', ## Small file (4.6 MB)
                'file:'+in_dir+'10400/MiniAODv2_10413.root'] ## Large file (8.2 MB)
if SAMP == 'HtoAA_MH-125_MA-20':
    in_dir = top_dir+'SUSY_GluGluH_01J_HToAATo4B_Pt150_M-20_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL18/'
    in_files = ['file:'+in_dir+'003A1234-0E1D-154A-9704-9406B61CB642.root',
                'file:'+in_dir+'0B5221FE-B9CF-A449-A523-33FFCAF65CD2.root',
                'file:'+in_dir+'0CBDE505-6EE4-B44D-97B2-7CA3AB7C9E5F.root',
                'file:'+in_dir+'0E2F71F8-7E51-BC4B-A159-7CD4E2732F60.root'],
if SAMP == 'QCD_BGen_HT700to1000':
    in_dir = top_dir+'QCD_HT700to1000_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18/'
    in_files = ['file:'+in_dir+'04193046-685A-9541-881A-AF38A95F79BA.root',
                'file:'+in_dir+'0678A9F0-E3E7-3244-8FBF-9EFBF044B66B.root',
                'file:'+in_dir+'0C6DD58D-403B-6D40-BD6A-6A8C598A2DA0.root'],
if SAMP == 'QCD_bEnr_HT700to1000':
    in_dir = top_dir+'QCD_bEnriched_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18/'
    in_files = ['file:'+in_dir+'26DB15A1-158E-B24A-84C7-7CD85D760D02.root',
                'file:'+in_dir+'2789F3AB-BCBC-DE47-BA4E-9365E2C9673C.root',
                'file:'+in_dir+'27DAB083-09A0-934D-BDE5-A4AF7F7697A0.root'],
if SAMP == 'ZJetsToQQ_HT-200to400':
    in_dir = top_dir+'ZJetsToQQ_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18/'
    in_files = ['file:'+in_dir+'01981D69-1A44-884F-9C59-D87F2A93FB7C.root',
                'file:'+in_dir+'1E403550-FF55-FE49-A689-84D787572386.root',
                'file:'+in_dir+'21C25769-AAE2-314A-98AE-EA5C0250F408.root'],
if SAMP == 'ZJetsToQQ_HT-400to600':
    in_dir = top_dir+'ZJetsToQQ_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18/'
    in_files = ['file:'+in_dir+'033D8320-E6B6-C448-99C7-CE64AAE1ED99.root',
                'file:'+in_dir+'038F73DA-DAFD-7946-BF55-BBB30C8B7F42.root',
                'file:'+in_dir+'03C3FE24-D062-1040-8117-C6386F05EFCD.root'],
if SAMP == 'ZJetsToQQ_HT-600to800':
    in_dir = top_dir+'ZJetsToQQ_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18/'
    in_files = ['file:'+in_dir+'0226D148-735C-CE48-A726-59B6B6DF5CCD.root',
                'file:'+in_dir+'07570633-3AE3-4149-93CB-8721448B3FDF.root',
                'file:'+in_dir+'09C0E916-F1A3-0749-96A0-7A15E8EE6D6B.root'],

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
out_file = 'file:output/HtoAA_addHto4b_'+SAMP
if SKIM_FAT: out_file += '_skim'
if MAX_EVT > 0: out_file += '_%dk' % (MAX_EVT / 1000)
out_file += '.root'

# Output definition
process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    skimFatJet = cms.untracked.bool(SKIM_FAT),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string(out_file),
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

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_addHto4b_cff
from PhysicsTools.NanoAOD.nano_addHto4b_cff import nanoAOD_customizeMC 

#call to customisation function nanoAOD_customizeMC imported from PhysicsTools.NanoAOD.nano_addHto4b_cff
process = nanoAOD_customizeMC(process, SKIM_FAT)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
