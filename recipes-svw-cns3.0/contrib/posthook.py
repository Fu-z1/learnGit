#!/usr/bin/env python3 
import sys
import os
import gzip
import json
from abc import abstractmethod


class Handler:
    def __init__(self, next=None):
        self._next = next

    @abstractmethod
    def handle(self):
        pass


class PublishHandler(Handler):
    '''
    create the symbol link to the build artifact which already uploaded
    in the repo, so user could access the daily build easily via http
    '''

    # ugly way to get url of upload server
    UPLOAD_URL = "http://10.57.9.156:82/cns-artefacts/"

    def action(self, results):

        for result in results:
            gzaudit = os.path.join(result, '../', 'audit.json.gz')
            with gzip.open(gzaudit) as jfaudit:
                audit = json.loads(jfaudit.read().decode('utf-8'))
                build_id = audit["artifact"]["build-id"]
                binary_url = self.UPLOAD_URL + build_id[:2] + "/" + \
                    build_id[2:4] + "/" + build_id[4:] + "-1.tgz"

            print(binary_url)

    def handle(self, results):

        # publish binary only built by jenkins
        if os.environ.get('USER', 'NOUSER') == 'jenkins':
            if results[0] == 'success':
                print("Handling in {}".format(self.__class__.__name__))
                self.action(results[1:])
            else:
                print('Skip handle in {} due to build status {}'.format(
                    self.__class__.__name__, results[0]))
        else:
            self.action(results[1:])

        if self._next:
            self._next.handle(results)


# TODO
class NotifyHandler(Handler):

    ''' mail notification may be placed here '''
    def handle(self, results):
        pass

        if self._next:
            self._next.handle(results)


# TODO
class ReleaseNoteHandler(Handler):

    ''' generate release note here '''
    def handle(self, results):
        pass

        if self._next:
            self._next.handle(results)


if __name__ == "__main__":
    
    handler = PublishHandler()
    handler.handle(sys.argv[1:])

