#import requests
import random
#import urllib.request
import urllib3
import json

EASY_STEPS = 4
HARD_STEPS = 8

cuisines = {            1:"African",
                        2:"American",
                        3:"British",
                        4:"Cajun",
                        5:"Carribean",
                        6:"Chinese",
                        7:"Eastern European",
                        8:"French",
                        9:"German",
                       10:"Greek",
                       11:"Indian",
                       12:"Irish",
                       13:"Italian",
                       14:"Japanese",
                       15:"Jewish",
                       16:"Korean",
                       17:"Latin American",
                       18:"Mexican",
                       19:"Middle Eastern",
                       20:"Nordic",
                       21:"Southern",
                       22:"Spanish",
                       23:"Thai",
                       24:"Vietnamese"
}

def get_cuisine_recipes(cuisine,difficulty):
    cuisines_url = "http://boilerpl8.me/api/cuisines"
    http = urllib3.PoolManager()
    cr = http.request('GET',cuisines_url)
    cx = json.loads(cr.data.decode('utf-8'))
    cl = cx['cuisines']
    recipes_url = "http://boilerpl8.me/api/recipes/"
    rr = http.request('GET', recipes_url)
    rx = json.loads(rr.data.decode('utf-8'))
    rl = rx['recipes']

    if cuisine != 0:
        id = 1
        for val in cl:
            if val['title'] == cuisines[cuisine]:
                id = val['id']
        result = []
        for val in rl:
            if val['cuisine_id'] == id:
                result.append(val)
    else:
        result = []
        for val in rl:
            result.append(val)

    final_result = []
    for item in result:
        if difficulty == 1:
            if item['numberOfSteps'] <= EASY_STEPS:
                final_result.append(item)
        elif difficulty == 2:
            if item['numberOfSteps'] > EASY_STEPS and item['numberOfSteps'] < HARD_STEPS:
                final_result.append(item)
        elif difficulty == 3:
            if item['numberOfSteps'] >= HARD_STEPS:
                final_result.append(item)
        else:
            final_result.append(item)

    return (random.choice(final_result))

def test_return():
	return "this is a test"
