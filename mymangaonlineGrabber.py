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
    scratchPage = webPageOpener('http://www.mymangaonline.com/search?keyword=' + searchTerm)
    scratchPage = scratchPage[scratchPage.index('box-item'):]
    resultsList = []
    resultsDict = {}
    resCount = 1
    while 'box-item' in scratchPage:
        resLink = 'http://www.mymangaonline.com/' + scratchPage[scratchPage.index('manga-info'):scratchPage.index('html')+4]
        scratchPage = scratchPage[scratchPage.index('alt')+5:]
        resName = scratchPage[:scratchPage.index('src')-2]
        scratchPage = scratchPage[scratchPage.index('src')+6:]
        resImage = 'http://www.mymangaonline.com/' + scratchPage[:scratchPage.index('" ')]
        scratchPage = scratchPage[scratchPage.index('</span>')+5:]
        resultsList.append([resName,[resLink,resImage]])
        resultsDict[resName]=resLink,resImage,resCount
        resCount += 1
        print resultsList

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
    while 'item-chapter' in homePage:
        homePage = homePage[homePage.index('item-chapter')+3:]
        chapterLink = 'http://www.mymangaonline.com/' + homePage[homePage.index('href')+6:homePage.index('html')+4]
        chapterList.insert(0,chapterLink)
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

x = chapterListMaker('http://www.mymangaonline.com/manga-info/death-note.html')
for each in x:
    imageGrabber(each)


''' 
if os.path.isfile(deathNote.p) == False:
    listOfImages = chapterSurfer(initialChapter)
    pickle.dump(a, open('deathNote.p', 'wb'))
else:
    listOfImages = pickle.load(open('deathNote.p', 'rb'))
'''

#x = searchMymangaonline('death+note')