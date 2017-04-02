#!/usr/bin/python

import urllib2
import pickle
import os

''' 
To Do List:
    Intergrate search function
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
    return opener.open(webPage).read()

######### Do a Search ###########

def searchMymangaonline(searchTerm):
    ''' 
    searchTerm: (+) concatenated string
    returns a dict with search results (name, page-link, image-link)
    '''
    scratchPage = webPageOpener('http://mangaonline.to/search.html?keyword=' + searchTerm)
    scratchPage = scratchPage[scratchPage.index('popular-body')+15:]
    resultsList = []
    resultsDict = {}
    resCount = 1
    while 'mask-title' in scratchPage:
        resLink = 'http://mangaonline.to/' + scratchPage[scratchPage.index('manga-info'):scratchPage.index('">')]
        scratchPage = scratchPage[scratchPage.index('src')+5:]
        resImage = scratchPage[:scratchPage.index('" ')]
        scratchPage = scratchPage[scratchPage.index('alt')+5:]
        resName = scratchPage[:scratchPage.index('"')]
        scratchPage = scratchPage[scratchPage.index('</span>')+5:]
        resultsList.append([resName,[resLink,resImage]])
        resultsDict[resName]=resLink,resImage,resCount
        resCount += 1
    return resultsList

def checkResultsPageCount(scratchPage):
    '''
    returns total number of pages of seach results
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
        chapterLink = 'http://mangaonline.to/' + homePage[:homePage.index('"')]
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
    return nameToFix

def imageGrabber(chapterPage, nameOfFile):
    '''
    chapterPage: address of chapter
    downloads images into a folder
    '''
    nameCounter = 111111
    chapterSource = webPageOpener(chapterPage)
    chapTitle = chapterTitle(chapterPage)
    chapTitle = nameFixer(chapTitle)
    chapTitle = nameOfFile + '/' + chapTitle
    os.system('mkdir ' + chapTitle)
    while 'img id' in chapterSource:
        chapterSource = chapterSource[chapterSource.index('img id'):]
        chapterSource = chapterSource[chapterSource.index(' src')+6:]
        if chapterSource[0] == '0':
            ending = "'"
            chapterSource = chapterSource[chapterSource.index('.src')+6:]
        else:
            ending = '"'
        imageLink = chapterSource[:chapterSource.index(ending)]
        os.system('wget -P ' + chapTitle + ' ' + imageLink)
        oldName = imageLink[imageLink.rindex('/'):]
        if 'jpg' in imageLink:
            newName = str(nameCounter) + '.jpg'
        elif 'png' in imageLink:
            newName = str(nameCounter) + '.png'
        else:
            print 'Unknown image type'
            break
        os.system('mv ' + chapTitle + '/' + oldName + ' ' + chapTitle + '/' + newName)
        nameCounter += 1

def whichChapters(startChapter, endChapter, chapterList, nameOfFile):
    '''
    downloads chapters from within range
    '''
    os.system('mkdir ' + nameOfFile)
    for i in range(startChapter-1,endChapter):
        imageGrabber(chapterList[i], nameOfFile)

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

def commandLineRun():
    clear()
    searchString = raw_input('...and what Manga would you like to search for today?\n\n')
    searchString = searchString.replace(' ', '+')
    searchResults = searchMymangaonline(searchString)
    clear()
    print 'We have found ' + str(len(searchResults)) + ' popular results.\nWhich Manga would you like to try? (1-' + str(len(searchResults)) + ')\n'
    count = 1
    for eachResult in searchResults:
        print str(count) + ') ' + eachResult[0]
        count += 1
    ########################### stick a try in here!!! ###############################
    selection = int(raw_input('\n'))-1
    thisManga = searchResults[selection]
    mangaName = thisManga[0]
    clear()
    confirm = raw_input('You would like to try "' + mangaName + '"? (Y/n) ')
    if confirm == 'n' or confirm == 'N':
        print '\nThen why did you select it...?\n'
        return
    chapterList = chapterListMaker(thisManga[1][0])
    clear()
    print 'There are ' + str(len(chapterList)) + ' chapters available for "' + mangaName + '".'
    print 'Which chapters would you like to download?\n'
    startChapter = int(raw_input('Starting chapter:\n'))
    endChapter = int(raw_input('\nEnd chapter:\n'))
    clear()
    print 'Ready to download chapters ' + str(startChapter) + ' to ' + str(endChapter) + ' from ' + mangaName + '.\n\n'
    nameOfFile = getNameOfFile()
    whichChapters(startChapter, endChapter, chapterList, nameOfFile)
    turnIntoCBZ(nameOfFile)
    
commandLineRun()