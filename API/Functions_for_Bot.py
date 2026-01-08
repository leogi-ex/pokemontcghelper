
#%% 
# Importing Libraries

import discord

from PIL import Image
import requests

import pokemontcgsdk
from pokemontcgsdk import RestClient
from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype
from pokemontcgsdk import Rarity



# Importing Libaries v3 features

# Base Python
import json
import os
import glob
import pickle
import datetime

# Pokemon API
import pokebase as pb
#https://github.com/PokeAPI/pokebase


# Data Stuff
import pandas







#%%

# Intializing

test_card = Card.find('swsh7-125')


#%%


def create_Poke_embed(card):
	
	info = get_poke_embed_info(card)
	large_image = info[2]
	# Checker for duplicates
	
	embed = discord.Embed(

        colour=info[3]
        #description= "This is Eevee, and hopefully the test works",
        #title="Eevee"
    )

    #embed.set_footer(text = "The footer")
    #embed.set_author(name = "Eevee", url = 'https://images.pokemontcg.io/swsh7/125_hires.png')
	embed.set_author(name = info[0], url = info[1])

	embed.set_thumbnail(url = info[4])
	embed.set_image(url = info[2])

	return embed #, large_image



#%%


colours = {
	'Colorless': 0xf6f4ef,
	'Fire': 0xf3634b,
	'Water': 0x6390F0,
	'Lightning': 0xF7D02C,
	'Grass': 0x7AC74C,
	# 'Ice': '#96D9D6',
	'Fighting': 0xdb6721,
	#'Poison': '#A33EA1',
	#'Ground': '#E2BF65',
	#'Flying': '#A98FF3',
	'Psychic': 0x9d6fad,
	#bug: '#A6B91A',
	#rock: '#B6A136',
	#ghost: '#735797',
	'Dragon': 0xb3a845,
	'Darkness': 0x007f9d,
	'Metal': 0xB7B7CE,
	#'Fairy': 0xD685AD,
}



def choose_color_embed(card):
	# Choosing the color of the embed

    dict_card = vars(card)
    # Turning object into dictionary

    color = colours[dict_card['types'][0]]
    # Navigating to types then selected the hexcode

    return color


# %%

# Getting Images


def get_poke_image_big(card):
    
	card_dict = vars(card)
    
	image = vars(card_dict['images'])['large']
      
	return image
     

#%%

# Getting Name

def get_poke_embed_info(card):
    # Getting information for embed author

	card_dict = vars(card)
	# Turn object to dict
       
	name = card_dict['name']
	# Getting card name
      
	url = vars(card_dict['tcgplayer'])['url']
	# Getting tcgplayer url for embed url
      
	poke_image = vars(card_dict['images'])['large']
    # Set the pokemon card image

	if card_dict['hp'] != None:
    
		color = colours[card_dict['types'][0]]
		# Set the outline color of embed

	else:

		color = 0xD3D3D3
    
	set_image = vars(vars(vars(card)['set'])['images'])['logo']
    # Setting thumbnail as set logo
      
	return name, url, poke_image, color, set_image
       
	
# %%


def combine_reprints(card_list):

	checkers = ['name', 'rules', 'attacks', 'hp']
	list_of_cards = []
	list_of_checked = []

	for i in card_list:
		#print(i)

		checking = []

		pulling = vars(i)

		for j in checkers:
			checking.append(pulling[j])
		
		if list_of_checked == []:
			list_of_checked.append(checking)
			list_of_cards.append(i)

		else:
			if checking in list_of_checked:
				print(vars(pulling['images'])['large'])

			else:
				list_of_checked.append(checking)
				list_of_cards.append(i)


	return list_of_cards
# %%


# Adding decks and recording logs
# New feature v3


def split_list_by_number(lst):
    result = []
    sublist = []

    for item in lst:
        if item[0].isdigit():
            sublist.append(item)
        else:
            if sublist != []: 
                result.append(sublist)
            sublist = []
            sublist.append(item)
        

    if sublist:  # Append the last sublist if not empty
        result.append(sublist)

    return result


def prepare_decklist(raw_decklist):

    split = raw_decklist.split("\n") 
    no_spaces = [x for x in split if x != ""]
    decklist = split_list_by_number(no_spaces)

    return decklist

def creating_deck(pokemon1, decklist, pokemon2 = None):

    prepared = prepare_decklist(decklist)

    if pokemon2 != None:
        name = pokemon1 + '_' + pokemon2
    else: 
        name = pokemon1

    path = os.getcwd()
    combined = path + f"/Combat Logs/Decks/{name}"

    if not os.path.exists(combined):
        os.makedirs(combined)
        print('Directory Created')

        os.makedirs(combined + "/v1")

        os.makedirs(combined + "/v1/combat_logs")


        with open(f"{combined}/v1/decklist.txt", "wb") as output:
            #output.write(str(decklist))
            pickle.dump(prepared, output)


    else:
        # print('Already Exists')
        return False
    
    return



## Adding Verisons:

def split_list_by_number(lst):
    result = []
    sublist = []

    for item in lst:
        if item[0].isdigit():
            sublist.append(item)
        else:
            if sublist != []: 
                result.append(sublist)
            sublist = []
            sublist.append(item)
        

    if sublist:  # Append the last sublist if not empty
        result.append(sublist)

    return result


def prepare_decklist(raw_decklist):

    split = raw_decklist.split("\n") 
    no_spaces = [x for x in split if x != ""]
    decklist = split_list_by_number(no_spaces)

    return decklist


def create_version(pokemon1, raw_decklist, pokemon2 = None):

    decklist = prepare_decklist(raw_decklist)

    if pokemon2 != None:
        name = pokemon1 + '_' + pokemon2
    else: 
        name = pokemon1

    path = os.getcwd()
    combined = path + f"/Combat Logs/Decks/{name}"

    if not os.path.exists(combined):
        print('No Base Deck')
        return False, False, None

    files = glob.glob(f"{combined}/**/decklist.txt")

    for i in files:

        with open(i, "rb") as f:
            tester = pickle.load(f)

        if tester == decklist:
            version = os.path.split(os.path.split(i)[0])[1]
            print(f"Already has version: {version}")
            return True, False, version

    version_num = len(files) + 1

    os.makedirs(f"{combined}/v{version_num}")
    os.makedirs(f"{combined}/v{version_num}/combat_logs")
    print("Directory Created")

    with open(f"{combined}/v{version_num}/decklist.txt", "wb") as output:
            #output.write(str(decklist))
            pickle.dump(decklist, output)

    return True, True, version


## Record raw combat logs

def record_raw_combat_logs(raw_combat_logs, deck, opponent_deck, version = None):

	if version == None:
		version = len(glob.glob(f"Combat Logs\\Decks\\{deck}\\**"))

	file_path = f"{os.getcwd()}\\Combat Logs\\Decks\\{deck}\\v{version}\\combat_logs\\"

	time = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M")

	with open(f"{file_path}{opponent_deck}_{time}.txt", "wb") as output:
		pickle.dump(raw_combat_logs, output)

	return