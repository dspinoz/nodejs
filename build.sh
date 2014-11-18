#!/bin/sh
# Build RPM's from spec files

set -e

for f in *.spec
do

  rpmbuild \
    --define "_rpmdir ./RPMS" \
    --define "_srcrpmdir ./SRPMS" \
    --define "_topdir `pwd`" \
    -ba $f

done
