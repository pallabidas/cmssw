import FWCore.ParameterSet.Config as cms

from RecoBTag.FeatureTools.pfDeepBoostedJetTagInfos_cfi import pfDeepBoostedJetTagInfos
from RecoBTag.ONNXRuntime.boostedJetONNXJetTagsProducer_cfi import boostedJetONNXJetTagsProducer
from RecoBTag.ONNXRuntime.pfParticleNetDiscriminatorsJetTags_cfi import pfParticleNetDiscriminatorsJetTags
from RecoBTag.ONNXRuntime.pfMassDecorrelatedParticleNetDiscriminatorsJetTags_cfi import pfMassDecorrelatedParticleNetDiscriminatorsJetTags

pfParticleNetTagInfos = pfDeepBoostedJetTagInfos.clone(
    use_puppiP4 = False
)

pfParticleNetJetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/General/V01/preprocess.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/General/V01/particle-net.onnx',
    flav_names = ["probTbcq",  "probTbqq",  "probTbc",   "probTbq",  "probTbel", "probTbmu", "probTbta",
                  "probWcq",   "probWqq",   "probZbb",   "probZcc",  "probZqq",  "probHbb", "probHcc",
                  "probHqqqq", "probQCDbb", "probQCDcc", "probQCDb", "probQCDc", "probQCDothers"],
)

pfMassDecorrelatedParticleNetJetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/MD-2prong/V01/preprocess.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/MD-2prong/V01/particle-net.onnx',
    flav_names = ["probXbb", "probXcc", "probXqq", "probQCDbb", "probQCDcc",
                  "probQCDb", "probQCDc", "probQCDothers"],
)

# pfMassDecorrelatedParticleNetHto4bJetTags = pfMassDecorrelatedParticleNetJetTags
pfMassDecorrelatedParticleNetHto4bJetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/MD-Hto4b/V01/preprocess_multiclass_wH-70_E02_AWB_2023_08_31_v12.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/MD-Hto4b/V01/multiclass_wH-70_E02_AWB_2023_08_31_v12.onnx',
    flav_names = ["probHaa4b", "probHaa3b", "probHaa2b", "probHaa01b",
                  "probQCD4b", "probQCD3b", "probQCD2b", "probQCD1b", "probQCD0b"],
)

pfParticleNetMassRegressionJetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/MassRegression/V01/preprocess.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/MassRegression/V01/particle-net.onnx',
    flav_names = ["mass"],
)

pfParticleNetHto4bMassRegressionHJetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionH/V01/preprocess_wide_H_calc_mass_regr_Si_2023_08_30_v12.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionH/V01/wide_H_calc_mass_regr_Si_2023_08_30_v12.onnx',
    flav_names = ["output"],
)

pfParticleNetHto4bMassRegressionAJetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionH/V01/preprocess_wide_H_calc_mass_regr_Si_2023_08_30_v12.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionH/V01/wide_H_calc_mass_regr_Si_2023_08_30_v12.onnx',
    flav_names = ["output"],
)

from CommonTools.PileupAlgos.Puppi_cff import puppi
from PhysicsTools.PatAlgos.slimming.primaryVertexAssociation_cfi import primaryVertexAssociation

# This task is not used, useful only if we run it from RECO jets (RECO/AOD)
pfParticleNetTask = cms.Task(puppi, primaryVertexAssociation, pfParticleNetTagInfos,
                             pfParticleNetJetTags, pfMassDecorrelatedParticleNetJetTags, pfParticleNetMassRegressionJetTags,
                             pfMassDecorrelatedParticleNetHto4bJetTags,
                             pfParticleNetHto4bMassRegressionHJetTags, pfParticleNetHto4bMassRegressionAJetTags,
                             pfParticleNetDiscriminatorsJetTags, pfMassDecorrelatedParticleNetDiscriminatorsJetTags)

# declare all the discriminators
# nominal: probs
_pfParticleNetJetTagsProbs = ['pfParticleNetJetTags:' + flav_name
                              for flav_name in pfParticleNetJetTags.flav_names]
# nominal: meta-taggers
_pfParticleNetJetTagsMetaDiscrs = ['pfParticleNetDiscriminatorsJetTags:' + disc.name.value()
                                   for disc in pfParticleNetDiscriminatorsJetTags.discriminators]
# mass-decorrelated: probs
_pfMassDecorrelatedParticleNetJetTagsProbs = ['pfMassDecorrelatedParticleNetJetTags:' + flav_name
                              for flav_name in pfMassDecorrelatedParticleNetJetTags.flav_names]
# mass-decorrelated: meta-taggers
_pfMassDecorrelatedParticleNetJetTagsMetaDiscrs = ['pfMassDecorrelatedParticleNetDiscriminatorsJetTags:' + disc.name.value()
                                   for disc in pfMassDecorrelatedParticleNetDiscriminatorsJetTags.discriminators]
# mass-decorrelated: H->aa->4b tagger
_pfMassDecorrelatedParticleNetHto4bJetTagsProbs = ['pfMassDecorrelatedParticleNetHto4bJetTags:' + flav_name
                                                   for flav_name in pfMassDecorrelatedParticleNetHto4bJetTags.flav_names]

_pfParticleNetMassRegressionOutputs = ['pfParticleNetMassRegressionJetTags:' + flav_name
                                       for flav_name in pfParticleNetMassRegressionJetTags.flav_names]

_pfParticleNetHto4bMassRegressionHOutputs = ['pfParticleNetHto4bMassRegressionHJetTags:' + flav_name
                                             for flav_name in pfParticleNetHto4bMassRegressionHJetTags.flav_names]

_pfParticleNetHto4bMassRegressionAOutputs = ['pfParticleNetHto4bMassRegressionAJetTags:' + flav_name
                                             for flav_name in pfParticleNetHto4bMassRegressionAJetTags.flav_names]

_pfParticleNetJetTagsAll = _pfParticleNetJetTagsProbs + _pfParticleNetJetTagsMetaDiscrs + \
                           _pfMassDecorrelatedParticleNetJetTagsProbs + _pfMassDecorrelatedParticleNetJetTagsMetaDiscrs + \
                           _pfMassDecorrelatedParticleNetHto4bJetTagsProbs

_pfParticleNetMassRegressionAll = _pfParticleNetMassRegressionOutputs + \
                                  _pfParticleNetHto4bMassRegressionHOutputs + \
                                  _pfParticleNetHto4bMassRegressionAOutputs
