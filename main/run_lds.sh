#!/bin/bash
## Import functions for workflow management
## Get the path to this function:
execpath="$0"
echo execpath
scriptpath="$neurocaasrootdir/ncap_utils"


source "$scriptpath/workflow.sh"
## Import functions for data transfer
source "$scriptpath/transfer.sh"


errorlog


## Now parse arguments in to relevant variables. These will be available to all scripts run from within.
# Bucket Name  $bucketname
# Group Directory $groupdir
# Results Directory $resultdir
# Analysis Output Directory $process
# Dataset Name (without path) $dataname
# Dataset Full Path $datapath
# Configuration Name # configname
# Configuration Path # configpath
set -a
parseargsstd "$1" "$2" "$3" "$4"
set +a



#environment setup
export PATH="/home/ubuntu/anaconda3/bin:$PATH"

source activate lds



userhome="/home/ubuntu" #declaring variables
datastore="lds/main/localdata/" #declaring variables
configstore="lds/main/localconfig/" #declaring variables
#outstore="epi/scripts/data/lds_2D_linear2D_freq/" #declaring variables
outstore="lds/main/data/" #declaring variables
## Make local storage locations
accessdir "$userhome/$datastore" "$userhome/$configstore" "$userhome/$outstore" #initializing local storage locations


## Stereotyped download script for data. The only reason this comes after something custom is because we depend upon the AWS CLI and installed credentials.
download "$inputpath" "$bucketname" "$datastore" #downloading data to immutable analysis environment

## Stereotyped download script for config:
download "$configpath" "$bucketname" "$configstore" # downloading config to immutable analysis environment
## Check if it's yaml, and if so convert to json:
## Reset to correctly get out json:
configname=$(python $neurocaasrootdir/ncap_utils/yamltojson.py "$userhome"/"$configstore"/"$configname")

###############################################################################################
## Custom bulk processing.
cd lds/main # going to script directory

bash clean_KF.sh "$userhome"/"$datastore""$dataname" # script in EPI to run EPI optimization for given random seed.

export resultsstore="data/results" # export result directory.


## copy the output to our results directory:
cd $resultsstore  # go to result directory.
echo $PWD "working directory"
echo  "results aimed at" "s3://$bucketname/$groupdir/$processdir/" # report to user through stdout
aws s3 sync ./ "s3://$bucketname/$groupdir/$processdir/per_hp" # upload back to user.

###############################################################################################
