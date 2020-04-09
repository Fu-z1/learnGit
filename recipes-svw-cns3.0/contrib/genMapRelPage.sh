#!/bin/bash


USER=jpcc_test
PASSWD="test"
SERVER="http://10.57.9.140"
#KEY="JPCCTEST"
KEY="PCNS3"

TITLE=${TITLE_NAVIMAP:?"Page title not defined"}
WEEK=${WEEK_NAVIMAP:?"Week Not defined"}
BASE_NAME=${BASE_NAME:?"base name not defined"}

CHN_SPECIFIC_VERSION=${zr3_navimap_CHN_SPECIFIC_VERSION}
TW_SPECIFIC_VERSION=${zr3_navimap_TW_SPECIFIC_VERSION}
CHN_2MESH_SPECIFIC_VERSION=${zr3_navimap_CHN_2mesh_SPECIFIC_VERSION}

CHN_SW_VERSION=${zr3_navimap_CHN_SW_VERSION_NAVIMAP}
TW_SW_VERSION=${zr3_navimap_TW_SW_VERSION_NAVIMAP}
CHN_2MESH_SW_VERSION=${zr3_navimap_CHN_2mesh_SW_VERSION_NAVIMAP}

CHN_TAG=${zr3_navimap_CHN_TAG_NAVIMAP}
TW_TAG=${zr3_navimap_TW_TAG_NAVIMAP}
CHN_2MESH_TAG=${zr3_navimap_CHN_2mesh_TAG_NAVIMAP}

CHN_NAVI_TARBALL1=${zr3_navimap_CHN_NAVI_TARBALL1}
TW_NAVI_TARBALL1=${zr3_navimap_CHN_NAVI_TARBALL1}
CHN_2MESH_NAVI_TARBALL1=${zr3_navimap_CHN_2mesh_NAVI_TARBALL1}

CHN_NAVI_TARBALL2=${zr3_navimap_CHN_NAVI_TARBALL2}
TW_NAVI_TARBALL2=${zr3_navimap_CHN_NAVI_TARBALL2}
CHN_2MESH_NAVI_TARBALL2=${zr3_navimap_CHN_2mesh_NAVI_TARBALL2}

CHN_NAVI_TARBALL3=${zr3_navimap_CHN_NAVI_TARBALL4}
TW_NAVI_TARBALL3=${zr3_navimap_TW_NAVI_TARBALL5}
CHN_2MESH_NAVI_TARBALL3=${zr3_navimap_CHN_2mesh_NAVI_TARBALL3}

CHN_PACKAGE=${zr3_navimap_CHN_PACKAGE_NAVIMAP}
TW_PACKAGE=${zr3_navimap_TW_PACKAGE_NAVIMAP}
CHN_2MESH_PACKAGE=${zr3_navimap_CHN_2mesh_PACKAGE_NAVIMAP}

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
<th>zr3_navimap_CHN</th>\
<th>zr3_navimap_TW</th>\
<th>zr3_navimap_CHN_2mesh</th>\
</tr></thead><tbody>\
<tr>\
<th>Specific Version</th>\
<td>${CHN_SPECIFIC_VERSION}</td>\
<td>${TW_SPECIFIC_VERSION}</td>\
<td>${CHN_2MESH_SPECIFIC_VERSION}</td>\
</tr>\
<tr>\
<th>SW Version</th>\
<td>${CHN_SW_VERSION}</td>\
<td>${TW_SW_VERSION}</td>\
<td>${CHN_2MESH_SW_VERSION}</td>\
</tr>\
<tr>\
<th>Tag</th>\
<td>${CHN_TAG}</td>\
<td>${TW_TAG}</td>\
<td>${CHN_2MESH_TAG}</td></tr>\
<tr>\
<th rowspan=\"3\">Navi Engine</th>\
<td>${CHN_NAVI_TARBALL1}</td>\
<td>${TW_NAVI_TARBALL1}</td>\
<td>${CHN_2MESH_NAVI_TARBALL1}</td>\
</tr>\
<tr>\
<td>${CHN_NAVI_TARBALL2}</td>\
<td>${TW_NAVI_TARBALL2}</td>\
<td>${CHN_2MESH_NAVI_TARBALL2}</td>\
</tr>\
<tr>\
<td>${CHN_NAVI_TARBALL3}</td>\
<td>${TW_NAVI_TARBALL3}</td>\
<td>${CHN_2MESH_NAVI_TARBALL3}</td>\
</tr>\
<tr>\
<th>UpdateContainer Package</th>\
<td><a href=\"${CHN_PACKAGE}\">${CHN_PACKAGE}</a></td>\
<td><a href=\"${TW_PACKAGE}\">${TW_PACKAGE}</a></td>\
<td><a href=\"${CHN_2MESH_PACKAGE}\">${CHN_2MESH_PACKAGE}</a></td>\
</tr>\
</tbody></table>\
<h2>Changes:</h2>\
<p class=\"auto-cursor-target\"><a href=\"${CHANGES_URL}\">${CHANGES_URL}</a></p>\
","representation":"storage"}
}
}
EOF
}

curl -u ${USER}:${PASSWD} -X POST -H "Content-Type: application/json" -d "$(generate_relpage_data)"  ${SERVER}:8090/rest/api/content/ | python -mjson.tool

