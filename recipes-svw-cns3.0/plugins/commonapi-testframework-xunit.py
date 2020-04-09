from xml.etree import ElementTree

XUNIT_PLUGIN = ElementTree.fromstring("""
    <xunit plugin="xunit@1.102">
      <types>
        <CppUnitJunitHudsonTestType>
          <pattern>**/dist/**/communication/tsd-commonapi-testframework/dist/1/*.cppunitreport</pattern>
          <skipNoTestFiles>true</skipNoTestFiles>
          <failIfNotNew>false</failIfNotNew>
          <deleteOutputFiles>true</deleteOutputFiles>
          <stopProcessingIfError>true</stopProcessingIfError>
        </CppUnitJunitHudsonTestType>
      </types>
      <thresholds>
        <org.jenkinsci.plugins.xunit.threshold.FailedThreshold>
          <unstableThreshold>5</unstableThreshold>
          <unstableNewThreshold>1</unstableNewThreshold>
          <failureThreshold></failureThreshold>
          <failureNewThreshold></failureNewThreshold>
        </org.jenkinsci.plugins.xunit.threshold.FailedThreshold>
        <org.jenkinsci.plugins.xunit.threshold.SkippedThreshold>
          <unstableThreshold></unstableThreshold>
          <unstableNewThreshold></unstableNewThreshold>
          <failureThreshold></failureThreshold>
          <failureNewThreshold></failureNewThreshold>
        </org.jenkinsci.plugins.xunit.threshold.SkippedThreshold>
      </thresholds>
      <thresholdMode>1</thresholdMode>
      <extraConfiguration>
        <testTimeMargin>3000</testTimeMargin>
      </extraConfiguration>
    </xunit>
""")

def equalXML(x1, x2):
    return [l.strip()  for l in ElementTree.tostring(x1, encoding="UTF-8").strip().splitlines()] == \
           [l.strip()  for l in ElementTree.tostring(x2, encoding="UTF-8").strip().splitlines()]

def checkTests(config, checkoutSteps, buildSteps, packageSteps, **kwargs):
    found = False
    changed = False

    for s in packageSteps:
        if "communication::tsd-commonapi-testframework" == s.getPackage().getName().split('/')[-1]:
            found = True
            break

    if found:
        root = ElementTree.fromstring(config)
        publishers = root.find("publishers")

        xunit = publishers.find("xunit")
        if xunit is not None:
            # remove previous config (for cases XUNIT_PLUGIN config has changed)
            if not equalXML(xunit, XUNIT_PLUGIN):
                publishers.remove(xunit)
                publishers.append(XUNIT_PLUGIN)
                changed = True
        else:
            publishers.append(XUNIT_PLUGIN)
            changed = True

    return ElementTree.tostring(root, encoding="UTF-8") if changed else config

manifest = {
    'apiVersion' : "0.3",
    'hooks' : {
        'jenkinsJobCreate' : checkTests,
        'jenkinsJobPostUpdate' : checkTests
    }
}
