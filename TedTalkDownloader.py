import requests #getting content of the TED Talk page

from bs4 import BeautifulSoup #web scraping

import re #Regular Expression pattern matching

# from urllib.request import urlretrieve #downloading mp4

import sys #for argument parsing  to generalize the code for multiple urls as a combined package

# Exception Handling

if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    sys.exit("Error: Please enter the TED Talk URL")

#url = "https://www.ted.com/talks/jia_jiang_what_i_learned_from_100_days_of_rejection"

#url = "https://www.ted.com/talks/ken_robinson_says_schools_kill_creativity"

r = requests.get(url)

#indicate user the request is done
print("Download about to start")

#need to use response.content to get the actual content
soup = BeautifulSoup(r.content, features="lxml")
#print(soup)

#find text in source code that are in the <script> tag
for val in soup.findAll("script"):
    #print(val)
    if(re.search("(?P<url>https?://[^\s]+)(mp4)",str(val))) is not None:
        result = str(val)
        #print(result)

# print(result)
#regex = starts with https...and contains mp4_url
#the response will containt multiple valid urls since there's url for high, medium, low quality...etc
result_mp4 = re.search("(?P<url>https?://[^\s]+)(mp4)", result).group("url")

#split all results with a seperator and only getting the first item
mp4_url = result_mp4.split('"')[0]
mp4_url = mp4_url + "mp4"
print(mp4_url)

print("Downloading video from ..... " + mp4_url)

# #an example of the file name in the mp4url is https://...../filename.mp4?apikey=....
# #so the below splits mp4url with '/', getting the last element after /, and then get the first element before ?
file_name = mp4_url.split("/")[len(mp4_url.split("/"))-1].split('?')[0]
print(file_name)

print("Storing video in ..... " + file_name)

#request the original video content using http request
rMp4 = requests.get(mp4_url)

#get the actual video content using response.webcontent
#and write the file to a filename called xxx.mp4
with open(file_name,'wb') as f:
  f.write(rMp4.content)

# Alternate method
#urlretrieve(mp4_url,file_name)

print("Download Process finished")
