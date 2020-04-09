#!/bin/bash
echo "*******************" >> /tmp/xulix.log
export BOB_ARTIFACT_CACHE="$(dirname $WORKSPACE)/.bobCache" 
echo "BOB_LOCAL_ARTIFACT  = $BOB_LOCAL_ARTIFACT" >> /tmp/xulix.log
echo "BOB_REMOTE_ARTIFACT = $BOB_REMOTE_ARTIFACT" >> /tmp/xulix.log
echo " BOB_ARTIFACT_CACHE = $BOB_ARTIFACT_CACHE" >> /tmp/xulix.log
#echo "         MU_VERSION = $MU_VERSION" >> /tmp/xulix.log
#echo "     SWI_MU_VERSION = $SWI_MU_VERSION" >> /tmp/xulix.log

export CACHED_ARTIFACT="$BOB_ARTIFACT_CACHE/$BOB_REMOTE_ARTIFACT"
export TEMP_CACHED_ARTIFACT="$BOB_ARTIFACT_CACHE/$BOB_REMOTE_ARTIFACT.$(basename $BOB_LOCAL_ARTIFACT)"

# set |sort >> /tmp/xulix.log
shopt -s extglob # Required to trim whitespace; see below

function checkUrl() {
    while IFS=':' read key value; do
        # trim whitespace in "value"
        value=${value##+([[:space:]])}; value=${value%%+([[:space:]])}

        case "$key" in
            Server) SERVER="$value"
                    ;;
            Content-Type) CT="$value"
                    ;;
            HTTP*) read PROTO STATUS MSG <<< "$key{$value:+:$value}"
                    ;;
        esac
    done < <(curl -sI "$1")
}

if [[ ! -f "$CACHED_ARTIFACT" ]] 
then
    TGZ_URL="http://download.swi.technisat-digital/swibob/$BOB_REMOTE_ARTIFACT"
    checkUrl $TGZ_URL
    echo "$STATUS von $TGZ_URL" >> /tmp/xulix.log
    if [[  $STATUS -ne 200 ]]
    then
        exit 42
    fi
    curl -sSg --fail --create-dirs -o $TEMP_CACHED_ARTIFACT $TGZ_URL 
    if [[ ! -f "$CACHED_ARTIFACT" ]] 
    then
        mv $TEMP_CACHED_ARTIFACT $CACHED_ARTIFACT
    fi
else
    echo "use cached $BOB_REMOTE_ARTIFACT" >> /tmp/xulix.log
fi
[[ -e $BOB_LOCAL_ARTIFACT ]] && rm -rf $BOB_LOCAL_ARTIFACT
ln -s $CACHED_ARTIFACT $BOB_LOCAL_ARTIFACT
