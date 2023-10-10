#!/bin/bash

# for MASS in 15 20 25 30 35 40 45 50 55 60
for MASS in 15 40
do
    echo "crab status -d crab/r1/crab_SUSY_GluGluH_01J_HToAATo4B_Pt150_M-${MASS}_TuneCP5_13TeV_madgraph_pythia8"
    crab status -d crab/r1/crab_SUSY_GluGluH_01J_HToAATo4B_Pt150_M-${MASS}_TuneCP5_13TeV_madgraph_pythia8
done

# for MASS in 15 40
# do
#     echo "crab resubmit -d crab/r1/crab_SUSY_GluGluH_01J_HToAATo4B_Pt150_M-${MASS}_TuneCP5_13TeV_madgraph_pythia8"
#     crab resubmit -d crab/r1/crab_SUSY_GluGluH_01J_HToAATo4B_Pt150_M-${MASS}_TuneCP5_13TeV_madgraph_pythia8
# done
