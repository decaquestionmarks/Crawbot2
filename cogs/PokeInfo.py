import discord
import os
from discord.ext import commands
from dictInterpreter import builddict
import random
from dotenv import load_dotenv
import copy

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
        self.pokemon = copy.deepcopy(self.oldmons)
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
        self.typechart = {}
        with open(dawndata + "typechart.ts", "r+") as f:
            builddict(f,self.typechart)
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
        dellist = []
        for key in self.pokemon.keys():
            if "num" not in self.pokemon[key]:
                dellist.append(key)   
        for key in dellist:
            del self.pokemon[key]
        #Typechart specific cleaning
        convtable = [1.0, 2.0, 0.5, 0]
        del self.typechart["spiral"]
        del self.typechart["void"]
        for key in self.typechart:
            del self.typechart[key]["damageTaken"]["Spiral"]
            del self.typechart[key]["damageTaken"]["Void"]
            for type in self.typechart[key]["damageTaken"]:
                self.typechart[key]["damageTaken"][type] = convtable[self.typechart[key]["damageTaken"][type]]
        # print(self.typechart) 
        #Populate lists
        self.types = set()
        for key in self.pokemon.keys():
            for type in self.pokemon[key]["types"]:
                self.types.add(type)
        self.types.remove("Bird")
        print("Types ",self.types)
        self.categories = {"physical","special","status"}
        self.stats = {"atk","def","hp","spa","spd","spe"}
        self.flags = set()
        for key in self.moves.keys():
            try:
                for flag in self.moves[key]["flags"]:
                    self.flags.add(flag)
            except:
                print(key, self.moves[key])
        print("Flags", self.flags)
        self.colors = set()
        for key in self.pokemon.keys():
                self.colors.add(self.pokemon[key]["color"])
        print("Colors", self.colors)
        self.eggGroups = set()
        for key in self.pokemon.keys():
            for type in self.pokemon[key]["eggGroups"]:
                self.eggGroups.add(type)
        print("eggGroups", self.eggGroups)
        self.evotypes = {"lc", "nfe", "fe"}
        
        print("PokeInfo Cog has been set up")

    @commands.command(name='awake', help = "determine if PokeInfo populated its knowledge base.")
    async def awake(self, ctx):
        print(f"Bot has been Pinged by {ctx.author}")
        await ctx.send('PokeInfo was successfully loaded')
    
    def name_convert(self, arg:str)->str:
        return arg.replace("-", "").replace(" ", "").lower()

    def learnrec(self, mon: str, move: str, data: dict)->bool:
        if "prevo" not in data[mon].keys() or self.name_convert(data[mon]["prevo"]) not in data[mon]["learnset"].keys():
            return move in data[mon]["learnset"]
        else:
            return move in data[mon]["learnset"] or self.learnrec(self.name_convert(data[mon]["prevo"]),move,data)

    @commands.command(name='dt', help='Shows info about a Pokemon, Move, or Ability')
    async def data(self, ctx, *args):
        try:
            arg = " ".join(args)
            arg = self.name_convert(arg)
            print(f"{ctx.author} Requesting data on {arg}")
            embed = discord.Embed()
            if arg in self.pokemon.keys():
                # print(self.pokemon[arg])
                embed = discord.Embed(title = self.pokemon[arg]["name"])
                embed.add_field(name = "Type", value = "/".join(self.pokemon[arg]["types"]), inline = True)
                if "natDexTier" in self.pokemon[arg].keys():
                    embed.add_field(name = "Tier", value = self.pokemon[arg]["natDexTier"], inline = True)
                embed.add_field(name = "Abilities", value = "\n".join([str(key) + ": " + str(self.pokemon[arg]["abilities"][key]) for key in self.pokemon[arg]["abilities"]]), inline = False)
                embed.add_field(name = "Stats", value = "/".join([str(value) for value in self.pokemon[arg]["baseStats"].values()]), inline = True)
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

    @commands.command(name='changes', help='Shows a Pokemon\'s changes from the base game')
    async def changes(self, ctx, *args):
        # try:
            arg = " ".join(args)
            arg = self.name_convert(arg)
            print(f"{ctx.author} Requesting changes on {arg}")
            embed = discord.Embed()
            if arg in self.oldmons.keys():
                # print(self.pokemon[arg])
                embed = discord.Embed(title = self.pokemon[arg]["name"])
                # print(self.oldmons[arg]["types"], self.pokemon[arg]["types"])
                if(self.oldmons[arg]["types"]!=self.pokemon[arg]["types"]):
                    embed.add_field(name = "Type", value = "/".join(self.oldmons[arg]["types"]) + "->" + "/".join(self.pokemon[arg]["types"]), inline = False)
                if(self.oldmons[arg]["abilities"]!=self.pokemon[arg]["abilities"]):
                    abilitychanges = []
                    for key in self.pokemon[arg]["abilities"]:
                        if key not in self.oldmons[arg]["abilities"]:
                            abilitychanges.append(f"New Ability {key}: {self.pokemon[arg]["abilities"][key]}")
                        elif self.oldmons[arg]["abilities"][key]!=self.pokemon[arg]["abilities"][key]:
                            abilitychanges.append(f"{key}: {self.oldmons[arg]["abilities"][key]} -> {self.pokemon[arg]["abilities"][key]}")
                    embed.add_field(name = "Abilities", value = "\n".join(abilitychanges), inline=False)
                if(self.oldmons[arg]["baseStats"]!=self.pokemon[arg]["baseStats"]):
                    statchanges = []
                    for key in self.pokemon[arg]["baseStats"]:
                        if self.oldmons[arg]["baseStats"][key]!=self.pokemon[arg]["baseStats"][key]:
                            statchanges.append(f"{key}: {self.oldmons[arg]["baseStats"][key]} -> {self.pokemon[arg]["baseStats"][key]}")
                    embed.add_field(name = "Stats", value = "\n".join(statchanges), inline=False)
                formarg = arg
                if "learnset" not in self.pokemon[arg].keys():
                    formarg = self.name_convert(self.pokemon[arg]["baseSpecies"])
                gained = []
                for key in self.pokemon[formarg]["learnset"]:
                    if not self.learnrec(formarg, key, self.oldmons):
                        gained.append(self.moves[key]["name"])
                lost = []
                for key in self.oldmons[formarg]["learnset"]:
                    if not self.learnrec(formarg, key, self.pokemon):
                        lost.append(self.moves[key]["name"])
                if gained or lost:
                    v = ""
                    if gained:
                        v += f"Gained: {", ".join(gained)}"
                    if lost:
                        v+= f"\nLost: {", ".join(lost)}"
                    embed.add_field(name = "Moves", value = v, inline=False)
            else:
                await ctx.channel.send("That Pokemon could not be found or is a new pokemon")
            if embed.title is not None:
                if(len(embed.fields)==0):
                    embed.description = "No changes found"
                await ctx.channel.send(embed = embed)
        # except Exception as e:
        #     await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")

    @commands.command(name = 'learn', help = 'Tells if a pokemon can learn a move')
    async def learn(self, ctx, *args):
        try:
            args = " ".join(args)
            args = args.split(",")
            mon = self.name_convert(args[0])
            move = self.name_convert(args[1])
            if mon in self.pokemon.keys() and "learnset" in self.pokemon[mon].keys():
                if move in self.moves.keys():
                    if self.learnrec(mon, move, self.pokemon):
                        await ctx.channel.send(f"{self.moves[move]["name"]} is learnable by {self.pokemon[mon]["name"]}")
                    else:
                        await ctx.channel.send(
                            f"{self.moves[move]["name"]} is not learnable by {self.pokemon[mon]["name"]}")
                else:
                    await ctx.channel.send(f"Move {move} cannot be found in the database")
            else:
                await ctx.channel.send(f"Pokemon {mon} cannot be found in the database")
        except Exception as e:
            await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")

    @commands.command(name = 'weak', help = 'Shows a pokemon\'s or type\'s weaknesses')
    async def weakness(self, ctx, *args):
        # try:
            args = (" ".join(args)).split(",")
            if len(args) == 1:
                if self.name_convert(args[0]) in self.pokemon.keys():
                    args = [type for type in self.pokemon[self.name_convert(args[0])]["types"] if type in self.types]
            print(f"Requesting Weaknesses for {args}")
            matchup = {}
            for arg in args:
                arg = self.name_convert(arg)
                if arg not in self.typechart.keys():
                    await ctx.channel.send(f"Type {arg} could not be found in the database")
                    return 
                for type in self.typechart[arg]["damageTaken"]:
                    if type in matchup.keys():
                        matchup[type] *= self.typechart[arg]["damageTaken"][type]
                    else:
                        matchup[type] = self.typechart[arg]["damageTaken"][type]
            weak = [f"**{key}**" for key in matchup.keys() if matchup[key]>=4]
            weak.extend([key for key in matchup.keys() if matchup[key]==2])
            neutral = [key for key in matchup.keys() if matchup[key]==1]
            resist = [key for key in matchup.keys() if matchup[key]==0.5]
            resist.extend([f"**{key}**" for key in matchup.keys() if 0<matchup[key]<0.5])
            immune = [key for key in matchup.keys() if matchup[key]==0]
            embed = discord.Embed(title = ", ".join(args))
            embed.add_field(name = "Weak: ", value = ", ".join(weak), inline = False)
            embed.add_field(name = "Neutral: ", value = ", ".join(neutral), inline = False)
            embed.add_field(name = "Resists: ", value = ", ".join(resist), inline = False)
            if len(immune)!=0:
                embed.add_field(name = "Immune: ", value = ", ".join(immune), inline = False)
            await ctx.channel.send(embed=embed)
        # except Exception as e:
        #     await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")

async def setup(bot):
    await bot.add_cog(PokeInfo(bot))

