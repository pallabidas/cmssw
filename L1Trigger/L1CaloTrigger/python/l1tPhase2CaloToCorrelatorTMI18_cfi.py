import FWCore.ParameterSet.Config as cms

l1tPhase2CaloToCorrelatorTMI18  = cms.EDProducer("Phase2L1CaloToCorrelatorTMI18",
                                  egtocorr18 = cms.InputTag("l1tPhase2L1CaloEGammaEmulator","GCTDigitizedClusterToCorrelatorTMI18"),
                                  pftocorr18 = cms.InputTag("l1tPhase2CaloPFClusterEmulator","GCTDigitizedPFClusterToCorrelatorTMI18")
)
