#!/bin/bash

set -ue

temp_dir=$(mktemp -d)

cp -r data $temp_dir

rm -r $temp_dir/data/photos/sorted

rm -r $temp_dir/data/photos/original

cp aws/cron.yaml $temp_dir

cp aws/Dockerrun.aws.json $temp_dir

cp Dockerfile $temp_dir

cp app.py $temp_dir

cp requirements.txt $temp_dir

CWD=$(pwd)

cd $temp_dir

zip -r source.zip *

cd $CWD

mv $temp_dir/source.zip .

rm -rf $temp_dir