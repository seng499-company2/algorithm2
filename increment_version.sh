#!/bin/bash
version_string=$(cat version.txt)

major_version=${version_string:0:1}
minor_version=${version_string:2:1}
patch_version=${version_string:4:1}

((patch_version=patch_version+1))

if [[ $patch_version -gt 9 ]];
then
  patch_version=0
  ((minor_version=minor_version+1))
fi

if [[ $minor_version -gt 9 ]];
then
  minor_version=0
  ((major_version=major_version+1))
fi

output_version="$major_version.$minor_version.$patch_version"
echo $output_version > version.txt