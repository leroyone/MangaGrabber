#!/usr/bin/python

import urllib2
from lxml import html
import os
import re
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
            print '%s) %s' % (count, each)
            count += 1

    def nameFixer(self, nameToFix):
        nameToFix = re.sub('[a-zA-Z0-9 ', '', nameToFix)
        return re.sub(' ', '-', nameToFix)

class Manganelo(Website):
    """docstring for Manganelo"""
    def __init__(self):
        self.searchResults = []
        self.chapterList = []
    
    def search(self, searchTerm):
        '''
        searchTerm = string
        '''
        searchTerm = searchTerm.replace(' ', '_')
        page = self.webPageOpener('https://manganelo.com/search/' + searchTerm)
        pageTree = html.fromstring(page)
        namesList = pageTree.xpath('//span[@class="item-name"]/a/text()')
        linksList = pageTree.xpath('//span[@class="item-name"]/a/@href')
        #linksList = ['https:' + each for each in linksList]
        self.searchResults = zip(namesList,linksList)

    def chapterListMaker(self, contentsPageLink):
        '''
        contentsPage: address for a manga contents page
        returns a list of chapter links
        '''
        contentsPage = self.webPageOpener(contentsPageLink)
        contentsTree = html.fromstring(contentsPage)
        resultingChapterList = contentsTree.xpath('//div[@class="chapter-list"]//@href')
        #resultingChapterList = ['https:' + link for link in resultingChapterList]
        resultingChapterList.reverse()
        self.chapterList = resultingChapterList

first = Manganelo()

searchString = raw_input('...and what Manga would you like to search for today?\n\n')

first.search(searchString)
first.printSearch()

selection = int(raw_input('\nWe have found {0} popular results.\nWhich Manga would you like to try? (1-{0})\n'.format(len(first.searchResults)) ) )-1

first.chapterListMaker(first.searchResults[selection][1])

for each in first.chapterList:
    print each