import aiohttp
import asyncio

REQ_PREFIX = 'https://codeforces.com/api/'

# TODO: Use only 1 connection for the entire application
#       Could use signal for that


async def get(name, params):
    """
    Performs the GET request by constructing the request from the name and params, Then return the Json result
    Refer: https://codeforces.com/apiHelp/ 
    """

    # construct the url for the request
    # Examples: 
    # >>> get("user.info","handles=tourist")
    # request: 
    request = f'{REQ_PREFIX}{name}?{params}'
    

    # send the request and return the result
    async with aiohttp.ClientSession() as session:
        async with session.get(request) as response:
            # debug
            # print(request)
            resp = await response.json()
            await session.close()
            return resp
