import yaml
import discord
from discord.ext import commands

client = commands.Bot(command_prefix='=')
uid = 94902686654136320

@client.event
async def on_ready():
    print("I LIVE")

@client.command()
async def test(ctx):
    ctx.send("cringe")

with open('characters.yaml') as f:
    things = yaml.load(f, Loader=yaml.FullLoader)
    for thing in things:
        for uid, v in thing.items():
            print(str(uid), "->", v)

#[{94902686654136320: [{'name': ''}, {'class': ''}, {'MC': ''}, {'Str': ''}, {'Dur': ''}, {'Spd': ''}, {'Arc': ''}]}]


#client.run('TOKEN')
