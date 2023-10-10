#!/bin/bash

TOP='/eos/cms/store/group/phys_susy/HToaaTo4b/NanoAOD/2018/MC/PNet_v1_2023_10_06/'
MACRO='/afs/cern.ch/work/a/abrinke1/public/HiggsToAA/NanoAOD/crab/2018/CMSSW_10_6_26/src/PhysicsTools/NanoAOD/macros/haddnano.py'

# for MASS in 12 15 20 25 30 35 40 45 50 55 60
# for MASS in 15 20 25 30 35 45 50 55
for MASS in 40
do
    cd ${TOP}SUSY_GluGluH_01J_HToAATo4B_Pt150_M-${MASS}_TuneCP5_13TeV_madgraph_pythia8/r1/
    pwd
    echo "python ${MACRO} PNet_v1.root */0000/PNet_v1_*.root"
    python ${MACRO} PNet_v1.root */0000/PNet_v1_*.root
    cd -
done
