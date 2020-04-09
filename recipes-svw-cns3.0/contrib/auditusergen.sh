#!/bin/bash
CWD=$(pwd)
if [ ${#} -lt 1 ]
then
   echo "Usage: auditusergen.sh audit.json.gz..." 1>&2
   echo "" 1<&2
   echo "Generates SCM overrides with actually used revisions from the given audit files." 1>&2
   echo "" 1<&2
   echo "Assumes that all checkouts for a certain repository were done with the same" 1>&2
   echo "revision." 1>&2
   exit 1
elif [ -e $CWD/user.yaml ]
then
   echo "user.yaml already exists in $CWD" 1>&2
elif [ ! -d $CWD/recipes ]
then
   echo "switch to a bob project directory" 1>&2
else
   echo "scmOverrides:" >> $CWD/user.yaml
   zcat $@ | jq --raw-output '.references[].scms[] | .remotes.origin + " " + .commit | select(length > 1)' | sort | uniq |
   while read line
   do
      url=$(echo $line | cut -f1 -d' ')
      commit=$(echo $line | cut -f2 -d' ')
      cat >> $CWD/user.yaml << EOF 
  -
    match:
      url: "$url"
    del: [commit, tag]
    set:
      commit: $commit
EOF
   done
fi
