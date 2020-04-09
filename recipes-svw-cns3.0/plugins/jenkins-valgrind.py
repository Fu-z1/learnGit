# This plugin adds a support for valgrind plugin (both: builder and publisher)
# to be run for every unittests job
# Supported env variables:
#  CONFIG_JENKINS_VALGRIND [set/unset]
#  CONFIG_JENKINS_VALGRIND_CMD [command string]

from xml.etree import ElementTree
import os

PLUGIN_CMD_TMPL = """
  <hudson.tasks.Shell>
    <command>%(command)s
    </command>
  </hudson.tasks.Shell>
"""

# exclude static libraries and tests that confuse valgrind/hang up
EXCLUDE_PATTERN = "**/*.a,**/*.txt,**/*.cmake,**/*.cppunitreport,**/*.so,**/tsd.communication.messaging.test.shm,**/tsd.media.common.test.arenaallocatortest,**/tsd.nav.sdk.mapdisplay.*,**/tsd.nav.testinterface.test.*,**/tsd.nav.utils.test.navsystemTest,**/tsd.common.test.dispatch.genericserializedobject,**/tsd.common.checksums.test.ReedSolomon,**/tsd.media.engine.cinemo.test.mondcachetest,**/tsd.nav.middleware.nds.test.hybrid,**/tsd.audio.audiomgr.audiocontrol.test.stm,**/tsd.nav.utils.test.MainTest,**/tsd.logging.mib3.test.LogClientTest,**/tsd.logging.mib3.test.JournalReaderTest,**/tsd.media.common.test.platform,**/tsd.logging.mib3.test.LogServerTest,**/tsd.common.test.ipc.posix.SocketOperationTest"

PLUGIN_BUILDER = """
    <org.jenkinsci.plugins.valgrind.ValgrindBuilder plugin="valgrind@0.27">
      <valgrindExecutable/>
      <workingDirectory>${WORKSPACE}</workingDirectory>
      <includePattern>**/build/**/dist/**/*tsd.*test*</includePattern>
      <excludePattern>%(exclude_pattern)s</excludePattern>
      <outputDirectory/>
      <outputFileEnding>.memcheck</outputFileEnding>
      <programOptions/>
      <tool class="org.jenkinsci.plugins.valgrind.ValgrindBuilder$ValgrindToolMemcheck">
        <showReachable>false</showReachable>
        <undefinedValueErrors>true</undefinedValueErrors>
        <leakCheckLevel>full</leakCheckLevel>
        <trackOrigins>true</trackOrigins>
      </tool>
      <valgrindOptions/>
      <ignoreExitCode>true</ignoreExitCode>
      <traceChildren>false</traceChildren>
      <childSilentAfterFork>false</childSilentAfterFork>
      <generateSuppressions>true</generateSuppressions>
      <suppressionFiles>${WORKSPACE}/valgrind/suppressions.txt</suppressionFiles>
      <removeOldReports>true</removeOldReports>
    </org.jenkinsci.plugins.valgrind.ValgrindBuilder>
"""

PLUGIN_PUBLISHER = """
    <org.jenkinsci.plugins.valgrind.ValgrindPublisher plugin="valgrind@0.27">
      <valgrindPublisherConfig>
        <pattern>*.memcheck</pattern>
        <failThresholdInvalidReadWrite>%(fail_th)s</failThresholdInvalidReadWrite>
        <failThresholdDefinitelyLost>%(fail_th)s</failThresholdDefinitelyLost>
        <failThresholdTotal>%(fail_th)s</failThresholdTotal>
        <unstableThresholdInvalidReadWrite>%(unstable_th)s</unstableThresholdInvalidReadWrite>
        <unstableThresholdDefinitelyLost>%(unstable_th)s</unstableThresholdDefinitelyLost>
        <unstableThresholdTotal>%(unstable_th)s</unstableThresholdTotal>
        <publishResultsForAbortedBuilds>false</publishResultsForAbortedBuilds>
        <publishResultsForFailedBuilds>false</publishResultsForFailedBuilds>
        <failBuildOnMissingReports>false</failBuildOnMissingReports>
        <failBuildOnInvalidReports>false</failBuildOnInvalidReports>
      </valgrindPublisherConfig>
    </org.jenkinsci.plugins.valgrind.ValgrindPublisher>
"""

def equalXML(x1, x2):
    return [l.strip()  for l in ElementTree.tostring(x1, encoding="UTF-8").strip().splitlines()] == \
           [l.strip()  for l in ElementTree.tostring(x2, encoding="UTF-8").strip().splitlines()]

def checkValgrind(config, checkoutSteps, buildSteps, packageSteps, **kwargs):
    # iterate all available steps to find right recipes
    unittest_found = False
    for s in (s  for steps in (checkoutSteps, buildSteps, packageSteps) for s in steps):
        # enable for all unittest recipes, with exception of root recipe (pointless)
        pkg = s.getPackage().getName().split('/')[-1]
        if "-unittests" in pkg:
            unittest_found = True
            break

    # activate only if env variable set and job is a unittest job
    if 'CONFIG_JENKINS_VALGRIND' in os.environ and unittest_found:
        root = ElementTree.fromstring(config)

        builders = root.find("builders")
        if builders is not None:
            valgrind_builder = builders.find("org.jenkinsci.plugins.valgrind.ValgrindBuilder")
            if valgrind_builder is None:
                # inject shell command to download suppression.txt before valgrind run
                if 'CONFIG_JENKINS_VALGRIND_CMD' in os.environ:
                    builders.append(ElementTree.fromstring(PLUGIN_CMD_TMPL % { 'command' : os.environ ['CONFIG_JENKINS_VALGRIND_CMD'] }))
                builders.append(ElementTree.fromstring(PLUGIN_BUILDER % { 'exclude_pattern' : EXCLUDE_PATTERN }))

        if 'CONFIG_JENKINS_VALGRIND_FAIL_THRESHOLD' in os.environ:
            fail_th = os.environ['CONFIG_JENKINS_VALGRIND_FAIL_THRESHOLD']
        else:
            fail_th = ''
        if 'CONFIG_JENKINS_VALGRIND_UNSTABLE_THRESHOLD' in os.environ:
            unstable_th = os.environ['CONFIG_JENKINS_VALGRIND_UNSTABLE_THRESHOLD']
        else:
            unstable_th = ''

        VALGRIND = ElementTree.fromstring(PLUGIN_PUBLISHER % {'fail_th': fail_th,
                                                              'unstable_th': unstable_th})

        publishers = root.find("publishers")
        if publishers is not None:
            valgrind_publisher = publishers.find("org.jenkinsci.plugins.valgrind.ValgrindPublisher")
            if valgrind_publisher is None:
                publishers.append(VALGRIND)
            else:
                if not equalXML(valgrind_publisher, VALGRIND):
                    publishers.remove(valgrind_publisher)
                    publishers.append(VALGRIND)

        config = ElementTree.tostring(root, encoding="UTF-8")

    return config

manifest = {
    'apiVersion' : "0.3",
    'hooks' : {
        'jenkinsJobCreate' : checkValgrind,
        'jenkinsJobPostUpdate' : checkValgrind
    }
}
