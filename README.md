# si507_final_project
Final project of SI507 by Yifei Zou

This paroject could search the champions mastery of top 100 summoners in NA. You can also see which champion has highest mastery points and which champion has the lowest mastery points.

Please run final_with_flask.py at first. This app will generate an html by flask. After runing the python, you need to open (default address)http://127.0.0.1:5000/ to use this app.

Python packages used:
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import json

API used:(reminder: this API key is dynamic and update every 24 hours, contact me if you need the new data)
URL:https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}, API key required
URL:https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}, API key required

scraped data:
URL:https://www.leagueofgraphs.com/rankings/summoners/na

Data structure:
For data structure, I will create a binary search trees based on user’s input. Each summoner’s champions’ mastery corresponding to one BST.
I will ask user which summoner and which champion would you like to search. The input champion will be used as the root node. Then a binary search tree will be generated based on the champions point.

Directory explain:
static: contains all the images will be used
templates: contains all the flask html file 

File explain:
riot_api_key: contains the api key to access riot api
final_with_flask.py: final diliverable
Fianl_without_flask.py: final code without using flask. All the interactions are in terminal
ID_name.json: a dictionary of champions' ID in League of Legends, one name corresponds to one ID
output.html: cache file; the html scraped from the web, contains the information of top 100 summoners of NA
output.json: main cache; catains all champions' mastery of every summoner who are top 100 in NA
top100.txt: contains summoners name of top100 summoners in NA
tree.json: Contains the tree structure build based on users operation.
BST.py:A python file that constructs binary search trees from my stored data using classes



