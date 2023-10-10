
### Establish 7-day GRID proxy
```
voms-proxy-init --voms cms --valid 168:00
```

### Scripts for job submission, status, resubmit, and getlog
#### Copy and modify crab_ZJets.sh for MC, crab_JetHT.sh for data
```
scripts/crab_ZJets.sh
scripts/crab_JetHT.sh
```

### Check jobs status
```
crab status -d crab/r1/[dir_name] --verboseErrors
```

### Check for exact failed jobs
```
crab status -d crab/r1/[dir_name] --long | grep "failed"
```

### Get logs for failed jobs
```
crab getlog -d crab/r1/[dir_name] --jobids [job,IDs]
```

### Force resubmit specific failed jobs with longer max runtime
```
crab resubmit -d crab/r1/[dir_name] --force --maxjobruntime=3000 --jobids [job,IDs]
```