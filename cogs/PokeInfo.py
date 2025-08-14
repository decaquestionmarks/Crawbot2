import discord
import os
from discord.ext import commands
from dictInterpreter import builddict
import random
from dotenv import load_dotenv

class PokeInfo(commands.Cog):
    def __init__(self, bot):
        print("PokeInfo Cog loading")
        self.bot = bot
        #fill dictionary memory
        load_dotenv()
        dawnloc = os.getenv('DAWN_LOC')
        dawnbasedata = dawnloc + "/data/"
        dawndata = dawnbasedata + "/mods/gen9sanctified/"
        self.oldmons = {}
        with open(dawnbasedata + "pokedex.ts", "r+") as f:
            builddict(f,self.oldmons)
        self.pokemon = self.oldmons.copy()
        with open(dawnbasedata + "learnsets.ts", "r+") as f:
            builddict(f,self.oldmons)
        with open(dawndata+"pokedex.ts", "r+") as f:
            builddict(f,self.pokemon)
        with open(dawndata+"learnsets.ts", "r+") as f:
            builddict(f,self.pokemon)
        with open(dawndata+"formats-data.ts", "r+") as f:
            builddict(f,self.pokemon)
        self.moves = {}
        with open(dawnbasedata+"moves.ts", "r+") as f:
            builddict(f,self.moves)
        with open(dawndata+"moves.ts", "r+") as f:
            builddict(f,self.moves)
        with open(dawnbasedata+"text/moves.ts", "r+") as f:
            builddict(f,self.moves)
        self.abilities = {}
        with open(dawndata+"abilities.ts", "r+") as f:
            builddict(f,self.abilities)
        with open(dawnbasedata+"text/abilities.ts", "r+") as f:
            builddict(f,self.abilities)
        #clean dictionary memory

        print("PokeInfo Cog has been set up")

    @commands.command(name='awake', help = "determine if PokeInfo populated its knowledge base.")
    async def awake(self, ctx):
        await ctx.send('PokeInfo was successfully loaded')
    
async def setup(bot):
    await bot.add_cog(PokeInfo(bot))

