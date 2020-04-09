#!/usr/bin/python
# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt

class PieFunction:
    def __init__(self):
        pass

    def draw(self, labels, quants, expl, colors, title, image):
        plt.figure(1, figsize=(8,8))
        plt.pie(quants, explode=expl, colors=colors, labels=labels, autopct='%1.1f%%',pctdistance=0.8, shadow=True)
        plt.title(title, bbox={'facecolor':'0.8', 'pad':5})
        plt.savefig(image)
        plt.close()
