


#%%
## Importing Libraries


import matplotlib.pyplot as plt
import matplotlib.image as mpimg
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


#%%
## Configuration

#export POKEMONTCG_IO_API_KEY='12345678-1234-1234-1234-123456789ABC'

with open("API_KEY.txt", "r") as f:
    API_KEY = f.read()
    RestClient.configure(API_KEY)

# %%

## CARD Searches

# cards = Card.all()
# 59.3 seconds

Card.where(q='set.name:generations subtypes:mega name:charizard hp:[* TO 100] attacks.name:Spelunk', 
           orderBy='-set.releaseDate')
#https://docs.pokemontcg.io/api-reference/cards/search-cards

# "*" wildcard matching, name:char*der
# Exact matching, !name:charizard

standard_only = 'legalities.standard:legal'

standard_cards = Card.where(q=f'{standard_only}')



#%%

# CARD Information


"""
abilities
artist
ancientTrait
attacks
convertedRetreatCost
evolvesFrom
flavorText
hp
id
images
legalities
regulationMark
name
nationalPokedexNumbers
number
rarity
resistances
retreatCost
rules
set
subtypes
supertype
tcgplayer
types
weaknesses
"""


#%%

num_of_cards = len(standard_cards)

search_for = 'heal'

for i in standard_cards:
    card_S = vars(i)

    if card_S['abilities'] != None:

        ability = vars(card_S['abilities'][0])

        if search_for in ability['text']:
            print(card_S['name'] )
            print(ability)
            img = mpimg.imread('https://images.pokemontcg.io/swsh7/125_hires.png')
            imgplot = plt.imshow(img)
            plt.show()


#%%
