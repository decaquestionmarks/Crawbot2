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
        print(f"Bot has been Pinged by {ctx.author}")
        await ctx.send('PokeInfo was successfully loaded')
    
    def name_convert(self, arg:str)->str:
        return arg.replace("-", "").replace(" ", "").lower()

    @commands.command(name='dt', help='Shows info about a Pokemon')
    async def data(self, ctx, *args):
        # try:
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
                embed.add_field(name = "Total", value=sum(list(self.pokemon[arg]["baseStats"].values())), inline = True)
            # elif arg in moves.keys():
            #     embed = discord.Embed(title = moves[arg]["name"][1:-1])
            #     try:
            #         embed.description = motext[arg]["shortDesc"][1:-1]
            #     except KeyError:
            #         embed.description = "Couldn't find Description"
            #     embed.add_field(name = "Type", value = moves[arg]["type"][1:-1], inline = True)
            #     embed.add_field(name = "Power", value = moves[arg]["basePower"], inline = True)
            #     embed.add_field(name = "Category", value = moves[arg]["category"][1:-1], inline = True)
            #     embed.add_field(name = "Accuracy", value = str(moves[arg]["accuracy"])+"%", inline=True)
            #     embed.add_field(name = "PP", value = int(int(moves[arg]["pp"])*(16/10)),inline = True)
            #     embed.add_field(name = "Priority", value = int(moves[arg]["priority"]), inline = True)
            #     embed.add_field(name = "flags", value = ", ".join(list(moves[arg]["flags"].keys())), inline= False)

            # elif arg in abilities.keys():
            #     embed = discord.Embed(title = abilities[arg]["name"][1:-1])
            #     try:
            #         embed.description = abtext[arg]["shortDesc"][1:-1]
            #     except KeyError:
            #         embed.description = "Unchanged"
            else:
                await ctx.channel.send("No data could be found in Pokemon, Moves, or Abilities")
            if embed.title is not None:
                await ctx.channel.send(embed = embed)
        # except Exception as e:
        #     await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")

async def setup(bot):
    await bot.add_cog(PokeInfo(bot))

