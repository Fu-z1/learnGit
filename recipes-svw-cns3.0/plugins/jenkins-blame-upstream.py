from xml.etree import ElementTree
import os

PLUGIN = ElementTree.fromstring("""
<jenkins.plugins.displayupstreamchanges.DisplayUpstreamChangesRecorder plugin="display-upstream-changes@0.3.2"/>
""")


def blameUpstream(config, checkoutSteps, **kwargs):
    if 'CONFIG_JENKINS_BLAME_UPSTREAM_COMMITS' in os.environ:
        root = ElementTree.fromstring(config)

        publishers = root.find("publishers")
        if publishers is not None:
            upstreamPublisher = publishers.find("jenkins.plugins.displayupstreamchanges.DisplayUpstreamChangesRecorder")
            if upstreamPublisher is None:
                publishers.append(PLUGIN)

        config = ElementTree.tostring(root, encoding="UTF-8")

    return config

manifest = {
    'apiVersion' : "0.4",
    'hooks' : {
        'jenkinsJobCreate' : blameUpstream,
        'jenkinsJobPostUpdate' : blameUpstream
    }
}
