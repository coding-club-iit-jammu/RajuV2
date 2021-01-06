from packages.codeforces.commands import getProblem, getUserInfo
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
    async def cf(self, ctx):
        # Todo: Add Error Message here
        if ctx.invoked_subcommand is None:
            await ctx.send("Call further commands in Codeforces")

    @cf.command()
    async def listcontests(self, ctx):
        """
        List the upcoming contest list. 
        Uses the Optional arg for filtering for div:1,2,3 
        """
        # TODO: Fetch atmost 5 days of contests
        pass

    @cf.command()
    async def ratings(self, ctx):
        """
        List the current rating list of all registered IIT Jammu members.
        """
        # Todo: Get the user-handle from and proceed
        pass

    @cf.command()
    async def assign_roles(self, ctx):
        """ 
        Assign discord roles based on the CF role, and also assign appropriete colors
        """
        # Todo: Lookup role assignments
        pass

    # TODO: ONLY FOR DEVELOPMENT.
    # REMOVE ON RELEASE

    @cf.command()
    async def testProblem(self, ctx, *, args):
        # handles contains of all the args
        # TEST1======= =>
        import packages.codeforces as cf
        import json
        # def get_rating(user): return user['rating']
# 
        # handle_list = [handle for handle in handles.split(' ')]
        # users = (await cf.getUserInfo(handle_list) )
        # msg = [str(a) + ": "+str(b)
        #        for (a, b) in zip(handle_list, users) ]
        args = list(args.split(" "))
        problems = await cf.getProblem(args)

        await ctx.send(json.dumps(problems,indent = 3))


def setup(bot):
    bot.add_cog(CodeForces(bot))
