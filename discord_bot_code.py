"""
Created on Tue Oct 22 19:48:09 2024

@author: Preston Robertson
"""

#pip install discord.py
# If needed
#  c:\GitLaptop\.venv\Scripts\python.exe -m pip install pokemontcgsdk



#%%
# Importing Libraries

# General
import json
import io

# For Discord Bot
import discord
from CreateQRCodes.Create_QR_Codes_Discord import *
from discord.ext import commands

# For Slash Commands
from discord import app_commands
from discord import interactions


# For Embeds
# from API.Functions_for_Bot import *


# For Dillan Command
import random

# For Pokemon API
#import pokemontcgsdk
#from pokemontcgsdk import RestClient
#from pokemontcgsdk import Card
#from pokemontcgsdk import Set
#from pokemontcgsdk import Type
#from pokemontcgsdk import Supertype
#from pokemontcgsdk import Subtype
#from pokemontcgsdk import Rarity


# For testing
import pickle





#%%
# Intializing the bot


# Loading BOT secrets
with open('config.txt') as f:
    config = json.load(f)


# Set-up the TCGbothelper channel and command
bot = commands.Bot(command_prefix="!P ", intents=discord.Intents.all())

channel_id = config['Channel_ID']
#API_KEY = config['API_KEY']
#RestClient.configure(API_KEY)


# For Dillan Insults
with open("insults.txt", "r") as f:
    insults = f.read()
    insults = insults.split('\n')


#with open("API_KEY.txt", "r") as f:
    #API_KEY = f.read()
    #RestClient.configure(API_KEY)


#%%
# Bot Start-up Process

@bot.event
async def on_ready():
    #print("Hello World!")
    channel = bot.get_channel(channel_id)

    # Sync slash commands
    try: 
        # Try Syncing the bot commands from local python
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")

    except Exception as e:
        print(f"Error syncing commands: {e}")
    

    await channel.send("I'm Ready!")
    # Once bot start-up is done, it will send "I'm Ready"


#%% 


@bot.tree.command(name = "hello", description= "Typical test command")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!")

#%%

@bot.hybrid_command(name = "getqrcodes", description = "A command to create QR codes")
@app_commands.describe(codes_for_qr = "Please copy and paste the QR codes with no changes")
async def getqrcodes(ctx, codes_for_qr: str): # interaction: discord.Interaction, 
    #await interaction.response.send_message(f"Working on it!", delete_after=1)

    arr = codes_for_qr

    channel = bot.get_channel(channel_id)

    fileslist = []

    data = fixing_PTCGL_codes(arr)

    #Setting intial values
    tracker = 0
    # This value will determine if 10 codes have been transferred
    
    images = []
    # This is where we store the images until printed


    x = (len(data) - len([s for s in data if " " in s])) % 10

    if x >= 10 or x == 0:
        x = 10
    
    
    await ctx.send('# ' + data[0])
    # Printing the title with largness

    #print(len(data))

    #print(len(data[0:-(len(data) % 10)]))
    
    #(len(data)-x)
    for item in data[1:-x]:
    # Looping through each code in 'data'

        #print(tracker)

        
        
        if " " in item:
        # Checking to see if title or expansion name was mentioned

            tracker = 0
            # Setting the tracker back to 0 to restart the chain for the next expansion

            if not images: 
                await ctx.send("# " + item)
                continue

            fig, axes = plt.subplots(2, 5, figsize=(20, 9))
            # Setting size, tested with the official app
            
            #plt.tight_layout()
            # Gives more lateral space and makes it easier to scan
                

            for ax, image in zip(axes.flat, images):
            # Scanning each axis after flattenting the subplots + looping images
            
                ax.imshow(image, cmap='gray')
                # Seting grayscale image of each QR code to each axis point
                
            for ax in axes.flat:
            # Scanning each axis after flattenting the subplots
            
                ax.axis('off')
                # Turning off axis seperately to prevent random grids from showing up
                
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            await ctx.send(file=discord.File(buffer, 'plot.png'))

            # Running function to print the QR chunk

            images=[]
            # Resetting images for the next QR chunk

            await ctx.send("# " + item)
            # Printing expansion name in large font
        
        
        
        else:
        # If item is not an expansion name
            
            if tracker == 9:
            # Check if the current item is the 10th data chunk
                
                tracker = 0
                # Reset tracker for next data chunk
                
                images.append(create_QR(item))
                # Add the current QR code to images
                
                fig, axes = plt.subplots(2, 5, figsize=(20, 9))
                # Setting size, tested with the official app
                
                #plt.tight_layout()
                # Gives more lateral space and makes it easier to scan
                    

                for ax, image in zip(axes.flat, images):
                # Scanning each axis after flattenting the subplots + looping images
                
                    ax.imshow(image, cmap='gray')
                    # Seting grayscale image of each QR code to each axis point
                    
                for ax in axes.flat:
                # Scanning each axis after flattenting the subplots
                
                    ax.axis('off')
                    # Turning off axis seperately to prevent random grids from showing up
                    
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)

                await ctx.send(file=discord.File(buffer, 'plot.png'))
                    # Print the QR chunk
                
                images=[]
                # Reset images for the next QR chunk
                
            else:
            # if this is not the 10 QR code
            
                tracker += 1
                # Increase tracker

                
                images.append(create_QR(item))
                # Add current QR code to images


            #await ctx.send(files=fileslist)
            

    #if x != 0:
    images = []

    for item in data[-x:-1]:

        images.append(create_QR(item))
        # Add current QR code to images

    images.append(create_QR(data[-1]))


    fig, axes = plt.subplots(2, 5, figsize=(20, 9))
    # Setting size, tested with the official app
    
    #plt.tight_layout()
    # Gives more lateral space and makes it easier to scan
        

    for ax, image in zip(axes.flat, images):
    # Scanning each axis after flattenting the subplots + looping images
    
        ax.imshow(image, cmap='gray')
        # Seting grayscale image of each QR code to each axis point
        
    for ax in axes.flat:
    # Scanning each axis after flattenting the subplots
    
        ax.axis('off')
        # Turning off axis seperately to prevent random grids from showing up
        
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    await ctx.send(file=discord.File(buffer, 'plot.png'))
        # Print the QR chunk
    
    images=[]
    # Reset images for the next QR chunk



#%%

# Make decks and record combat logs
# New Feature v3

@bot.hybrid_command(name = 'create_deck', description = "Create a new deck for tracking")
@app_commands.describe(main_pokemon = "Name of the Main Pokemon (do not add spaces)", 
                       decklist = "Export the decklist from PTCGL", 
                       sub_pokemon = "Name of the Secondary Pokemon (do not add spaces)")
async def create_deck(ctx, main_pokemon, decklist, sub_pokemon = None):

    try: 
        x = creating_deck(pokemon1=main_pokemon, decklist=decklist, pokemon2=sub_pokemon) 
    except Exception as e:
        await ctx.send(f"Something went wrong: {e}")
    else:
        if x == False: 
            await ctx.send("Deck Already Exists")
        else:
            await ctx.send("Directory Created")

@bot.hybrid_command(name = 'create_deck_version', description = "Create a new version of a deck for tracking")
@app_commands.describe(main_pokemon = "Name of the Main Pokemon (do not add spaces)", 
                       decklist = "Export the decklist from PTCGL", 
                       sub_pokemon = "Name of the Secondary Pokemon (do not add spaces)")
async def create_deck_version(ctx, main_pokemon, decklist, sub_pokemon = None):

    try: 
        x , y , z = create_version(pokemon1=main_pokemon, raw_decklist=decklist, pokemon2=sub_pokemon)
    except Exception as e:
        await ctx.send(f"Something went wrong: {e}")
    else:
        if x == True:
            if y == True:
                await ctx.send(f"New Version created: {z}")
            else:
                await ctx.send(f"Why make a new version when you already have: {z}?")
        else:
            await ctx.send("There are no decks with this name")


@bot.hybrid_command(name = "record_combat", description = "Records the raw combat logs from the previous message, new features coming")
@app_commands.describe(deck = "What was the deck you played?",
                       opponent_deck = "What did your opponent play?",
                       #combat_logs = "Copy the exact combat logs from PTCGL",
                       version = "What version of your deck were you playing?")
async def record_combat(ctx, deck, opponent_deck, previous_message = True, version = None):


    if previous_message == True:
        try: 
            #channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
            async for message in ctx.channel.history(limit=1): 
            #await ctx.send(f"Last message is: {message.content}")

                try:
                    message.attachments[0]
                except Exception as e:
                    await ctx.send(f"Something went wrong: {e}")

                else:
                    attachment = message.attachments[0]
                        # Check the file type (e.g., image, text, etc.)
                    try:

                        if version == None:
                            version = len(glob.glob(f"Combat Logs\\Decks\\{deck}\\**"))

                        file_path = f"{os.getcwd()}\\Combat Logs\\Decks\\{deck}\\v{version}\\combat_logs\\"

                        time = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M")

                        combined = f"{file_path}{opponent_deck}_{time}.txt"



                        # Save the attachment content
                        content = await attachment.save(fp = combined)

                    except Exception as e:
                        await ctx.send(f"Something went wrong: {e}")
                    
                    else:
                        await ctx.send(f"Combat Saved in deck: {deck}, version: {version}, with name: {opponent_deck}_{time}. Deleting previous message")

                        await message.delete()
                            

        except Exception as e:
            await ctx.send(f"Error: {e}")







#%%

@bot.command()
async def GetQR(ctx, *, arr, description = "Creates QR codes"):

    channel = bot.get_channel(channel_id)

    fileslist = []

    data = fixing_PTCGL_codes(arr)

    #Setting intial values
    tracker = 0
    # This value will determine if 10 codes have been transferred
    
    images = []
    # This is where we store the images until printed


    x = (len(data) - len([s for s in data if " " in s])) % 10

    if x >= 10 or x == 0:
        x = 10
    
    
    await ctx.send('# ' + data[0])
    # Printing the title with largness

    #print(len(data))

    #print(len(data[0:-(len(data) % 10)]))
    
    #(len(data)-x)
    for item in data[1:-x]:
    # Looping through each code in 'data'

        #print(tracker)

        
        
        if " " in item:
        # Checking to see if title or expansion name was mentioned

            tracker = 0
            # Setting the tracker back to 0 to restart the chain for the next expansion

            if not images: 
                await ctx.send("# " + item)
                continue

            fig, axes = plt.subplots(2, 5, figsize=(20, 9))
            # Setting size, tested with the official app
            
            #plt.tight_layout()
            # Gives more lateral space and makes it easier to scan
                

            for ax, image in zip(axes.flat, images):
            # Scanning each axis after flattenting the subplots + looping images
            
                ax.imshow(image, cmap='gray')
                # Seting grayscale image of each QR code to each axis point
                
            for ax in axes.flat:
            # Scanning each axis after flattenting the subplots
            
                ax.axis('off')
                # Turning off axis seperately to prevent random grids from showing up
                
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            await ctx.send(file=discord.File(buffer, 'plot.png'))

            # Running function to print the QR chunk

            images=[]
            # Resetting images for the next QR chunk

            await ctx.send("# " + item)
            # Printing expansion name in large font
        
        
        
        else:
        # If item is not an expansion name
            
            if tracker == 9:
            # Check if the current item is the 10th data chunk
                
                tracker = 0
                # Reset tracker for next data chunk
                
                images.append(create_QR(item))
                # Add the current QR code to images
                
                fig, axes = plt.subplots(2, 5, figsize=(20, 9))
                # Setting size, tested with the official app
                
                #plt.tight_layout()
                # Gives more lateral space and makes it easier to scan
                    

                for ax, image in zip(axes.flat, images):
                # Scanning each axis after flattenting the subplots + looping images
                
                    ax.imshow(image, cmap='gray')
                    # Seting grayscale image of each QR code to each axis point
                    
                for ax in axes.flat:
                # Scanning each axis after flattenting the subplots
                
                    ax.axis('off')
                    # Turning off axis seperately to prevent random grids from showing up
                    
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)

                await ctx.send(file=discord.File(buffer, 'plot.png'))
                    # Print the QR chunk
                
                images=[]
                # Reset images for the next QR chunk
                
            else:
            # if this is not the 10 QR code
            
                tracker += 1
                # Increase tracker

                
                images.append(create_QR(item))
                # Add current QR code to images


            #await ctx.send(files=fileslist)
            

    #if x != 0:
    images = []

    for item in data[-x:-1]:

        images.append(create_QR(item))
        # Add current QR code to images

    images.append(create_QR(data[-1]))


    fig, axes = plt.subplots(2, 5, figsize=(20, 9))
    # Setting size, tested with the official app
    
    #plt.tight_layout()
    # Gives more lateral space and makes it easier to scan
        

    for ax, image in zip(axes.flat, images):
    # Scanning each axis after flattenting the subplots + looping images
    
        ax.imshow(image, cmap='gray')
        # Seting grayscale image of each QR code to each axis point
        
    for ax in axes.flat:
    # Scanning each axis after flattenting the subplots
    
        ax.axis('off')
        # Turning off axis seperately to prevent random grids from showing up
        
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    await ctx.send(file=discord.File(buffer, 'plot.png'))
        # Print the QR chunk
    
    images=[]
    # Reset images for the next QR chunk

            





#%%


bot.run(config['TOKEN'])

# %%
