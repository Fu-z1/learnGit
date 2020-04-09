#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess as sp
import argparse
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from string import Template

def send_email(receivers, email_message):
    mail_host="smtpnin.cn.prehgad.local"
    mail_user="gitlab.jpcc"
    sender = 'gitlab.jpcc@preh.cn'
    receiver_list = "; ".join(receivers)
    
    message = MIMEText(email_message,'html','utf-8')
    message['From'] = Header("Gitlab JPCC", 'utf-8')
    message['To'] = receiver_list

    subject = 'Gitlab Repository Commit Update'
    message['Subject'] = Header(subject, 'utf-8')

    smtpObj = smtplib.SMTP() 
    smtpObj.connect(mail_host, 25)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print ">> \033[92mSucceed send email   to: %s\033[0m"%("; ".join(receivers))

def git_diff(commit1, commit2):
    file_list = []
    cmd = ['git', 'diff', '--name-only', commit1, commit2]
    out = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
    lines = out.stdout.readlines()
    for line in lines:
        file = line.strip()
        file_list.append(file)
    return file_list

def get_changes(commit1, commit2, file):
    paragraph = ""
    cmd = ['git', 'diff', commit1, commit2, file]
    out = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
    while True:
        line = out.stdout.readline()
        if not line:
            break
        if line.startswith('diff --git'):
            print "\033[93m%s\033[0m"%line[:-1]
            info = "<font color=\"#D9B300\">%s</font><br/>"%(line[:-1].replace(" ", "&nbsp;"))
        elif line.startswith('-'):
            print "\033[91m%s\033[0m"%line[:-1]
            info = "<font color=\"#FF0000\">%s</font><br/>"%(line[:-1].replace(" ", "&nbsp;"))
        elif line.startswith('+'):
            print "\033[92m%s\033[0m"%line[:-1]
            info = "<font color=\"#00FF00\">%s</font><br/>"%(line[:-1].replace(" ", "&nbsp;"))
        elif line.startswith('@@'):
            print "\033[96m%s\033[0m"%line[:-1]
            info = "<font color=\"#0000FF\">%s</font><br/>"%(line[:-1].replace(" ", "&nbsp;"))
        else:
            print line[:-1]
            info = "<font color=\"#000000\">%s</font><br/>"%(line[:-1].replace(" ", "&nbsp;"))
        paragraph += info
    return paragraph

if __name__ == "__main__":
    
    git_dict = {"navigation/tsd-nav-vehiclestatus-api"             : "hu.yang@preh.cn",
                "vehicle-connectivity/canstack/tsd-canstack-api"   : "hu.yang@preh.cn",
                "phone/bt-organizer/tsd-organizer-mib3-api"        : "jianguang.sun@preh.cn",
                "navigation/tsd-nav-pos-gps-api"                   : "jianguang.sun@preh.cn",
                "media/mountingservice/tsd-media-mount-status-api" : "yi.liu@preh.cn"}
    
    parser = argparse.ArgumentParser(description='Judge specific recipe update')
    parser.add_argument("-u", "--upstream", required=True, type=str, help="Upstream commit SHA1, or the parent commit")
    parser.add_argument("-d", "--downstream", required=True, type=str, help="Downstream commit SHA1, or the latest commit")
    parser.add_argument("-b", "--branch", required=True, type=str, help="Branch name for git repository")
    parser.add_argument("-p", "--project", required=True, type=str, help="Git repository URL")
    args = parser.parse_args()
    
    upstream = args.upstream
    downstream = args.downstream
    branch = args.branch
    project = args.project
    
    content = '''
        <html>
        <head>
        <meta charset="UTF-8">
        </head>

        <body leftmargin="8" marginwidth="0" topmargin="8" marginheight="4"
            offset="0">
            <table width="95%" cellpadding="0" cellspacing="0"
                style="font-size: 11pt; font-family: Tahoma, Arial, Helvetica, sans-serif">
                <tr>
                    <td>(This email is triggered automatically.Please do not reply!!)</td>
                </tr>
                <tr>
                    <td><h2>
                            <font color="#0000FF">Changes in: ${RECIPE}</font>
                        </h2></td>
                </tr>
                <tr>
                    <td><br />
                    <b><font color="#0B610B">Project information</font></b>
                    <hr size="2" width="100%" align="center" /></td>
                </tr>
                <tr>
                    <td>
                        <ul>
                            <li>Project&nbsp;&nbsp;&nbsp;:&nbsp;${PROJECT}</li>
                            <li>Commits&nbsp;:&nbsp;${COMMITS}</li>
                            <li>Branch&nbsp;&nbsp;&nbsp;:&nbsp;${BRANCH}</li>
                        </ul>
                    </td>
                </tr>
                <tr>
                    <td><b><font color="#0B610B">Git Diff</font></b>
                    <hr size="2" width="100%" align="center" /></td>
                </tr>
                <tr>
                    <td>
                        <p>${PARAGRAPH}</p>
                    </td>
                </tr>
                <tr>
                    <td><hr size="2" width="100%" align="center" /></td>
                </tr>
            </table>
        </body>
        </html>
    '''
    
    email_template = Template(content)
    file_list = git_diff(upstream, downstream)
    for i in git_dict:
        receiver = ["jiahui.ying@preh.cn"]
        recipe = "recipes/" + i + ".yaml"
        if recipe in file_list:
            receiver.append(git_dict[i])
            commits = "http://" + project[4:-4].replace(":", "/") + "/commit/" + downstream
            
            print ">> \033[92mRecipes in: %s\033[0m"%recipe
            print ">> \033[92mCommits in: %s\033[0m"%commits
            print ">> \033[92mEmail   to: %s\033[0m"%("; ".join(receiver))
            para = get_changes(upstream, downstream, recipe)
            
            email_content = email_template.safe_substitute(RECIPE=recipe, PROJECT=project, COMMITS=commits, BRANCH=branch, PARAGRAPH=para)
            send_email(receiver, email_content)
        else:
            print ">> \033[91mNo changes for %s\033[0m"%recipe
