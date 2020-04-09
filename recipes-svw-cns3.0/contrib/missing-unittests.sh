#!/bin/bash

containsElement () {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}

declare -A REPOSITORIES
declare -a WHITELIST
FOUND=0

while getopts ":w:" opt; do
   case $opt in
      w)
         if [[ -e "${OPTARG}" ]]; then
            WHITELIST=($(cat $OPTARG))
         fi
         ;;
   esac
done

# get all repositories
echo "Gather all repositories..."
while read TYPE URL ; do
   if [[ $TYPE == git && $URL == */tsd.*.git ]] ; then
      if [[ "$(containsElement "${URL}" "${WHITELIST[@]}"; echo $?)" == "1" ]]; then
         REPOSITORIES[$URL]=0
      else
         : $(( FOUND++ ))
      fi
   fi
done < <( bob query-scm -r -f "git=git {url}" zr3 )

# mark tested repositories
echo "Determinte unit-tested repositories..."
for i in $(bob ls -p unittests) ; do
   while read TYPE URL ; do
      if [[ $TYPE == git && $URL == */tsd.*.git ]] ; then
         REPOSITORIES[$URL]=1
      fi
   done < <( bob query-scm -f "git=git {url}" $i )
done

TESTED=0
UNTESTED=0

echo ""
echo "Repositores without unittests:"
echo "=============================="

for i in "${!REPOSITORIES[@]}" ; do
   if [[ ${REPOSITORIES[$i]} -eq 0 ]] ; then
      echo "$i"
      : $(( UNTESTED++ ))
   else
      : $(( TESTED++ ))
   fi
done

echo ""
echo "Summary:"
echo "========"
echo $(( TESTED+UNTESTED )) repositories, $TESTED have unittests, $UNTESTED have no unittest recipe, $FOUND whitelist repositories found
