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

    # iterate through the id's to return the details related to the ids
    for x in top_40_id:
        url = "https://hacker-news.firebaseio.com/v0/item/" + str(x) + ".json?print=pretty"
        response = requests.request("GET", url)
        response_dict = response.json()
        dict_subset = {your_key: response_dict[your_key] for your_key in your_keys}
        dict[x] = dict_subset

    data = pd.DataFrame.from_dict(dict, orient="index")
    data['rank'] = np.arange(len(data)) + 1
    output = data[['title', 'rank']]
    print(output)


def prediction():
    # Opening JSON file
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
        output = round(data['wordCount'].mean() * 100 , 2)
        print('The likelihood the technology appears is ' + str(output)+ '%')
    else:
        print('Entry is not in the list provided')


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(prog='Hacker News',
    #                                  usage='Choose a technology and this will predict likelihood of appearing in HN',
    #                                  description='Description: This tool has 2 capabilities'
    #                                              '1:Provide a list of HN top stories '
    #                                              '2: Predict if a technology appears in HN in the following month',
    #                                  epilog='Copy @ Adam Jankelow',
    #                                  formatter_class= argparse.RawDescriptionHelpFormatter,
    #                                  add_help= True
    #                                  )
    # parser.add_argument('--top40', '-top40', type= str, help= 'Enter query to return the list of top 40 stories'
    #                     , required=False )
    arg = sys.argv
    if arg[1] == '1':
        topArticles(1)
    elif arg[1] == '2':
        prediction()
    else:
        print('Argument provided is invalid: Please provide the intger 1 or 2 as an argument')


    # topArticles(2)
