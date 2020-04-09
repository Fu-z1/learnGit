import os
from xml.etree import ElementTree

CPPCHECK_CHECKOUT = ElementTree.fromstring("""
<hudson.plugins.copyartifact.CopyArtifact plugin="copyartifact@1.38.1">
      <project>additional-kw-scripts</project>
      <filter></filter>
      <target>additional-kw-scripts</target>
      <excludes></excludes>
      <selector class="hudson.plugins.copyartifact.StatusBuildSelector"/>
      <doNotFingerprintArtifacts>false</doNotFingerprintArtifacts>
    </hudson.plugins.copyartifact.CopyArtifact>
""")
CPPCHECK_BUILDSTEP = ElementTree.fromstring("""
    <hudson.tasks.Shell>
      <command>#cppcheck
# which neccesary because cppcheck won&apos;t find his cfg-file otherwise.
export CPPCHECK_PATH=$(which cppcheck)
for folder in $(find . -type d -name &quot;.git&quot; -execdir pwd \;); do
	cd  $folder
    [ $(find . \( -path ./test -o -path ./test_doubles -o -path ./swit -o -path ./swit_white \) -prune -o -name *.cpp -print |wc -l)  -eq  0 ] &amp;&amp; echo &quot;No cpp files found, skipping cppcheck&quot; &amp;&amp; exit 0
    sh -c &apos;${WORKSPACE}/additional-kw-scripts/additionalScripts_mib3/cppCheck.sh ${WORKSPACE}/additional-kw-scripts/additionalScripts_mib3 $(pwd)||true&apos;
done
</command>
    </hudson.tasks.Shell>
""")
CPPCHECK_PLUGIN = ElementTree.fromstring("""
    <org.jenkinsci.plugins.cppcheck.CppcheckPublisher plugin="cppcheck@1.21">
      <cppcheckConfig>
        <pattern>**/cppcheck.xml</pattern>
        <ignoreBlankFiles>false</ignoreBlankFiles>
        <allowNoReport>true</allowNoReport>
        <configSeverityEvaluation>
          <threshold></threshold>
          <newThreshold></newThreshold>
          <failureThreshold></failureThreshold>
          <newFailureThreshold></newFailureThreshold>
          <healthy></healthy>
          <unHealthy></unHealthy>
          <severityError>true</severityError>
          <severityWarning>true</severityWarning>
          <severityStyle>true</severityStyle>
          <severityPerformance>true</severityPerformance>
          <severityInformation>true</severityInformation>
          <severityNoCategory>true</severityNoCategory>
          <severityPortability>true</severityPortability>
        </configSeverityEvaluation>
        <configGraph>
          <xSize>500</xSize>
          <ySize>200</ySize>
          <numBuildsInGraph>30</numBuildsInGraph>
          <displayAllErrors>true</displayAllErrors>
          <displayErrorSeverity>true</displayErrorSeverity>
          <displayWarningSeverity>true</displayWarningSeverity>
          <displayStyleSeverity>true</displayStyleSeverity>
          <displayPerformanceSeverity>true</displayPerformanceSeverity>
          <displayInformationSeverity>true</displayInformationSeverity>
          <displayNoCategorySeverity>true</displayNoCategorySeverity>
          <displayPortabilitySeverity>true</displayPortabilitySeverity>
        </configGraph>
      </cppcheckConfig>
    </org.jenkinsci.plugins.cppcheck.CppcheckPublisher>
""")


def enableCppcheck(config, checkoutSteps, **kwargs):
    if 'CONFIG_JENKINS_ENABLE_CPPCHECK' in os.environ:
        root = ElementTree.fromstring(config)
        publishers = root.find("publishers")
        if publishers is not None:
            cppcheckPublisher = publishers.find("org.jenkinsci.plugins.cppcheck.CppcheckPublisher")
            if cppcheckPublisher is not None:
                publishers.remove(cppcheckPublisher)
            publishers.append(CPPCHECK_PLUGIN)

        builders = root.find("builders")
        if builders is not None:
            for copyArtifact in builders.iter("hudson.plugins.copyartifact.copyArtifact"):
                if copyartifact.find("project").text == "additional-kw-scripts":
                    builders.remove(copyartifact)
            builders.append(CPPCHECK_CHECKOUT)
            for hudsonshell in builders.iter("hudson.tasks.Shell"):
                if hudsonshell.find("command").text[:11] == "#cppcheck":
                    builders.remove(hudsonshell)
            builders.append(CPPCHECK_BUILDSTEP)

        config = ElementTree.tostring(root, encoding="UTF-8")
    return config


manifest = {
    'apiVersion': "0.4",
    'hooks': {
        'jenkinsJobCreate': enableCppcheck,
        'jenkinsJobPostUpdate': enableCppcheck
    }
}
