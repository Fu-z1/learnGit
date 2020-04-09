from xml.etree import ElementTree

VALGRIND_PLUGIN = ElementTree.fromstring("""
    <org.jenkinsci.plugins.valgrind.ValgrindPublisher plugin="valgrind@0.27">
      <valgrindPublisherConfig>
        <pattern>**/*.valgrind_result</pattern>
        <failThresholdInvalidReadWrite/>
        <failThresholdDefinitelyLost/>
        <failThresholdTotal/>
        <unstableThresholdInvalidReadWrite/>
        <unstableThresholdDefinitelyLost/>
        <unstableThresholdTotal/>
        <publishResultsForAbortedBuilds>false</publishResultsForAbortedBuilds>
        <publishResultsForFailedBuilds>false</publishResultsForFailedBuilds>
        <failBuildOnMissingReports>false</failBuildOnMissingReports>
        <failBuildOnInvalidReports>false</failBuildOnInvalidReports>
      </valgrindPublisherConfig>
    </org.jenkinsci.plugins.valgrind.ValgrindPublisher>
""")

def equalXML(x1, x2):
    return [l.strip()  for l in ElementTree.tostring(x1, encoding="UTF-8").strip().splitlines()] == \
           [l.strip()  for l in ElementTree.tostring(x2, encoding="UTF-8").strip().splitlines()]

def checkValgrind(config, checkoutSteps, buildSteps, packageSteps, **kwargs):
    found = False
    changed = False

    for s in packageSteps:
        if "communication::tsd-commonapi-testframework" == s.getPackage().getName().split('/')[-1]:
            found = True
            break

    if found:
        root = ElementTree.fromstring(config)
        publishers = root.find("publishers")

        valgrind = publishers.find("org.jenkinsci.plugins.valgrind.ValgrindPublisher")
        if valgrind is not None:
            # remove previous config (for cases XUNIT_PLUGIN config has changed)
            if not equalXML(valgrind, VALGRIND_PLUGIN):
                publishers.remove(valgrind)
                publishers.append(VALGRIND_PLUGIN)
                changed = True
        else:
            publishers.append(VALGRIND_PLUGIN)
            changed = True

    return ElementTree.tostring(root, encoding="UTF-8") if changed else config

manifest = {
    'apiVersion' : "0.3",
    'hooks' : {
        'jenkinsJobCreate' : checkValgrind,
        'jenkinsJobPostUpdate' : checkValgrind
    }
}
