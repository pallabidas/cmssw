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

pfMassDecorrelatedParticleNetHto4bMJetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/MD-Hto4b/V01/preprocess_multiclass_wH-70_E30_AWB_2023_08_31_v12.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/MD-Hto4b/V01/multiclass_wH-70_E30_AWB_2023_08_31_v12.onnx',
    flav_names = ["probHaa4b", "probHaa3b", "probHaa2b", "probHaa01b",
                  "probQCD4b", "probQCD3b", "probQCD2b", "probQCD1b", "probQCD0b"],
)

pfMassDecorrelatedParticleNetHto4bB1JetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/MD-Hto4b/V01/preprocess_binary_wH-70_E30_AWB_2023_08_31_v12.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/MD-Hto4b/V01/binary_wH-70_E30_AWB_2023_08_31_v12.onnx',
    flav_names = ["probHaa4b", "probQCD"],
)

pfMassDecorrelatedParticleNetHto4bB2JetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/MD-Hto4b/V01/preprocess_binaryLF_wH-70_E30_AWB_2023_08_31_v12.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/MD-Hto4b/V01/binaryLF_wH-70_E30_AWB_2023_08_31_v12.onnx',
    flav_names = ["probHaa4b", "probQCDlf"],
)

pfParticleNetMassRegressionJetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/MassRegression/V01/preprocess.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/MassRegression/V01/particle-net.onnx',
    flav_names = ["mass"],
)

pfParticleNetHto4bMassRegressionH0JetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionH/V01/preprocess_wide_H_calc_mass_regr_loss3_Si_2023_08_31_v12_orig.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionH/V01/wide_H_calc_mass_regr_loss3_Si_2023_08_31_v12_orig.onnx',
    flav_names = ["outputH0"],
)

pfParticleNetHto4bMassRegressionH1JetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionH/V01/preprocess_wide_H_calc_mass_regr_loss3_Si_2023_08_31_v12.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionH/V01/wide_H_calc_mass_regr_loss3_Si_2023_08_31_v12.onnx',
    flav_names = ["outputH1"],
)

pfParticleNetHto4bMassRegressionH2JetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionH/V01/preprocess_wide_H_calc_mass_regr_loss0_Si_2023_08_31_v12.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionH/V01/wide_H_calc_mass_regr_loss0_Si_2023_08_31_v12.onnx',
    flav_names = ["outputH2"],
)

pfParticleNetHto4bMassRegressionH3JetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionH/V01/preprocess_wide_H_calc_logMass_regr_loss0_Si_2023_08_31_v12.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionH/V01/wide_H_calc_logMass_regr_loss0_Si_2023_08_31_v12.onnx',
    flav_names = ["outputH3"],
)

pfParticleNetHto4bMassRegressionH4JetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionH/V01/preprocess_wide_H_calc_massOverfj_mass_regr_loss3_Si_2023_08_31_v12.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionH/V01/wide_H_calc_massOverfj_mass_regr_loss3_Si_2023_08_31_v12.onnx',
    flav_names = ["outputH4"],
)

pfParticleNetHto4bMassRegressionA1JetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionA/V01/preprocess_MA-regr_mass_mode3_mH-125_E40_AWB_2023_08_31_v12.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionA/V01/MA-regr_mass_mode3_mH-125_E40_AWB_2023_08_31_v12.onnx',
    flav_names = ["outputA1"],
)

pfParticleNetHto4bMassRegressionA2JetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionA/V01/preprocess_MA-regr_mass_mode0_mH-125_E40_AWB_2023_08_31_v12.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionA/V01/MA-regr_mass_mode0_mH-125_E40_AWB_2023_08_31_v12.onnx',
    flav_names = ["outputA2"],
)

pfParticleNetHto4bMassRegressionA3JetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionA/V01/preprocess_MA-regr_log_mode0_mH-125_E40_AWB_2023_08_31_v12.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionA/V01/MA-regr_log_mode0_mH-125_E40_AWB_2023_08_31_v12.onnx',
    flav_names = ["outputA3"],
)

pfParticleNetHto4bMassRegressionA4JetTags = boostedJetONNXJetTagsProducer.clone(
    src = 'pfParticleNetTagInfos',
    preprocess_json = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionA/V01/preprocess_MA-regr_ratio_mode3_mH-125_E40_AWB_2023_08_31_v12.json',
    model_path = 'RecoBTag/Combined/data/ParticleNetAK8/Hto4bMassRegressionA/V01/MA-regr_ratio_mode3_mH-125_E40_AWB_2023_08_31_v12.onnx',
    flav_names = ["outputA4"],
)


from CommonTools.PileupAlgos.Puppi_cff import puppi
from PhysicsTools.PatAlgos.slimming.primaryVertexAssociation_cfi import primaryVertexAssociation

# This task is not used, useful only if we run it from RECO jets (RECO/AOD)
pfParticleNetTask = cms.Task(puppi, primaryVertexAssociation, pfParticleNetTagInfos,
                             pfParticleNetJetTags, pfMassDecorrelatedParticleNetJetTags, pfParticleNetMassRegressionJetTags,
                             pfMassDecorrelatedParticleNetHto4bMJetTags,
                             pfMassDecorrelatedParticleNetHto4bB1JetTags,
                             pfMassDecorrelatedParticleNetHto4bB2JetTags,
                             pfParticleNetHto4bMassRegressionH0JetTags,
                             pfParticleNetHto4bMassRegressionH1JetTags,
                             pfParticleNetHto4bMassRegressionH2JetTags,
                             pfParticleNetHto4bMassRegressionH3JetTags,
                             pfParticleNetHto4bMassRegressionH4JetTags,
                             pfParticleNetHto4bMassRegressionA1JetTags,
                             pfParticleNetHto4bMassRegressionA2JetTags,
                             pfParticleNetHto4bMassRegressionA3JetTags,
                             pfParticleNetHto4bMassRegressionA4JetTags,
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
_pfMassDecorrelatedParticleNetHto4bJetTagsProbs = ['pfMassDecorrelatedParticleNetHto4bMJetTags:' + flav_name
                                                   for flav_name in pfMassDecorrelatedParticleNetHto4bMJetTags.flav_names] + \
                                                  ['pfMassDecorrelatedParticleNetHto4bB1JetTags:' + flav_name
                                                   for flav_name in pfMassDecorrelatedParticleNetHto4bB1JetTags.flav_names] + \
                                                  ['pfMassDecorrelatedParticleNetHto4bB2JetTags:' + flav_name
                                                   for flav_name in pfMassDecorrelatedParticleNetHto4bB2JetTags.flav_names]

_pfParticleNetMassRegressionOutputs = ['pfParticleNetMassRegressionJetTags:' + flav_name
                                       for flav_name in pfParticleNetMassRegressionJetTags.flav_names]

_pfParticleNetHto4bMassRegressionOutputs = ['pfParticleNetHto4bMassRegressionH0JetTags:' + flav_name
                                            for flav_name in pfParticleNetHto4bMassRegressionH0JetTags.flav_names] + \
                                           ['pfParticleNetHto4bMassRegressionH1JetTags:' + flav_name
                                            for flav_name in pfParticleNetHto4bMassRegressionH1JetTags.flav_names] + \
                                           ['pfParticleNetHto4bMassRegressionH2JetTags:' + flav_name
                                            for flav_name in pfParticleNetHto4bMassRegressionH2JetTags.flav_names] + \
                                           ['pfParticleNetHto4bMassRegressionH3JetTags:' + flav_name
                                            for flav_name in pfParticleNetHto4bMassRegressionH3JetTags.flav_names] + \
                                           ['pfParticleNetHto4bMassRegressionH4JetTags:' + flav_name
                                            for flav_name in pfParticleNetHto4bMassRegressionH4JetTags.flav_names] + \
                                           ['pfParticleNetHto4bMassRegressionA1JetTags:' + flav_name
                                            for flav_name in pfParticleNetHto4bMassRegressionA1JetTags.flav_names] + \
                                           ['pfParticleNetHto4bMassRegressionA2JetTags:' + flav_name
                                            for flav_name in pfParticleNetHto4bMassRegressionA2JetTags.flav_names] + \
                                           ['pfParticleNetHto4bMassRegressionA3JetTags:' + flav_name
                                            for flav_name in pfParticleNetHto4bMassRegressionA3JetTags.flav_names] + \
                                           ['pfParticleNetHto4bMassRegressionA4JetTags:' + flav_name
                                            for flav_name in pfParticleNetHto4bMassRegressionA4JetTags.flav_names]

_pfParticleNetJetTagsAll = _pfParticleNetJetTagsProbs + _pfParticleNetJetTagsMetaDiscrs + \
                           _pfMassDecorrelatedParticleNetJetTagsProbs + _pfMassDecorrelatedParticleNetJetTagsMetaDiscrs + \
                           _pfMassDecorrelatedParticleNetHto4bJetTagsProbs

_pfParticleNetMassRegressionAll = _pfParticleNetMassRegressionOutputs + \
                                  _pfParticleNetHto4bMassRegressionOutputs
