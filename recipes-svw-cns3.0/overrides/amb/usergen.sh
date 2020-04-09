#!/bin/bash
# usage: ./usergen.sh [group] [path where recipes folder is stored] [--integration]
# Creator: Kai Ehrhardt
if [ ${#} == 2 ] || [ ${#} == 3 ]
then
   files=$(find ${2}/recipes/${1}/* -name "*.yaml")
   if [ "${1}" == "radio" ]
   then
      ext="${2}/recipes/hmi/tsd-dsi-haswrapper.yaml"
      files="$files $ext"
   fi
   if [ "${3}" != "--integration" ]
   then
      file="user.yaml"
   else
      mkdir -p ${2}/overrides/amb
      file="${2}/overrides/amb/${1}.yaml"
   fi

   grep -q "^scmOverrides:$" $file &>/dev/null
   if [ $? -ne 0 ]; then
      echo "scmOverrides:" >> $file
   fi
   url=$(grep -ho "git@.*" $files | grep -v "/ext" )
   for j in $url; do
      cat >> $file << EOF 
  -
    match:
      url: "${j}"
    del: [commit, tag]
    set:
      branch: develop_mqb_sop1_eu
EOF
   done
else
   echo "usage: ./usergen.sh [group] [path where recipes folder is stored] [--integration]"
fi
