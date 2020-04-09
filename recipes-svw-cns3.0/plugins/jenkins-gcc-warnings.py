
from xml.etree import ElementTree

PLUGIN = ElementTree.fromstring("""
    <hudson.plugins.warnings.WarningsPublisher plugin="warnings@4.56">
      <healthy/>
      <unHealthy/>
      <thresholdLimit>low</thresholdLimit>
      <pluginName>[WARNINGS] </pluginName>
      <defaultEncoding/>
      <canRunOnFailed>false</canRunOnFailed>
      <usePreviousBuildAsReference>false</usePreviousBuildAsReference>
      <useStableBuildAsReference>false</useStableBuildAsReference>
      <useDeltaValues>false</useDeltaValues>
      <thresholds plugin="analysis-core@1.79">
        <unstableTotalAll/>
        <unstableTotalHigh/>
        <unstableTotalNormal/>
        <unstableTotalLow/>
        <unstableNewAll/>
        <unstableNewHigh/>
        <unstableNewNormal/>
        <unstableNewLow/>
        <failedTotalAll/>
        <failedTotalHigh/>
        <failedTotalNormal/>
        <failedTotalLow/>
        <failedNewAll/>
        <failedNewHigh/>
        <failedNewNormal/>
        <failedNewLow/>
      </thresholds>
      <shouldDetectModules>false</shouldDetectModules>
      <dontComputeNew>true</dontComputeNew>
      <doNotResolveRelativePaths>true</doNotResolveRelativePaths>
      <includePattern/>
      <excludePattern/>
      <messagesPattern/>
      <parserConfigurations/>
      <consoleParsers>
        <hudson.plugins.warnings.ConsoleParser>
          <parserName>GNU C Compiler 4 (gcc)</parserName>
        </hudson.plugins.warnings.ConsoleParser>
      </consoleParsers>
    </hudson.plugins.warnings.WarningsPublisher>
""")

def checkWarnings(config, checkoutSteps, **kwargs):
    found = False
    for s in checkoutSteps:
        if "git" in s.getScript(): found = True

    if found:
        root = ElementTree.fromstring(config)
        publishers = root.find("publishers")
        if publishers.find("hudson.plugins.warnings.WarningsPublisher") is None:
            publishers.append(PLUGIN)
            config = ElementTree.tostring(root, encoding="UTF-8")

    return config

manifest = {
    'apiVersion' : "0.4",
    'hooks' : {
        'jenkinsJobCreate' : checkWarnings,
        'jenkinsJobPostUpdate' : checkWarnings
    }
}
