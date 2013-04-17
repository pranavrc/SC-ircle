#!/usr/bin/env python

import urllib2
from BeautifulSoup import BeautifulSoup as bs
import sys
import socket

def returnBlacklist(username):
    followingList = [] 
    followedList = []
    blackSheep = ''
    pageNumber = 1
    scrapeFollowing = True
    scrapeFollowers = True

    while True:
        try:
            if scrapeFollowing:
                followingPage = urllib2.urlopen("http://soundcloud.com/" + username + "/following?page=" + str(pageNumber), timeout = 3).read()
            if scrapeFollowers:
                followersPage = urllib2.urlopen("http://soundcloud.com/" + username + "/followers?page=" + str(pageNumber), timeout = 3).read()
        except urllib2.HTTPError, e:
            return 'User not found.'
        except urllib2.URLError, e:
            if pageNumber > 1:
                break
            else:
                if isinstance(e.reason, socket.timeout):
                    return 'Timed out.'
                return 'Bummer, failed to connect :('

        followingSoup = bs(followingPage).findAll("div", {"class" :"userbadge full"})
        followersSoup = bs(followersPage).findAll("div", {"class" :"userbadge full"})

        if (len(followingSoup) == 0):
            scrapeFollowing = False

        if (len(followersSoup) == 0):
            scrapeFollowers = False

        if not scrapeFollowing and not scrapeFollowers:
            break

        for following in followingSoup:
            followingList.append(following.find("a").get("href"))

        for followed in followersSoup:
            followedList.append(followed.find("a").get("href"))

        pageNumber = pageNumber + 1

    temp = [x for x in followingList if x not in set(followedList)]
    
    if len(temp) == 0:
        return 'Looks like circlejerks weren\'t pulled on this user.'

    for followerName in temp:
        blackSheep = blackSheep + '<a href="http://soundcloud.com' + followerName + '/">' + followerName[1:] + '</a>' + '<br />'
    
    return blackSheep.encode('ascii', 'ignore')

if __name__ == "__main__":
    uname = str(raw_input("Enter your Soundcloud Username: "))
    print returnBlacklist(uname)
