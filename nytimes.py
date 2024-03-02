import requests
import re

API_Key = "U1uz8zemY29hRq2nZFAfb4aXnWGI9WGj"
query = "covid"

url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q={}&api-key={}".format(query, API_Key)

response = requests.get(url)
content = response.json()

count = 1
for item in content["response"]["docs"]:
    try:
        print(count,item["abstract"],item["section_name"])
    except:
        continue
    count = count + 1
