import packages.codeforces as cf
from packages import db
import discord
from discord.ext import commands
import json
import asyncio

CODEEFORCES_THUMBNAIL = "https://sta.codeforces.com/s/96009/images/codeforces-telegram-square.png"
CODING_CLUB_URL = "https://www.codingclubiitjammu.tech"
CODING_CLUB_LOGO = "https://www.codingclubiitjammu.tech/assets/cc.png"

ROLES = ["beginner", "newbie", "pupil",
         "specialist," "expert", "candidate master", "GAWD"]
ROLE_COLOR = {"beginner": 0xfff3e6, "newbie": 0xdddddd, "pupil": 0xc0e218,
              "specialist": 0x64dfdf, "expert": 0x1a508b, "candidate master": 0x48426d, "GAWD": 0xffcc29}


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
        allContests = await cf.getContests()

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
            embedVar = makeContestEmbed(contest)
            await ctx.send(embed=embedVar)

        pass

    @cf.command()
    async def ratings(self, ctx):
        """
        List the current rating list of all registered IIT Jammu members.
        """
        allRecords = await db.getAllUser()
        handles = []
        for record in allRecords:
            if('handle' in record):
                handles.append(record['handle'])

        users = await cf.getUserInfo(handles)
        user_list = []
        for user in users:
            user_list.append((user['handle'], user['rating']))

        # Sort according to the user-rating
        def rating(u):
            return u[1]
        user_list.sort(key=rating, reverse=True)
        rating_result = [x[0]+":  "+str(x[1]) for x in user_list]

        embedVar = makeEmbedTemplate(
            "Coding Club IITJ Member- Ratings", CODING_CLUB_URL, CODING_CLUB_LOGO)
        printString = '\n'.join(rating_result)
        embedVar.description = printString

        await ctx.send(embed=embedVar)

    @ cf.command()
    async def assign_roles(self, ctx):
        """
        Assign discord roles based on the CF role, and also assign appropriete colors
        """
        # Todo: Lookup role assignments
        discordId = ctx.author.id
        isPresent = await db.if_exists(discordId)
        user = ctx.guild.get_member(discordId)
        if(isPresent == False):
            await ctx.send(f'User: {user.mention} does not exists in our records. Please use userAdd command to add your cf handle first')
            return
        userHandle = await db.getUserHandle(discordId)
        userData = await cf.getUserInfo([userHandle])
        userRank = userData[0].get("rank", None)
        if(userRank):
            for role in user.roles:
                if(role.name in ROLES):
                    await user.remove_roles(role)
            if(userData[0].get("rating", 0) >= 2100):
                await give_role(user, "GAWD", discord.Colour(ROLE_COLOR["GAWD"]))
                await ctx.send(f'You have been awarded GAWD status !! {user.mention}')
            else:
                await give_role(user, userRank, discord.Colour(ROLE_COLOR[userRank]))
                await ctx.send(f'Updated user-role to {userRank} for {user.mention}')

        else:
            await give_role(user, "beginner", discord.Colour(ROLE_COLOR["beginner"]))
            await ctx.send(f'No rank on CodeForces, given beginner status to {user.mention}')
        pass

    @ cf.command()
    async def Problem(self, ctx, *, args):
        """
        Display a problem with the given tags and rating limit
        """
        import packages.codeforces as cf
        import json

        maxRating = ""
        # check if user has given a maxRating parameter
        if("#" in args):
            args, maxRating = (args.split("#"))

        # remove spaces
        # split the tags by commas and strip each tag
        maxRating = maxRating.strip()
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
            embedVar = makeProblemEmbed(problem)
            await ctx.send(embed=embedVar)

    @ cf.command()
    async def userAdd(self, ctx, handle: str):
        """
        Add a user to the db
        """
        discordId = ctx.author.id
        isPresent = await db.if_exists(discordId)
        user = ctx.guild.get_member(discordId)
        if(isPresent):
            await ctx.send(
                f'User: {user.mention} already exists in records. You can still update your records')
            return
        handle = handle.strip()
        verified = await verify_user(ctx, handle)
        if(verified):
            await db.addUser(discordId, handle)
            await ctx.send(f'User: {user.mention} is added successfully to our records')
        else:
            await ctx.send("Couldnot Complete Verification")

    @ cf.command()
    async def userInfo(self, ctx, *handles):
        """
        Get user information based on their handle
        """
        try:
            userData = await cf.getUserInfo(handles)
            for user in userData:
                userHandle = user["handle"]
                userUrl = "https://codeforces.com/profile/"+userHandle
                userPic = "https:"+user["titlePhoto"]
                userFirstName = user.get("firstName", None)
                userLastName = user.get("lastName", "")
                embedVar = makeEmbedTemplate(userHandle, userUrl, userPic)
                if(userFirstName):
                    embedVar.add_field(
                        name="Name", value=userFirstName+" "+userLastName, inline=False)
                embedVar.add_field(
                    name="Rank", value=user["rank"], inline=False)
                embedVar.add_field(
                    name="Rating", value=user["rating"], inline=False)
                await ctx.send(embed=embedVar)
        except Exception as e:
            print("Debug", e)
            await ctx.send("Either an handle does not exist or the arguments are not specified")


def setup(bot):
    bot.add_cog(CodeForces(bot))


async def give_role(member, roles, colour):
    try:
        verf_role = discord.utils.get(member.guild.roles, name=roles)
        await member.add_roles(verf_role)
    except:
        verf_role = await member.guild.create_role(name=roles, mentionable=True, colour=colour)
        await member.add_roles(verf_role)


async def verify_user(ctx, handle) -> bool:
    """
    Verify a user handle via a submission on a random problem on codeforces
    """
    # Get the fields
    problem = await cf.getRandomProblem()
    embedVar = makeProblemEmbed(problem)
    # send the problem to the user
    await ctx.send(
        "Make a submission which results in COMPILATION ERROR on the following problem within 3 minutes:")
    await ctx.send(embed=embedVar)
    await asyncio.sleep(180)

    try:
        userStatus = await cf.getUserStatus(handle)
        latestSubmission = userStatus[0]
        verdict = latestSubmission['verdict']
        title = latestSubmission['problem']['name']

        if(verdict == "COMPILATION_ERROR" and title == problem['name']):
            return True
        else:
            return False
    except:
        return False

########################################################
# DISPLAY UTILITIES


def convertTime(time):
    """
    Converting time in seconds to datetime object
    returns: string
    """
    from datetime import datetime
    s = (datetime.fromtimestamp(time).strftime("%I:%M %p %A, %B %d, %Y "))
    return s


def makeEmbedTemplate(Title, Url, Thumbnail=CODEEFORCES_THUMBNAIL):
    """
    Makes an embedTemplate given Title, url and thumbnail
    returns: Embed Object
    """
    embedVar = discord.Embed(
        title=Title, color=0xbedcfa, url=Url)
    embedVar.set_thumbnail(url=Thumbnail)
    return embedVar


def makeContestEmbed(contest):
    """
    Makes an embed for a contest
    returns: Embed Object
    """
    Title = contest["name"]
    Type = contest["type"]
    StartTime = convertTime(contest["startTimeSeconds"])
    contestID = contest["id"]
    Url = "http://codeforces.com/contests/" + str(contestID)

    embedVar = makeEmbedTemplate(Title, Url)
    embedVar.add_field(name="Type", value=Type, inline=False)
    embedVar.add_field(name="Start Time", value=StartTime, inline=False)
    return embedVar


def makeProblemEmbed(problem):
    """
    Makes an embed for a Problem
    returns: Embed Object
    """
    Title = problem["name"]
    problemContestId = problem["contestId"]
    problemIndex = problem["index"]
    Url = "https://codeforces.com/contest/" + \
        str(problemContestId)+"/problem/"+str(problemIndex)
    Rating = problem.get("rating", "Un-rated")
    Tags = ",".join(problem["tags"])

    embedVar = makeEmbedTemplate(Title, Url)
    embedVar.add_field(name="Rating", value=Rating, inline=False)
    embedVar.add_field(name="Tags", value=Tags, inline=False)

    return embedVar

########################################################
# Checking Arguement Validity


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
########################################################
