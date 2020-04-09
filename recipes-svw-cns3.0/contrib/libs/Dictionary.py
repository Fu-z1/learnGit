#!/usr/bin/python
# -*- coding:utf-8 -*-


class DictFunction:
    def __init__(self, dict):
        self.dict = dict

    def rank_as_value_length(self):
        dictionay = self.dict
        rank_dict = sorted(dictionay.iteritems(),key=lambda a:len(a[1]),reverse=True)
        return rank_dict

    def rank_according_dict(self, role_dict, key):
        format_dict = {}
        dictionay = self.dict
        for i in dictionay:
            for j in dictionay[i]:
                for k in role_dict:
                    if not format_dict.has_key(k):
                        format_dict[k] = 0
                    if j[key].endswith(role_dict[k]):
                        format_dict[k] += 1
        return format_dict
    '''
    def rank_according_key(self, key, msg_key, exception_mgs):
        format_dict = {}
        dictionay = self.dict
        for i in dictionay:
            for j in dictionay[i]:
                if not format_dict.has_key(j[key]):
                    format_dict[j[key]] = []
                if not (j[msg_key]).startswith(exception_mgs):
                    format_dict[j[key]].append()  #not clear with this output
        return format_dict
    '''