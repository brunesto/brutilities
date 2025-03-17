#!/bin/bash

# Licence GPL v3
#
# similar to git-ignore but for svn
#
set -e

for file in $* ; do
  if [ -e $file ]; then
    pushd `dirname $file` > /dev/null
    set +e
    svn propget svn:ignore . > /tmp/svnignored 2>//dev/null
    set -e
    echo `basename $file` >> /tmp/svnignored
    svn propset svn:ignore  -F /tmp/svnignored . > /dev/null
    popd > /dev/null
    echo "added to svn:ignore:$file"
  else
    echo "skipped:$file"
  fi 
  
done
