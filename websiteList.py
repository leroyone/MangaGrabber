#!/usr/bin/python

import urllib2
from lxml import html
import os
import re

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

    def nameFixer(self, nameToFix):
        nameToFix = re.sub('[^a-zA-Z0-9 ]', '', nameToFix)
        return re.sub(' ', '-', nameToFix)
    
    def whichChapters(self, startChapter, endChapter):
        '''
        downloads chapters from within range
        '''
        mangaName = self.nameFixer(self.selection[0])
        os.mkdir(mangaName)
        for i in range(startChapter-1,endChapter):
            self.imageGrabber(self.chapterList[i], mangaName, i)

class Manganelo(Website):
    """docstring for Manganelo"""
    def __init__(self):
        self.searchResults = []
        self.selection = []
        self.chapterList = []
    
    def search(self, searchTerm):
        '''
        searchTerm = string
        saves a list of search results
        '''
        searchTerm = searchTerm.replace(' ', '_')
        page = self.webPageOpener('https://manganelo.com/search/' + searchTerm)
        pageTree = html.fromstring(page)
        namesList = pageTree.xpath('//span[@class="item-name"]/a/text()')
        linksList = pageTree.xpath('//span[@class="item-name"]/a/@href')
        #linksList = ['https:' + each for each in linksList]
        self.searchResults = zip(namesList,linksList)

    def chapterListMaker(self):
        '''
        saves list of chapter links
        '''
        contentsPageLink = self.selection[1]
        contentsPage = self.webPageOpener(contentsPageLink)
        contentsTree = html.fromstring(contentsPage)
        ChapterLinkList = contentsTree.xpath('//div[@class="chapter-list"]//@href')
        ChapterNamesList = contentsTree.xpath('//div[@class="chapter-list"]//a/text()')
        #resultingChapterList = ['https:' + link for link in resultingChapterList]
        resultingChapterList = zip(ChapterLinkList, ChapterNamesList)
        resultingChapterList.reverse()
        self.chapterList = resultingChapterList

    def imageGrabber(self, chapterPage, nameOfFile, chapterNumber):
        '''
        chapterPage: address of chapter
        downloads images into a folder
        '''
        nameCounter = 111111
        chapterSource = self.webPageOpener(chapterPage[0])
        tree = html.fromstring(chapterSource)
        chapTitle = self.nameFixer(chapterPage[1])
        chapTitle = '%s-%s' % (10001 + chapterNumber, chapTitle)
        chapTitle = '{0}/{1}'.format(nameOfFile, chapTitle)
        os.mkdir(chapTitle)
        '''
        chapTitle = str(10001 + chapterNumber) + '-' + chapTitle

        chapTitle = nameOfFile + '/' + chapTitle
        os.system('mkdir ' + chapTitle)
        imageLink = tree.xpath('//img[@class="fullsizable"]/@src')
        for each in range(len(imageLink)):
            if len(imageLink[each]) > 0 and imageLink[each][:2] == '//':
                imageLink[each] = 'https:' + imageLink[each]
            if 'http' in imageLink[each]:
                os.system('wget -P ' + chapTitle + ' ' + imageLink[each])
                oldName = imageLink[each][imageLink[each].rindex('/'):]
                if 'jpg' in imageLink[each] or 'jpeg' in imageLink[each]:
                    newName = str(nameCounter) + '.jpg'
                elif 'png' in imageLink[each]:
                    newName = str(nameCounter) + '.png'
                else:
                    print 'Unknown image type'
                    break
                os.system('mv ' + chapTitle + '/' + oldName + ' ' + chapTitle + '/' + newName)
                nameCounter += 1
            else:
                missing.append([chapTitle, chapterNumber, each, str(nameCounter)])
                nameCounter += 1
        return missing
        '''

first = Manganelo()

searchString = raw_input('...and what Manga would you like to search for today?\n\n')

first.search(searchString)
first.printSearch()

selection = int(raw_input('\nWe have found {0} popular results.\nWhich Manga would you like to try? (1-{0})\n'.format(len(first.searchResults)) ) )-1

first.selection = first.searchResults[selection]
first.chapterListMaker()

print 'There are %s chapters available for "%s".' % (len(first.chapterList), first.selection[0])
print 'Which chapters would you like to download?\n'
startChapter = int(raw_input('Starting chapter:\n'))
endChapter = int(raw_input('\nEnd chapter:\n'))

first.whichChapters(startChapter, endChapter)