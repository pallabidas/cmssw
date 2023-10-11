#!/bin/bash

## Construct the string for samples in DAS (https://cmsweb.cern.ch/das/)
## dataset dataset=/JetHT/Run2018*-UL2018_MiniAODv2_GT36-v1/MINIAOD
## dataset dataset=/SingleMuon/Run2018*-UL2018_MiniAODv2_GT36-v1/MINIAOD
PD="JetHT"
# PD="SingleMuon"
PREF="Run2018"
SUFF="-UL2018_MiniAODv2_GT36-"
OUTD="/store/group/phys_susy/HToaaTo4b/NanoAOD/2018/data/PNet_v1_2023_10_06/"

## Run ./scripts/crab_Data.sh CMD [TST] [OPT1] ... [OPT7]
## Where CMD = 'submit' or 'status',
##   and TST = 'test' for test mode
## See crab/README.md for some typical options, or run
## 'crab --help' for a more complete list, including:
## <<< crab status >>>
## '--verboseErrors' : Additional info on failed jobs
## '--long'   : Lists status of each individual job
## <<< crab resubmit >>> and <<< crab getlog >>>
## '--jobids' : Comma-separated list of job IDs
## <<< crab resubmit >>>
## '--force'  : What it sounds like
## '--maxjobruntime=3000' : Allow job to run for 2 days


CMD=$1
TST=$2
if [ "$TST" != "test" ] && [ "$TST" != "Test" ] && [ "$TST" != "TEST" ]; then
    OPTS="$2 $3 $4 $5 $6 $7 $8"
else
    OPTS="$3 $4 $5 $6 $7 $8 $9"
fi

## Run in "test mode" if 2nd command is "test"
if [ "$TST" != "test" ] && [ "$TST" != "Test" ] && [ "$TST" != "TEST" ]; then
    echo -e "\nGoing to run: 'crab $CMD $OPTS'\n"
else
    echo -e "\nGoing to run: 'crab $CMD $OPTS' (in TEST mode)\n"
fi

## Check to make sure the CRAB command is valid
if [ "$CMD" != "submit" ] && [ "$CMD" != "status" ] && [ "$CMD" != "resubmit" ] && [ "$CMD" != "getlog" ]; then
    echo -e "\n'crab $CMD' not an option! Quitting.\n"
    exit
fi

## Loop over data-taking eras
for IDX in "A" "B" "C" "D"
do
    ERA="${PREF}${IDX}${SUFF}"

    ## Adjust ERA and # of LS depending on dataset and era
    if [ "$PD" = "JetHT" ]; then
	ERA="${ERA}v1"
    	LS="6"
    	if [ "${IDX}" = "D" ]; then
    	    LS="13"
    	fi
    elif  [ "$PD" = "SingleMuon" ]; then
	ERA="${ERA}v2"
    	LS="12"
    	if [ "${IDX}" = "C" ]; then
	    ERA="${ERA}v3"
    	elif [ "${IDX}" = "D" ]; then
    	    LS="52"
    	fi
    fi

    ## <<< *********************************** >>>
    ## <<< ** crab status, resubmit, getlog ** >>>
    ## <<< *********************************** >>>
    if [ "$CMD" = "status" ] || [ "$CMD" = "resubmit" ] || [ "$CMD" = "getlog" ]; then
	echo crab ${CMD} -d crab/r1/crab_${PD}_${ERA} $OPTS
	if [ "$TST" != "test" ] && [ "$TST" != "Test" ] && [ "$TST" != "TEST" ]; then
	    crab ${CMD} -d crab/r1/crab_${PD}_${ERA} $OPTS
	fi
    fi

    ## <<< ***************** >>>
    ## <<< ** crab submit ** >>>
    ## <<< ***************** >>>
    if [ "$CMD" = "submit" ]; then
    	## Create output directory if it doesn't exist
    	if [ ! -d "/eos/cms${OUTD}${ERA}" ]; then
    	    echo mkdir /eos/cms${OUTD}${ERA}
    	    if [ "$TST" != "test" ] && [ "$TST" != "Test" ] && [ "$TST" != "TEST" ]; then
    		mkdir /eos/cms${OUTD}${ERA}
    	    fi
    	fi
    	## Submit crab jobs
    	echo crab submit -c crab/crabConfigData.py $OPTS Data.inputDataset="/${PD}/${ERA}/MINIAOD" General.requestName="${PD}_${ERA}" Data.outLFNDirBase="${OUTD}${ERA}/" config.Data.unitsPerJob="${LS}"
    	if [ "$TST" != "test" ] && [ "$TST" != "Test" ] && [ "$TST" != "TEST" ]; then
    	    crab submit -c crab/crabConfigData.py $OPTS Data.inputDataset="/${PD}/${ERA}/MINIAOD" General.requestName="${PD}_${ERA}" Data.outLFNDirBase="${OUTD}${ERA}/" config.Data.unitsPerJob="${LS}"
    	fi
    fi

done
