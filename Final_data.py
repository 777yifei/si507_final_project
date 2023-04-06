import requests
from bs4 import BeautifulSoup
import json

def main():
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
if __name__ == '__main__':
    main()