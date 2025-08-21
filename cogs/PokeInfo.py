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
        self.eggmap = {}
        for egg in self.eggGroups:
            self.eggmap[self.name_convert(egg)] = egg
        print("eggGroups", self.eggGroups,self.eggmap)
        self.evotypes = {"lc", "nfe", "fe"}
        # self.typemap = {}
        # for type in self.types:
        #     self.typemap[type.lower()] = type
        self.tiers = set()
        for key in self.pokemon.keys():
            try:
                self.tiers.add(self.pokemon[key]["natDexTier"])
            except:
                # print(key)
                self.pokemon[key]["natDexTier"] = "Illegal"
        self.tiermap = {}
        for tier in self.tiers:
            self.tiermap[tier.lower()] = tier
        print("Tiers", self.tiers, self.tiermap)
        self.tagmap = {}
        for key in self.pokemon.keys():
            if "tags" in self.pokemon[key].keys():
                if self.pokemon[key]["tags"][0] not in self.tagmap.keys():
                    self.tagmap[self.name_convert(self.pokemon[key]["tags"][0])] = self.pokemon[key]["tags"][0]
        print("Poketags", self.tagmap)
        print("PokeInfo Cog has been set up")

    @commands.command(name='awake', help = "determine if PokeInfo populated its knowledge base.")
    async def awake(self, ctx):
        print(f"Bot has been Pinged by {ctx.author}")
        await ctx.send('PokeInfo was successfully loaded')
    
    def name_convert(self, arg:str)->str:
        return arg.replace("-", "").replace(".", "").replace(" ", "").lower()

    def learnrec(self, mon: str, move: str, data: dict)->bool:
        ##### Do form check for certain forms
        if "learnset" not in self.pokemon[mon].keys() and "baseSpecies" in self.pokemon[mon].keys():
            # print("checking only ", data[mon]["baseSpecies"])
            return self.learnrec(self.name_convert(self.pokemon[mon]["baseSpecies"]),move, data)
        elif "prevo" in data[mon].keys() and self.name_convert(data[mon]["prevo"]) in data.keys():
            # print("checking", data[mon]["prevo"])
            return move in data[mon]["learnset"] or self.learnrec(self.name_convert(data[mon]["prevo"]),move,data)
        elif "learnset" in self.pokemon[mon].keys() and "baseSpecies" in self.pokemon[mon].keys() and len(self.pokemon[mon]["learnset"])<=5:
            # print("checking", data[mon]["baseSpecies"])
            return move in data[mon]["learnset"] or self.learnrec(self.name_convert(self.pokemon[mon]["baseSpecies"]),move, data)
        elif "learnset" not in self.pokemon[mon].keys() and "baseSpecies" not in self.pokemon[mon].keys() and "prevo" not in data[mon].keys():
            # print(f"{mon} has no data on moves")
            return False
        else:
            # print("checking only", mon)
            return move in data[mon]["learnset"]

    def _typemod(self, types: list[str], atk:str):
        ret = 1
        for type in types:
            if type in self.types:
                type = self.name_convert(type)
                ret *= self.typechart[self.name_convert(type)]["damageTaken"][atk]
        return ret

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
                moves = []
                for key in self.moves.keys():
                    if self.learnrec(arg, key, self.pokemon):
                        moves.append(key)
                embed.add_field(name = "Moves", value=len(moves), inline = False)
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
        try:
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
                # formarg = arg
                # if "learnset" not in self.pokemon[arg].keys():
                #     formarg = self.name_convert(self.pokemon[arg]["baseSpecies"])
                gained = []
                for key in self.moves.keys():
                    if not self.learnrec(arg, key, self.oldmons) and self.learnrec(arg, key, self.pokemon):
                        gained.append(self.moves[key]["name"])
                lost = []
                for key in self.moves.keys():
                    if not self.learnrec(arg, key, self.pokemon) and self.learnrec(arg, key, self.oldmons) :
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
        except Exception as e:
            await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")

    @commands.command(name = 'learn', help = 'Tells if a pokemon can learn a move')
    async def learn(self, ctx, *args):
        try:
            args = " ".join(args)
            args = args.split(",")
            mon = self.name_convert(args[0])
            move = self.name_convert(args[1])
            print(f"{ctx.author} Requesting whether {mon} can learn {move}")
            if mon in self.pokemon.keys():
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
        try:
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
        except Exception as e:
            await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")

    @commands.command(name='sprite', help='Shows a sprite')
    async def sprite(self, ctx, arg):
        print(f"{ctx.author} Requesting Sprite for {arg}")
        arg = self.name_convert(arg)
        try:
            if arg in self.pokemon.keys() and arg not in self.oldmons.keys():
                await ctx.channel.send(f"https://raw.githubusercontent.com/Dawn-Pokemon-Showdown/Sprites/master/sprites/gen5/{self.pokemon[arg]["name"].lower()}.png")
            elif arg in self.oldmons.keys():
                await ctx.channel.send(f"https://play.pokemonshowdown.com/sprites/gen5/{self.pokemon[arg]["name"].lower()}.png")
            else:
                await ctx.channel.send("I cannot find the sprite of the pokemon")
        except Exception as e:
            await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")

    @commands.command(name = 'coverage', help = 'Shows the coverage for inputted types')
    async def coverage(self, ctx, *args):
        args = (" ".join(args)).split(",")
        print(f"{ctx.author} Requesting coverage for {args}")
        try:
            supereff = set()
            neutral = set()
            resisted = set()
            immune = set()
            for arg in args:
                arg = self.name_convert(arg)
                if arg.capitalize() not in self.types:
                    await ctx.channel.send(f"Type {arg} could not be found in the database")
                    return 
                arg = arg.capitalize()
                for type in self.types:
                    if self.typechart[self.name_convert(type)]["damageTaken"][arg]==2:
                        supereff.add(type)
                        neutral.discard(type)
                        resisted.discard(type)
                        immune.discard(type)
                    elif self.typechart[self.name_convert(type)]["damageTaken"][arg]==1 and type not in supereff:
                        neutral.add(type)
                        resisted.discard(type)
                        immune.discard(type)
                    elif self.typechart[self.name_convert(type)]["damageTaken"][arg]==0.5 and type not in supereff and type not in neutral:
                        resisted.add(type)
                        immune.discard(type)
                    elif self.typechart[self.name_convert(type)]["damageTaken"][arg]==0.5 and type not in supereff and type not in neutral and type not in resisted:
                        immune.add(type)
            embed = discord.Embed(title = ", ".join(args))
            if len(supereff)!=0:
                embed.add_field(name = "Super Effective: ", value = ", ".join(supereff), inline = False)
            if len(neutral)!=0:
                embed.add_field(name = "Neutral: ", value = ", ".join(neutral), inline = False)
            if len(resisted)!=0:
                embed.add_field(name = "Not Very Effective: ", value = ", ".join(resisted), inline = False)
            if len(immune)!=0:
                embed.add_field(name = "Immune: ", value = ", ".join(immune), inline = False)
            await ctx.channel.send(embed=embed)
        except Exception as e:
            await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")  

    def dfilter(self, args: list, mons: set) -> set:
        print(f"filtering for {args}")
        for arg in args:
            ### Special Modifier Args
            if "|" in arg:
                orargs = arg.split("|")
                orset = set()
                for orarg in orargs:
                    orset|=self.dfilter([orarg],mons.copy())
                mons = orset
            elif arg.strip().startswith("!"):
                mons -=self.dfilter([arg.strip()[1:]], mons.copy())
            ### Keyword Args
            elif self.name_convert(arg.replace("type-","")).capitalize() in self.types:
                arg = self.name_convert(arg.replace("type-",""))
                newset = set()
                for mon in mons:
                    if arg.capitalize() in self.pokemon[mon]["types"]:
                        newset.add(mon)
                mons = newset
            elif self.name_convert(arg.replace("move-","")) in self.moves.keys():
                arg = self.name_convert(arg.replace("move-",""))
                newset = set()
                for mon in mons:
                    if "learnset" in self.pokemon[mon].keys() or "baseSpecies" in self.pokemon[mon].keys():
                        if self.learnrec(mon, arg, self.pokemon):
                            newset.add(mon)
                mons = newset
            elif self.name_convert(arg.replace("ability-", "")) in self.abilities.keys():
                arg = self.name_convert(arg.replace("ability-",""))
                arg = self.abilities[arg]["name"]
                newset = set()
                for mon in mons:
                    if "abilities" in self.pokemon[mon].keys():
                        if arg in self.pokemon[mon]["abilities"].values():
                            newset.add(mon)
                mons = newset
            elif self.name_convert(arg.replace("color-", "")).capitalize() in self.colors:
                arg = self.name_convert(arg.replace("color-", "")).capitalize()
                # print(arg)
                newset = set()
                for mon in mons:
                    if "color" in self.pokemon[mon].keys():
                        if arg == self.pokemon[mon]["color"]:
                            newset.add(mon)
                mons = newset
            elif self.name_convert(arg.replace("egg-", "")) in self.eggmap.keys():
                arg = self.eggmap[self.name_convert(arg.replace("egg-", ""))]
                # print(arg)
                newset = set()
                for mon in mons:
                    if "eggGroups" in self.pokemon[mon].keys():
                        if arg in self.pokemon[mon]["eggGroups"]:
                            newset.add(mon)
                mons = newset
            elif self.name_convert(arg) in self.evotypes:
                arg = self.name_convert(arg)
                newset = set()
                if arg == "fe":
                    for mon in mons:
                        if "evos" not in self.pokemon[mon].keys():
                            newset.add(mon)
                if arg == "nfe":
                    for mon in mons:
                        if "evos" in self.pokemon[mon].keys() and "prevo" in self.pokemon[mon].keys():
                            newset.add(mon)
                if arg == "lc":
                    for mon in mons:
                        if "evos" in self.pokemon[mon].keys() and "prevo" not in self.pokemon[mon].keys():
                            newset.add(mon)
                mons = newset
            elif self.name_convert(arg.replace("tier-","")) in self.tiermap:
                arg = self.tiermap[self.name_convert(arg.replace("tier-", ""))]
                # print(arg)
                newset = set()
                for mon in mons:
                    if "natDexTier" in self.pokemon[mon].keys():
                        if arg == self.pokemon[mon]["natDexTier"]:
                            newset.add(mon)
                mons = newset
            elif self.name_convert(arg.replace("tag-","")) in self.tagmap:
                arg = self.name_convert(arg.replace("tag-",""))
                newset = set()
                for mon in mons:
                    if "tags" in self.pokemon[mon].keys():
                        if self.tagmap[arg] in self.pokemon[mon]["tags"]:
                            newset.add(mon)
                mons = newset
            elif self.name_convert(arg) == "new":
                newset = set()
                for mon in mons:
                    if mon not in self.oldmons.keys():
                        newset.add(mon)
                mons = newset
            ### Type Args
            elif self.name_convert(arg).startswith("weak"):
                arg = self.name_convert(arg).replace("weak","")
                if arg.capitalize() not in self.types:
                    print(f"{arg} could not be found")
                    return arg
                newset = set()
                for mon in mons:
                    if self._typemod(self.pokemon[mon]["types"],arg.capitalize())>1:
                        newset.add(mon)
                mons = newset
            elif self.name_convert(arg).startswith("resists"):
                arg = self.name_convert(arg).replace("resists","")
                if arg.capitalize() not in self.types:
                    print(f"{arg} could not be found")
                    return arg
                newset = set()
                for mon in mons:
                    if self._typemod(self.pokemon[mon]["types"],arg.capitalize())<1:
                        newset.add(mon)
                mons = newset
            ### Comparison Args
            else:
                print(f"{arg} could not be found")
                return arg
        return mons
    
    @commands.command(name = 'ds', help = 'Search the dex for mons that match')
    async def dsearch(self, ctx, *args):
        args = (" ".join(args)).split(",")
        print(f"{ctx.author} Requesting dex search for {args}")
        # try:
        ret = self.dfilter(args, set(self.pokemon.keys()))
        print(f"got {ret}")
        if type(ret) == str:
            await ctx.channel.send(f"argument {ret} could not be found")
        elif len(ret) != len(self.pokemon.keys()) and len(ret) != 0:
            ret = sorted([self.pokemon[key]["name"]for key in ret])
            ret = ", ".join(ret)
            while len(ret)>2000:
                await ctx.channel.send(", ".join(ret.split(", ")[:100]))
                ret = ", ".join(ret.split(", ")[100:])
            await ctx.channel.send(ret)
        elif len(ret) == 0:
            await ctx.channel.send("Search resulted in no Pokemon.")
        else:
            await ctx.channel.send("Search resulted in all Pokemon.")
        # except Exception as e:
        #     await ctx.channel.send(f"An Error has occurred, {e.__class__.__name__}: {e}")

    @commands.command(name = 'DeMorgan', help = "display De Morgan's laws")
    async def demorgan(self, ctx):
        await ctx.channel.send("https://en.wikipedia.org/wiki/De_Morgan%27s_laws")

    
async def setup(bot):
    await bot.add_cog(PokeInfo(bot))

