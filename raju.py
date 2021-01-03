import os
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(
        command_prefix='~',
        description='Raju v2',
        case_insensitive=True,
        intents=intents
    )

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='code..'))
    print(f'{bot.user.mention} has connected to Discord!')

@bot.command()
async def hi(ctx):
    await ctx.send(f'{ctx.author.mention} Hi I Raju v2 in making')

@bot.command()
async def leave(ctx):
    await ctx.send('Leaving server. BYE!')
    await bot.close()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        msg_s = f"{ctx.author.mention} Invalid Command"
        await ctx.send(msg_s)
    else:
        raise error

bot.run(TOKEN)
