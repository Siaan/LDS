#!/bin/bash
## Get the path to this function:

execpath="$0"
echo $execpath
scriptpath="$neurocaasrootdir/ncap_utils"

## Import functions for workflow management
source "$scriptpath/workflow.sh"
## Import functions for data transfer
source "$scriptpath/transfer.sh"


errorlog
errorlog_init

## Set up STDOUT and STDERR Monitoring:
errorlog_background &
background_pid=$!
echo $background_pid, "is the pid of the background process"



## Now parse arguments in to relevant variables. These will be available to all scripts run from within.
# Bucket Name  $bucketname
# Group Directory $groupdir
# Results Directory $resultdir
# Analysis Output Directory $process
# Dataset Name (without path) $dataname
# Dataset Full Path $datapath
# Configuration Name # configname
# Configuration Path # configpath



#environment setup
export PATH="/home/ubuntu/anaconda3/bin:$PATH"

source activate lds



userhome="/home/ubuntu" #declaring variables
datastore="LDS/main/localdata/" #declaring variables
configstore="LDS/main/localconfig/" #declaring variables
#outstore="epi/scripts/data/lds_2D_linear2D_freq/" #declaring variables
outstore="LDS/main/data/" #declaring variables


## Make local storage locations
accessdir "$userhome/$datastore" "$userhome/$configstore" "$userhome/$outstore" #initializing local storage locations


## Stereotyped download script for data.
download "$inputpath" "$bucketname" "$datastore" #downloading data to immutable analysis environment

## Stereotyped download script for config:
download "$configpath" "$bucketname" "$configstore" # downloading config to immutable analysis environment
## Check if it's yaml, and if so convert to json:
## Reset to correctly get out json:
configname=$(python $neurocaasrootdir/ncap_utils/yamltojson.py "$userhome"/"$configstore"/"$configname")

###############################################################################################
## Custom bulk processing.
cd NeuroCAAS/LDS_algo/LDS/main # going to script directory


python clean_KF.py "$userhome/$configstore/$configname" "$userhome/$configstore" "$userhome/$datastore/$dataname" "$userhome/$outstore"

export resultsstore="data/results" # export result directory.


## copy the output to our results directory:
cd $resultsstore  # go to result directory.
echo $PWD "working directory"
echo  "results aimed at" "s3://$bucketname/$groupdir/$processdir/" # report to user through stdout
aws s3 sync ./ "s3://$bucketname/$groupdir/$processdir/per_hp" # upload back to user.

###############################################################################################

errorlog_final
kill "$background_pid"
