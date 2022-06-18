#!/bin/sh
old_version=$(cat version.txt)
patch_number=$(echo "$old_version" | cut -c 5)
new_patch=$(echo "$((patch_number + 1))")
echo $new_patch
var1="0.0."
output_version="$var1$new_patch"
echo "$output_version" > version.txt