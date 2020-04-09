from xml.etree import ElementTree
import os

PLUGIN = ElementTree.fromstring("""
<org.jvnet.hudson.plugins.groovypostbuild.GroovyPostbuildRecorder plugin="groovy-postbuild@2.3.1">
<script plugin="script-security@1.24">
<script>def log = manager.build.logFile.text
def uploads = log =~ /(?&lt;=\+\sBOB_REMOTE_ARTIFACT=).*/
def name = log =~ /(?&lt;=\+\sBOB_LOCAL_ARTIFACT=).*/
def summary = manager.createSummary('package.png')
def externalDownloadUrl = 'http://artefact-host.mib3.technisat-digital/'

def uploadList = []
for (i = 0; i &lt; uploads.size(); i++) {
  uploadList.add("${name[i]} - ${uploads[i]}")
  summary.appendText("${name[i]}: &lt;a name='download' href='${externalDownloadUrl}/${uploads[i]}'&gt;DOWNLOAD&lt;/a&gt;&lt;br /&gt;" , false)
}
if (uploads.size() == 0) {
  summary.appendText("No upload in this build - maybe artefacts already exist!", false)
} else {
  manager.addBadge('save.gif',uploadList.join("\\n\\n"),"/job/" + manager.getEnvVariable('JOB_NAME') + "/" + manager.getEnvVariable('BUILD_ID') + '#download')
}
</script>
<sandbox>true</sandbox>
</script>
<behavior>0</behavior>
<runForMatrixParent>false</runForMatrixParent>
</org.jvnet.hudson.plugins.groovypostbuild.GroovyPostbuildRecorder>
""".encode('utf-8'))


def uploadBadge(config, name, prefix, **kwargs):
    if 'CONFIG_JENKINS_UPLOAD_BADGE' in os.environ:
        if not name.startswith(prefix + 'zr3-variant'):
            return config
        root = ElementTree.fromstring(config)

        publishers = root.find("publishers")
        if publishers is not None:
            groovyPublisher = publishers.find("org.jvnet.hudson.plugins.groovypostbuild.GroovyPostbuildRecorder")
            if groovyPublisher is None:
                publishers.append(PLUGIN)

        config = ElementTree.tostring(root, encoding="UTF-8")

    return config

manifest = {
    'apiVersion' : "0.4",
    'hooks' : {
        'jenkinsJobCreate' : uploadBadge,
        'jenkinsJobPostUpdate' : uploadBadge
    }
}
