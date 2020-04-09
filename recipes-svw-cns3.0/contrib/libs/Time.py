#!/usr/bin/python
# -*- coding:utf-8 -*-


import datetime

class TimeFunction:
    def __init__(self):
        pass

    def get_current_time(self, format):
        '''
        format could be '%Y-%m-%dT%H:%M:%S.000+08:00'
        '''
        current_time = datetime.datetime.strftime(datetime.datetime.now(), format)
        return current_time

    def transfer_to_isoTime(self, str):
        '''
        str is the version of android, such as '201812031501'
        return a iso time format, such as '2018-12-03T15:00:01.000+08:00'
        '''
        iso_time = "%s.000+08:00"%datetime.datetime.strptime(str, "%Y%m%d%H%M%S").isoformat()
        return iso_time

    def get_current_week(self):
        current_week = ((datetime.date.today()).isocalendar())[1]
        return current_week

    def get_last_week(self):
        last_week = ((datetime.date.today()-datetime.timedelta(days=7)).isocalendar())[1]
        return last_week
