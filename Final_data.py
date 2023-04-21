import requests
from bs4 import BeautifulSoup
import json

def main():
    new = 0
    if(new):
        api_key = 'RGAPI-b3a9ba94-ac05-4fd0-9841-2bda3c8ef555'
        summoners = read_new_top100()

        ##############test############
        '''   
        id = get_id(api_key, "lunacia")

        data = get_mastery(api_key, id)
        new_data = [{'championId': d['championId'], 'championLevel': d['championLevel'], 'championPoints': d['championPoints']} for d in data]
        new_data.append("C9+Lost")
        '''
        json_data = {}
        for summoner in summoners:
            print(summoner)
            id = get_id(api_key, summoner)
            if(id != "error"):
                data = get_mastery(api_key, id)
                new_data = [{'championId': d['championId'], 'championLevel': d['championLevel'], 'championPoints': d['championPoints']} for d in data]
                json_data[summoner] = new_data
        
        with open('output.json', 'w') as outfile:
            json.dump(json_data, outfile)
    else:
        with open('output.json', 'r') as readfile:
            json_data = json.load(readfile)
    
    info = json_data['DouyinTonyTop']
    print(info)
    championId = 5

def get_id(api_key, summoner_name):
    url = f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
    headers = {'X-Riot-Token': api_key}

    response = requests.get(url, headers=headers)
    data = response.json()
    try:
        return data['id']
    except:
        return "error"

def get_mastery(api_key,summoner_id):
    url = f'https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}'
    headers = {'X-Riot-Token': api_key}

    response = requests.get(url, headers=headers)
    return response.json()


#############################################################################
#load the top 100 summoners in NA from the web and store them into top100.txt
def read_new_top100():
    url = 'https://www.leagueofgraphs.com/rankings/summoners/na'
    lolgraphys = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
    #print(opgg.content)
    soup = BeautifulSoup(lolgraphys.content, 'html.parser')

    #with open('output.html', 'w', encoding='utf-8') as file:
    #    file.write(str(soup))


    summoners = []
    temp = soup.find_all('a')
    for summoner in temp:
        string = str(summoner.get('href'))
        
        if("/summoner/na/" in string):
            name = string[13:]
            if name not in summoners:
                summoners.append(name)

    with open('top100.txt', 'w') as file:
        for summoner in summoners:
            file.write(summoner + '\n')
    return summoners
############################################################################
#########create binary search tree#################
class Node:
    def __init__(self, champion_id, champion_points, champion_level):
        self.left = None
        self.right = None
        self.champion_id = champion_id
        self.champion_points = champion_points
        self.champion_level = champion_level
        
def insert_node(root, champion_id, champion_points, champion_level):
    if root is None:
        return Node(champion_id, champion_points, champion_level)

    if champion_points < root.champion_points:
        root.left = insert_node(root.left, champion_id, champion_points, champion_level)
    elif champion_points > root.champion_points:
        root.right = insert_node(root.right, champion_id, champion_points, champion_level)
    else:
        if champion_id < root.champion_id:
            root.left = insert_node(root.left, champion_id, champion_points, champion_level)
        else:
            root.right = insert_node(root.right, champion_id, champion_points, champion_level)

    return root

if __name__ == '__main__':
    main()