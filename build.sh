#!/bin/sh
# Build RPM's from spec files

set -e

FILES=( $* )

if [ ${#FILES[@]} -eq 0 ]
then
  FILES='*.spec'
fi

for f in $FILES
do

  rpmbuild \
    --define "_rpmdir ./RPMS" \
    --define "_srcrpmdir ./SRPMS" \
    --define "_topdir `pwd`" \
    -ba $f

done
