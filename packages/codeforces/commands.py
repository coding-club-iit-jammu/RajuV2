# Add new commands in this file
# Also modify `__init__.py` to expose the methods in the package
from .utils import get
import json
from .config import Config
from random import sample


async def getUserInfo(handles):
    """
    Refer: https://codeforces.com/apiHelp/methods#user.info

    Fetches the user info of the given handles

    Parameters
    ----------
    handles: list<str>
        List of handles of all users

    Returns
    -------
    list
        List of json objects contating user info for the handles
    """
    methodName = 'user.info'
    handleParams = 'handles=' + ';'.join(handles)
    return (await get(methodName, handleParams))['result']


async def getContests(all=False):
    """
    Refer: https://codeforces.com/apiHelp/methods#contest.list

    Fetches information about all the future contests

    Parameters
    ----------
    all: bool
        false: Only fetch official CF division contests
        true: fetch all gymkhana contests as well
    Returns
    -------
    Returns a list of `Contest` objects.

    See Also: https://codeforces.com/apiHelp/objects#Contest
    """
    methodName = 'contest.list'
    methodParam = 'gym=' + str(all)

    # GET the json request
    allContests = (await get(methodName, methodParam))['result']

    # Filter the response for only future contests
    # define the filter clause lambda
    def clause(x): return x['phase'] == "BEFORE"
    futureContests = list(filter(clause, allContests))

    return futureContests


async def getProblem(tags, counts=2, maxRating=None):
    """
    Refer: https://codeforces.com/apiHelp/methods#problemset.problems

    Fetches a list of all problems filtered by tags

    Parameters
    ----------
    tags: list
        list of tags

    Returns
    -------
    List of `Problem` objects

    See Also: https://codeforces.com/apiHelp/objects#Problem
    """
    methodName = "problemset.problems"
    methodParams = "tags=" + ";".join(tags)

    # Get the json request
    problems = await get(methodName, methodParams)

    # Only get a max-amount (N) of problems
    # from the responce problemset
    counts = min(counts, Config['MAX_PROBLEMS'])

    allProblems = problems['result']['problems']

    # filter by maxRatings using a clause
    if(maxRating):
        def clause(x):
            try:
                return x['rating'] <= maxRating
            except:
                return True
        allProblems = list(filter(clause, allProblems))

    lenProblems = len(allProblems)

    # if no problems are found return empty Array
    if(lenProblems < counts):
        return allProblems

    # randomly select the N problems from the problemset
    randomProblemsIdxs = sample(range(lenProblems), counts)
    sampledProblems = [allProblems[i] for i in randomProblemsIdxs]

    return sampledProblems


async def randomProblem():
    """
    Get a random problem from Codeforces. 

    Returns
    -------
    A `Problem` object

    See Also: https://codeforces.com/apiHelp/objects#Problem
    """
    # A list of problem tags
    tags = ["fft",
            "two pointers",
            "binary search",
            "dsu",
            "strings",
            "number theory",
            "data structures",
            "hashing",
            "shortest paths",
            "matrices",
            "string suffix structures",
            "graph matchings",
            "dp",
            "dfs and similar",
            "meet-in-the-middle",
            "games",
            "schedules",
            "constructive algorithms",
            "greedy",
            "bitmasks",
            "divide and conquer",
            "flows",
            "geometry",
            "math"]
    problem = None  
    while(problem is None):
    # Get a random tag
        n = sample(range(len(tags)),1)[0] 
        tag = tags[n]
        problem = await getProblem([tag],counts=1)
    
    return problem

# For Testing


async def test():
    # Add debug/testing code here
    # resp = await getProblem(["dp"], 2, 2000)
    # resp_question = await getProblem(["implementation", "dp"])
    # resp = await getContests()
    resp = await randomProblem()
    print(json.dumps(resp, indent=3))
    return

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
