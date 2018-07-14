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
        folderName = self.nameFixer(self.mangaName)
        print folderName
        os.mkdir(folderName)
        for i in range(startChapter-1, endChapter):
            chapterPath = self.chapterPath(folderName, self.chapterList[i][1], i)
            os.mkdir(chapterPath)
            images = self.getImageLinks(self.chapterList[i])
            self.saveChapters(images, chapterPath)

    def chapterPath(self, folderName, chapterName, chapterNumber):
        chapTitle = self.nameFixer(chapterName)
        chapTitle = '%s-%s' % (10000 + chapterNumber, chapTitle)
        chapTitle = '%s/%s' % (folderName, chapTitle)
        return chapTitle

    def saveChapters(self, images, chapterPath):
        for imageLink in images:
            imagePath = '%s/%s' % (chapterPath, 10001 + images.index(imageLink))
            if 'http' in imageLink and 'jpg' in imageLink or 'jpeg' in imageLink:
                image = self.webPageOpener(imageLink)
                with open('%s.jpg' % imagePath, 'wb') as f:
                    f.write(image)
            elif 'http' in imageLink and 'png' in imageLink:
                image = self.webPageOpener(imageLink)
                with open('%s.png' % imagePath, 'wb') as f:
                    f.write(image)
            else:
                self.missingPages.append('Page %s in %s' % (images.index(imageLink), chapterPath))

class Manganelo(Website):
    """docstring for Manganelo"""
    def __init__(self):
        self.mangaLink = ''
        self.mangaName = ''
        self.searchResults = []
        self.chapterList = []
        self.missingPages = []
    
    def selectionMade(self, selection):
        self.mangaLink = self.searchResults[selection][1]
        self.mangaName = self.searchResults[selection][0]

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
        contentsPage = self.webPageOpener(self.mangaLink)
        contentsTree = html.fromstring(contentsPage)
        ChapterLinkList = contentsTree.xpath('//div[@class="chapter-list"]//@href')
        ChapterNamesList = contentsTree.xpath('//div[@class="chapter-list"]//a/text()')
        #resultingChapterList = ['https:' + link for link in resultingChapterList]
        resultingChapterList = zip(ChapterLinkList, ChapterNamesList)
        resultingChapterList.reverse()
        self.chapterList = resultingChapterList

    def getImageLinks(self, chapterPage):
        '''
        chapterPage: address of chapter
        returns: list of image links
        '''
        chapterSource = self.webPageOpener(chapterPage[0])
        tree = html.fromstring(chapterSource)
        images = tree.xpath('//img[@class="img_content"]/@src')
        return images

first = Manganelo()

searchString = raw_input('...and what Manga would you like to search for today?\n\n')

first.search(searchString)
first.printSearch()

selection = int(raw_input('\nWe have found {0} popular results.\nWhich Manga would you like to try? (1-{0})\n'.format(len(first.searchResults)) ) )-1

first.selectionMade(selection)
first.chapterListMaker()

print 'There are %s chapters available for "%s".' % (len(first.chapterList), first.mangaName)
print 'Which chapters would you like to download?\n'
startChapter = int(raw_input('Starting chapter:\n'))
endChapter = int(raw_input('\nEnd chapter:\n'))

first.whichChapters(startChapter, endChapter)