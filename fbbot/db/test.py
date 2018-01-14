def delUser(userid):
    import sqlite3
    conn = sqlite3.connect("istockbot.db")
    c = conn.cursor()
    c.execute("DELETE FROM user WHERE userid=?", (userid,)) 
    conn.commit()
    conn.close()
    
#delUser()