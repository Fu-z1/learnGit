from xml.etree import ElementTree
import os

PLUGIN = ElementTree.fromstring("""
<hudson.plugins.emailext.ExtendedEmailPublisher plugin="email-ext@2.53">
<configuredTriggers>
<hudson.plugins.emailext.plugins.trigger.FailureTrigger>
<email>
<subject>$PROJECT_DEFAULT_SUBJECT</subject>
<body>$PROJECT_DEFAULT_CONTENT</body>
<recipientProviders>
<hudson.plugins.emailext.plugins.recipients.DevelopersRecipientProvider/>
<hudson.plugins.emailext.plugins.recipients.ListRecipientProvider/>
<hudson.plugins.emailext.plugins.recipients.UpstreamComitterRecipientProvider/>
</recipientProviders>
<attachmentsPattern/>
<attachBuildLog>false</attachBuildLog>
<compressBuildLog>false</compressBuildLog>
<replyTo>$PROJECT_DEFAULT_REPLYTO</replyTo>
<contentType>project</contentType>
</email>
</hudson.plugins.emailext.plugins.trigger.FailureTrigger>
<hudson.plugins.emailext.plugins.trigger.FixedTrigger>
<email>
<subject>$PROJECT_DEFAULT_SUBJECT</subject>
<body>$PROJECT_DEFAULT_CONTENT</body>
<recipientProviders>
<hudson.plugins.emailext.plugins.recipients.DevelopersRecipientProvider/>
<hudson.plugins.emailext.plugins.recipients.ListRecipientProvider/>
<hudson.plugins.emailext.plugins.recipients.UpstreamComitterRecipientProvider/>
</recipientProviders>
<attachmentsPattern/>
<attachBuildLog>false</attachBuildLog>
<compressBuildLog>false</compressBuildLog>
<replyTo>$PROJECT_DEFAULT_REPLYTO</replyTo>
<contentType>project</contentType>
</email>
</hudson.plugins.emailext.plugins.trigger.FixedTrigger>
</configuredTriggers>
<contentType>default</contentType>
<defaultSubject>$DEFAULT_SUBJECT</defaultSubject>
<defaultContent>$DEFAULT_CONTENT</defaultContent>
<attachmentsPattern/>
<presendScript>$DEFAULT_PRESEND_SCRIPT</presendScript>
<postsendScript>$DEFAULT_POSTSEND_SCRIPT</postsendScript>
<attachBuildLog>false</attachBuildLog>
<compressBuildLog>false</compressBuildLog>
<replyTo>$DEFAULT_REPLYTO</replyTo>
<saveOutput>true</saveOutput>
<disabled>false</disabled>
</hudson.plugins.emailext.ExtendedEmailPublisher>
""")


def sendMail(config, checkoutSteps, **kwargs):
    if 'CONFIG_JENKINS_SEND_MAIL' in os.environ:
        root = ElementTree.fromstring(config)

        publishers = root.find("publishers")
        if publishers is not None:
            upstreamPublisher = publishers.find("hudson.plugins.emailext.ExtendedEmailPublisher")
            if upstreamPublisher is None:
                publishers.append(PLUGIN)

        config = ElementTree.tostring(root, encoding="UTF-8")

    return config

manifest = {
    'apiVersion' : "0.4",
    'hooks' : {
        'jenkinsJobCreate' : sendMail,
        'jenkinsJobPostUpdate' : sendMail
    }
}
