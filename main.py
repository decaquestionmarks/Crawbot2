# bot.py
import discord
import os
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
intents.all()

compre = os.getenv("COMPRE")

# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix=compre, intents=intents)

token = os.getenv('DISCORD_TOKEN')

async def setup_cogs(bot):
    cogs = ['cogs.PokeInfo']
    for cog in cogs:
        if not cog in bot.extensions:
            await bot.load_extension(cog)
    return True

@bot.event
async def on_ready():
    await setup_cogs(bot)
    print("Logged in as a bot {0.user}".format(bot))

@bot.command(name='info', help='Tells you about the bot')
async def info(ctx):
    message = random.choice(["I'm the base 640 bot.", "Careful, I'm a bit of Klutz.", "Worst STABs since 2020.", "I wonder what I can't learn?", "Back and better than ever"])
    await ctx.channel.send(f"{ctx.author.mention}"+message)


bot.run(token, reconnect=True)