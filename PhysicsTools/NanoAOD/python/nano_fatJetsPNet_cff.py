from __future__ import print_function
import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.NanoAOD.nano_eras_cff import *
from PhysicsTools.NanoAOD.fatJetsPNet_cff import *
from PhysicsTools.NanoAOD.vertices_cff import *
from PhysicsTools.NanoAOD.NanoAODEDMEventContent_cff import *

nanoMetadata = cms.EDProducer("UniqueStringProducer",
    strings = cms.PSet(
        tag = cms.string("untagged"),
    )
)

nanoSequenceCommon = cms.Sequence(
    nanoMetadata + fatJetSequence + fatJetsPNetTable )


from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppiesFromMiniAOD

def nanoAOD_addDeepInfoAK8(process, addParticleNet, addParticleNetMass, jecPayload):
    _btagDiscriminators=[]
    if addParticleNet:
        print("Updating process to run ParticleNet before it's included in MiniAOD")
        from RecoBTag.ONNXRuntime.pfParticleNet_cff import _pfParticleNetJetTagsAll as pfParticleNetJetTagsAll
        _btagDiscriminators += pfParticleNetJetTagsAll
    if addParticleNetMass:
        from RecoBTag.ONNXRuntime.pfParticleNet_cff import _pfParticleNetMassRegressionAll as pfParticleNetMassRegressionAll
        _btagDiscriminators += pfParticleNetMassRegressionAll
    if len(_btagDiscriminators)==0: return process
    print("Will recalculate the following discriminators on AK8 jets: "+", ".join(_btagDiscriminators))
    updateJetCollection(
       process,
       jetSource = cms.InputTag('slimmedJetsAK8'),
       pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
       svSource = cms.InputTag('slimmedSecondaryVertices'),
       rParam = 0.8,
       jetCorrections = (jecPayload.value(), cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None'),
       btagDiscriminators = _btagDiscriminators,
       postfix='AK8WithDeepInfo',
       printWarning = False
       )
    process.jetCorrFactorsAK8.src="selectedUpdatedPatJetsAK8WithDeepInfo"
    process.updatedJetsAK8.jetSource="selectedUpdatedPatJetsAK8WithDeepInfo"
    return process

def nanoAOD_customizeCommon(process):
    makePuppiesFromMiniAOD(process,True)
    process.puppiNoLep.useExistingWeights = True
    process.puppi.useExistingWeights = True
    run2_nanoAOD_106Xv1.toModify(process.puppiNoLep, useExistingWeights = False)
    run2_nanoAOD_106Xv1.toModify(process.puppi, useExistingWeights = False)

    nanoAOD_addDeepInfoAK8_switch = cms.PSet(
        nanoAOD_addParticleNet_switch = cms.untracked.bool(True),
        nanoAOD_addParticleNetMass_switch = cms.untracked.bool(True),
        jecPayload = cms.untracked.string('AK8PFPuppi')
        )
    # Don't run on old mini due to compatibility
    # 80X contains ak8PFJetsCHS jets instead of puppi
    run2_miniAOD_80XLegacy.toModify(nanoAOD_addDeepInfoAK8_switch,
                                    nanoAOD_addParticleNet_switch = False,
                                    nanoAOD_addParticleNetMass_switch = False,
                                    jecPayload = 'AK8PFchs')
    process = nanoAOD_addDeepInfoAK8(process,
                                     addParticleNet=nanoAOD_addDeepInfoAK8_switch.nanoAOD_addParticleNet_switch,
                                     addParticleNetMass=nanoAOD_addDeepInfoAK8_switch.nanoAOD_addParticleNetMass_switch,
                                     jecPayload=nanoAOD_addDeepInfoAK8_switch.jecPayload)
    return process

def nanoAOD_customizeData(process):
    process = nanoAOD_customizeCommon(process)
    return process

def nanoAOD_customizeMC(process):
    process = nanoAOD_customizeCommon(process)
    return process

### Era dependent customization
_80x_sequence = nanoSequenceCommon.copy()

run2_miniAOD_80XLegacy.toReplaceWith( nanoSequenceCommon, _80x_sequence)

_102x_sequence = nanoSequenceCommon.copy()

for modifier in run2_nanoAOD_94XMiniAODv1, run2_nanoAOD_94XMiniAODv2, run2_nanoAOD_102Xv1:
    modifier.toReplaceWith(nanoSequenceCommon, _102x_sequence)
