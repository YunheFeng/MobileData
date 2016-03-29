#!/bin/sh

# prompts first

cd /local/MobileData
svn ci -m "autosaving"
cd /local/Scripts
svn ci -m "autosaving"

cd /mydata
rm check_points.tar.gz
tar czvf check_points.tar.gz ./check_points
scp /mydata/check_points.tar.gz lanterns2.eecs.utk.edu:/local_scratch/

echo "You are all set."
