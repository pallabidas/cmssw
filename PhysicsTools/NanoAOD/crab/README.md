
## Establish 7-day GRID proxy
voms-proxy-init --voms cms --valid 168:00

## Check jobs status
crab status -d crab/r1/[dir_name] --verboseErrors

## Check for exact failed jobs
crab status -d crab/r1/[dir_name] --long | grep "failed"

## Get logs for failed jobs
crab getlog -d crab/r1/[dir_name] --jobids [job,IDs]

## Force resubmit specific failed jobs with longer max runtime
crab resubmit -d crab/r1/[dir_name] --force --maxjobruntime=3000 --jobids [job,IDs]
