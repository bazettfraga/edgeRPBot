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
    return val

def displayCharacter(uid, cid):
    charInfo = loadCharacter(uid, cid)
    if not type(charInfo) is  tuple:
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
    c.execute('update characters set ? = ? where uid = ? and cid is ?', (key, userid, charid, value))
    c.commit()

@client.command()
async def edit_name(ctx, name, cid = None):
    edit("name", ctx.author.id, cid, name)
    await ctx.send("**[{}]**".format(name))

@client.command()
async def test(ctx):
    ctx.send("cringe")

@client.command()
async def show(ctx, cid = None):
    await ctx.send("**", displayCharacter(ctx.author.id, cid), "**")

print(displayCharacter(uid,None)) #debug
#try:
#    with open('config.ini') as f:
#        config.read_file(f)
#        client.run(config['DEFAULT']['token'])
#except IOError:
#    config['DEFAULT'] = {'token': ''}
#    with open('config.ini', 'w') as configfile:
#        config.write(configfile)
#    print("No config file found. A new config file has been generated, please fill it out.")
