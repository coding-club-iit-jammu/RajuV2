import discord
from discord.ext import commands


class CodeForces(commands.Cog):
    """
    Define Operations for getting data from the Codeforces platform.
    """

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Module: CodeForces Loaded")

    @commands.group(pass_context=True)
    async def Codeforces(self, ctx):
        # Todo: Add Error Message here
        if ctx.invoked_subcommand is None:
            await ctx.send("Error Msg")

    @Codeforces.command()
    async def listcontests(self, ctx):
        """
        List the upcoming contest list. 
        Uses the Optional arg for filtering for div:1,2,3 
        """
        # TODO: Fetch atmost 5 days of contests
        pass

    @Codeforces.command()
    async def ratings(self, ctx):
        """
        List the current rating list of all registered IIT Jammu members.
        """
        # Todo: Get the user-handle from and proceed
        pass

    @Codeforces.command()
    async def assign_roles(self, ctx):
        """ 
        Assign discord roles based on the CF role, and also assign appropriete colors
        """
        # Todo: Lookup role assignments
        pass
