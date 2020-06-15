import os
import random
import urllib3

from ashrpg.class_client import ClassClient
from ashrpg.feat_client import FeatClient
from ashrpg.roll_client import RollClient
from dotenv import load_dotenv
from discord import Embed, Color, Game
from discord.ext import commands

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

class_client = ClassClient()
feat_client = FeatClient()
roll_client = RollClient()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    with open('.pid', 'w') as f:
        f.write(str(os.getpid()))
    await bot.change_presence(activity=Game(name="AshRPG"), status="https://ashenkingdoms.com")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'tangle' in message.content.lower():
        response = '🐍Ssssssssss 🐍'
        return await message.channel.send(response)

    if '\\ashrpg/' in message.content.lower():
        response = '\\ashrpg/'
        return await message.channel.send(response)

    await bot.process_commands(message)

@bot.command(name='ashrpg', help='Print the namesake')
async def ashrpg(ctx):
    """
    \ashrpg/
    """
    await ctx.send(f"{ctx.author.mention} \\ashrpg/")

@bot.command(name='feat', help='<search_query> -- Search the AshRPG game for a feat by its name')
async def get_feat(ctx, *args):
    """
    Search for feats, or get a list of feats matching a query.
    If none found, will return a message stating no feats found.
    """
    value = ' '.join(args)

    response = feat_client.search(value)

    await ctx.send(content=f"{ctx.author.mention}", embed=response)

@bot.command(name='class', help='<class_name> <query> -- Search for AshRPG class details and talents/ feats')
async def get_class_info(ctx, cls: str, *args):
    """
    Search for class information, or get a list of class talents and features matching a query.
    If the class doesn't exist, return message saying the class is incorrect.
    If no features found for a class, return message saying no talents/ features found.
    """
    value = ' '.join(args)

    if not cls in class_client.class_list.keys():
        res = Embed(title=f"Class not valid: \"{cls}\"", color=Color.red())
        res.add_field(name='Valid Classes', value='\n'.join(class_client.class_list.keys()))
        return await ctx.send(content=f"{ctx.author.mention}", embed=res)

    if not value:
        response = class_client.get_class_info(cls.lower())
    else:
        response = class_client.search_talents_and_feats(cls.lower(), value)

    await ctx.send(content=f"{ctx.author.mention}", embed=response)

@bot.command(name='roll', help='<#d#(+|-#)> -- Roll dice based on the parameters')
async def roll_dice(ctx, *args):
    """
    Roll dice, in the format #d# and optional [+|-] #
    If the format is incorrect, return message saying invalid format
    """
    value = ''.join(args)

    dice_roll = roll_client.roll_dice(value)

    if not dice_roll:
        response = Embed(title=f"Dice Roll Not Valid: \"{value}\"", color=Color.red())
    else:
        response = Embed(title=f"{dice_roll}", color=Color.green())

    await ctx.send(embed=response)

bot.run(TOKEN)
