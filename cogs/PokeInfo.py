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
        # print(self.moves)
        with open(dawndata+"moves.ts", "r+") as f:
            builddict(f,self.moves)
        # print(self.moves)
        with open(dawnbasedata+"text/moves.ts", "r+") as f:
            builddict(f,self.moves)
        # print(self.moves)
        self.abilities = {}
        with open(dawndata+"abilities.ts", "r+") as f:
            builddict(f,self.abilities)
        with open(dawnbasedata+"text/abilities.ts", "r+") as f:
            builddict(f,self.abilities)
        #clean dictionary memory
        dellist = []
        for key in self.moves.keys():
            if "num" not in self.moves[key]:
                dellist.append(key)
        for key in dellist:
            del self.moves[key]
        dellist = []
        for key in self.abilities.keys():
            if "num" not in self.abilities[key]:
                dellist.append(key)   
        for key in dellist:
            del self.abilities[key]    
        #Populate lists
        print("PokeInfo Cog has been set up")

    @commands.command(name='awake', help = "determine if PokeInfo populated its knowledge base.")
    async def awake(self, ctx):
        print(f"Bot has been Pinged by {ctx.author}")
        await ctx.send('PokeInfo was successfully loaded')
    
    def name_convert(self, arg:str)->str:
        return arg.replace("-", "").replace(" ", "").lower()

    @commands.command(name='dt', help='Shows info about a Pokemon')
    async def data(self, ctx, *args):
        try:
            arg = " ".join(args)
            arg = self.name_convert(arg)
            print(f"{ctx.author} Requesting data on {arg}")
            embed = discord.Embed()
            if arg in self.pokemon.keys():
                # print(self.pokemon[arg])
                embed = discord.Embed(title = self.pokemon[arg]["name"])
                embed.add_field(name = "Type", value = "/".join(self.pokemon[arg]["types"]), inline = False)
                embed.add_field(name = "Abilities", value = str(self.pokemon[arg]["abilities"]), inline = False)
                embed.add_field(name = "Stats", value = "/".join([str(value) for value in self.pokemon[arg]["baseStats"].values()]))
                # print(list(self.pokemon[arg]["baseStats"].values()))
                embed.add_field(name = "Total", value=sum(list(self.pokemon[arg]["baseStats"].values())), inline = True)
            elif arg in self.moves.keys():
                print(self.moves[arg])
                embed = discord.Embed(title = self.moves[arg]["name"])
                try:
                    embed.description = self.moves[arg]["shortDesc"]
                except KeyError:
                    embed.description = "Couldn't find Description"
                embed.add_field(name = "Type", value = self.moves[arg]["type"], inline = True)
                embed.add_field(name = "Power", value = self.moves[arg]["basePower"], inline = True)
                embed.add_field(name = "Category", value = self.moves[arg]["category"], inline = True)
                embed.add_field(name = "Accuracy", value = str(self.moves[arg]["accuracy"])+"%", inline=True)
                embed.add_field(name = "PP", value = int(int(self.moves[arg]["pp"])*(16/10)),inline = True)
                embed.add_field(name = "Priority", value = int(self.moves[arg]["priority"]), inline = True)
                embed.add_field(name = "flags", value = ", ".join(list(self.moves[arg]["flags"].keys())), inline= False)

            elif arg in self.abilities.keys():
                embed = discord.Embed(title = self.abilities[arg]["name"])
                try:
                    embed.description = self.abilities[arg]["shortDesc"]
                except KeyError:
                    embed.description = "No desciption Found"
            else:
                await ctx.channel.send("No data could be found in Pokemon, Moves, or Abilities")
            if embed.title is not None:
                await ctx.channel.send(embed = embed)
        except Exception as e:
            await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")

async def setup(bot):
    await bot.add_cog(PokeInfo(bot))

