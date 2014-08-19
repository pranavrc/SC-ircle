#!/usr/bin/env python

import urllib2
from BeautifulSoup import BeautifulSoup as bs
import sys
import socket

def returnBlacklist(username):
    followingList = {}
    followedList = []
    blackSheep = ''
    pageNumber = 1
    scrapeFollowing = True
    scrapeFollowers = True

    while True:
        try:
            if scrapeFollowing:
                followingPage = urllib2.urlopen("http://soundcloud.com/" + username + "/following?page=" + str(pageNumber)).read()
            if scrapeFollowers:
                followersPage = urllib2.urlopen("http://soundcloud.com/" + username + "/followers?page=" + str(pageNumber)).read()
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
            followingList[following.findAll(text=True)[0]] = following.find("a").get("href")

        for followed in followersSoup:
            followedList.append(followed.find("a").get("href"))

        pageNumber = pageNumber + 1

    for followerName, eachFollower in followingList.items():
        if eachFollower in followedList:
            del followingList[followerName]

    if len(followingList.keys()) == 0:
        return 'Looks like circlejerks weren\'t pulled on this user.'

    for followerName, eachFollower in followingList.items():
        blackSheep = blackSheep + '<a href="http://soundcloud.com' + eachFollower + '/" target="_blank">' + followerName + '</a>' + '<br />'
    
    return blackSheep.encode('ascii', 'ignore')

if __name__ == "__main__":
    uname = str(raw_input("Enter your Soundcloud Username: "))
    print(returnBlacklist(uname))
