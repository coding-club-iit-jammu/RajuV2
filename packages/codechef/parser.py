# A Parser for the https://www.codechef.com/contests page

import aiohttp
from bs4 import BeautifulSoup
# Some useful contests
URL = "https://www.codechef.com/contests/"
FUTURE_CONTESTS_START = '<h3 id="future-contests">Future Contests</h3>'
FUTURE_CONTESTS_END = '<h3 id="past-contests">Past Contests</h3>'


async def getFutureContests():
    """
    Returns a table of the Future Contests listed on contestsPage: "https://www.codechef.com/contests/"
    Columns for the table:         
    ['CODE', 'NAME', 'START', 'END']

    # Example: 
    ----------
    >>> getFutureContests()

    [['CODE', 'NAME', 'START', 'END'], 
    ['CMR12121', 'CodeMate Round 1', '09 Jan 2021 19:00:00', '09 Jan 2021 21:00:00'], 
    ['NITJ2021', 'Code IT NITJ', '10 Jan 2021 19:00:00', '10 Jan 2021 21:00:00'], 
    ['COOK126', 'January Cook-Off 2021', '24 Jan 2021 21:30:00', '25 Jan 2021 00:00:00']]

    """
    # Change user-agent to appear as a browser to get the result. To not get 403 Forbidden Response.
    async with aiohttp.ClientSession(headers={'User-agent': 'Mozilla/5.0'}) as session:
        async with session.get(URL) as response:

            resp = await response.text()
            await session.close()

            # !!!!!!!!!!!!!!!!!!!!!!!!
            # THIS IS A VERY BAD HACK!
            # IF IT FAILS, THEN REWRITE IT TO GET THE FUTURE CONTESTS RESULT ON THE WEBPAGE

            # The content table is between the two string START, END
            # Check the html data for the same
            future_contests_and_rest = resp.split(
                FUTURE_CONTESTS_START, maxsplit=1)[1]
            future_contests = future_contests_and_rest.split(
                FUTURE_CONTESTS_END, maxsplit=1)[0]

            # This gets me the parsed html
            parsed_resp = BeautifulSoup(
                future_contests, features='html.parser')

            parsed_resp.get_text()
            table_html = parsed_resp.find('table')
            # print(parsed_resp)
            return tableDataText(table_html)


# Refer: https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
# Contruct a table from the html data.
def tableDataText(table):
    rows = []
    trs = table.find_all('tr')
    headerow = [td.get_text(strip=True)
                for td in trs[0].find_all('th')]  # header row
    if headerow:  # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs:  # for every table row
        # *Changed the separators to join multiple string properly
        rows.append([td.get_text(strip=True, separator=" ")
                     for td in tr.find_all('td')])  # data row
    return rows


async def test():
    print(await getFutureContests())
    pass

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
