#!/bin/bash


USER=jpcc_test
PASSWD="test"
SERVER="http://10.57.9.140"
#KEY="JPCCTEST"
KEY="PCNS3"

TITLE=${TITLE:?"Page title not defined"}
WEEK=${WEEK:?"Week Not defined"}
BASE_NAME=${BASE_NAME:?"base name not defined"}

VW_CHN_SPECIFIC_VERSION=${VW_CHN_SPECIFIC_VERSION}
VW_TW_SPECIFIC_VERSION=${VW_TW_SPECIFIC_VERSION}
VW_HM_SPECIFIC_VERSION=${VW_HM_SPECIFIC_VERSION}
SK_CHN_SPECIFIC_VERSION=${SK_CHN_SPECIFIC_VERSION}
SK_TW_SPECIFIC_VERSION=${SK_TW_SPECIFIC_VERSION}

VW_CHN_SW_VERSION=${VW_CHN_SW_VERSION}
VW_TW_SW_VERSION=${VW_TW_SW_VERSION}
VW_HM_SW_VERSION=${VW_HM_SW_VERSION}
SK_CHN_SW_VERSION=${SK_CHN_SW_VERSION}
SK_TW_SW_VERSION=${SK_TW_SW_VERSION}

VW_CHN_TAG=${VW_CHN_TAG}
VW_TW_TAG=${VW_TW_TAG}
VW_HM_TAG=${VW_HM_TAG}
SK_CHN_TAG=${SK_CHN_TAG}
SK_TW_TAG=${SK_TW_TAG}

VW_CHN_SDS=${VW_CHN_SDS}
VW_TW_SDS=${VW_TW_SDS}
VW_HM_SDS=${VW_HM_SDS}
SK_CHN_SDS=${SK_CHN_SDS}
SK_TW_SDS=${SK_TW_SDS}

VW_CHN_ISSW=${VW_CHN_ISSW}
VW_TW_ISSW=${VW_TW_ISSW}
VW_HM_ISSW=${VW_HM_ISSW}
SK_CHN_ISSW=${SK_CHN_ISSW}
SK_TW_ISSW=${SK_TW_ISSW}

VW_CHN_NAVI_TARBALL1=${VW_CHN_NAVI_TARBALL1}
VW_TW_NAVI_TARBALL1=${VW_TW_NAVI_TARBALL1}
VW_HM_NAVI_TARBALL1=${VW_HM_NAVI_TARBALL1}
SK_CHN_NAVI_TARBALL1=${SK_CHN_NAVI_TARBALL1}
SK_TW_NAVI_TARBALL1=${SK_TW_NAVI_TARBALL1}

VW_CHN_NAVI_TARBALL2=${VW_CHN_NAVI_TARBALL2}
VW_TW_NAVI_TARBALL2=${VW_TW_NAVI_TARBALL2}
VW_HM_NAVI_TARBALL2=${VW_HM_NAVI_TARBALL2}
SK_CHN_NAVI_TARBALL2=${SK_CHN_NAVI_TARBALL2}
SK_TW_NAVI_TARBALL2=${SK_TW_NAVI_TARBALL2}

VW_CHN_NAVI_TARBALL3=${VW_CHN_NAVI_TARBALL3}
VW_TW_NAVI_TARBALL3=${VW_TW_NAVI_TARBALL3}
VW_HM_NAVI_TARBALL3=${VW_HM_NAVI_TARBALL3}
SK_CHN_NAVI_TARBALL3=${SK_CHN_NAVI_TARBALL3}
SK_TW_NAVI_TARBALL3=${SK_TW_NAVI_TARBALL3}

VW_CHN_NAVI_TARBALL4=${VW_CHN_NAVI_TARBALL4}
VW_TW_NAVI_TARBALL4=${VW_TW_NAVI_TARBALL4}
VW_HM_NAVI_TARBALL4=${VW_HM_NAVI_TARBALL4}
SK_CHN_NAVI_TARBALL4=${SK_CHN_NAVI_TARBALL4}
SK_TW_NAVI_TARBALL4=${SK_TW_NAVI_TARBALL4}

VW_CHN_HMI=${VW_CHN_HMI}
VW_TW_HMI=${VW_TW_HMI}
VW_HM_HMI=${VW_HM_HMI}
SK_CHN_HMI=${SK_CHN_HMI}
SK_TW_HMI=${SK_TW_HMI}

VW_CHN_ANDROID=${VW_CHN_ANDROID}
VW_TW_ANDROID=${VW_TW_ANDROID}
VW_HM_ANDROID=${VW_HM_ANDROID}
SK_CHN_ANDROID=${SK_CHN_ANDROID}
SK_TW_ANDROID=${SK_TW_ANDROID}

VW_CHN_ANDROID_URL=${VW_CHN_ANDROID_URL}
VW_TW_ANDROID_URL=${VW_TW_ANDROID_URL}
VW_HM_ANDROID_URL=${VW_HM_ANDROID_URL}
SK_CHN_ANDROID_URL=${SK_CHN_ANDROID_URL}
SK_TW_ANDROID_URL=${SK_TW_ANDROID_URL}

VW_CHN_HV=${VW_CHN_HV}
VW_TW_HV=${VW_TW_HV}
VW_HM_HV=${VW_HM_HV}
SK_CHN_HV=${SK_CHN_HV}
SK_TW_HV=${SK_TW_HV}

VW_CHN_PACKAGE=${VW_CHN_PACKAGE}
VW_TW_PACKAGE=${VW_TW_PACKAGE}
VW_HM_PACKAGE=${VW_HM_PACKAGE}
SK_CHN_PACKAGE=${SK_CHN_PACKAGE}
SK_TW_PACKAGE=${SK_TW_PACKAGE}

VW_CHN_PACKAGE_FC=${VW_CHN_PACKAGE_FC}
VW_TW_PACKAGE_FC=${VW_TW_PACKAGE_FC}
VW_HM_PACKAGE_FC=${VW_HM_PACKAGE_FC}
SK_CHN_PACKAGE_FC=${SK_CHN_PACKAGE_FC}
SK_TW_PACKAGE_FC=${SK_TW_PACKAGE_FC}

CHANGES_URL=${CHANGES_URL}

#"id":2359302  4329660
generate_weekpage_data()
{
cat << EOF
{
"type":"page",
"title":"${WEEK}",
"ancestors":[{"id":4329660}],
"space":{"key":"${KEY}"},
"body":{"storage":{"value":"","representation":"storage"}
}
}
EOF
}

find_weekpage_id()
{
curl -s -u ${USER}:${PASSWD} -X GET -G \
--data-urlencode "spaceKey=${KEY}" --data-urlencode "title=${WEEK}" \
"${SERVER}:8090/rest/api/content/" | python -mjson.tool | jq '.results[0].id'
}

curl -u ${USER}:${PASSWD} -X POST -H "Content-Type: application/json" -d "$(generate_weekpage_data)"  ${SERVER}:8090/rest/api/content/ | python -mjson.tool
PARENT=$(find_weekpage_id)
echo PARENT=$PARENT

generate_weekpage_data()
{
cat << EOF
{
"type":"page",
"title":"${WEEK}",
"ancestors":[{"id":4329660}],
"space":{"key":"${KEY}"},
"body":{"storage":{"value":"","representation":"storage"}
}
}
EOF
}

find_weekpage_id()
{
curl -s -u ${USER}:${PASSWD} -X GET -G \
--data-urlencode "spaceKey=${KEY}" --data-urlencode "title=${WEEK}" \
"${SERVER}:8090/rest/api/content/" | python -mjson.tool | jq '.results[0].id'
}

curl -u ${USER}:${PASSWD} -X POST -H "Content-Type: application/json" -d "$(generate_weekpage_data)"  ${SERVER}:8090/rest/api/content/ | python -mjson.tool
PARENT=$(find_weekpage_id)
echo PARENT=$PARENT
if [ ${PARENT} = "null" ]
then
echo "find weekpage id failed... exit" 
exit 1
fi

generate_relpage_data()
{
cat << EOF
{
"type":"page",
"title":"${TITLE}",
"ancestors":[{"id":${PARENT}}],
"space":{"key":"${KEY}"},
"body":{"storage":
{"value":
"<h1>Base: ${BASE_NAME}</h1>\
<h2>Versions:</h2>\
<table class=\"relative-table\" style=\"width: 99.2356%;\"><colgroup><col style=\"width: 9.19411%;\" /><col style=\"width: 45.8584%;\" /><col style=\"width: 44.9054%;\" /></colgroup>\
<thead>\
<tr>\
<th>\
Component</th>\
<th>zr3-variant-VW_CHN</th>\
<th>zr3-variant-VW_TW</th>\
<th>zr3-variant-VW_HM</th>\
<th>zr3-variant-SK_CHN</th>\
<th>zr3-variant-SK_TW</th>\
</tr></thead><tbody>\
<tr>\
<th>Specific Version</th>\
<td>${VW_CHN_SPECIFIC_VERSION}</td>\
<td>${VW_TW_SPECIFIC_VERSION}</td>\
<td>${VW_HM_SPECIFIC_VERSION}</td>\
<td>${SK_CHN_SPECIFIC_VERSION}</td>\
<td>${SK_TW_SPECIFIC_VERSION}</td>\
</tr>\
<tr>\
<th>SW Version</th>\
<td>${VW_CHN_SW_VERSION}</td>\
<td>${VW_TW_SW_VERSION}</td>\
<td>${VW_HM_SW_VERSION}</td>\
<td>${SK_CHN_SW_VERSION}</td>\
<td>${SK_TW_SW_VERSION}</td>\
</tr>\
<tr>\
<th>Tag</th>\
<td>${VW_CHN_TAG}</td>\
<td>${VW_TW_TAG}</td>\
<td>${VW_HM_TAG}</td>\
<td>${SK_CHN_TAG}</td>\
<td>${SK_TW_TAG}</td></tr>\
<tr>\
<th>SDS</th>\
<td>${VW_CHN_SDS}</td>\
<td>${VW_TW_SDS}</td>\
<td>${VW_HM_SDS}</td>\
<td>${SK_CHN_SDS}</td>\
<td>${SK_TW_SDS}</td></tr>\
<tr>\
<th>CARSSW</th>\
<td>${VW_CHN_ISSW}</td>\
<td>${VW_TW_ISSW}</td>\
<td>${VW_HM_ISSW}</td>\
<td>${SK_CHN_ISSW}</td>\
<td>${SK_TW_ISSW}</td></tr>\
<tr>\
<th rowspan=\"4\">Navi Engine</th>\
<td>${VW_CHN_NAVI_TARBALL1}</td>\
<td>${VW_TW_NAVI_TARBALL1}</td>\
<td>${VW_HM_NAVI_TARBALL1}</td>\
<td>${SK_CHN_NAVI_TARBALL1}</td>\
<td>${SK_TW_NAVI_TARBALL1}</td>\
</tr>\
<tr>\
<td>${VW_CHN_NAVI_TARBALL2}</td>\
<td>${VW_TW_NAVI_TARBALL2}</td>\
<td>${VW_HM_NAVI_TARBALL2}</td>\
<td>${SK_CHN_NAVI_TARBALL2}</td>\
<td>${SK_TW_NAVI_TARBALL2}</td>\
</tr>\
<tr>\
<td>${VW_CHN_NAVI_TARBALL3}</td>\
<td>${VW_TW_NAVI_TARBALL3}</td>\
<td>${VW_HM_NAVI_TARBALL3}</td>\
<td>${SK_CHN_NAVI_TARBALL3}</td>\
<td>${SK_TW_NAVI_TARBALL3}</td>\
</tr>\
<tr>\
<td>${VW_CHN_NAVI_TARBALL4}</td>\
<td>${VW_TW_NAVI_TARBALL4}</td>\
<td>${VW_HM_NAVI_TARBALL4}</td>\
<td>${SK_CHN_NAVI_TARBALL4}</td>\
<td>${SK_TW_NAVI_TARBALL4}</td>\
</tr>\
<tr><th>HMI</th>\
<td>${VW_CHN_HMI}</td>\
<td>${VW_TW_HMI}</td>\
<td>${VW_HM_HMI}</td>\
<td>${SK_CHN_HMI}</td>\
<td>${SK_TW_HMI}</td>\
</tr>\
<tr><th>ANDROID VERSION</th>\
<td>${VW_CHN_ANDROID}</td>\
<td>${VW_TW_ANDROID}</td>\
<td>${VW_HM_ANDROID}</td>\
<td>${SK_CHN_ANDROID}</td>\
<td>${SK_TW_ANDROID}</td>\
</tr>\
<tr><th>ANDROID URL</th>\
<td>${VW_CHN_ANDROID_URL}</td>\
<td>${VW_TW_ANDROID_URL}</td>\
<td>${VW_HM_ANDROID_URL}</td>\
<td>${SK_CHN_ANDROID_URL}</td>\
<td>${SK_TW_ANDROID_URL}</td>\
</tr>\
<tr><th>HYPERVISOR</th>\
<td>${VW_CHN_HV}</td>\
<td>${VW_TW_HV}</td>\
<td>${VW_HM_HV}</td>\
<td>${SK_CHN_HV}</td>\
<td>${SK_TW_HV}</td>\
</tr>\
<tr>\
<th>UpdateContainer Package</th>\
<td><a href=\"${VW_CHN_PACKAGE}\">${VW_CHN_PACKAGE}</a></td>\
<td><a href=\"${VW_TW_PACKAGE}\">${VW_TW_PACKAGE}</a></td>\
<td><a href=\"${VW_HM_PACKAGE}\">${VW_HM_PACKAGE}</a></td>\
<td><a href=\"${SK_CHN_PACKAGE}\">${SK_CHN_PACKAGE}</a></td>\
<td><a href=\"${SK_TW_PACKAGE}\">${SK_TW_PACKAGE}</a></td>\
</tr>\
<tr>\
<th>FlashContainer Package</th>\
<td><a href=\"${VW_CHN_PACKAGE_FC}\">${VW_CHN_PACKAGE_FC}</a></td>\
<td><a href=\"${VW_TW_PACKAGE_FC}\">${VW_TW_PACKAGE_FC}</a></td>\
<td><a href=\"${VW_HM_PACKAGE_FC}\">${VW_HM_PACKAGE_FC}</a></td>\
<td><a href=\"${SK_CHN_PACKAGE_FC}\">${SK_CHN_PACKAGE_FC}</a></td>\
<td><a href=\"${SK_TW_PACKAGE_FC}\">${SK_TW_PACKAGE_FC}</a></td>\
</tr></tbody></table>\
<h2>Changes:</h2>\
<p class=\"auto-cursor-target\"><a href=\"${CHANGES_URL}\">${CHANGES_URL}</a></p>\
","representation":"storage"}
}
}
EOF
}

curl -u ${USER}:${PASSWD} -X POST -H "Content-Type: application/json" -d "$(generate_relpage_data)"  ${SERVER}:8090/rest/api/content/ | python -mjson.tool

