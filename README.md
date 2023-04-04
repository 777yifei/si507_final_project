# si507_final_project
Final project of SI507

SI 507 Final Project Proposal - Yifei Zou
API to use:
https://developer.riotgames.com/apis#champion-mastery-v4_
This is the API of League of Legends of the Riot game(API key required).
It will return the champion mastery of the different champion from
different summoner. I will use the data collected form to this API to make
a tree structure
Tree structure:
The tree structure looks like below:
Interaction:
Functions:
1. The basic function is that user could input the summoner ID and the
name of the champion to check the specific champion Mastery.
2. Print the top #(1-5) champions of a summoner that has the highest
mastery points.
3. I allowed user to compare the mastery of the same champion between
different summoners.
 Each time the user inputs a new summoner’s ID, the infomation of the
champions’ mastery will be saved into a cache. The code will first check
the cache file, if there is no such a summoner, if will fetch the
information from the API.
Display:
The output will be print to the terminal at first. Then the users will be
asked if they want save the result into a txt file.
For the second function, the user could choose to generate a graph of the
champion with the highest mastery score. 
