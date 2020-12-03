import yaml
import discord
from discord.ext import commands
import configparser

config = configparser.ConfigParser()
client = commands.Bot(command_prefix='=')
uid = 94902686654136320
a = "main"

def displayCharacter(userid, charid):
    with open('characters.yaml') as f:
        characters = yaml.load(f, Loader=yaml.FullLoader)
        try:
            name = characters[userid]
        except KeyError:
            return("You do not have any characters! Please make a character.")
        try:
            name = characters[userid][charid]['name']
        except KeyError:
            return("This character does not exist. Are you sure you didn't make a mistake?")
        cls = characters[userid][charid]['class']
        hp = characters[userid][charid]['health']
        mc = characters[userid][charid]['magiccircuit']
        strn =characters[userid][charid]['str']
        dur = characters[userid][charid]['dur']
        spd = characters[userid][charid]['spd']
        arc = characters[userid][charid]['arc']
        base = ("[{}]\n-- {}\nHEALTH: {}\nMC: {}\nStrength - {}\nDurability - {}\nSpeed - {}\nArcana - {}".format(name, cls, hp, mc, strn, dur, spd, arc)) 
        if characters[userid][charid]['inventory'] is not None:
            base = base + "\nInventory:"
            for index, item in enumerate(characters[userid][charid]['inventory']):
                base = base + "\n\t{}: {}".format(index+1, item)
        return(base)
@client.event
async def on_ready():
    print("I LIVE")

@client.command()
async def test(ctx):
    ctx.send("cringe")

@client.command()
async def show(ctx, cid = "main"):
        await ctx.send(displayCharacter(ctx.author.id, cid))

#with open('characters.yaml') as f:
    #things = yaml.load(f, Loader=yaml.FullLoader)
    #print(things[uid]['secondary'])

#displayCharacter(uid)
try:
    with open('config.ini') as f:
        config.read_file(f)
        client.run(config['DEFAULT']['token'])
except IOError:
    config['DEFAULT'] = {'token': ''}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("No config file found. A new config file has been generated, please fill it out.")
