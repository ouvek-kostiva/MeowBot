import sqlite3

def insertRec(dbName, tableName, userid, text, timestamp, ack):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    count = 0
    conn.execute("INSERT INTO {} (userid, text, timestamp, ack) VALUES (?,?,?,?)".format(tableName),(userid, text, timestamp, ack))
    conn.commit()
    conn.close()
    count = count + 1
    print("User:",userid,"Time:",timestamp)
    return count
    
def queryRec(dbName, tableName, userid):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute("SELECT * FROM ack WHERE userid=?", (userid,))
    data=c.fetchone()
    conn.close()
    #print(data)
    if data is None:
        userid = "Non"
        text = "Blank"
        timestamp = "NA"
        ack = "1"
        return userid, text, timestamp, ack
    else:
        userid = data[1]
        text = data[2]
        timestamp = data[3]
        ack = data[4]
        return userid, text, timestamp, ack
        
def updateACK(dbName, tableName, userid, timestamp):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute("UPDATE {tn} SET ack='{ak}' WHERE timestamp='{time}' AND userid='{usr}'".format(tn=tableName, usr=userid, time=timestamp, ak=1))
    conn.commit()
    conn.close()
    return True
    
def checkNotAck(dbName, tableName):
    import sqlite3
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute("SELECT * FROM ack WHERE ack!=1")
    data=c.fetchone()
    conn.close()
    if data is None:
        userid = "Non"
        text = "Blank"
        timestamp = "NA"
        ack = "1"
        return userid, text, timestamp, ack
    else:
        userid = data[1]
        text = data[2]
        timestamp = data[3]
        ack = data[4]
        return userid, text, timestamp, ack