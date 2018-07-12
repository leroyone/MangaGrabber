#!/usr/bin/python

import urllib2
from lxml import html
import os
#from tools import *

class Website(object):
    """docstring for Website"""
    def __init__(self):
        pass

    def webPageOpener(self, webPage):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        attempt = 1
        while True:
            try:
                x = opener.open(webPage).read()
                break
            except urllib2.URLError:
                print 'Reconnection attempt: ' + str(attempt)
                attempt += 1
        return x

    def printSearch(self):
        count = 1
        for each in self.searchResults:
            print '%s) %s' % (count, each[0])
            count += 1


class Manganelo(Website):
    """docstring for Manganelo"""
    def __init__(self):
        self.searchResults = []
    
    def search(self, searchTerm):
        '''
        searchTerm = string
        '''
        searchTerm = searchTerm.replace(' ', '_')
        page = self.webPageOpener('https://manganelo.com/search/' + searchTerm)
        pageTree = html.fromstring(page)
        namesList = pageTree.xpath('//span[@class="item-name"]/a/text()')
        linksList = pageTree.xpath('//span[@class="item-name"]/a/@href')
        linksList = ['https:' + each for each in linksList]
        self.searchResults = zip(namesList,linksList)

first = Manganelo()
first.search('youkai')
first.printSearch()
