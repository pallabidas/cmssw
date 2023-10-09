from __future__ import print_function
import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.NanoAOD.nano_eras_cff import *
from PhysicsTools.NanoAOD.fatJetsHto4b_cff import *
from PhysicsTools.NanoAOD.vertices_cff import *
from PhysicsTools.NanoAOD.NanoAODEDMEventContent_cff import *

nanoMetadata = cms.EDProducer("UniqueStringProducer",
    strings = cms.PSet(
        tag = cms.string("untagged"),
    )
)

nanoSequenceCommon = cms.Sequence(
    nanoMetadata + fatJetSequence + fatJetsHto4bTable )


from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppiesFromMiniAOD

def nanoAOD_addDeepInfoAK8(process):
    _btagDiscriminators=[]

    print("\n*** Updating process to re-run ParticleNet before it's included in MiniAOD ***\n")

    from RecoBTag.ONNXRuntime.pfParticleNet_cff import _pfMassDecorrelatedParticleNetHto4bJetTagsProbs as Hto4bTags
    _btagDiscriminators += ( ['pfMassDecorrelatedParticleNetJetTags:probXbb'] + \
                             ['pfParticleNetDiscriminatorsJetTags:H4qvsQCD']  + \
                             Hto4bTags )

    from RecoBTag.ONNXRuntime.pfParticleNet_cff import _pfParticleNetHto4bMassRegressionOutputs as Hto4bMass

    _btagDiscriminators += ( ['pfParticleNetMassRegressionJetTags:mass'] + \
                             Hto4bMass )

    if len(_btagDiscriminators)==0: return process
    print("Will recalculate the following discriminators on AK8 jets: "+", ".join(_btagDiscriminators))
    updateJetCollection(
       process,
       jetSource = cms.InputTag('slimmedJetsAK8'),
       pvSource = cms.InputTag('offlineSlimmedPrimaryVertices'),
       svSource = cms.InputTag('slimmedSecondaryVertices'),
       rParam = 0.8,
       jetCorrections = ( cms.untracked.string('AK8PFPuppi').value(),
                          cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']),
                          'None' ),
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
    process = nanoAOD_addDeepInfoAK8(process)
    return process

### Era dependent customization
_80x_sequence = nanoSequenceCommon.copy()

run2_miniAOD_80XLegacy.toReplaceWith( nanoSequenceCommon, _80x_sequence)

_102x_sequence = nanoSequenceCommon.copy()

for modifier in run2_nanoAOD_94XMiniAODv1, run2_nanoAOD_94XMiniAODv2, run2_nanoAOD_102Xv1:
    modifier.toReplaceWith(nanoSequenceCommon, _102x_sequence)
