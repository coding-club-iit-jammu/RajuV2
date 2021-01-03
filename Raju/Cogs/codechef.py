import os
import discord
import pprint
from discord.ext import commands
from datetime import datetime
import pytz
import requests
import json

tz = pytz.timezone('Asia/Kolkata')

class CodeChef(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Codechef command added")   

    @commands.group(pass_context=True)
    async def Codechef(self, ctx):
        print("1212")
        if ctx.invoked_subcommand is None:
            await ctx.send("Ping 1")

    @Codechef.command()
    async def listcontests(self, ctx):
        await ctx.send("contests")
    
    @Codechef.command()
    async def contestsinfo(self, ctx, code : str):
        uri = f'https://www.codechef.com/api/contests/{code}'
        res = requests.get(uri)
        rev_json = json.loads(res.content)
        if(rev_json['status'] == 'success'):
            emb = discord.Embed(title=code, description=rev_json['name'])
            img_url = f"https://s3.amazonaws.com/codechef_shared{rev_json['banner']}"
            emb.set_image(url=img_url)
            await ctx.send(embed = emb)
        else:
            await ctx.send("Invalid Contest Code")

def setup(bot):
    bot.add_cog(CodeChef(bot))
