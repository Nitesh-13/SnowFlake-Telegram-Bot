def checkIfExist(userId,user,submitstatus):
    id = str(userId);
    if id in user.keys() and id in submitstatus.keys():
        return 1
    else:
        submitstatus[id] = False
        user[id] = []
        return 0

def showRollCall(userid,user,present):
    for x in user[str(userid)]:
        if user[str(userid)][len(user[str(userid)])-1] == x:
            present = present + x + "."
        else:
            present = present + x + ", "
    return present

def resetRollCall(userId,user):
    user[str(userId)].clear()
