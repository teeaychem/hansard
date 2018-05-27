import sys
print(sys.path)


import time
import urllib
import urllib.request
import urllib.error


baseURL = "http://www.hansard-archive.parliament.uk/The_Official_Report,_House_of_Commons_(6th_Series)_Vol_1_(March_1981)_to_2004/"

for j in range(1,3):
  for i in range(1, 101):
    zipPrefix = "S6CV0"
    zipNum = str(i)
    while len(zipNum) < 3:
      zipNum = "0" + zipNum
    zipMain = zipPrefix + zipNum

    print(zipMain)


    zipMain = zipMain + "P" + str(j) + ".zip"

    time.sleep(2)

    print(zipMain)

    requestURL = baseURL + zipMain

    request = urllib.request.urlopen(requestURL)
    try:
        urllib.request.urlretrieve(requestURL, '/Users/sparkes/hansard/' + zipMain)

    except urllib.error.URLError: # 404, 500, etc..
        pass


# try:
#   urllib.request.urlretrieve('https://i1.wp.com/python3.codes/wp-content/uploads/2015/06/Python3-powered.apng?fit=650%2C350', '/Users/sparkes/hansard/f.jpg')
# except urllib.error.URLError: # 404, 500, etc..
#   pass


# S6CV0090P0.zip

# urllib.request.urlretrieve('https://i1.wp.com/python3.codes/wp-content/uploads/2015/06/Python3-powered.apng?fit=650%2C350', '/Users/sparkes/hansard/t.jpg')