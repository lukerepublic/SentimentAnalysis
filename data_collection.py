import requests

API_Key = "U1uz8zemY29hRq2nZFAfb4aXnWGI9WGj"

# url and file setup for October 1918 (Spanish Flu pandemic)
query1918 = "1918/10"
flu_url = f"https://api.nytimes.com/svc/archive/v1/{query1918}.json?api-key={API_Key}"
titles1918 = open("titles_1918.txt", "w")

# url and file setup for October 2020 (COVID pandemic)
query2020 = "2020/10"
covid_url = f"https://api.nytimes.com/svc/archive/v1/{query2020}.json?api-key={API_Key}"
titles2020 = open("titles_2020.txt", "w")

##========================================================================##

# title collection for October 1918 (Spanish Flu pandemic)
flu_data = requests.get(flu_url)
flu_data = flu_data.json()

flu_articles = flu_data["response"]["docs"]
total_articles = len(flu_articles) - 1

for article in flu_articles:

    # check for the last article -- shouldn't get a newline
    if flu_articles.index(article) == total_articles: 
        title = str(article["headline"]["main"])
        titles1918.write(title)

    # all other articles get newlines
    else:
        title = str(article["headline"]["main"]) + "\n"
        titles1918.write(title)

##========================================================================##

# title collection for October 2020 (COVID pandemic)
covid_data = requests.get(covid_url)
covid_data = covid_data.json()

covid_articles = covid_data["response"]["docs"]
total_articles = len(covid_articles) - 1

for article in covid_articles:

    # check for the last article -- shouldn't get a newline
    if covid_articles.index(article) == total_articles: 
        title = str(article["headline"]["main"])
        titles2020.write(title)

    # all other articles get newlines
    else:
        title = str(article["headline"]["main"]) + "\n"
        titles2020.write(title)