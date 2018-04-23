#!/usr/bin/python

import urllib2
from lxml import html
import os
from websiteList import *

''' 
To Do List:
    Create some graphic interface
    Retain the ability to work from command
    Organize folder structure
    Work in multiple website searches
    Create percentage bar
    Give option to update
    Give option to select which chapters to download
    Save information about previous downloads and searches
'''
def webPageOpener(webPage):
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

######### Do a Search ###########

def searchSite(searchTerm):
    ''' 
    searchTerm: (+) concatenated string
    returns a list of tuples with search results (name, page-link)
    '''
    kissPage = webPageOpener('https://kiss-manga.com/search?type=all&query=' + searchTerm)
    kissTree = html.fromstring(kissPage)
    namesKissList = kissTree.xpath('//a[@class="manga-name"]/text()')
    linksKissList = kissTree.xpath('//a[@class="manga-name"]/@href')
    kissResults = zip(namesKissList,linksKissList)
    return kissResults

def retrieveTheImages(missing,page):
    stillMissing = []
    
    scratchPage = webPageOpener(page)
    scratchTree = html.fromstring(scratchPage)
    
    chapterList = scratchTree.xpath('//div[@class="list_chapters"]//a/@href')
    clear()
    chapterList.reverse()
    chapNum = 999999999
    for each in missing:
        if each[1] != chapNum:
            chapNum = each[1]
            chapScratch = webPageOpener('https://kiss-manga.com' + chapterList[chapNum])
            chapTree = html.fromstring(chapScratch)
        imageLinksList = chapTree.xpath('//img[@class="fullsizable"]/@src')
        if each[2] in range(len(imageLinksList)):
            imageLink = imageLinksList[each[2]]
            os.system('wget -P ' + each[0] + ' ' + imageLink)
            oldName = imageLink[imageLink.rindex('/'):]
            if 'jpg' in imageLink or 'jpeg' in imageLink:
                newName = each[3] + '.jpg'
            elif 'png' in imageLink:
                newName = each[3] + '.png'
            else:
                print 'Unknown image type'
                break
            os.system('mv ' + each[0] + '/' + oldName + ' ' + each[0] + '/' + newName)
        else:
            stillMissing.append(each)
    return stillMissing

def searchKissManga(missing, searchTerm):
    scratchPage = webPageOpener('https://kiss-manga.com/search?type=all&query=' + searchTerm)
    scratchTree = html.fromstring(scratchPage)
    namesScratchList = scratchTree.xpath('//a[@class="manga-name"]/text()')
    linksScratchList = scratchTree.xpath('//a[@class="manga-name"]/@href')
    searchResults = zip(namesScratchList,linksScratchList)
    
    clear()
    for each in range(len(searchResults)):
        print str(each) + ') ' + searchResults[each][0]
    selection = int(raw_input('\nWhich one...?'))
    raw_input('\n\nIs this correct...?\n\n(' + searchResults[selection][0] + ')')
    stillMissing = retrieveTheImages(missing,'https://kiss-manga.com' + searchResults[selection][1])
    return stillMissing

def checkResultsPageCount(scratchPage):
    '''
    returns total number of pages of search results
    '''
    if 'class="last"' in scratchPage:
        scratchPage = scratchPage[scratchPage.index('class="last"'):]
        scratchPage = scratchPage[scratchPage.index('page=')+5:]
        resPageCount = scratchPage[:scratchPage.index('"')]
        return int(resPageCount)
    else:
        return 0

############## Get the Images ###################


def chapterListMaker(homePage):
    '''
    homePage: address for a manga main page
    returns a list of chapter links
    '''
    kissHomePage = webPageOpener(homePage)
    kissHomeTree = html.fromstring(kissHomePage)
    chapterList = kissHomeTree.xpath('//div[@class="list_chapters"]//@href')
    resultingChapterList = ['https://kiss-manga.com' + link for link in chapterList]
    resultingChapterList.reverse()
    return resultingChapterList

def chapterTitle(chapterPage):
    '''
    chapterPage: address of chapter
    returns chapter name as str
    '''
    chapterPage = webPageOpener(chapterPage)
    chapterPage = chapterPage[chapterPage.index('<h1>')+4:]
    return chapterPage[:chapterPage.index('</h1>')]

def nameFixer(nameToFix):
    nameToFix = nameToFix.replace(' ','-')
    nameToFix = nameToFix.replace('&#39;','')
    nameToFix = nameToFix.replace('&quot;','')
    nameToFix = nameToFix.replace('#','')
    nameToFix = nameToFix.replace('&','')
    nameToFix = nameToFix.replace(';','')
    nameToFix = nameToFix.replace(':','')
    nameToFix = nameToFix.replace("'","")    
    nameToFix = nameToFix.replace('"','')
    nameToFix = nameToFix.replace('(','')
    nameToFix = nameToFix.replace(')','')
    return nameToFix

def imageGrabber(chapterPage, nameOfFile, chapterNumber):
    '''
    chapterPage: address of chapter
    downloads images into a folder
    '''
    missing = []
    nameCounter = 111111
    chapterSource = webPageOpener(chapterPage)
    tree = html.fromstring(chapterSource)
    chapTitle = tree.xpath('//div[@class="series__title"]/h1/text()')
    chapTitle = nameFixer(chapTitle[0])
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

def whichChapters(startChapter, endChapter, chapterList, nameOfFile):
    '''
    downloads chapters from within range
    '''
    missingPages = []
    os.system('mkdir ' + nameOfFile)
    for i in range(startChapter-1,endChapter):
        missingPages += imageGrabber(chapterList[i], nameOfFile, i)
    return missingPages

def getnameOfFile():
    a = raw_input('What would you like to name the file?\n')
    a = nameFixer(a)
    return a

def turnIntoCBZ(nameOfFile):
    os.system('cd ' + nameOfFile + ' ; zip -r ' + nameOfFile + ' ./*')
    os.system('mv ' + nameOfFile + '/' + nameOfFile + '.zip ./' + nameOfFile + '.cbz')
    os.system('rm -r ' + nameOfFile + '/')

def clear():
    os.system('clear')

def getMissing(missing, searchString):
    clear()
    for each in missing:
        print each
    goGetEm = raw_input('\nThese pages are missing. Do you want to search another site? (Y/n)\n')
    if goGetEm in ('Y','y'):
        stillMissing = searchKissManga(missing, searchString)
    return stillMissing

def commandLineRun():
    clear()
    searchStringOriginal = raw_input('...and what Manga would you like to search for today?\n\n')
    searchString = searchStringOriginal.replace(' ', '+')
    searchResults = searchSite(searchString)
    clear()
    count = 1
    for eachResult in searchResults:
        print str(count) + ') ' + eachResult[0]
        count += 1
    ########################### stick a try in here!!! ###############################
    if len(searchResults) > 0:
        foundText = '\nWe have found ' + str(len(searchResults)) + ' popular results.\nWhich Manga would you like to try? (1-' + str(len(searchResults)) + ')\n'
    else:
        raw_input('We have found no results for "' + searchStringOriginal + '"\nPlease try again.\n')
        commandLineRun()
        return
    selection = int(raw_input(foundText))-1
    thisManga = searchResults[selection]
    mangaName = thisManga[0]
    clear()
    confirm = raw_input('You would like to try "' + mangaName + '"? (Y/n) ')
    if confirm == 'n' or confirm == 'N':
        print '\nThen why did you select it...?\n'
        return
    chapterList = chapterListMaker('https://kiss-manga.com' +thisManga[1])
    clear()
    print 'There are ' + str(len(chapterList)) + ' chapters available for "' + mangaName + '".'
    print 'Which chapters would you like to download?\n'
    startChapter = int(raw_input('Starting chapter:\n'))
    endChapter = int(raw_input('\nEnd chapter:\n'))
    clear()
    print 'Ready to download chapters ' + str(startChapter) + ' to ' + str(endChapter) + ' from ' + mangaName + '.\n\n'
    nameOfFile = getnameOfFile()
    missingPages = whichChapters(startChapter, endChapter, chapterList, nameOfFile)
    if len(missingPages) >0:
        clear()
        for each in missingPages:
            print each
        print '\nThese pages are missing...\n'
        raw_input('Press enter to zip me up and cbz me out')
    turnIntoCBZ(nameOfFile)
    
commandLineRun()