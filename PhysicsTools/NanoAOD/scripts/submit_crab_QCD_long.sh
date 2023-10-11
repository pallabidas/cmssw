#!/bin/bash

for SAMP in "/QCD_HT100to200_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" "/QCD_HT200to300_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM"
do
    ## First split full path name to find sample name
    IFS='/'  ## Forward slash (/) is set as bash delimiter
    read -ra ADDR <<< "$SAMP"
    declare -i n=0  ## Count sub-string of the full path name 
    for SUB in "${ADDR[@]}"
    do
	n=$((n+1))  ## Iterate count
	if [ $n -eq 2 ]; then  ## Sample name is 2nd sub-string
	    IFS=' '  ## Set IFS back to default space
	    echo ""
	    echo crab submit -c crab/crabConfigMC.py Data.inputDataset=$SAMP General.requestName=$SUB JobType.maxJobRuntimeMin=3000 Data.splitting="FileBased" Data.unitsPerJob=1
	    echo ""
	    crab submit -c crab/crabConfigMC.py Data.inputDataset=$SAMP General.requestName=$SUB JobType.maxJobRuntimeMin=3000 Data.splitting="FileBased" Data.unitsPerJob=1
	    echo ""
	    break  ## We're all done now! On to the next sample
	fi
    done
    # break  ## Skip out early for testing
done
