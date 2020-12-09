#import yaml
import sqlite3 #fuck yaml.
import discord
from discord.ext import commands
import configparser

config = configparser.ConfigParser()
client = commands.Bot(command_prefix='=')
conn = sqlite3.connect('characters')
c = conn.cursor()
stats = { 0:'S', 1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F'}
uid = 94902686654136320

def loadCharacter(userid, charid):
    val = c.execute("SELECT * from characters where uid = ? and cid is ?", (userid,charid)).fetchone() 
    if val is None:
        val = "This character does not exist, please check for typos."
        if c.execute("SELECT * from characters where uid = ?", (uid,)).fetchone() is None:
            val = "You do not have any characters <@{}>. Please make a character...".format(uid)
    return val #FIXME: THIS IS BAD. ALL OF THIS IS BADNESS. MAKE IT RETURN NULL AND IMPLEMENT *ACTUAL* FUCKING ERROR HANDLING!!!!!!

def displayCharacter(uid, cid):
    charInfo = loadCharacter(uid, cid)
    if not type(charInfo) is tuple:
        return(charInfo)
    base = ("[{}]\n-- {}\nHEALTH: {}\nMC: {}\nStrength - {}\nDurability - {}\nSpeed - {}\nArcana - {}".format(charInfo[2], charInfo[3], charInfo[4], charInfo[5], stats[charInfo[6]], stats[charInfo[7]], stats[charInfo[8]], stats[charInfo[9]])) 
    if charInfo[10] is not None:
        base = base + "\nInventory:"
        for index, item in enumerate(characters[userid][charid]['inventory']):
            base = base + "\n\t{}: {}".format(index+1, item)
    return(base)

@client.event
async def on_ready():
    print("I LIVE")

def edit(key, userid, charid, value):
    c.execute('update characters set {} = ? where uid = ? and cid is ?'.format(key), (value, userid, charid)) # please inject me senpai!
    #FIXME: make a disgusting elif chain or make edit functions their own thing, this is fucking dogshit but it 'works'.
    conn.commit()

@client.command()
async def edit_name(ctx, val, cid = None):
    edit("name", ctx.author.id, cid, val)
    await ctx.send("**[{}]**".format(val))

@client.command()
async def edit_hp(ctx, val:int, cid = None):
    edit("health", ctx.author.id, cid, val)
    await ctx.send("Health: **[{}]**".format(val))

@client.command()
async def edit_mc(ctx, val:int, cid = None):
    edit("magiccircuit", ctx.author.id, cid, val)
    await ctx.send("**Magic Circuits: [{}]**".format(val))

@client.command()
async def edit_str(ctx, val, cid = None):
    if val != 'S' or 'A' or 'B' or 'C' or 'D' or 'E' or 'F':
        await ctx.send("Please input a rank from S to F.")
    edit("strength", ctx.author.id, cid, val)
    await ctx.send("Strength: **{}**".format(val))

@client.command()
async def edit_dur(ctx, val, cid = None):
    if val != 'S' or 'A' or 'B' or 'C' or 'D' or 'E' or 'F':
        await ctx.send("Please input a rank from S to F.")
    edit("durability", ctx.author.id, cid, val)
    await ctx.send("Durability: **{}**".format(val))

@client.command()
async def edit_spd(ctx, val, cid = None):
    if val != 'S' or 'A' or 'B' or 'C' or 'D' or 'E' or 'F':
        await ctx.send("Please input a rank from S to F.")
    edit("speed", ctx.author.id, cid, val)
    await ctx.send("Speed: **{}**".format(val))

@client.command()
async def edit_arc(ctx, val, cid = None):
    if val != 'S' or 'A' or 'B' or 'C' or 'D' or 'E' or 'F':
        await ctx.send("Please input a rank from S to F.")
    edit("arcana", ctx.author.id, cid, val)
    await ctx.send("Arcana: **{}**".format(val))

@client.command()
async def set_up(ctx, cid = None):
    print(cid)
    charInfo = loadCharacter(uid, cid)
    if type(charInfo) is tuple:
        await ctx.send("That character already exists!")
    else:
        print("does it even????")
        c.execute('insert into characters(uid,cid) values(?,?)', (ctx.author.id,cid))
        conn.commit()
        print("help???????????")
        await ctx.send("**{}**".format(displayCharacter(ctx.author.id, cid)))
        print("XD")

@client.command()
async def show(ctx, cid = None):
    #print(displayCharacter(ctx.author.id, cid))
    await ctx.send("** {} **".format(displayCharacter(ctx.author.id,cid)))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send("Please input a number...")

#print(displayCharacter(uid,None)) #debug
try:
    with open('config.ini') as f:
        config.read_file(f)
        client.run(config['DEFAULT']['token'])
except IOError:
    config['DEFAULT'] = {'token': ''}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("No config file found. A new config file has been generated, please fill it out.")
