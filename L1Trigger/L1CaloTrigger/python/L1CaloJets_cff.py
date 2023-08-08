import FWCore.ParameterSet.Config as cms

# This cff file is based off of the L1T Phase-2 Menu group using
# the process name "REPR"

from L1Trigger.L1CaloTrigger.l1tPhase2L1CaloEGammaEmulator_cfi import * #Added by Pallabi


# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1EGCrystal clusters using Emulator

from L1Trigger.L1CaloTrigger.l1tEGammaCrystalsEmulatorProducer_cfi import *
l1tEGammaClusterEmuProducer.ecalTPEB = cms.InputTag("simEcalEBTriggerPrimitiveDigis","","")


# --------------------------------------------------------------------------------------------
#
# ----    Produce the calibrated tower collection combining Barrel, HGCal, HF

from L1Trigger.L1CaloTrigger.l1tTowerCalibrationProducer_cfi import *
l1tTowerCalibrationProducer.L1HgcalTowersInputTag = cms.InputTag("l1tHGCalTowerProducer","HGCalTowerProcessor","")
#l1tTowerCalibrationProducer.l1CaloTowers = cms.InputTag("l1tEGammaClusterEmuProducer","L1CaloTowerCollection","")
l1tTowerCalibrationProducer.l1CaloTowers = cms.InputTag("l1tPhase2L1CaloEGammaEmulator","GCTFullTowers","") #Added by Pallabi



# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1CaloJets

#from L1Trigger.L1CaloTrigger.l1tCaloJetProducer_cfi import *
#l1tCaloJetProducer.l1CaloTowers = cms.InputTag("l1tTowerCalibrationProducer","L1CaloTowerCalibratedCollection","")
#l1tCaloJetProducer.L1CrystalClustersInputTag = cms.InputTag("l1tEGammaClusterEmuProducer", "L1EGXtalClusterEmulator","")
from L1Trigger.L1CaloTrigger.l1tPhase2CaloJetEmulator_cfi import *
l1tPhase2CaloJetEmulator.gctFullTowers = cms.InputTag("l1tPhase2L1CaloEGammaEmulator","GCTFullTowers") #Added by Pallabi



# --------------------------------------------------------------------------------------------
#
# ----    Produce the CaloJet HTT Sums

from L1Trigger.L1CaloTrigger.l1tCaloJetHTTProducer_cfi import *



L1TCaloJetsSequence = cms.Sequence( 
        #l1tEGammaClusterEmuProducer *
        l1tPhase2L1CaloEGammaEmulator* #Added by Pallabi
        l1tTowerCalibrationProducer *
        #l1tCaloJetProducer *
        l1tPhase2CaloJetEmulator* #Added by Pallabi
        l1tCaloJetHTTProducer
)
