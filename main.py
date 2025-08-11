# bot.py
import discord
import os
import random
from dotenv import load_dotenv
from discord.ext import commands
from dictInterpreter import builddict
load_dotenv()

#dictionary population step
file = open("Dawn/data/pokedex.ts","r+")
basepokemon = builddict(file,dict())
file = open("Dawn/data/mods/gen9sanctified/pokedex.ts","r+")
pokemon = builddict(file,basepokemon.copy())



intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
intents.all()

# client = discord.Client(intents=intents)
client = commands.Bot(command_prefix="!", intents=intents)

token = os.getenv('DISCORD_TOKEN')

@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

@client.command(name='info', help='Tells you about the bot')
async def info(ctx):
    message = random.choice(["I'm the base 640 bot.", "Careful, I'm a bit of Klutz.", "Worst STABs since 2020.", "I wonder what I can't learn?", "Back and better than ever"])
    await ctx.channel.send(f"{ctx.author.mention}"+message)


client.run(token)