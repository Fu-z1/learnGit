#!/usr/bin/python
# -*- coding:utf-8 -*-

from atlassian import Confluence

class ConfluenceAPI:

#================================Get page info=================================#

    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        self.cf = Confluence(self.url, self.user, self.password)

    def if_page_exists(self, space, title):
        '''
        Check page exists
        :space: key for space, eg. "GSCMINTE"
        :title: Full name for Page, eg. "CNS3.0 VARIANT-DATA"
        '''
        return self.cf.page_exists(space, title)

    def get_page_ids(self, space, title):
        '''
        Provide content id from search result by title and space
        :space: key for space, eg. "GSCMINTE"
        :title: Full name for Page, eg. "CNS3.0 VARIANT-DATA"
        '''
        page_id =self.cf.get_page_id(space, title)
        return page_id

    def get_page_child_by_types(self, page_id):
        '''
        Provide content by type (page, blog, comment)
        :page_id: id of page, eg. '28542924'
        :return: a list of all page, including status,title,_expandable,extensions,_links,type,id
        '''
        info_list = self.cf.get_page_child_by_type(page_id, type='page', start=None, limit=None)
        for i in info_list:
            print ">>title: %s"%(i['title'])
            print ">>id: %s"%(i['id'])
            print ">>links: %s"%(i['_links']['self'])
            print ">>children: %s"%(i['_expandable']['children'])
        return info_list

    def get_page_spaces(self, title):
        '''
        title: Full name for Page, eg. "CNS3.0 VARIANT-DATA"
        '''
        page_id = get_page_id(self, space, title)
        space_name = confluence.get_page_space(page_id)
        return space_name

    def get_pages_by_title(self, space, title):
        '''
        Returns the list of labels on a piece of Content
        :space: key for space, eg. "GSCMINTE"
        :title: Full name for Page, eg. "CNS3.0 VARIANT-DATA"
        '''
        info_list = self.cf.get_page_by_title(space, title, start=None, limit=None)
        result = {}
        result['title'] = info_list['title']
        result['id'] = info_list['id']
        result['links'] = info_list['_links']['self']
        result['children'] = info_list['_expandable']['children']
        result['body'] = info_list['body']['storage']['value']
        
        print ">>title: %s"%(result['title'])
        print ">>id: %s"%(result['id'])
        print ">>links: %s"%(result['links'])
        print ">>children: %s"%(result['children'])
        print ">>body: %s"%(result['body'])
        
        return result

    def get_pages_by_id(self, page_id):
        '''
        Get page by ID
        :page_id: id of page, eg. '28542924'
        :return: A dict with information of status,space,_expandable,title,version,extensions,_links,type,id,history
        :expand: explicitly expand any or all of the following items relating to the returned content item(s):
                history, body, container, ancestors, children, descendants, space, version, metadata.
        '''
        info_list = self.cf.get_page_by_id(page_id, expand=None)
        info_body = self.cf.get_page_by_id(page_id, expand='body.storage')
        
        result = {}
        result['title'] = info_list['title']
        result['id'] = info_list['id']
        result['links'] = info_list['_links']['self']
        result['space'] = info_list['space']['name']
        result['body'] = info_body['body']['storage']['value']
        
        print ">>title: %s"%(result['title'])
        print ">>id: %s"%(result['id'])
        print ">>links: %s"%(result['links'])
        print ">>space: %s"%(result['space'])
        print ">>body: %s"%(result['body'])
        
        return result

    def get_pages_labels(self, page_id):
        '''
        page_id: id of page, eg. '28542924'
        return: A dict with information of 
        '''
        info_list = self.cf.get_page_labels(page_id, prefix=None, start=None, limit=None)
        return info_list

    def get_draft_pages_by_id(self, page_id):
        '''
        page_id: id of page, eg. '28542924'
        return: A dict with information of status,space,_expandable,title,version,extensions,_links,type,id,history
        '''
        info_list = self.cf.get_draft_page_by_id(page_id, status='draft')
        print ">>title: %s"%(info_list['title'])
        print ">>id: %s"%(info_list['id'])
        print ">>space: %s"%(info_list['space']['name'])
        print ">>CreatedBy: %s"%(info_list['history']['createdBy'])
        print ">>CreatedDate: %s"%(info_list['history']['createdDate'])
        return info_list

    def get_all_pages_by_labels(self, label):
        '''
        label: 
        return: 
        '''
        info_list = self.cf.get_all_pages_by_label(label, start=0, limit=50)
        return info_list

    def get_all_pages_from_spaces(self, space):
        '''
        space: key for space, eg. "GSCMINTE"
        return: 
        '''
        info_list = self.cf.get_all_pages_from_space(space, start=0, limit=500)
        return info_list

    def get_all_pages_from_space_trashes(self, space):
        '''
        space: key for space, eg. "GSCMINTE"
        return: 
        '''
        info_list = self.cf.get_all_pages_from_space_trash(space, start=0, limit=500, status='trashed')
        return info_list

    def get_all_draft_pages_from_spaces(self, space):
        '''
        space: key for space, eg. "GSCMINTE"
        return: 
        '''
        info_list = self.cf.get_all_draft_pages_from_space(space, start=0, limit=500, status='draft')
        return info_list

    def get_all_draft_pages_from_space_through_cqls(self, space):
        '''
        space: key for space, eg. "GSCMINTE"
        return: 
        '''
        info_list = self.cf.get_all_draft_pages_from_space_through_cql(space, start=0, limit=500, status='draft')
        return info_list

    def get_all_restictions_for_contents(self, content_id):
        '''
        content_id: 
        return: 
        '''
        info_list = self.cf.get_all_restictions_for_content(content_id)
        return info_list

#================================Page Actions=================================#

    def create_pages(self, space, title, body, parent_id):
        '''
        Create page from scratch
        :space: key for space, eg. "GSCMINTE"
        :title: Full name for Page, eg. "CNS3.0 VARIANT-DATA"
        :body: content of page, should be in HTML format, eg. "<p>test self.cf api</p>"
        :parent_id: parent page id, eg. "25068445", 
                   or should be None if would like to create the page in the root of the space
        :return: A dict of page information
        '''
        self.cf.create_page(space, title, body, parent_id=parent_id, type='page')

    def remove_pages(self, page_id):
        '''
        Remove page
        :page_id: id of page, eg. '28542924'
        :return: A dict of page information
        '''
        self.cf.remove_page(page_id, status=None)

    def update_pages(self, parent_id, page_id, title, body):
        '''
        Update page if already exist
        :parent_id: parent page id, eg. "25068445", 
                   or should be None if would like to create the page in the root of the space
        :page_id: id of page, eg. '28542924'
        :title: Full name for Page, eg. "CNS3.0 VARIANT-DATA"
        :body: content of page, should be in HTML format, eg. "<p>test self.cf api</p>"
        :return: A dict of page information
        '''
        self.cf.update_page(parent_id, page_id, title, body, type='page')

    def update_or_create_pages(self, parent_id, title, body):
        '''
        Update page or create page if it is not exists
        :parent_id: parent page id, eg. "25068445", 
                   or should be None if would like to create the page in the root of the space
        :title: Full name for Page, eg. "CNS3.0 VARIANT-DATA"
        :body: content of page, should be in HTML format, eg. "<p>test self.cf api</p>"
        :return: A dict of page information
        '''
        self.cf.update_or_create(parent_id, title, body)

    def get_pages_ancestors(self, page_id):
        '''
        Get page ancestors
        :page_id: id of page, eg. '28542924'
        :return: A list of page information with status,title,_expandable,extensions,_links,type,id
        '''
        info_list = self.cf.get_page_ancestors(page_id)
        ancestor_id = info_list[0]['id']
        ancestor_info = get_page_by_id(self, page_id)
        ancestor_name = ancestor_info['title']
        return ancestor_name

    def attach_files(self, filename, page_id, title, space, comment):
        # Attach (upload) a file to a page, if it exists it will update the
        # automatically version the new file and keep the old one
        '''
        filename: file real path
        page_id: id of page, eg. '28542924'
        title: page title
        space: space key
        comment: description for this attachment
        return: A dict of attachment information
        '''
        self.cf.attach_file(filename, page_id=page_id, title=title, space=space, comment=comment)

    def export_pages(self, page_id):
        '''
        Export page as PDF, api_version needs to be set to 'cloud' when exporting from Confluence Cloud.
        page_id: id of page, eg. '28542924'
        '''
        self.cf.export_page(page_id)

#================================Get spaces info=================================#

    def list_spaces(self):
        '''
        Get all spaces with provided limit
        Return : A list of space information with dicts of name,_expandable,_links,key,type,id
        '''
        info_list = self.cf.get_all_spaces(start=0, limit=500)
        for sp in info_list:
            print sp['name']
            print sp['id']
            print sp['key']
        return info_list

    def get_spaces(self, space_key):
        '''
        Get information about a space through space key
        Return: A dict with description,_expandable,homepage,_links,key,type,id,name
        '''
        info_list = self.cf.get_space(space_key, expand='description.plain,homepage')
        print info_list['id']
        print info_list['name']
        return info_list

#================================Users and Groups=================================#

    def list_groups(self):
        '''
        Get all groups from Confluence User management
        Return: A list with dict info of _links, type, name
        '''
        info_list = self.cf.get_all_groups(start=0, limit=1000)
        for grp in info_list:
            print grp['name']
        return info_list

    def list_group_members(self, group_name):
        '''
        Get a paginated collection of users in the given group
        '''
        info_list = self.cf.get_group_members(group_name=group_name, start=0, limit=1000)
        for usr in info_list:
            print usr['displayName']
        return info_list

    def get_user_details_by_usernames(self, username):
        '''
        Get information about a user through user name
        '''
        info_list = self.cf.get_user_details_by_username(username, expand=None)
        print info_list['displayName']
        return info_list

    def get_user_details_by_userkeys(self, userkey):
        '''
        Get information about a user through user key, eg."ff8081815d5453ae015d5456ed2c0026"
        '''
        info_list = self.cf.get_user_details_by_userkey(userkey, expand=None)
        print info_list['displayName']
        return info_list
