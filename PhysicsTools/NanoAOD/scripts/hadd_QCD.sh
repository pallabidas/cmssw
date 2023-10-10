#!/bin/bash

TOP='/eos/cms/store/group/phys_susy/HToaaTo4b/NanoAOD/2018/MC/PNet_v1_2023_10_06/'
SUFF='_13TeV-madgraph-pythia8'
MACRO='/afs/cern.ch/work/a/abrinke1/public/HiggsToAA/NanoAOD/crab/2018/CMSSW_10_6_26/src/PhysicsTools/NanoAOD/macros/haddnano.py'

#127M ${TOP}QCD_bEnriched_HT100to200_TuneCP5${SUFF} +
#375M ${TOP}QCD_HT100to200_TuneCP5_PSWeights${SUFF} +
#378M ${TOP}QCD_bEnriched_HT200to300_TuneCP5${SUFF} +
#798M ${TOP}QCD_HT200to300_BGenFilter_TuneCP5${SUFF} ++
#1.2G ${TOP}QCD_HT100to200_BGenFilter_TuneCP5${SUFF} +
#1.3G ${TOP}QCD_HT200to300_TuneCP5_PSWeights${SUFF} +

# # for SAMP in 'QCD_bEnriched_HT100to200_TuneCP5' 'QCD_HT100to200_TuneCP5_PSWeights' 'QCD_bEnriched_HT200to300_TuneCP5' 'QCD_HT100to200_BGenFilter_TuneCP5' 'QCD_HT200to300_TuneCP5_PSWeights'
# for SAMP in 'QCD_HT200to300_BGenFilter_TuneCP5'
# do
#     cd ${TOP}${SAMP}${SUFF}/r1/
#     pwd
#     echo "python ${MACRO} PNet_v1.root */0000/PNet_v1_*.root"
#     python ${MACRO} PNet_v1.root */0000/PNet_v1_*.root
#     cd -
# done

# #4.1G ${TOP}QCD_bEnriched_HT1000to1500_TuneCP5${SUFF}
# #4.4G ${TOP}QCD_HT1500to2000_BGenFilter_TuneCP5${SUFF} +
# #4.7G ${TOP}QCD_HT2000toInf_BGenFilter_TuneCP5${SUFF}
# #4.7G ${TOP}QCD_bEnriched_HT2000toInf_TuneCP5${SUFF} +
# #5.0G ${TOP}QCD_bEnriched_HT1500to2000_TuneCP5${SUFF} +
# #5.2G ${TOP}QCD_HT1000to1500_BGenFilter_TuneCP5${SUFF}
# #5.8G ${TOP}QCD_bEnriched_HT700to1000_TuneCP5${SUFF} +

# for SAMP in 'QCD_HT1500to2000_BGenFilter_TuneCP5' 'QCD_bEnriched_HT2000toInf_TuneCP5' 'QCD_bEnriched_HT1500to2000_TuneCP5' 'QCD_bEnriched_HT700to1000_TuneCP5'
# do
#     cd ${TOP}${SAMP}${SUFF}/r1/
#     pwd
#     for IDX in {0..4}
#     do
# 	declare -i JOBA=$IDX*2
# 	declare -i JOBB=$JOBA+1
# 	echo "python ${MACRO} PNet_v1_${JOBA}_${JOBB}.root */0000/PNet_v1_*${JOBA}.root */0000/PNet_v1_*${JOBB}.root"
# 	python ${MACRO} PNet_v1_${JOBA}_${JOBB}.root */0000/PNet_v1_*${JOBA}.root */0000/PNet_v1_*${JOBB}.root
#     done
#     cd -
# done

# #14G  ${TOP}QCD_HT300to500_BGenFilter_TuneCP5${SUFF} +
# #17G  ${TOP}QCD_bEnriched_HT300to500_TuneCP5${SUFF}  (2)
# #19G  ${TOP}QCD_HT2000toInf_TuneCP5_PSWeights${SUFF}
# #22G  ${TOP}QCD_HT500to700_BGenFilter_TuneCP5${SUFF}  (2)
# #24G  ${TOP}QCD_bEnriched_HT500to700_TuneCP5${SUFF} +
# #31G  ${TOP}QCD_HT1500to2000_TuneCP5_PSWeights${SUFF}  (3)
# #46G  ${TOP}QCD_HT1000to1500_TuneCP5_PSWeights${SUFF} + (2)
# #59G  ${TOP}QCD_HT300to500_TuneCP5_PSWeights${SUFF} (3)
# #130G ${TOP}QCD_HT500to700_TuneCP5_PSWeights${SUFF}  (6)
# #139G ${TOP}QCD_HT700to1000_TuneCP5_PSWeights${SUFF} ++  (9)

# for SAMP in 'QCD_HT300to500_BGenFilter_TuneCP5' 'QCD_bEnriched_HT500to700_TuneCP5' 'QCD_HT1000to1500_TuneCP5_PSWeights'
for SAMP in 'QCD_HT700to1000_TuneCP5_PSWeights'
do
    cd ${TOP}${SAMP}${SUFF}/r1/
    pwd
    for DIR in {0..8}
    do
	# for JOB in {0..9}
	# do
	#     echo "python ${MACRO} PNet_v1_${DIR}-${JOB}.root */000${DIR}/PNet_v1_*${JOB}.root"
	#     python ${MACRO} PNet_v1_${DIR}-${JOB}.root */000${DIR}/PNet_v1_*${JOB}.root
	# done

	for IDX in {0..4}
	do
	    declare -i JOBA=$IDX*2
	    declare -i JOBB=$JOBA+1
	    echo "python ${MACRO} PNet_v1_${DIR}-${JOBA}_${JOBB}.root */000${DIR}/PNet_v1_*${JOBA}.root */000${DIR}/PNet_v1_*${JOBB}.root"
	    python ${MACRO} PNet_v1_${DIR}-${JOBA}_${JOBB}.root */000${DIR}/PNet_v1_*${JOBA}.root */000${DIR}/PNet_v1_*${JOBB}.root
	done

    done
    cd -
done
