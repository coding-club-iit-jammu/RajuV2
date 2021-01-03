import os
import discord
from discord.ext import commands

class CodeChef(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Codechef command added")   

    @commands.command()
    async def codechef(self, ctx, role_name: str = ""):
        await ctx.send(f"this is codechef command") 

def setup(bot):
    bot.add_cog(CodeChef(bot))
