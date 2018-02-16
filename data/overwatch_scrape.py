#!C:/Python27/python
import urllib2
import BeautifulSoup

wiki = "https://overwatch.gamepedia.com/Ana"
page = urllib2.urlopen(wiki)
soup = BeautifulSoup(page)
