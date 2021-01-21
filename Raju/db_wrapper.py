from Raju import db


def makeDoc(discordId, handle=None):
    doc = {'discordId': discordId}
    if(handle is None):
        pass
    else:
        doc['handle'] = handle
    return doc


async def addUser(discordId, handle):
    """
    Add the handle against the discordId
    """
    db.users.insert_one(makeDoc(discordId, handle))


async def updateUser(discordId, handle):
    """
    Update the handle of a user in the database
    """
    db.users.replace_one(makeDoc(discordId), makeDoc(discordId, handle))


async def deleteUser(discordId):
    """
    Remove the user with the following discord Id
    """
    db.users.delete_one(makeDoc(discordId))


async def if_exists(discordId):
    """
    Checks if the given Id exists in the record
    """
    user = db.users.find_one(makeDoc(discordId), {'id':0, 'discordId' : 1})
    if(user is None):
        return False
    else:
        return True


async def getUserHandle(discordId):
    """
    Returns the userHandle for a discord Id, 
    Make sure to check if_exists first
    """
    user = db.users.find_one(makeDoc(discordId), {'id':0, 'handle' : 1})
    if(user is None):
        return None
    else:
        return user["handle"]


async def getAllUser(projection : dict):
    return list(db.users.find({}, projection))
