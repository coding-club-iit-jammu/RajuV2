import os
import discord
import pprint
from discord.ext import commands
from datetime import datetime
import pytz
import requests
import json
import packages.codechef as cc

tz = pytz.timezone('Asia/Kolkata')
CODECHEF_LOGO = 'https://i.pinimg.com/originals/c5/d9/fc/c5d9fc1e18bcf039f464c2ab6cfb3eb6.jpg'


class CodeChef(commands.Cog):
    """
    Define commands which use data from CodeChef platform.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Module Codechef Loaded")

    @commands.group(pass_context=True)
    async def Codechef(self, ctx):
        # TODO: Remove on release
        print("1212")
        if ctx.invoked_subcommand is None:
            await ctx.send("Ping 1")

    @Codechef.command()
    async def listcontests(self, ctx):
        """
        Fetches the contests from https://www.codechef.com/contests and displays the future contests
        """
        # Get the list of table contents
        # remove the title row
        contest_table = (await cc.getFutureContests())[1:]

        # Contruct the message embed and send
        for contest in contest_table:
            (CODE, NAME, START, _) = contest
            URL = f'https://www.codechef.com/{CODE}'
            embed = discord.Embed(title=NAME, color=0x00b4b4, url=URL)
            embed.set_thumbnail(url=CODECHEF_LOGO)
            embed.add_field(name='Start Time', value=START[:-3], inline=False)
            await ctx.send(embed=embed)

    @Codechef.command()
    async def contestsinfo(self, ctx, code: str):
        uri = f'https://www.codechef.com/api/contests/{code}'
        res = requests.get(uri)
        rev_json = json.loads(res.content)
        if(rev_json['status'] == 'success'):
            emb = discord.Embed(title=code, description=rev_json['name'])
            img_url = f"https://s3.amazonaws.com/codechef_shared{rev_json['banner']}"
            emb.set_image(url=img_url)
            await ctx.send(embed=emb)
        else:
            await ctx.send("Invalid Contest Code")


def setup(bot):
    bot.add_cog(CodeChef(bot))
