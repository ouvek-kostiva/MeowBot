from db.dbquery import *
from scripts.templates import send_text_message

def chkNewUser(userid):
    c, conn = openCursor("db/istockbot.db")
    usrXist = existUser(c, conn,"user", userid)
    if usrXist != True:
        welcome_message = "歡迎您使用本服務\n"
        print("New User:",userid)
        insertUser(c, conn,"user", userid)
        cookie, points, tutorial, daily = queryUser(c, conn,"user", userid)
        points = int(points) + 1000
        updateUserPts(c, conn,"user", userid, points)
        welcome_message = welcome_message + "您現在有 " + str(points) + " 點\n"
        welcome_message = welcome_message + "按「功能說明 *help」或直接輸入「*help」顯示說明"
        send_text_message(userid, welcome_message)
        closeCursor(conn)
        return True
    closeCursor(conn)
    
def hasPts(userid, pts):
    c, conn = openCursor("db/istockbot.db")
    cookie, points, tutorial, daily = queryUser(c, conn,"user", userid)
    closeCursor(conn)
    if int(points) >= int(pts):
        return True
    else:
        return False
        
def addPts(userid, pts):
    c, conn = openCursor("db/istockbot.db")
    cookie, points, tutorial, daily = queryUser(c, conn,"user", userid)
    points = int(points) + int(pts)
    updateUserPts(c, conn,"user", userid, points)
    closeCursor(conn)
    
def subPts(userid, pts):
    c, conn = openCursor("db/istockbot.db")
    cookie, points, tutorial, daily = queryUser(c, conn,"user", userid)
    points = int(points) - int(pts)
    updateUserPts(c, conn,"user", userid, points)
    closeCursor(conn)
    
def chgCookie(userid, cookie):
    c, conn = openCursor("db/istockbot.db")
    oldcookie, points, tutorial, daily = queryUser(c, conn,"user", userid)
    updateUserCookie(c, conn,"user", userid, cookie)
    closeCursor(conn)
    
def getCookie(userid):
    c, conn = openCursor("db/istockbot.db")
    cookie, points, tutorial, daily = queryUser(c, conn,"user", userid)
    closeCursor(conn)
    #print(cookie, points, tutorial, daily)
    return cookie