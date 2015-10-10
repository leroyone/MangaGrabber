#!/home/leroy/EPD/epd_free-7.3-2-rh5-x86/bin/python

from HTMLParser import HTMLParser
import urllib2
import os

###### Initialize manga website ######

startpage = urllib2.urlopen('http://www.mangapanda.com/135/fairy-tail.html')
starthtml = startpage.read()

###### Get Chapter URL ######

def getChapPage(chapnumber):
    ''' 
    chapnumber = int
    returns: Address for first page of chapter
    '''
    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == 'a':
                for name, value in attrs:
                    if name == 'href' and value.endswith(str(chapnumber)):
                        self.output = value
    parser = MyHTMLParser()
    parser.feed(starthtml)
    chapterAddress = parser.output
    return chapterAddress

###### Get Number of Pages in Chapter ######

def pageGet(chapAddress):
    ''' 
    chapAddress = web address for chapter (str)
    returns: int
    '''
    chapURL = urllib2.urlopen(chapAddress)
    chapConts = chapURL.read()

    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == 'option':
                for name, value in attrs:
                    if name == 'value':
                        self.output = value
    parser = MyHTMLParser()
    parser.feed(chapConts)
    numberLine = parser.output
    a = numberLine.split('/')
    return int(a[-1])
    
###### Get Image URL ######

def theChunk(pageInChapter):
    ''' 
    pageInChapter = web address containing imgae (str)
    returns: web address of image only (str)
    '''
    page = urllib2.urlopen(pageInChapter)
    html = page.read()
    
    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag == 'img':
                for name, value in attrs:
                    if name == 'src' and value.endswith('jpg'):
                        self.output = value
    
    parser = MyHTMLParser()
    parser.feed(html)
    imgurl = parser.output
    return imgurl

###################
def getChapName(numToLengthen):
    if len(str(numToLengthen)) == 1:
        return 'FTchapter-000' + str(numToLengthen)
    elif len(str(numToLengthen)) == 2:
        return 'FTchapter-00' + str(numToLengthen)
    elif len(str(numToLengthen)) == 3:
        return 'FTchapter-0' + str(numToLengthen)
    elif len(str(numToLengthen)) == 4:
        return 'FTchapter-' + str(numToLengthen)

###################
os.system('clear')
welcomeScreen = raw_input('\n\n\nWelcome to the wonderful Fairy Tail chapter downloader made by Me :)\n\n\n')
startingChapter = int(raw_input('Which chapter would you like to start from? '))
endingChapter = int(raw_input('\n\n\n...and how many chapters would you like to download? '))

chapterRange = range(startingChapter, startingChapter+endingChapter)

for eachChapter in chapterRange:
    chapname = getChapName(eachChapter)
    if os.path.exists(chapname + '.cbz') == True:
        print '\n' + str(chapname) + ' appears to already have been saved.'
        whatNext = raw_input('Press any key to continue.')
    else:
        os.system('mkdir ' + chapname)
         
        hat = getChapPage(eachChapter)
        numberOfPages = pageGet('http://www.mangapanda.com' + str(hat))
        for eachPage in range(1,numberOfPages+1):
            pageLocation = theChunk('http://www.mangapanda.com' + str(hat) + '/' + str(eachPage))
            print '\n\n\nDownloading Chapter ' + str(eachChapter) + '. page ' + str(eachPage) + '/' + str(numberOfPages) + '\n\n'
            os.system('wget -P ' + chapname + ' ' + str(pageLocation))
        #os.system('zip -r ' + chapname + ' ' + chapname + '/')
        #os.system('rm -r ' + chapname + '/')

#os.system("rename '\s/\.zip$/\.cbz/' *.zip")
