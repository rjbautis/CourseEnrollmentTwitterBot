import tweepy
import time
import secrets
import urllib.request
from bs4 import BeautifulSoup

# Tweepy auth
auth = tweepy.OAuthHandler(secrets.c_key, secrets.c_secret)
auth.set_access_token(secrets.a_token, secrets.a_token_secret)

api = tweepy.API(auth)


# urllib & BeautifulSoup setup
# load webpage-to-be-scraped from secrets
website = secrets.website
course_name = secrets.course_name
page = urllib.request.urlopen(website)
soup = BeautifulSoup(page, 'html.parser')


# return list of all 'dd' tags from page
ddTags = soup.findAll('dd')

# initialize enrollment values
available_seats = ''
enrollment_capacity = ''
enrolled = ''


# find 1st instance in the tree where class="col-xs-6", which displays current quarter
current_quarter = soup.find("div", class_="col-xs-6")
current_quarter = " ".join(current_quarter.text.split())


# return True if enrollment values are updated on site
# else return False
def updated():
   try:
      page = urllib.request.urlopen(website)
   except:
      print("Error: cannot make request")
      return False

   soup = BeautifulSoup(page, 'html.parser')
   
   global available_seats, enrollment_capacity, enrolled

   # check if values are still the same
   if(available_seats == ddTags[7].text and enrollment_capacity == ddTags[8].text and
   enrolled == ddTags[9].text):
      print("Enrollment values are unchanged")
      return False

   # if not, update variables with newest values
   available_seats = ddTags[7].text
   enrollment_capacity = ddTags[8].text
   enrolled = ddTags[9].text

   print("{}/{} students have enrolled in {} for {}." \
      " There are {} seats available.".format(enrolled, enrollment_capacity, course_name, current_quarter, available_seats))

   return True


# post tweet
def postTweet():
   api.update_status("{}/{} students have enrolled in {} for {}." \
      " There are {} seats available.".format(enrolled, enrollment_capacity, course_name, current_quarter, available_seats))


if __name__ == '__main__':
   while True:
      if updated():
         postTweet()
      time.sleep(10)      

