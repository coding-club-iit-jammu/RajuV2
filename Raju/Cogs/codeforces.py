from packages.codeforces.commands import getProblem, getUserInfo, getContests
import discord
from discord.ext import commands
import json

CODEEFORCES_THUMBNAIL = "https://sta.codeforces.com/s/96009/images/codeforces-telegram-square.png"


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
    async def listcontests(self, ctx, division=None):
        """
        List the upcoming contest list. 
        Uses the Optional arg for filtering for div:1,2,3 
        Checks arg type, and if valid (1-3).
        """
        # TODO: Fetch atmost 5 days of contests

        allContests = await getContests()
        if(division):
            errorCode, errorMessage = checkTypeInt(division, "division")
            if(errorCode == -1):
                await ctx.send(errorMessage)
                return
            division = int(division)
            errorCode, errorMessage = checkValidDiv(division)
            if(errorCode == -1):
                await ctx.send(errorMessage)
                return

            allContests = filterContest(allContests, division)
            if(len(allContests) == 0):
                await ctx.send("No Contests found for Div. "+str(division))

        for contest in allContests:
            Title, Url, Type, StartTime = extractContestFields(contest)
            embedVar = makeContestEmbed(Title, Url, Type, StartTime)
            await ctx.send(embed=embedVar)
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

        # Initialize maxRating as an empty String
        maxRating = ""
        # check if user has given a maxRating parameter
        if("#" in args):
            args, maxRating = (args.split("#"))
        # remove spaces
        maxRating = maxRating.strip()
        # split the tags by commas and strip each tag
        args = list(args.split(","))
        args = [arg.strip() for arg in args]

        if(maxRating == ""):
            problems = await cf.getProblem(args)
        else:
            # type checking the maxRating
            errorCode, errorMessage = checkTypeInt(maxRating, "maxRating")
            if(errorCode == -1):
                await ctx.send(errorMessage)
                return
            problems = await cf.getProblem(args, 2, int(maxRating))

        if(len(problems) == 0):
            errorTag = ",".join(args)
            await ctx.send("No problems found with tags "+errorTag)

        for problem in problems:
            problemTitle, problemURL, problemRating, problemTags = extractProblemFields(
                problem)
            embedVar = makeProblemEmbed(
                problemTitle,  problemURL, problemRating, problemTags)
            await ctx.send(embed=embedVar)

        # await ctx.send(json.dumps(problems, indent=3))


def setup(bot):
    bot.add_cog(CodeForces(bot))


"""
    Added extra functionality for better display
"""


def convertTime(time):
    """
    Converting time in seconds to datetime object
    returns: string
    """
    from datetime import datetime
    s = (datetime.fromtimestamp(time).strftime("%I:%M %p %A, %B %d, %Y "))
    return s


def extractProblemFields(problem):
    """
     Extract Fields from a JSON
    returns: the extracted fields
    """
    problemTitle = problem["name"]
    problemContestId = problem["contestId"]
    problemIndex = problem["index"]
    problemURL = "https://codeforces.com/contest/" + \
        str(problemContestId)+"/problem/"+str(problemIndex)
    problemRating = problem.get("rating", "Un-rated")
    problemTags = ",".join(problem["tags"])

    return problemTitle, problemURL, problemRating, problemTags


def extractContestFields(contest):
    """
    Extract Fields from a JSON
    returns: the extracted fields
    """
    contestTitle = contest["name"]
    contestType = contest["type"]
    contestTime = convertTime(contest["startTimeSeconds"])
    contestID = contest["id"]
    contestURL = "http://codeforces.com/contests/" + str(contestID)
    return contestTitle, contestURL, contestType, contestTime


def makeEmbedTemplate(Title, Url, Thumbnail=CODEEFORCES_THUMBNAIL):
    """
    Makes an embedTemplate given Title, url and thumbnail
    returs: Embed Object
    """
    embedVar = discord.Embed(
        title=Title, color=0x00ff00, url=Url)
    embedVar.set_thumbnail(url=Thumbnail)
    return embedVar


def makeContestEmbed(Title, Url, Type, StartTime):
    """
    Makes an embed for a contest 
    returns: Embed Object
    """
    embedVar = makeEmbedTemplate(Title, Url)
    embedVar.add_field(name="Type", value=Type, inline=False)
    embedVar.add_field(name="Start Time", value=StartTime, inline=False)
    return embedVar


def makeProblemEmbed(Title, Url, Rating, Tags):
    """
    Makes an embed for a Problem
    returns: Embed Object
    """
    embedVar = makeEmbedTemplate(Title, Url)
    embedVar.add_field(name="Rating", value=Rating, inline=False)
    embedVar.add_field(name="Tags", value=Tags, inline=False)

    return embedVar


"""
    Functions for checking Arguments Validity
"""


def checkTypeInt(argument, name):
    try:
        argument = int(argument)
        return 1, ""
    except:
        return -1, "Please send a valid integer argument for "+name


def checkValidDiv(division):
    """
    Checks whether divsion lies in a range of 1-3
    """

    if(division < 1 or division > 3):
        return -1, str(division)+" is not a valid Division"
    return 1, ""


def filterContest(allContests, division):
    """
    Filters contest by their division
    """

    filterTag = "Div. "+str(division)
    filteredContests = []
    for contest in allContests:
        if(filterTag in contest["name"]):
            filteredContests.append(contest)
    return filteredContests
