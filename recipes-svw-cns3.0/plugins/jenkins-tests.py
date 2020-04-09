# Sample plugin showing how to add a plugin to some Jenkins jobs
#
# This plugin adds a cobertura coverage publisher post-build-action to all jobs
# that contain at least one package that ends with 'unittests'.

from xml.etree import ElementTree
import os

COBERTURA_PLUGIN = ElementTree.fromstring("""
    <hudson.plugins.cobertura.CoberturaPublisher plugin="cobertura@1.9.8">
      <coberturaReportFile>**/coverage.xml</coberturaReportFile>
      <onlyStable>false</onlyStable>
      <failUnhealthy>false</failUnhealthy>
      <failUnstable>false</failUnstable>
      <autoUpdateHealth>false</autoUpdateHealth>
      <autoUpdateStability>false</autoUpdateStability>
      <zoomCoverageChart>false</zoomCoverageChart>
      <maxNumberOfBuilds>0</maxNumberOfBuilds>
      <failNoReports>false</failNoReports>
      <healthyTarget>
        <targets class="enum-map" enum-type="hudson.plugins.cobertura.targets.CoverageMetric">
          <entry>
            <hudson.plugins.cobertura.targets.CoverageMetric>METHOD</hudson.plugins.cobertura.targets.CoverageMetric>
            <int>8000000</int>
          </entry>
          <entry>
            <hudson.plugins.cobertura.targets.CoverageMetric>LINE</hudson.plugins.cobertura.targets.CoverageMetric>
            <int>8000000</int>
          </entry>
          <entry>
            <hudson.plugins.cobertura.targets.CoverageMetric>CONDITIONAL</hudson.plugins.cobertura.targets.CoverageMetric>
            <int>7000000</int>
          </entry>
        </targets>
      </healthyTarget>
      <unhealthyTarget>
        <targets class="enum-map" enum-type="hudson.plugins.cobertura.targets.CoverageMetric">
          <entry>
            <hudson.plugins.cobertura.targets.CoverageMetric>METHOD</hudson.plugins.cobertura.targets.CoverageMetric>
            <int>0</int>
          </entry>
          <entry>
            <hudson.plugins.cobertura.targets.CoverageMetric>LINE</hudson.plugins.cobertura.targets.CoverageMetric>
            <int>0</int>
          </entry>
          <entry>
            <hudson.plugins.cobertura.targets.CoverageMetric>CONDITIONAL</hudson.plugins.cobertura.targets.CoverageMetric>
            <int>0</int>
          </entry>
        </targets>
      </unhealthyTarget>
      <failingTarget>
        <targets class="enum-map" enum-type="hudson.plugins.cobertura.targets.CoverageMetric">
          <entry>
            <hudson.plugins.cobertura.targets.CoverageMetric>METHOD</hudson.plugins.cobertura.targets.CoverageMetric>
            <int>0</int>
          </entry>
          <entry>
            <hudson.plugins.cobertura.targets.CoverageMetric>LINE</hudson.plugins.cobertura.targets.CoverageMetric>
            <int>0</int>
          </entry>
          <entry>
            <hudson.plugins.cobertura.targets.CoverageMetric>CONDITIONAL</hudson.plugins.cobertura.targets.CoverageMetric>
            <int>0</int>
          </entry>
        </targets>
      </failingTarget>
      <sourceEncoding>ASCII</sourceEncoding>
    </hudson.plugins.cobertura.CoberturaPublisher>
""")

XUNIT_PLUGIN = """
    <xunit plugin="xunit@1.102">
      <types>
        <CppUnitJunitHudsonTestType>
          <pattern>**/dist/**/*.cppunitreport</pattern>
          <skipNoTestFiles>false</skipNoTestFiles>
          <failIfNotNew>true</failIfNotNew>
          <deleteOutputFiles>true</deleteOutputFiles>
          <stopProcessingIfError>true</stopProcessingIfError>
        </CppUnitJunitHudsonTestType>
      </types>
      <thresholds>
        <org.jenkinsci.plugins.xunit.threshold.FailedThreshold>
          <unstableThreshold></unstableThreshold>
          <unstableNewThreshold>%(unstable_th)s</unstableNewThreshold>
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
"""

def equalXML(x1, x2):
    return [l.strip()  for l in ElementTree.tostring(x1, encoding="UTF-8").strip().splitlines()] == \
           [l.strip()  for l in ElementTree.tostring(x2, encoding="UTF-8").strip().splitlines()]

def checkTests(config, checkoutSteps, buildSteps, packageSteps, **kwargs):
    found = False
    changed = False

    for s in checkoutSteps:
        pkg = s.getPackage().getName().split('/')[-1]
        if "-unittests" in pkg: found = True
        if "-swittests" in pkg: found = True
    for s in buildSteps:
        pkg = s.getPackage().getName().split('/')[-1]
        if "-unittests" in pkg: found = True
        if "-swittests" in pkg: found = True
    for s in packageSteps:
        pkg = s.getPackage().getName().split('/')[-1]
        if "-unittests" in pkg: found = True
        if "-swittests" in pkg: found = True

    if found:
        root = ElementTree.fromstring(config)
        publishers = root.find("publishers")

        cobertura = publishers.find("hudson.plugins.cobertura.CoberturaPublisher")
        if cobertura is not None:
            # remove previous config (for cases COBERTURA_PLUGIN config has changed)
            if not equalXML(cobertura, COBERTURA_PLUGIN):
                publishers.remove(cobertura)
                publishers.append(COBERTURA_PLUGIN)
                changed = True
        else:
            publishers.append(COBERTURA_PLUGIN)
            changed = True

        if 'CONFIG_JENKINS_XUNIT_UNSTABLE_NEW_THRESHOLD' in os.environ:
            failed_th = os.environ['CONFIG_JENKINS_XUNIT_UNSTABLE_NEW_THRESHOLD']
        else:
            failed_th = ''
        XUNIT_PUBLISHER = ElementTree.fromstring(XUNIT_PLUGIN % {'unstable_th': failed_th})

        xunit = publishers.find("xunit")
        if xunit is not None:
            # remove previous config (for cases XUNIT_PLUGIN config has changed)
            if not equalXML(xunit, XUNIT_PUBLISHER):
                publishers.remove(xunit)
                publishers.append(XUNIT_PUBLISHER)
                changed = True
        else:
            publishers.append(XUNIT_PUBLISHER)
            changed = True

    return ElementTree.tostring(root, encoding="UTF-8") if changed else config

manifest = {
    'apiVersion' : "0.3",
    'hooks' : {
        'jenkinsJobCreate' : checkTests,
        'jenkinsJobPostUpdate' : checkTests
    }
}
