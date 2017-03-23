#!/usr/bin/python

import urllib2
import os

def webPageOpener(webPage):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    return opener.open(webPage).read()

def getChapterList(mangaName):
    chapterList = []
    conts = webPageOpener('http://www.mymanga.me/manga/' + mangaName)
    conts = conts[conts.index('"/manga/' + mangaName + '/'):]
    while '"/manga/' + mangaName + '/' in conts:
        conts = conts[conts.index('"/manga/' + mangaName + '/')+8:]
        chapterLink = 'http://www.mymanga.me/manga/' + conts[:conts.index('"')]
        chapterList.insert(0,chapterLink)
    return chapterList

def pageGetter(chapterPage):
    scb = webPageOpener(chapterPage)
    scb = scb[scb.index('option value'):]
    pageList = []
    while 'option value' in scb:
        scb = scb[scb.index('"')+1:]
        theThing = scb[:scb.index('"')]
        if len(theThing) > 2:
            break
        pageList.append(theThing)
        scb = scb[scb.index('option value'):]
    return pageList

def imgLinkGetter(pageLink):
    dfs = webPageOpener(pageLink)
    dfs = dfs[dfs.index('onerror'):]
    #dfs = dfs[dfs.index('class'):]
    dfs = dfs[dfs.index('src')+5:]
    linkyLink = dfs[:dfs.index('"')-1]
    return linkyLink

def imageGetter(pageList, count, getPage):
    chapTitle = 'chapter-' + count
    os.system('mkdir '+ chapTitle)
    xox = 111
    for each in pageList:
        pageLink = getPage + each
        imageLink = imgLinkGetter(pageLink)
        imgName = imageLink[imageLink.rindex('/'):]
        os.system('wget -P ' + chapTitle + ' ' + imageLink)
        sysCommand = 'mv ' + chapTitle + imgName + ' ' + chapTitle + '/' + str(xox) + '.jpg'
        os.system(sysCommand)
        xox += 1

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

def getNameOfFile():
    a = raw_input('What would you like to name the file?\n')
    a = nameFixer(a)
    return a

def zipAndCbz(nameOfFile):
    os.system('zip -r ' + nameOfFile + ' chapter-*')
    os.system('mv ' + nameOfFile + '.zip ' + nameOfFile + '.cbz')
    os.system('rm -r chapter-*')

def whichChapters(startChapter,endChapter,chapterList):
    for eachChapter in range(startChapter-1,endChapter):
        pageList = pageGetter(chapterList[eachChapter])
        imageGetter(pageList, str(eachChapter+1110), chapterList[eachChapter][:-1])

def commandLineRun():
    mangaName = raw_input('Enter name of manga as written in URL: ')
    chapterList = getChapterList(mangaName)
    os.system('clear')
    print 'There are ' + str(len(chapterList)) + ' chapters available for "' + mangaName + '".'
    print 'Which chapters would you like to download?\n'
    startChapter = int(raw_input('Starting chapter:\n'))
    endChapter = int(raw_input('\nEnd chapter:\n'))
    os.system('clear')
    print 'Ready to download chapters ' + str(startChapter) + ' to ' + str(endChapter) + ' from ' + mangaName + '.\n\n'
    nameOfFile = getNameOfFile()
    whichChapters(startChapter,endChapter,chapterList)
    zipAndCbz(nameOfFile)

commandLineRun()