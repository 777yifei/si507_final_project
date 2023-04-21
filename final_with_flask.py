from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import json
from BST import BST
from riot_api_key import riot_api_key

def get_id(api_key, summoner_name):
    """
    retun the summoner's ID from the API, with the input summoner's name

    Param:
    api_key: string, the api key requierd for accessing the api
    summoner_name: string, the name of the summoner
    """ 
    url = f'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
    headers = {'X-Riot-Token': api_key}

    response = requests.get(url, headers=headers)
    data = response.json()
    try:
        return data['id']
    except:
        return "error"

def get_mastery(api_key,summoner_id):
    """
    retun the summoner's champions' mastery information from the Api, wchih the input summoner's ID

    Param:
    api_key: string, the api key requierd for accessing the api
    summoner_id: string, the id of the summoner
    """ 
    url = f'https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}'
    headers = {'X-Riot-Token': api_key}

    response = requests.get(url, headers=headers)
    return response.json()



#load the top 100 summoners in NA from the web and store them into top100.txt
def read_new_top100():
    """
    scraping and retun a dictionary which contains names of top 100 summoners form a web
    the scraped data will be stored into top100.txt

    """ 
    url = 'https://www.leagueofgraphs.com/rankings/summoners/na'
    lolgraphys = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
    soup = BeautifulSoup(lolgraphys.content, 'html.parser')


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
        
# Define a helper function to convert the BST to a dictionary
def bst_to_dict(node):
    """
    helper function to convert the BST to a dictionary
    return a dictionary form of bst and will be stored into a json file

    Param:
    node: BST(), the binary search tree
    """ 
    if not node:
        return None
    return {
        'championId': node.data['championId'],
        'championLevel': node.data['championLevel'],
        'championPoints': node.data['championPoints'],
        'left': bst_to_dict(node.left),
        'right': bst_to_dict(node.right)
    }

#create a tree
def create_bi_tree(info, root_ID):
    """
    return a binary search tree based on root node, 
    root ID is the champion's ID of the root node

    Param:
    info: dictionary, cotains all the node required to build the BST
    root ID: the champion's ID of the root node
    """ 
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
    """
    input the champion's ID and return the corresponding champion's name

    Param:
    id_num: int, champion's ID
    file: dictionary, contains the relation of champion's ID and its name
    """    
    for champ_name, champ_id in file.items():
        #print(f'{champ_name}, {champ_id}')
        if champ_id == id_num:
            return champ_name
    return None

def get_champion_ID(name, file):
    """
    input the champion's name and return the corresponding champion's ID

    Param:
    id_num: int, champion's ID
    file: dictionary, contains the relation of champion's ID and its name
    """     
    for champ_name, champ_id in file.items():
        if champ_name == name:
            return champ_id
    return None

#print the tree, used for debug
def print_tree(node, level=0):
    """
    a debug function used to print the tree structure in the terminal

    Param:
    node: TreeNode(), the root node
    """
    if node is not None:
        print_tree(node.right, level + 1)
        print(f"{level} " + node.data)
        print_tree(node.left, level + 1)

app = Flask(__name__)

@app.route('/')
def index():
    '''
    the home page of my application
    '''
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    '''
    the page pops after click submit button
    this page contains all the required data
    '''
    # Get user input from the form
    new_input = request.form.get('new_input_field')
    summoner_name = request.form.get('summoner_name_field')
    root_name = request.form.get('root_name_field')
    find_name = request.form.get('find_name_field')
    see_max = request.form.get('display_max_field')
    see_min = request.form.get('display_min_field')
    display_image = request.form.get('display_image')


    if new_input.lower() in ['yes', 'y', 'yup']:
        new = 1#user input
    else:
        new = 0
    
    #fetch new data form the API, if new is 1
    if(new):
        api_key = riot_api_key#this is a dynamic API key that update every 24hours
        summoners = read_new_top100()

        json_data = {}
        for summoner in summoners:
            #print(summoner)
            id = get_id(api_key, summoner)
            if(id != "error"):
                data = get_mastery(api_key, id)
                print(data)
                new_data = [{'championId': d['championId'], 'championLevel': d['championLevel'], 'championPoints': d['championPoints']} for d in data]
                json_data[summoner] = new_data
        
        with open('output.json', 'w') as outfile:
            json.dump(json_data, outfile)
    else:
        with open('output.json', 'r') as readfile:
            json_data = json.load(readfile)

    #print error message if user input is not in top100
    if summoner_name not in json_data:
        return render_template('final_output.html', error_message="Summoner not found or not in top 100.")

    #fech data from cache file
    info = json_data[summoner_name] 

    with open('ID_name.json', 'r') as f:
        ID_name = json.load(f)

    #print error message if user input is not a valid champion's name
    if root_name.lower() not in ID_name:
        return render_template('final_output.html', error_message="Root champion not found.")

    #transfer user input into a champion's ID, and then create binary tree
    root_ID = get_champion_ID(root_name.lower(), ID_name)
    binary_tree = create_bi_tree(info, root_ID)

    # Convert the BST to a dictionary
    bst_dict = bst_to_dict(binary_tree.root)

    # Write the dictionary to a JSON file
    with open('tree.json', 'w') as f:
        json.dump(bst_dict, f)

    #get the information of champions with max and min mastery points
    max = binary_tree.get_max_value()
    min = binary_tree.get_min_value()
    max_name= get_champion_name(max['championId'], ID_name)
    max_image_path = f"static/mastery{max['championLevel']}.jpg"
    min_name= get_champion_name(min['championId'], ID_name)
    min_image_path = f"static/mastery{min['championLevel']}.jpg"

    num_larger = binary_tree.count_nodes_greater_than_root()
    num_smaller = binary_tree.count_nodes_smaller_than_root()

    #print error message if user input is not a valid champion's name
    if find_name.lower() not in ID_name:
        return render_template('final_output.html', error_message="Champion not found.")

    find_ID = get_champion_ID(find_name.lower(), ID_name)
    find = binary_tree.find(find_ID)
        
    find_image_path = f"static/mastery{find['championLevel']}.jpg"
    
    #user can decide if display the image in submit
    if display_image not in ['yes']:
        display_image = None

    if see_max not in ['yes']:
        see_max = None
    
    if see_min not in ['yes']:
        see_min = None

    # Render the output on the web page
    return render_template('final_output.html', max_name=max_name, max_level=max['championLevel'], max_points=max['championPoints'], 
                           min_name=min_name, min_level=min['championLevel'], min_points=min['championPoints'], 
                           num_smaller=num_smaller, num_larger=num_larger, find_level=find['championLevel'],
                           find_points=find['championPoints'], find_image_path=find_image_path, max_message=see_max, min_message=see_min
                           ,max_image_path = max_image_path, min_image_path=min_image_path, display_image=display_image)

if __name__ == '__main__':
    app.run(debug=True)