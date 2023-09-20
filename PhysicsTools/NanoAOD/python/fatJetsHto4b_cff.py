import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.nano_eras_cff import *
from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *

jetCorrFactorsAK8 = patJetCorrFactors.clone(src='slimmedJetsAK8',
    levels = cms.vstring('L1FastJet',
        'L2Relative',
        'L3Absolute',
	'L2L3Residual'),
    payload = cms.string('AK8PFPuppi'),
    primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
)
run2_miniAOD_80XLegacy.toModify(jetCorrFactorsAK8, payload = cms.string('AK8PFchs')) # ak8PFJetsCHS in 2016 80X miniAOD

from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cfi import *

updatedJetsAK8 = updatedPatJets.clone(
	addBTagInfo=False,
	jetSource='slimmedJetsAK8',
	jetCorrFactorsSource=cms.VInputTag(cms.InputTag("jetCorrFactorsAK8") ),
)

looseJetIdAK8 = cms.EDProducer("PatJetIDValueMapProducer",
			  filterParams=cms.PSet(
			    version = cms.string('WINTER16'),
			    quality = cms.string('LOOSE'),
			  ),
                          src = cms.InputTag("updatedJetsAK8")
)
tightJetIdAK8 = cms.EDProducer("PatJetIDValueMapProducer",
			  filterParams=cms.PSet(
			    version = cms.string('SUMMER18PUPPI'),
			    quality = cms.string('TIGHT'),
			  ),
                          src = cms.InputTag("updatedJetsAK8")
)
tightJetIdLepVetoAK8 = cms.EDProducer("PatJetIDValueMapProducer",
			  filterParams=cms.PSet(
			    version = cms.string('SUMMER18PUPPI'),
			    quality = cms.string('TIGHTLEPVETO'),
			  ),
                          src = cms.InputTag("updatedJetsAK8")
)
run2_jme_2016.toModify( tightJetIdAK8.filterParams, version = "WINTER16" )
run2_jme_2016.toModify( tightJetIdLepVetoAK8.filterParams, version = "WINTER16" )
run2_jme_2017.toModify( tightJetIdAK8.filterParams, version = "WINTER17PUPPI" )
run2_jme_2017.toModify( tightJetIdLepVetoAK8.filterParams, version = "WINTER17PUPPI" )
for modifier in run2_nanoAOD_106Xv1, run2_nanoAOD_106Xv2, run2_miniAOD_devel:
  modifier.toModify( tightJetIdAK8.filterParams, version = "RUN2ULPUPPI" )
  modifier.toModify( tightJetIdLepVetoAK8.filterParams, version = "RUN2ULPUPPI" )
(run2_jme_2016 & (run2_nanoAOD_106Xv2 | run2_miniAOD_devel)).toModify( tightJetIdAK8.filterParams, version = "RUN2UL16PUPPI" )
(run2_jme_2016 & (run2_nanoAOD_106Xv2 | run2_miniAOD_devel)).toModify( tightJetIdLepVetoAK8.filterParams, version = "RUN2UL16PUPPI" )

updatedJetsAK8WithUserData = cms.EDProducer("PATJetUserDataEmbedder",
     src = cms.InputTag("updatedJetsAK8"),
      userInts = cms.PSet(
        tightId = cms.InputTag("tightJetIdAK8"),
        tightIdLepVeto = cms.InputTag("tightJetIdLepVetoAK8"),
      ),
)
run2_jme_2016.toModify(updatedJetsAK8WithUserData.userInts,
    looseId = cms.InputTag("looseJetIdAK8"),
)

finalJetsAK8 = cms.EDFilter("PATJetRefSelector",
    src = cms.InputTag("updatedJetsAK8WithUserData"),
    cut = cms.string("pt > 170")
)

##################### Tables for final output and docs ##########################

## BOOSTED STUFF #################
fatJetsHto4bTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("finalJetsAK8"),
    cut = cms.string(" pt > 170"), #probably already applied in miniaod
    name = cms.string("FatJet"),
    doc  = cms.string("slimmedJetsAK8, i.e. ak8 fat jets for boosted analysis"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the jets
    variables = cms.PSet(
        ## Debug jet matching when merging NanoAOD output ROOT files
        pt_debug   = Var("pt",  float,doc="Copy of FatJet_pt for debugging",  precision=10),
        eta_debug  = Var("eta", float,doc="Copy of FatJet_eta for debugging", precision=10),
        phi_debug  = Var("phi", float,doc="Copy of FatJet_phi for debugging", precision=10),
        mass_debug = Var("mass",float,doc="Copy of FatJet_mass for debugging",precision=10),
        msoftdrop_debug = Var("groomedMass('SoftDropPuppi')",float, doc="Copy of FatJet_msoftdrop f<or debugging",precision=10),
        ## Confirm identical ParticleNet output when merging ROOT files
        particleNet_mass_debug = Var("bDiscriminator('pfParticleNetMassRegressionJetTags:mass')",float,
                                     doc="Copy of FatJet_particleNet_mass for debugging",precision=10),
        particleNetMD_Xbb_debug = Var("bDiscriminator('pfMassDecorrelatedParticleNetJetTags:probXbb')",float,
                                         doc="Copy of FatJet_particleNetMD_Xbb for debugging",precision=10),
        particleNet_H4qvsQCD_debug = Var("bDiscriminator('pfParticleNetDiscriminatorsJetTags:H4qvsQCD')",float,
                                         doc="Copy of FatJet_particleNet_H4qvsQCD for debugging",precision=10),
        ## New ParticleNet quantities
        particleNet_massH_Hto4b_v0 = Var("bDiscriminator('pfParticleNetHto4bMassRegressionH0JetTags:outputH0')",float,doc="ParticleNet Higgs mass regression for H->aa->bbbb (mass regr, mode 3 - original)",precision=10),
        particleNet_massH_Hto4b_v1 = Var("bDiscriminator('pfParticleNetHto4bMassRegressionH1JetTags:outputH1')",float,doc="ParticleNet Higgs mass regression for H->aa->bbbb (mass regr, mode 3)",precision=10),
        particleNet_massA_Hto4b_v1 = Var("bDiscriminator('pfParticleNetHto4bMassRegressionA1JetTags:outputA1')",float,doc="ParticleNet a boson mass regression for H->aa->bbbb (mass regr, mode 3)",precision=10),
        particleNet_massH_Hto4b_v2 = Var("bDiscriminator('pfParticleNetHto4bMassRegressionH2JetTags:outputH2')",float,doc="ParticleNet Higgs mass regression for H->aa->bbbb (mass regr, mode 0)",precision=10),
        particleNet_massA_Hto4b_v2 = Var("bDiscriminator('pfParticleNetHto4bMassRegressionA2JetTags:outputA2')",float,doc="ParticleNet a boson mass regression for H->aa->bbbb (mass regr, mode 0)",precision=10),
        particleNet_massH_Hto4b_v3 = Var("exp(bDiscriminator('pfParticleNetHto4bMassRegressionH3JetTags:outputH3'))",float,doc="ParticleNet Higgs mass regression for H->aa->bbbb (logMass regr, mode 0)",precision=10),
        particleNet_massA_Hto4b_v3 = Var("exp(bDiscriminator('pfParticleNetHto4bMassRegressionA3JetTags:outputA3'))",float,doc="ParticleNet a boson mass regression for H->aa->bbbb (logMass regr, mode 0)",precision=10),
        particleNet_massH_Hto4b_v4 = Var("mass * bDiscriminator('pfParticleNetHto4bMassRegressionH4JetTags:outputH4')",float,doc="ParticleNet Higgs mass regression for H->aa->bbbb (mass ratio regr, mode 3)",precision=10),
        particleNet_massA_Hto4b_v4 = Var("mass * bDiscriminator('pfParticleNetHto4bMassRegressionA4JetTags:outputA4')",float,doc="ParticleNet a boson mass regression for H->aa->bbbb (mass ratio regr, mode 3)",precision=10),
        particleNetMD_Hto4b_Haa4b = Var("bDiscriminator('pfMassDecorrelatedParticleNetHto4bMJetTags:probHaa4b')",float,doc="Mass-decorrelated multiclass ParticleNet tagger for H->aa->bbbb",precision=10),
        particleNetMD_Hto4b_Haa3b = Var("bDiscriminator('pfMassDecorrelatedParticleNetHto4bMJetTags:probHaa3b')",float,doc="Mass-decorrelated multiclass ParticleNet tagger for H->aa->bbbb",precision=10),
        particleNetMD_Hto4b_Haa2b = Var("bDiscriminator('pfMassDecorrelatedParticleNetHto4bMJetTags:probHaa2b')",float,doc="Mass-decorrelated multiclass ParticleNet tagger for H->aa->bbbb",precision=10),
        particleNetMD_Hto4b_Haa01b = Var("bDiscriminator('pfMassDecorrelatedParticleNetHto4bMJetTags:probHaa01b')",float,doc="Mass-decorrelated multiclass ParticleNet tagger for H->aa->bbbb",precision=10),
        particleNetMD_Hto4b_QCD4b = Var("bDiscriminator('pfMassDecorrelatedParticleNetHto4bMJetTags:probQCD4b')",float,doc="Mass-decorrelated multiclass ParticleNet tagger for H->aa->bbbb",precision=10),
        particleNetMD_Hto4b_QCD3b = Var("bDiscriminator('pfMassDecorrelatedParticleNetHto4bMJetTags:probQCD3b')",float,doc="Mass-decorrelated multiclass ParticleNet tagger for H->aa->bbbb",precision=10),
        particleNetMD_Hto4b_QCD2b = Var("bDiscriminator('pfMassDecorrelatedParticleNetHto4bMJetTags:probQCD2b')",float,doc="Mass-decorrelated multiclass ParticleNet tagger for H->aa->bbbb",precision=10),
        particleNetMD_Hto4b_QCD1b = Var("bDiscriminator('pfMassDecorrelatedParticleNetHto4bMJetTags:probQCD1b')",float,doc="Mass-decorrelated multiclass ParticleNet tagger for H->aa->bbbb",precision=10),
        particleNetMD_Hto4b_QCD0b = Var("bDiscriminator('pfMassDecorrelatedParticleNetHto4bMJetTags:probQCD0b')",float,doc="Mass-decorrelated multiclass ParticleNet tagger for H->aa->bbbb",precision=10),
        particleNetMD_Hto4b_binary_Haa4b = Var("bDiscriminator('pfMassDecorrelatedParticleNetHto4bB1JetTags:probHaa4b')",float,doc="Mass-decorrelated binary ParticleNet tagger for H->aa->bbbb vs. QCD",precision=10),
        particleNetMD_Hto4b_binary_QCD   = Var("bDiscriminator('pfMassDecorrelatedParticleNetHto4bB1JetTags:probQCD')",  float,doc="Mass-decorrelated binary ParticleNet tagger for H->aa->bbbb vs. QCD",precision=10),
        particleNetMD_Hto4b_binaryLF_Haa4b = Var("bDiscriminator('pfMassDecorrelatedParticleNetHto4bB2JetTags:probHaa4b')",float,doc="Mass-decorrelated binary ParticleNet tagger for H->aa->bbbb vs. QCD (<=2 b)",precision=10),
        particleNetMD_Hto4b_binaryLF_QCDlf = Var("bDiscriminator('pfMassDecorrelatedParticleNetHto4bB2JetTags:probQCDlf')",float,doc="Mass-decorrelated binary ParticleNet tagger for H->aa->bbbb vs. QCD (<= 2b)",precision=10),
    )
)

fatJetSequence = cms.Sequence(jetCorrFactorsAK8+updatedJetsAK8+tightJetIdAK8+tightJetIdLepVetoAK8+updatedJetsAK8WithUserData+finalJetsAK8)

_fatJetSequence_2016 = fatJetSequence.copy()
_fatJetSequence_2016.insert(_fatJetSequence_2016.index(tightJetIdAK8), looseJetIdAK8)
run2_jme_2016.toReplaceWith(fatJetSequence, _fatJetSequence_2016)
