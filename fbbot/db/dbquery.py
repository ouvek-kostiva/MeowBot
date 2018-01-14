import sqlite3
def openCursor(dbName):
    import sqlite3
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    #print("Cursor Open")
    return c, conn
    
def closeCursor(dbConn):
    conn = dbConn
    import sqlite3
    conn.close()
    #print("Cursor Close")

def queryQuest(dbCursor, dbConn, tableName, idx):
    import sqlite3
    c = dbCursor
    conn = dbConn
    c.execute("SELECT * FROM quest WHERE ind=?", (idx,))
    data=c.fetchone()
    if data is None:
        cookie = "NA"
        text = "該文件不存在，請輸入 *help 取得提示"
        pay = 0
        points = 0
        return cookie, text, pay, points
    else:
        cookie = data[1]
        text = data[2]
        pay = data[3]
        points = data[4]
        return cookie, text, pay, points
        
def insertUser(dbCursor, dbConn, tableName, userid):
    import sqlite3
    c = dbCursor
    conn = dbConn
    count = 0
    conn.execute("INSERT INTO {} (userid, cookie, points, tutorial, daily) VALUES (?,?,?,?,?)".format(tableName),(userid, "home", 0,0,"NotTaken"))
    conn.commit()
    count = count + 1
    print("New User:",userid,"added to database")
    return count
    
def existUser(dbCursor, dbConn, tableName, userid):
    import sqlite3
    c = dbCursor
    conn = dbConn
    c.execute("SELECT ind FROM user WHERE userid = ?", (userid,))
    data=c.fetchone()
    if data is None:
        return False
    else:
        return True
        
def queryUser(dbCursor, dbConn, tableName, userid):
    import sqlite3
    c = dbCursor
    conn = dbConn
    c.execute("SELECT * FROM user WHERE userid=?", (userid,))
    data=c.fetchone()
    if data is None:
        cookie = "NA"
        points = 0.0
        tutorial = "0"
        daily = "0"
        return cookie, points, tutorial, daily
    else:
        cookie = data[2]
        points = data[3]
        tutorial = data[4]
        daily = data[5]
        return cookie, points, tutorial, daily
        
def updateUserPts(dbCursor, dbConn, tableName, userid, points):
    import sqlite3
    c = dbCursor
    conn = dbConn
    c.execute("UPDATE {tn} SET points={pts} WHERE userid={usr}".format(tn=tableName, pts=points, usr=userid))
    conn.commit()
    data=c.fetchone()
    
def updateUserCookie(dbCursor, dbConn, tableName, userid, cookie):
    import sqlite3
    c = dbCursor
    conn = dbConn
    #print(cookie)
    c.execute("UPDATE {tn} SET cookie='{cook}' WHERE userid={usr}".format(tn=tableName, cook=cookie, usr=userid))
    conn.commit()
    data=c.fetchone()
    
def updateUserTutorial(dbCursor, dbConn, tableName, userid, tuto):
    import sqlite3
    c = dbCursor
    conn = dbConn
    c.execute("UPDATE {tn} SET tutorial={tut} WHERE userid={usr}".format(tn=tableName, tut=tuto, usr=userid))
    conn.commit()
    data=c.fetchone()
    
def updateUserDaily(dbCursor, dbConn, tableName, userid, dayl):
    import sqlite3
    c = dbCursor
    conn = dbConn
    c.execute("UPDATE {tn} SET daily='{tut}' WHERE userid={usr}".format(tn=tableName, tut=dayl, usr=userid))
    conn.commit()
    data=c.fetchone()
    
def queryIndex(dbCursor, dbConn, tableName, typ):
    import sqlite3
    c = dbCursor
    conn = dbConn
    c.execute("SELECT title FROM text WHERE type=?", (typ,))
    data=c.fetchall()
    if data is None:
        return None
    else:
        dat = []
        for i in data:
            dat.append(str(i[0]))
        return dat
        
def queryText(dbCursor, dbConn, tableName, idx):
    import sqlite3
    c = dbCursor
    conn = dbConn
    c.execute("SELECT * FROM text WHERE ind=?", (idx,))
    data=c.fetchone()
    #print(data)
    if data is None:
        title = "NA"
        typ = "NA"
        text = "NA"
        pay = 0
        points = 0
        return title, typ, text, pay, points
    else:
        title = data[1]
        typ = data[2]
        text = data[3]
        pay = data[4]
        points = data[5]
        return title, typ, text, pay, points