#!/usr/bin/python

import urllib2
from lxml import html
import os

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

def searchMymangaonline(searchTerm):
    ''' 
    searchTerm: (+) concatenated string
    returns a list of tuples with search results (name, page-link)
    '''
    scratchPage = webPageOpener('http://mangaonlinehere.com/search.html?keyword=' + searchTerm)
    scratchTree = html.fromstring(scratchPage)
    
    namesScratchList = scratchTree.xpath('//div[@class="popular-body"]//img/@alt')
    linksScratchList = scratchTree.xpath('//div[@class="popular-body"]//a/@href')
    resultsList = zip(namesScratchList,linksScratchList)
    return resultsList

def searchKissManga(missing, searchTerm):
    scratchPage = webPageOpener('https://kiss-manga.com/search?type=all&query=' + searchTerm)
    scratchTree = html.fromstring(scratchPage)
    namesScratchList = scratchTree.xpath('//a[@class="manga-name"]/text()')
    linksScratchList = scratchTree.xpath('//a[@class="manga-name"]/@href')
    searchResults = zip(namesScratchList,linksScratchList)
    
###################################
    count = 1
    for eachResult in searchResults:
        print str(count) + ') ' + eachResult[0]
        count += 1
    if len(searchResults) > 0:
        foundText = '\nWe have found ' + str(len(searchResults)) + ' popular results.\nWhich Manga would you like to try? (1-' + str(len(searchResults)) + ')\n'
    else:
        raw_input('We have found no results for "' + searchStringOriginal + '"\nPlease try again.\n')
        return
    selection = int(raw_input(foundText))-1
    thisManga = searchResults[selection]
    mangaName = thisManga[0]
    clear()
    confirm = raw_input('You would like to try "' + mangaName + '"? (Y/n) ')
####################################


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
    homePage = webPageOpener(homePage)
    chapterList = []
    while 'read-online' in homePage:
        homePage = homePage[homePage.index('read-online'):]
        chapterLink = 'http://mangaonlinehere.com/' + homePage[:homePage.index('"')]
        chapterList.insert(0,chapterLink)
        homePage = homePage[homePage.index('href'):]
    return chapterList

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
    chapTitle = chapterTitle(chapterPage)
    chapTitle = nameFixer(chapTitle)
    chapTitle = str(10001 + chapterNumber) + '-' + chapTitle
    chapTitle = nameOfFile + '/' + chapTitle
    os.system('mkdir ' + chapTitle)
    tree = html.fromstring(chapterSource)
    imageLink = tree.xpath('//img[@id]/@src')
    for each in range(len(imageLink)):
        pass
        if 'http' in imageLink[each]:
            pass
            '''
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
            '''
        else:
            missing.append([chapTitle, str(chapterNumber+1), str(each+1)])
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

def getNameOfFile():
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
        searchKissManga(missing, searchString)

def commandLineRun():
    clear()
    searchStringOriginal = raw_input('...and what Manga would you like to search for today?\n\n')
    searchString = searchStringOriginal.replace(' ', '+')
    searchResults = searchMymangaonline(searchString)
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
    chapterList = chapterListMaker('http://mangaonlinehere.com/' +thisManga[1])
    clear()
    print 'There are ' + str(len(chapterList)) + ' chapters available for "' + mangaName + '".'
    print 'Which chapters would you like to download?\n'
    startChapter = int(raw_input('Starting chapter:\n'))
    endChapter = int(raw_input('\nEnd chapter:\n'))
    clear()
    print 'Ready to download chapters ' + str(startChapter) + ' to ' + str(endChapter) + ' from ' + mangaName + '.\n\n'
    nameOfFile = getNameOfFile()
    missingPages = whichChapters(startChapter, endChapter, chapterList, nameOfFile)
    if len(missingPages) >0:
        getMissing(missingPages, searchString)
    turnIntoCBZ(nameOfFile)
    
commandLineRun()