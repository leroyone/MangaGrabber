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
    page = urllib2.urlopen(webPage)
    return page.read()

######### Do a Search ###########

def searchMymangaonline(searchTerm):
    ''' 
    searchTerm: (+) concatenated string
    returns a dict with search results (name, page-link, image-link)
    '''
    scratchPage = webPageOpener('http://mangaonline.to/search.html?key=' + searchTerm)
    scratchPage = scratchPage[scratchPage.index('popular-body'):]
    resultsList = []
    resultsDict = {}
    resCount = 1
    while 'mask-title' in scratchPage:
        resLink = 'http://mangaonline.to/' + scratchPage[scratchPage.index('manga-info'):scratchPage.index('html')+4]
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
        chapterLink = 'http://mangaonline.to/' + homePage[:homePage.index('html')+4]
        chapterList.insert(0,chapterLink)
        homePage = homePage[homePage.index('href'):]
    return chapterList

def chapterTitle(chapterPage):
    '''
    chapterPage: address of chapter
    returns chapter name as str
    '''
    chapterPage = webPageOpener(chapterPage)
    chapterPage = chapterPage[chapterPage.index('selected value')+16:]
    return chapterPage[:chapterPage.index('"')]

def imageGrabber(chapterPage):
    '''
    chapterPage: address of chapter
    downloads images into a folder
    '''
    chapterSource = webPageOpener(chapterPage)
    chapterSource = chapterSource[chapterSource.index('chapter-detail'):]
    chapTitle = chapterTitle(chapterPage)
    os.system('mkdir ' + chapTitle)
    while 'imgmax' in chapterSource:
        imageLink = chapterSource[chapterSource.index('src')+5:chapterSource.index('imgmax')+11]
        print imageLink
        os.system('wget -P ' + chapTitle + ' ' + imageLink)
        oldName = imageLink[imageLink.rindex('/'):]
        newName = imageLink[imageLink.rindex('/'):imageLink.index('?img')]
        os.system('mv ' + chapTitle + '/' + oldName + ' ' + chapTitle + '/' + newName)
        chapterSource = chapterSource[chapterSource.index('imgmax')+3:]

def whichChapters(startChapter, endChapter, chapterList):
    '''
    downloads chapters from within range
    '''
    pass


''' 
if os.path.isfile(deathNote.p) == False:
    listOfImages = chapterSurfer(initialChapter)
    pickle.dump(a, open('deathNote.p', 'wb'))
else:
    listOfImages = pickle.load(open('deathNote.p', 'rb'))
'''

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
    print 'There are ' + str(len(chapterList)) + ' chapter available for "' + mangaName + '".'
    print 'Which chapters would you like to download?\n'
    startChapter = raw_input('Starting chapter:\n')
    endChapter = raw_input('\nEnd chapter:\n')
    whichChapters(startChapter, endChapter, chapterList)
    
commandLineRun()