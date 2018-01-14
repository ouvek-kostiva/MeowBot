from random import randint
from scripts.user import *
from db.dbquery import *
import datetime

boxprice = 100
helptxt = "投資一定有風險，金融市場投資有賺有賠，本系統資訊僅供參考用途，且不保證正確性，請勿視為買賣基金、有價證券等金融商品之投資建議。本系統對資料之完整性、即時性和正確性不做任何擔保，如有錯誤或疏漏不負任何法律責任。投資人應自行判斷資料內容之正確性。內容如涉及有價證券或金融商品、市場等文字，並不構成要約、招攬、宣傳、建議或推薦買賣等任何形式之表示，請投資人應審慎考量本身之需求與投資風險。\n\n使用說明：\n\n輸入 4 位數股票代號\n顯示財務安全分析\n及股價趨勢預測\n\n金融類股因財務比率與其他產業不同，因此不進行安全分析\n\n輸入 *pf 顯示理財知識文章列表\n\n輸入 *box 花 100 點抽寶箱\n\n輸入 *box10 連抽 10 次寶箱\n\n輸入 *daily 領取每日登入獎勵及查詢目前點數餘額\n\n輸入 *help 顯示這篇說明"

def getHelpTXT():
    return helptxt

def lotto(userid, points, times):
    if times > 20:
        times = 20
    price = boxprice
    if int(points) >= int(times)*price:
        message = ""
        points = int(points)
        for i in range(times):
            boxnum = randint(0, 100000)
            points = points - price
            if boxnum < 40000:
                message_text = "抱歉您沒有中獎"
            elif (boxnum >= 40000) & (boxnum < 93000):
                message_text = "您中了回本獎，獲得 100 點"
                points = points + 100
            elif (boxnum >= 93000) & (boxnum < 98000):
                message_text = "您中了加倍獎，獲得 200 點"
                points = points + 200
            elif (boxnum >= 98000) & (boxnum <= 99400):
                message_text = "您中了稀有獎，獲得 500 點"
                points = points + 500
            elif (boxnum > 99400) & (boxnum <= 99900):
                message_text = "您中了 SR 獎，獲得 2000 點"
                points = points + 2000
            elif (boxnum > 99900) & (boxnum <= 99990):
                message_text = "您中了 SSR 獎，獲得 50000 點"
                points = points + 50000
            elif (boxnum > 99990) & (boxnum <= 99999):
                message_text = "您中了 EX 獎，獲得 100000 點"
                points = points + 100000
            elif (boxnum > 99999):
                message_text = "您中了 UTR 獎，獲得 500000 點"
                points = points + 500000
            message = message + str(i+1) + ". " + message_text + "\n"
        c, conn = openCursor("db/istockbot.db")
        updateUserPts(c, conn,"user", userid, points)
        closeCursor(conn)
        return message + "您目前有" + str(points) + "點"
    else:
        return "您目前有" + str(points) + "點\n抱歉您目前沒有足夠的點數"
    
def dailyCommand(sender_id, message_text):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    date = str(date)
    c, conn = openCursor("db/istockbot.db")
    cookie, points, tutorial, daily = queryUser(c, conn,"user", sender_id)
    if daily[:5] != "Taken":
        points = int(points) + 1000
        updateUserPts(c, conn,"user", sender_id, points)
        updateUserDaily(c, conn,"user", sender_id, "Taken{}".format(date))
        message_text = "*daily\n" + "獲得每日登入獎勵: 1000 點\n您目前有 " + str(int(points)) + " 點"
    else:
        if date != daily[5:]:
            points = int(points) + 1000
            updateUserPts(c, conn,"user", sender_id, points)
            updateUserDaily(c, conn,"user", sender_id, "Taken{}".format(date))
            message_text = "*daily\n" +"獲得每日登入獎勵: 1000 點\n您目前有 " + str(int(points)) + " 點"
        else:
            message_text = "*daily\n" +"您已領取過每日登入獎勵\n您目前有 " + str(int(points)) + " 點"
    closeCursor(conn)
    return sender_id, message_text
    
def getCommand(userid, text):
    if len(text) > 1:
        text = text[1:]
        if text.isdigit():
            c, conn = openCursor("db/text.db")
            title, typ, content, pay, points = queryText(c, conn,"text", text)
            closeCursor(conn)
            if title != "NA":
                text = "文章編號: " + text + "\n\n" + title + "\n" + content
                return text
            else:
                text = "文章編號: " + text + " 不存在"
                return text
        elif len(text) == 2:
            if text == "pf":
                c, conn = openCursor("db/text.db")
                pflist = queryIndex(c, conn,"text", "personalfinance")
                closeCursor(conn)
                text = "理財知識文章編號\n"
                for ind,cont in enumerate(pflist):
                    text = text + str(ind+1) + ". " + str(cont) + "\n"
                text = text + "\n例:輸入 *1 顯示編號 1 文章"
                return text
            if text == "bq":
                text = "BOXQuickReply"
                return text
            if text == "si":
                text = "StockInfo"
                return text
            if text == "fh":
                text = "FinancialHealth"
                return text
            if text == "pp":
                text = "PricePrediction"
                return text
            if text == "fc":
                text = "OtherFunctions"
                return text
        elif len(text) == 3:
            if text == "box":
                c, conn = openCursor("db/istockbot.db")
                cookie, points, tutorial, daily = queryUser(c, conn,"user", userid)
                closeCursor(conn)
                text = lotto(userid, points, 1)
                return text
        elif (len(text) >= 4) & (len(text) <= 6):
            if (len(text) == 5) & (text == "daily"):
                userid, text = dailyCommand(userid, text)
                return text
            elif (len(text) == 4) & (text == "help"):
                text = helptxt
                return text
            elif (len(text) == 4) & (text == "wait"):
                text = "功能尚未開放，敬請期待"
                return text
            elif text[0:3] == "box":
                text = text[3:]
                if (len(text) == 1) & text.isdigit():
                    times = int(text)
                    c, conn = openCursor("db/istockbot.db")
                    cookie, points, tutorial, daily = queryUser(c, conn,"user", userid)
                    closeCursor(conn)
                    text = lotto(userid, points, times)
                    return text
                elif (len(text) == 2) & text.isdigit():
                    times = int(text)
                    c, conn = openCursor("db/istockbot.db")
                    cookie, points, tutorial, daily = queryUser(c, conn,"user", userid)
                    closeCursor(conn)
                    text = lotto(userid, points, times)
                    return text
                return helptxt
        return helptxt
    else:
        return helptxt