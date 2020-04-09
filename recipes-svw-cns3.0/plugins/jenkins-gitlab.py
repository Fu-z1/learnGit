# Set repository browser of gitLab URLs

from xml.etree import ElementTree
import re

def processGit(git):
    url = git.find("./userRemoteConfigs/hudson.plugins.git.UserRemoteConfig/url").text
    m = re.match('^git@${DEFAULT_PCC_GIT_SERVER}:(.*)\\.git.*', url)
    if not m: return
    browser = git.find("browser")
    if browser is not None: git.remove(browser)
    browser = ElementTree.SubElement(git, "browser",
        {"class" : "hudson.plugins.git.browser.GitLab"})
    ElementTree.SubElement(browser, "url").text = \
        "https://${DEFAULT_PCC_GIT_SERVER}/" + m.group(1)
    ElementTree.SubElement(browser, "version").text = "8.1"

def setGitlabBrowser(config, **kwargs):
    root = ElementTree.fromstring(config)
    scm = root.find("scm")
    if scm is None: return config

    if scm.get("class") == "hudson.plugins.git.GitSCM":
        processGit(scm)
    elif scm.get("class") == "org.jenkinsci.plugins.multiplescms.MultiSCM":
        for s in scm.find("scms"):
            if s.tag != "hudson.plugins.git.GitSCM": continue
            processGit(s)

    return ElementTree.tostring(root, encoding="UTF-8")

manifest = {
    'apiVersion' : "0.3",
    'hooks' : {
        'jenkinsJobCreate' : setGitlabBrowser,
        'jenkinsJobPostUpdate' : setGitlabBrowser
    }
}
