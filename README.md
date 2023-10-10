
# SETUP

Following https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/HIG-RunIISummer20UL18NanoAODv9-02146
and https://cmsweb.cern.ch/das/request?instance=prod/global&input=config+dataset%3D%2FJetHT%2FRun2018D-UL2018_MiniAODv2_NanoAODv9_GT36-v1%2FNANOAOD

```
cd /afs/cern.ch/work/a/abrinke1/public/HiggsToAA/NanoAOD/crab/2018/
bash
export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram p CMSSW CMSSW_10_6_30
cd CMSSW_10_6_30/src
exit
```

```
cd /afs/cern.ch/work/a/abrinke1/public/HiggsToAA/NanoAOD/crab/2018/CMSSW_10_6_30/src
cmsenv
scram b -j 6

git cms-addpkg RecoBTag/Combined
git cms-addpkg RecoBTag/ONNXRuntime
git cms-addpkg PhysicsTools/NanoAOD
git cms-addpkg PhysicsTools/PatAlgos
git cms-addpkg DataFormats/PatCandidates
git cms-addpkg CommonTools/RecoAlgos

git clone git@github.com:cms-data/RecoBTag-Combined.git RecoBTag/Combined/data

git remote add abrinke1 ssh://git@gitlab.cern.ch:7999/abrinke1/cmssw.git
git checkout -b HtoAA_PNet_Prod_v1_2023_10_06
git pull abrinke1 HtoAA_PNet_Prod_v1_2023_10_06

cd RecoBtag/Combined/data/
git remote add abrinke1 git@github.com:abrinke1/RecoBTag-Combined.git
git checkout -b HtoAA_PNet_Prod_v1_2023_10_06_slim
git pull abrinke1 HtoAA_PNet_Prod_v1_2023_10_06_slim
cd -

scram b -j 6
```

## Move out some files that interfere with CRAB jobs

```
mkdir ../../crab_big_files
mv RecoBTag/Combined/data/.git/objects/pack/pack*.pack ../../crab_big_files/
mkdir -p ../../crab_big_files/CMSSW_10_6_30/ParticleNetAK8/General/V01/
mkdir -p ../../crab_big_files/CMSSW_10_6_30/ParticleNetAK8/MD-2prong/V01/
mkdir -p ../../crab_big_files/CMSSW_10_6_30/ParticleNetAK8/MassRegression/V01/
mv RecoBTag/Combined/data/ParticleNetAK8/General/V01/modelfile ../../crab_big_files/CMSSW_10_6_30/ParticleNetAK8/General/V01/
mv RecoBTag/Combined/data/ParticleNetAK8/MD-2prong/V01/modelfile ../../crab_big_files/CMSSW_10_6_30/ParticleNetAK8/MD-2prong/V01/
mv RecoBTag/Combined/data/ParticleNetAK8/MassRegression/V01/modelfile ../../crab_big_files/CMSSW_10_6_30/ParticleNetAK8/MassRegression/V01/
```

# RUNNING

```
cd /afs/cern.ch/work/a/abrinke1/public/HiggsToAA/NanoAOD/crab/2018/CMSSW_10_6_30/src/PhysicsTools/NanoAOD/
cmsenv
voms-proxy-init --voms cms --valid 168:00
```

## Default cfg file to generate NANOEDMAODSIM from MC
```
cmsDriver.py --python_filename HIG-RunIISummer20UL18NanoAODv9-02146_1_cfg.py --eventcontent NANOEDMAODSIM --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL18NanoAODv9-02146.root --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --filein "file:/eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/MC/SUSY_GluGluH_01J_HToAATo4B_Pt350_mH-70_mA-12_wH-70_wA-70_TuneCP5_13TeV_madgraph_pythia8/RunIISummer20UL18/10300/MiniAODv2_10312.root" --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --mc -n 100
cmsRun HIG-RunIISummer20UL18NanoAODv9-02146_1_cfg.py
```

## Default cfg file to generate NANOAOD from data
```
cmsDriver.py --python_filename JetHT-RunIISummer20UL18NanoAODv9_cfg.py --eventcontent NANOAOD --datatier NANOAOD --fileout file:JetHT-RunIISummer20UL18NanoAODv9.root --conditions 106X_dataRun2_v36 --step NANO --filein "file:/eos/cms/store/group/phys_susy/HToaaTo4b/MiniAOD/2018/data/JetHT/Run2018C-UL2018_MiniAODv2_GT36-v1/00286796-4A86-AD46-B017-149AEB39EC10.root" --era Run2_2018,run2_nanoAOD_106Xv2 --no_exec --data -n 100
```

# ADD NEW PARTICLENET MODELS
Start from `RecoBTag/ONNXRuntime/python/pfParticleNet_cff.py`

## Useful resource - Si's modifications
[https://github.com/cms-sw/cmssw/compare/cms-sw:cmssw:CMSSW_10_6_X...chosila:cmssw:addhtoaapnet](https://github.com/cms-sw/cmssw/compare/cms-sw:cmssw:CMSSW_10_6_X...chosila:cmssw:addhtoaapnet)
