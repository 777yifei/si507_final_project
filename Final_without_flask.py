import requests
from bs4 import BeautifulSoup
import json
from PIL import Image

def main():
    print("Welcome, you can quit @ any time")
    print("Do you want to fetch the newest data form the website? yes or no")
    new_input = input()
    if new_input.lower() in ['exit', 'quit']:
        return
    if new_input.lower() in ['yes', 'y', 'yup']:
        new = 1#user input
    else:
        new = 0
    #fetch new data form the API
    if(new):
        api_key = 'RGAPI-b3a9ba94-ac05-4fd0-9841-2bda3c8ef555'#this is a dynamic API key that update every 24hours
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
    

    
    #ask user with player they want to look @
    while 1:
        print(f"plz input the name of summoner you want to check(case sensitive): ")
        summoner_name = input()#user input
        if summoner_name.lower() in ['exit', 'quit']:
            return
        if summoner_name in json_data:
            break
        print(f"summoner not found or not in top 100")
    info = json_data[summoner_name] 

    with open('ID_name.json', 'r') as f:
        ID_name = json.load(f)

    while 1:
        print(f"plz input the name of the root champion(no space): ")
        root_name = input().lower()#userinput
        if root_name.lower() in ['exit', 'quit']:
            return
        if root_name in ID_name:
            break
        print(f"not found")
    root_ID = get_champion_ID(root_name, ID_name)
    binary_tree = create_bi_tree(info, root_ID)

    
    max = binary_tree.get_max_value()
    min = binary_tree.get_min_value()
    max_name= get_champion_name(max['championId'], ID_name)
    min_name= get_champion_name(min['championId'], ID_name)
    print(f"the champion with the max mastery is {max_name}, with mastery level {max['championLevel']} and mastery point {max['championPoints']}")
    print(f"the champion with the max mastery is {min_name}, with mastery level {min['championLevel']} and mastery point {min['championPoints']}")

    num_smaller = binary_tree.count_nodes_greater_than_root()
    num_larger = binary_tree.count_nodes_smaller_than_root()
    print(f'{num_smaller} champions have smaller mastery points')
    print(f'{num_larger} champions have larger mastery points')

    while 1:
        print(f"plz input the name of the champion that you want to find(no space): ")
        find_name = input().lower()#userinput
        if find_name.lower() in ['exit', 'quit']:
            return
        if find_name in ID_name:
            break
        print(f"not found")
    find_ID = get_champion_ID(find_name, ID_name)
    find = binary_tree.find(find_ID)
    print(f"the finded champion has mastery level {find['championLevel']} and mastery point {find['championPoints']}")

    image = Image.open(f"mastery{find['championLevel']}.jpg")
    image.show()
    #play with the tree
    #print(info)
    

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
class TreeNode:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

class BST:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = TreeNode(data)
        else:
            self.insert_nodes(data, self.root)

    def insert_nodes(self, data, current_node):
        if data['championPoints'] < current_node.data['championPoints']:
            if current_node.left is None:
                current_node.left = TreeNode(data)
            else:
                self.insert_nodes(data, current_node.left)
        elif int(data['championPoints']) > int(current_node.data['championPoints']):
            if current_node.right is None:
                current_node.right = TreeNode(data)
            else:
                self.insert_nodes(data, current_node.right)
        else:
            # duplicate, do nothing
            pass

    def find(self, ID):
        if self.root is not None:
            return self.find_temp(ID, self.root)
        else:
            return None

    def find_temp(self, ID, current_node):
        if ID == current_node.data['championId']:
            return current_node.data
        else:
            if self.find_temp(ID, current_node.left) is None:
                return self.find_temp(ID, current_node.right)
            else:
                return self.find_temp(ID, current_node.left)

    def get_min_value(self):
        if self.root is None:
            return None
        else:
            return self.min_value(self.root)

    def min_value(self, current_node):
        if current_node.left is None:
            return current_node.data
        else:
            return self.min_value(current_node.left)

    def get_max_value(self):
        if self.root is None:
            return None
        else:
            return self.max_value(self.root)

    def max_value(self, current_node):
        if current_node.right is None:
            return current_node.data
        else:
            return self.max_value(current_node.right)
    
    def count_nodes_greater_than_root(self):
        return self._count_greater_than_root_helper(self.root.right, self.root.data)

    def _count_greater_than_root_helper(self, node, val):
        if node is None:
            return 0
        elif node.data['championPoints'] > val['championPoints']:
            return 1 + self._count_greater_than_root_helper(node.left, val) + self._count_greater_than_root_helper(node.right, val)
        else:
            return self._count_greater_than_root_helper(node.right, val)

    def count_nodes_smaller_than_root(self):
        return self._count_smaller_than_root_helper(self.root.left, self.root.data)

    def _count_smaller_than_root_helper(self, node, val):
        if node is None:
            return 0
        elif node.data['championPoints'] < val['championPoints']:
            return 1 + self._count_smaller_than_root_helper(node.left, val) + self._count_smaller_than_root_helper(node.right, val)
        else:
            return self._count_smaller_than_root_helper(node.left, val)
'''   
def count_smaller(root):
    if root is None:
        return 0
    return count_smaller(root.left) + 1 + count_smaller(root.right) if root.left else 1 + count_smaller(root.right)

def count_larger(root):
    if root is None:
        return 0
    return count_larger(root.right) + 1 + count_larger(root.left) if root.right else 1 + count_larger(root.left)
'''
#create a tree
def create_bi_tree(info, root_ID):
    temp = {}
    #find the info of input champion
    for each in info:
        if each['championId'] == root_ID:
            temp = each
            break
    #create a root
    bst = BST()
    bst.insert(temp)
    for item in info:
        if(item['championId'] != root_ID):
            bst.insert(item)
    return bst


######################################
#######ID_Name converter def##########
######################################
def get_champion_name(id_num, file):    
    for champ_name, champ_id in file.items():
        #print(f'{champ_name}, {champ_id}')
        if champ_id == id_num:
            return champ_name
    return None

def get_champion_ID(name, file):    
    for champ_name, champ_id in file.items():
        if champ_name == name:
            return champ_id
    return None

#print the tree, used for debug
def print_tree(node, level=0):
    if node is not None:
        print_tree(node.right, level + 1)
        print(f"{level} " + node.data)
        print_tree(node.left, level + 1)

if __name__ == '__main__':
    main()