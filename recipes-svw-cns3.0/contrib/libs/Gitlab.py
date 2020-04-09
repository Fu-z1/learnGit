#!/usr/bin/python
# -*- coding:utf-8 -*-

import gitlab
import os
import sys

class GitlabAPI:
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.gl = gitlab.Gitlab(self.url, self.token)

    def get_grp_list(self):
        grp_list = {}
        groups = self.gl.groups.list(all=True)
        for g in groups:
            grp_list[g.full_path] = g.id
        return grp_list

    def get_grp_id(self,grp):
        '''
        str1: full path of group, eg. "android/platform/packages/apps"
        '''
        group_id = (self.gl.groups.get(grp)).id
        return group_id

    def get_grp_projects(self,grp):
        '''
        str1: full path of group, eg. "android/platform/packages/apps"
        '''
        project_list = []
        group = self.gl.groups.get(grp)
        projects = group.projects.list(all=True)
        for p in projects:
            project_list.append(p.path_with_namespace)
        return project_list

    def add_grp_member(self, grp, member_id, access_level):
        '''
        access_level: could be gitlab.MASTER_ACCESS, gitlab.DEVELOPER_ACCESS ...
        str1: full path of group, eg: root/test-project
        str2: id of the member, eg. 1
        '''
        group = self.gl.groups.get(grp)
        member = group.members.create({'user_id': member_id, 'access_level':access_level})
        group.save()

    def delete_grp_member(self, grp, member_id):
        '''
        str1: full path of group, eg: root/test-project
        str2: id of the member, eg. 1
        '''
        group = self.gl.groups.get(grp)
        group.members.delete(member_id)
        group.save()

    def modify_grp_member(self, grp, member_id, access_level):
        '''
        access_level: could be gitlab.MASTER_ACCESS, gitlab.DEVELOPER_ACCESS ...
        str1: full path of group, eg: test/test-group
        str2: id of the member, eg. 1
        '''
        group = self.gl.groups.get(grp)
        member = group.members.get(member_id)
        member.access_level = access_level
        member.save()

    def get_grp_members(self, grp):
        '''
        str1: full path of group, eg: test/test-group
        '''
        member_list = []
        group = self.gl.groups.get(grp)
        members = group.members.list(all=True)
        for i in members:
            member_list.append(i.id)
        return member_list

    def get_commit_time(self, prj, commit):
        '''
        str1: full path of project
        str1: commit id
        '''
        project = self.gl.projects.get(prj)
        commits = project.commits.get(commit)
        return commits.committed_date
    
    def get_prj_commit(self, prj, br, start, end):
        '''
        str1: full path of project
        str2: branch name
        str3: the beginning time, should be in format "2019-01-09T16:59:41.000+08:00"
        str4: the ending time, should be in format "2019-01-09T16:59:41.000+08:00"
        '''
        commit_history = {}
        commit_history[prj] = []
        project = self.gl.projects.get(prj)
        commits = project.commits.list(all=True,ref_name=br, since=start, until=end)
        for i in range (len(commits)):
            user     = commits[i].author_name
            email    = commits[i].author_email
            title    = commits[i].title
            id       = commits[i].id
            date     = commits[i].committed_date

            commit_history[prj].append({"user"   :user, 
                                        "email"  :email, 
                                        "id"     :id, 
                                        "title"  :title, 
                                        "date"   :date,
                                        "branch" : br})
            
        return commit_history

    def get_latest_commit(self, prj, rev):
        '''
        prj: full path of project
        rev: revision name, maybe branch name or commit number
        '''
        project = self.gl.projects.get(prj)
        commits = project.commits.list(ref_name=rev)
        return commits[0].id

    def compare_prj_commits(self, prj, rev1, rev2):
        '''
        rev1: the former commit or tag or branch
        rev2: the latest commit or tag or branch
        '''
        project = self.gl.projects.get(prj)
        result = project.repository_compare(rev1, rev2)
        return result['commits']

    def compare_prj_files(self, prj, rev1, rev2):
        '''
        rev1: the former commit or tag or branch
        rev2: the latest commit or tag or branch
        '''
        diff_list = []
        project = self.gl.projects.get(prj)
        result = project.repository_compare(rev1, rev2)
        for file_diff in result['diffs']:
            diff_list.append(file_diff['diff'])
        return diff_list

    def create_grp(self,grp):
        '''
        str1: full path of group, eg. "android/platform/packages/apps"
        '''
        grp_list = self.get_grp_list()
        if grp_list.has_key(grp):
            print ">> \033[91mGroup : %s already exists!\n\033[0m\n"%grp
        else:
            group = grp.split('/')[-1]
            parent = '/'.join(grp.split('/')[:-1])
            if parent:
                if grp_list.has_key(parent):
                    parent_id = (self.gl.groups.get(parent)).id
                    self.gl.groups.create({'name'                  : group,
                                           'path'                  : group,
                                           'parent_id'             : parent_id,
                                           'visibility'            : 'internal',
                                           'lfs_enabled'           : True,
                                           'request_access_enabled': True})
                    print ">> \033[92mCreate Group : %s\n\033[0m\n"%grp
                else:
                    self.create_grp(parent)
                    self.create_grp(grp)
            else:
                self.gl.groups.create({'name'                  : group,
                                       'path'                  : group,
                                       'visibility'            : 'internal',
                                       'lfs_enabled'           : True,
                                       'request_access_enabled': True})
                print ">> \033[92mCreate Group : %s\n\033[0m\n"%grp

    def remove_grp(self,grp):  #input full path of group
        group_id = (self.gl.groups.get(grp)).id
        self.gl.groups.delete(group_id)
        print ">> \033[92mRemove Group : %s\n\033[0m"%grp

    def update_prj_visibility(self, prj, visibility):
        '''
        str1: full path of project, eg: root/test-project
        str2: visibility level, could be private, internal, public
        '''
        project = self.gl.projects.get(prj)
        print ">>  %s"%(project.visibility)
        project.visibility = visibility
        project.save()
        print ">>   %s"%(project.visibility)

    def update_prj_lfs(self, prj, lfs):
        '''
        str1: full path of project, eg: root/test-project
        str2: lfs_enabled level, could be True, False
        '''
        project = self.gl.projects.get(prj)
        print ">>  %s"%(project.lfs_enabledd)
        project.lfs_enabled = lfs
        project.save()
        print ">>   %s"%(project.lfs_enabled)

    def update_prj_request_access(self, prj, request_access):
        '''
        str1: full path of project, eg: root/test-project
        str2: request_access_enabled level, could be True, False
        '''
        project = self.gl.projects.get(prj)
        print ">>  %s"%(project.request_access_enabled)
        project.request_access_enabled = request_access
        member = project.members.create({'user_id': 1, 'access_level':gitlab.MASTER_ACCESS})
        project.save()
        print ">>   %s"%(project.request_access_enabled)

    def add_prj_member(self, prj, member_id, access_level):
        '''
        access_level: could be gitlab.MASTER_ACCESS, gitlab.DEVELOPER_ACCESS ...
        str1: full path of project, eg: root/test-project
        str2: id of the member, eg. 1
        '''
        project = self.gl.projects.get(prj)
        member = project.members.create({'user_id': member_id, 'access_level':access_level})
        project.save()

    def modify_prj_member(self, prj, member_id, access_level):
        '''
        access_level: could be gitlab.MASTER_ACCESS, gitlab.DEVELOPER_ACCESS ...
        str1: full path of project, eg: root/test-project
        str2: id of the member, eg. 1
        '''
        project = self.gl.projects.get(prj)
        member = project.members.get(member_id)
        member.access_level = access_level
        member.save()

    def get_prj_members(self, prj):
        '''
        str1: full path of project, eg: root/test-project
        '''
        member_list = []
        project = self.gl.projects.get(prj)
        members = project.members.list(all=True)
        for i in members:
            member_list.append(i.id)
        return member_list

    def update_prj_status(self, prj, visibility, lfs, request_access):
        '''
        str1: full path of project, eg: root/test-project
        str2: visibility level, could be private, internal, public
        str3: lfs_enabled level, could be True, false
        str4: request_access_enabled level, ould be True, false
        '''
        project = self.gl.projects.get(prj)
        print ">>  %s %s %s"%(project.visibility, project.lfs_enabled, project.request_access_enabled)
        project.visibility = visibility
        project.lfs_enabled = lfs
        project.request_access_enabled = request_access
        member_list = self.get_prj_members(prj)
        if not 1 in member_list:
            member = project.members.create({'user_id': 1, 'access_level':gitlab.MASTER_ACCESS})
        project.save()
        print ">>   %s %s %s"%(project.visibility, project.lfs_enabled, project.request_access_enabled)

    def get_prj_list(self):
        prj_list = {}
        projects = self.gl.projects.list(all=True, as_list=False)
        for p in projects:
            prj_list[p.path_with_namespace] = p.id
        return prj_list

    def get_prj_id(self, prj):
        '''
        str1: full path of project, eg: root/test-project
        '''
        prj_id = (self.gl.projects.get(prj)).id
        return prj_id
        
    def create_prj(self, prj, grp):
        '''
        str1: project name, eg: test-project
        str1: full path of group, eg: android/platform/packages/apps
        '''
        prj_list = self.get_prj_list()
        if prj_list.has_key(grp + '/' + prj):
            print ">> \033[91mProject : %s already exists!\n\033[0m\n"%(grp + '/' + prj)
        else:
            if grp:
                grp_list = self.get_grp_list()
                if grp_list.has_key(grp):
                    group_id = (self.gl.groups.get(grp)).id
                    self.gl.projects.create({'name'                  : prj,
                                             'path'                  : prj,
                                             'namespace_id'          : group_id,
                                             'visibility'            : 'internal',
                                             'lfs_enabled'           : True,
                                             'request_access_enabled': True})
                    print ">> \033[92mCreate Project : %s\n\033[0m"%prj
                else:
                    self.create_grp(grp)
                    self.create_prj(prj, grp)
            else:
                self.gl.projects.create({'name'                  : prj,
                                         'path'                  : prj,
                                         'visibility'            : 'internal',
                                         'lfs_enabled'           : True,
                                         'request_access_enabled': True})
                print ">> \033[92mCreate Project : %s\n\033[0m"%prj

    def remove_prj(self, prj):  #input full path of project
        prj_id = self.get_prj_id(prj)
        self.gl.projects.delete(prj_id)
        print ">> \033[91mRemove Project : %s\n\033[0m"%prj

    def list_branch(self, prj):
        prj_branch = {}
        prj_branch[prj] = []
        project = self.gl.projects.get(prj)
        branches = project.branches.list(all=True)
        for b in branches:
            prj_branch[prj].append(b.name)
        return prj_branch

    def create_branch(self, prj, br, ref):
        branch_list = self.list_branch(prj)
        if br not in branch_list[prj]:
            project = self.gl.projects.get(prj)
            branch = project.branches.create({'branch': br, 'ref': ref})
            print ">>   Create Branch : %s"%br
        else:
            print ">>   Branch %s already exists!!"%br

    def delete_branch(self, prj, br):
        branch_list = self.list_branch(prj)
        if br not in branch_list[prj]:
            print ">>   Branch doesn't exist: %s"%br
        else:
            project = self.gl.projects.get(prj)
            project.branches.delete(br)
            print ">>   Delete Branch : %s"%br

    def get_p_branch_list(self, prj):
        project = self.gl.projects.get(prj)
        p_branches_list = []
        p_branches = project.protectedbranches.list(all=True)
        for p_b in p_branches:
            p_branches_list.append(p_b.name)
        return p_branches_list

    def create_protect_branch(self, prj, br):
        project = self.gl.projects.get(prj)
        branch = project.protectedbranches.create({'name': br})
        print ">>   Protect Branch : %s"%br

    def delete_protect_branch(self, prj, br):
        project = self.gl.projects.get(prj)
        project.protectedbranches.delete(br)
        print ">>   Detete Protect Branch : %s"%br

    def set_default_branch(self, prj, br):
        branch_list = self.list_branch(prj)
        if br not in branch_list[prj]:
            print ">>  Branch doesn't exist: %s"%br
            sys.exit(-1)
        else:
            project = self.gl.projects.get(prj)
            project.default_branch = br
            project.save()
            print ">>   Set %s as default branch!!"%br

    def get_prj_tags(self, prj):
        tag_list = []
        project = self.gl.projects.get(prj)
        tags = project.tags.list()
        for i in tags:
            tag_list.append(i.name)
        return tag_list

    def create_tag(self, prj, tg, ref):
        project = self.gl.projects.get(prj)
        tags = self.get_prj_tags(prj)
        if tg not in tags:
            project.tags.create({'tag_name': tag, 'ref': ref})
            print ">>   Create Tag : %s"%tg
        else:
            print ">>   TAG %s already exists!!"%tg

    def delete_tag(self, prj, tg):
        project = self.gl.projects.get(prj)
        tags = self.get_prj_tags(prj)
        if tg in tags:
            project.tags.delete(tg)
            print ">>   Delete Tag : %s"%tg
        else:
            print ">>   TAG %s doesn't exist!!"%tg

    def disable_project_service(self, prj, serv):
        '''
        services could be :
        ['jira', 'pipelines-email', 'drone-ci', 'flowdock', 'buildkite', 
        'gemnasium', 'hipchat', 'assembla', 'redmine', 'mattermost', 
        'external-wiki', 'pushover', 'pivotaltracker', 'teamcity', 
        'custom-issue-tracker', 'builds-email', 'emails-on-push', 
        'slack', 'irker', 'asana', 'campfire', 'bamboo']
        '''
        project = self.gl.projects.get(prj)
        service = project.services.get(serv)
        print(service.active)
        service.delete()
        print ">>   Disable Service : %s"%serv

    def list_project_service(self, prj):
        project = self.gl.projects.get(prj)
        services = project.services.available()
        return services

    def list_deploy_keys(self):
        keys_dict = {}
        keys = self.gl.deploykeys.list()
        if not keys == []:
            for key in keys:
                keys_dict['id'] = key.id
                keys_dict['title'] = key.title
                keys_dict['key'] = key.key
                keys_dict['created_at'] = key.created_at
        return keys_dict

    def list_project_deploy_key(self, prj):
        project = self.gl.projects.get(prj)
        keys = project.keys.list()
        return keys

    def get_deploy_key(self, prj, key_id):
        project = self.gl.projects.get(prj)
        key = project.keys.get(key_id)
        return key

    def create_deploy_key(self, prj, key_path, key_title):
        project = self.gl.projects.get(prj)
        key = project.keys.create({'title': key_title,
                                   'key': open(key_path).read()})

    def delete_deploy_key(self, prj, key_id):
        project = self.gl.projects.get(prj)
        key = project.keys.get(key_id)
        key.delete()
        print ">>   Delete deploy key : %s"%key_id

    def enable_deploy_key(self, prj, key_id):
        project = self.gl.projects.get(prj)
        project.keys.enable(key_id)
        print ">>   Enable deploy key : %s"%key_id

    def get_user_list(self):
        usr_list = {}
        users = self.gl.users.list(all=True)
        for s in users:
            usr_list[s.username] = {'id'       : s.id,
                                    'name'     : s.name,
                                    'email'    : s.email,
                                    'is_admin' : s.is_admin}
        return usr_list

    def create_user(self, username, name, email, reset_password='true', **kargs):
        '''
        Creates a new user. Note only administrators can create new users. 
        Either password, reset_password, or force_random_password must be specified. 
        If reset_password and force_random_password are both false, then password is required.
        Note that force_random_password and reset_password take priority over password. 
        In addition, reset_password and force_random_password can be used together.
        
        Parameters:
        email (required) - Email
        username (required) - Username
        name (required) - Name
        password (optional) - Password
        reset_password (optional) - Send user password reset link - true or false(default)
        admin (optional) - User is admin - true or false (default)
        can_create_group (optional) - User can create groups - true or false
        projects_limit (optional) - Number of projects user can create
        skype (optional) - Skype ID
        linkedin (optional) - LinkedIn
        twitter (optional) - Twitter account
        website_url (optional) - Website URL
        organization (optional) - Organization name
        extern_uid (optional) - External UID
        provider (optional) - External provider name
        bio (optional) - User’s biography
        location (optional) - User’s location
        public_email (optional) - The public email of the user
        skip_confirmation (optional) - Skip confirmation - true or false (default)
        external (optional) - Flags the user as external - true or false (default)
        avatar (optional) - Image file for user’s avatar
        private_profile (optional) - User’s profile is private - true or false (default)
        shared_runners_minutes_limit (optional) - Pipeline minutes quota for this user 
        extra_shared_runners_minutes_limit (optional) - Extra pipeline minutes quota for this user 
        '''
        usr_list = self.get_user_list()
        if not usr_list.has_key(username):
            init_info = {'email'          : email, 
                         'username'       : username, 
                         'name'           : name, 
                         'reset_password' : reset_password}
            user_info = dict(init_info, **kargs)
            user = self.gl.users.create(user_info)
            return user.id
        else:
            print "User has already existed!"
            return usr_list[username]['id']

    def get_user(self, user_info):
        if isinstance(user_info,int):
            user = gl.users.get(user_info)
        elif isinstance(user_info,str):
            user = gl.users.list(username=username)[0]
        else:
            print "Please input the correct user info, only user_id or username is permitted!!"
            sys.exit(-1)
        if user:
            print user.name
            print user.email
            print user.id
            return user

    def update_user(self, user_info, **kargs):
        user = self.get_user(user_info)
        for k, v in kargs.items():
            setattr(user, k, v)
            print "Update %s to %s"%(k, v)
        user.save()

    def delete_user(self, user_info):
        user = self.get_user(user_info)
        user.delete()

    def block_user(self, user_info):
        user = self.get_user(user_info)
        user.block()

    def unblock_user(self, user_info):
        user = self.get_user(user_info)
        user.unblock()

