#!/usr/bin/env python3

import gitlab3
import re
import sys
import urllib
import subprocess

# constant definition
server_url = 'https://git.mib3.technisat-digital'
hook_url = 'http://test13.mib3.technisat-digital:8080/gitlab/notify_commit'
private_token = sys.argv[1]

if len(sys.argv) == 3:
    modules = sys.argv[2]
else:
    # grep all repos from all recipes
    modules = subprocess.check_output("bob query-scm -DCONFIG_XTENSA=1 -DEXPORT_TOOLCHAIN=1 -r zr3 -f git={url}".split(" "),
        universal_newlines=True, cwd="..")

# update gitlab
gl = gitlab3.GitLab(server_url,private_token,ssl_verify=False)
for projectName in modules.split("\n"):
    projectName = projectName.strip()
    m = re.match('^git@git.mib3.technisat-digital:(.*)\\.git.*', projectName)
    if not m: continue
    projectName = m.group(1)
    print("Examine", projectName, "...")
    try:
        project = gl.project(urllib.parse.quote_plus(projectName))
        found = False
        for h in project.hooks():
            #print "  Hook:", h.url
            if h.url == hook_url: found = True
        if not found:
            print("  Add hook", hook_url)
            project.add_hook(hook_url)
    except Exception as e:
        print("  Failed", str(e))

