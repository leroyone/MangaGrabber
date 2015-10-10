#!/usr/bin/python

import urllib2
import os

###### Initialize manga website ######

startpage = urllib2.urlopen('http://www.mymangaonline.com/manga-info/death-note.html')
starthtml = startpage.read()

firstLink = starthtml[starthtml.rindex('div class="item-chapter'):]
firstLink = firstLink[firstLink.index('http'):]
initialChapter = firstLink[:firstLink.index('html')+4]

def eachChapter(scratchText):
    if 'chapter-detail' in scratchText:
        scratchText = scratchText[scratchText.index('chapter-detail'):]
        scratchText = scratchText[scratchText.index('http'):]
    imageList = []
    test = True
    while True:
        if 'imgmax' in scratchText:
            imageList.append(scratchText[:scratchText.index('?')])
            scratchText = scratchText[scratchText.index('?'):]
            scratchText = scratchText[scratchText.index('http'):]
        else:
            break
    return imageList

def webPageOpener(webPage):
    chapter = urllib2.urlopen(webPage)
    return chapter.read()

def chapterSurfer(webPage):
    chapterText = webPageOpener(webPage)
    chapterList = []

    chapterList.append(eachChapter(chapterText))
    
    while 'next' in chapterText:
        print len(chapterList)
        nextLink = chapterText[chapterText.index('next'):]
        nextLink = nextLink[nextLink.index('http'):]
        nextLink = nextLink[:nextLink.index('"')]
        chapterText = webPageOpener(nextLink)
        chapterList.append(eachChapter(chapterText))
    return chapterList

a = chapterSurfer(initialChapter)

#for each in a:
 #   print each