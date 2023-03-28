import datetime
from settings import *
import requests
import pandas as pd
import requests.exceptions as Requestexceptions 
from storage import DBStorage
from urllib.parse import quote_plus
 
# Takes a search query and return results
def search_api(query,pages=int(RESULT_COUNT/10)):    # if we have 30 results then we will have 3 pages. 
    results = []
    for i in range (0,pages): 
        start = i * 10 + i
        url = SEARCH_URL.format(
            key = SEARCH_KEY,
            cx = SEARCH_ID,
            query = quote_plus(query), # Turn searchs to valid queries
            start = start
        )
        response = requests.get(url)
        data = response.json()
        results += data["items"]
    res_df = pd.DataFrame.from_dict(results)
    res_df["rank"] = list(range(1,res_df.shape[0] + 1)) # Rank the results, it will get the ID from the search
    res_df = res_df[["link","rank","snippet","title"]]
    return res_df

# search_api("baby stroller")

def scrapa_page(links):
    html = []
    for link in links : 
        try: 
            data = requests.get(link, timeout=5)
            html.append(data.text)
        except: 
            html.append("")
    return html

def search(query):
    columns =["query","rank","link","title","snippet","html","created"]
    storage = DBStorage()
    storage_results = []
    storage_results =  storage.query_results(query) # Did we run query, and if so, are the results in the DB
    # If results in the database. 
    if storage_results.shape[0] > 0:
        storage_results["created"] = pd.to_datetime(storage_results["created"])
        return storage_results[columns]
    results = search_api(query)
    results["html"] = scrapa_page(results["link"])
    results =  results[results["html"].str.len() > 0].copy() # If no html do not copy the results
    results["query"] = query
    results["created"] = datetime.datetime.utcnow().strftime("%y-%m-%d %H:%M:%S") # SQLITE Takes this form of date
    results.apply(lambda x: storage.insert_row(x),axis=1)
    return results
 



# search("fc barcelone")

