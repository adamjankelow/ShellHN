import pandas as pd
import requests
import numpy as np
import json
import sys
import argparse


def topArticles(x):
    # Get the id for the top 40 stories from the api below
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    response = requests.request("GET", top_stories_url)
    top_stories_id = response.json()
    dict = {}
    your_keys = ['id', 'type', 'title', 'time', 'score']
    top_40_id = top_stories_id[0:x]

    # iterate through the id's to return the info related to the ids
    for x in top_40_id:
        url = "https://hacker-news.firebaseio.com/v0/item/" + str(x) + ".json?print=pretty"
        response = requests.request("GET", url)
        response_dict = response.json()
        dict_subset = {your_key: response_dict[your_key] for your_key in your_keys}
        dict[x] = dict_subset
    # convert the data to a pandas data frame
    data = pd.DataFrame.from_dict(dict, orient="index")
    # Since api returns the top stories in order of their rank, rank column is based off number
    data['rank'] = np.arange(len(data)) + 1
    output = data[['title', 'rank']]
    print(output.to_string(index=False))


def prediction():
    technologies = ['Kubernetes', 'Linux', 'Windows', 'Solarwinds', 'Garmin', 'AWS',
                    'Docker', 'Github', 'Wordpress', 'Rundck']
    print(technologies)
    n = str(input("Enter technology from list to get prediction : "))
    if n in technologies:
        word = str(n).lower()
        json1_file = open('/Users/adamjankelow/Documents/projects/Kovrr/hacker_news_data.json')
        json1_str = json1_file.read()
        json1_data = json.loads(json1_str)

        data = pd.DataFrame.from_dict(json1_data, orient="columns")
        data['title'] = data['title'].astype(str).str.lower()
        data['wordCount'] = data['title'].str.contains(word)
        output = round(data['wordCount'].mean() * 100, 2)
        print('The likelihood the technology appears is ' + str(output) + '%')
    else:
        print('Command failed: Entry is not in the list provided')


if __name__ == '__main__':

    print("Hi! The following code has 2 interactive capabilities:"
          "\n 1. Display a list of the 40 most popular articles ordered by their rank."
          "\n 2. Predict the likelihood of the technology to appear in HN next month."
          "\n Enter the number 1 or 2 to use either of the capabailites described above."
          )

    # arg = sys.argv
    arg = int(input())
    if arg == 1:
        topArticles(3)
    elif arg == 2:
        prediction()
    else:
        print('Command failed: Please provide the command 1 or 2 as an argument')
