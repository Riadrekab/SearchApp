from bs4 import BeautifulSoup
from urllib.parse import  urlparse
from settings import *

def get_page_content(row):
    soup = BeautifulSoup(row["html"]) # Get the page linked in the search engine
    text = soup.get_text() # Get only the text (not the images, nor the videos) because the more available text, the better it is.
    return text

class Filter():
    def __init__(self,results) :
        self.filtered = results.copy()

    def content_filter(self):
        page_content = self.filtered.apply(get_page_content,axis = 1) 
        word_count =  page_content.apply(lambda x: len(x.split(" "))) # Count how many words are available in text returned in get_page_content
        word_count /= word_count.median() # Divise the count by the median 

        word_count [word_count <= .5] = RESULT_COUNT # Fetch the results that are 2 times lower or more that the median
        word_count [word_count != RESULT_COUNT] = 0 # The ones that do not respect the previous condition are ranked the best
        self.filtered["rank"] += word_count 
        
    def filter(self):
        self.content_filter()
        self.filtered = self.filtered.sort_values("rank",ascending = True)
        self.filtered = self.filtered["rank"].round() 
        return self.filtered


