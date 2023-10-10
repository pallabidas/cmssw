#!/bin/bash

## Run ./scripts/crab_ZJets.sh CMD [TST] [OPT1] ... [OPT7]
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

## Construct the string for ZJetsToQQ samples in DAS (https://cmsweb.cern.ch/das/)
## dataset dataset=/ZJetsToQQ_HT-*to*_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16*/MINIAODSIM
PREF="ZJetsToQQ_HT-"
SUFF="_TuneCP5_13TeV-madgraphMLM-pythia8"
PROC="RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM"
OUTD="/store/group/phys_susy/HToaaTo4b/NanoAOD/2018/MC/PNet_v1_2023_10_06/"

## Loop over HT ranges
for HT in "800toInf" "600to800" "400to600" "200to400"
do

    ## <<< *********************************** >>>
    ## <<< ** crab status, resubmit, getlog ** >>>
    ## <<< *********************************** >>>
    if [ "$CMD" = "status" ] || [ "$CMD" = "resubmit" ] || [ "$CMD" = "getlog" ]; then
	echo crab ${CMD} -d crab/r1/crab_${PREF}${HT}${SUFF} $OPTS
	if [ "$TST" != "test" ] && [ "$TST" != "Test" ] && [ "$TST" != "TEST" ]; then
	    crab ${CMD} -d crab/r1/crab_${PREF}${HT}${SUFF} $OPTS
	fi
    fi

    ## <<< ***************** >>>
    ## <<< ** crab submit ** >>>
    ## <<< ***************** >>>
    if [ "$CMD" = "submit" ]; then
	## Create output directory if it doesn't exist
	if [ ! -d "/eos/cms${OUTD}" ]; then
            echo mkdir /eos/cms${OUTD}
            if [ "$TST" != "test" ] && [ "$TST" != "Test" ] && [ "$TST" != "TEST" ]; then
		mkdir /eos/cms${OUTD}
            fi
	fi
	## Submit crab jobs
	echo crab submit -c crab/crabConfigMC.py $OPTS Data.inputDataset="/${PREF}${HT}${SUFF}/${PROC}" General.requestName="${PREF}${HT}${SUFF}"
	if [ "$TST" != "test" ] && [ "$TST" != "Test" ] && [ "$TST" != "TEST" ]; then
	    crab submit -c crab/crabConfigMC.py $OPTS Data.inputDataset="/${PREF}${HT}${SUFF}/${PROC}" General.requestName="${PREF}${HT}${SUFF}"
	fi
    fi

done
