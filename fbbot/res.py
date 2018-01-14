from scripts.ack import insertRec, queryRec, updateACK, checkNotAck
from scripts.templates import send_text_message, send_pfquikreply_message, send_boxquikreply_message, send_img_message, send_stockquikreply_message, send_funcquikreply_message
from quote import *
from scripts.user import chkNewUser, chgCookie, getCookie, hasPts, subPts
from scripts.stock import getStock, getFA, getTA
from star import getCommand, getHelpTXT
import time
from scripts.ta.tapred import getCandleImage

helptxt = "投資一定有風險，金融市場投資有賺有賠，本系統資訊僅供參考用途，且不保證正確性，請勿視為買賣基金、有價證券等金融商品之投資建議。本系統對資料之完整性、即時性和正確性不做任何擔保，如有錯誤或疏漏不負任何法律責任。投資人應自行判斷資料內容之正確性。內容如涉及有價證券或金融商品、市場等文字，並不構成要約、招攬、宣傳、建議或推薦買賣等任何形式之表示，請投資人應審慎考量本身之需求與投資風險。\n\n使用說明：\n\n輸入 4 位數股票代號\n顯示財務安全分析\n及股價趨勢預測\n\n金融類股因財務比率與其他產業不同，因此不進行安全分析\n\n輸入 *pf 顯示理財知識文章列表\n\n輸入 *box 花 100 點抽寶箱\n\n輸入 *box10 連抽 10 次寶箱\n\n輸入 *daily 領取每日登入獎勵及查詢目前點數餘額\n\n輸入 *help 顯示這篇說明"
pts = 100

def respond():
    print("Start Responding....")
    while(True):
        time.sleep(0.2)
        userid, text, timestamp, ack = checkNotAck("db/rec.db","ack")
        ack = int(ack)
        if ack != 1:
            nUser = chkNewUser(userid)
            uACK = updateACK("db/rec.db", "ack", userid, timestamp)
            print("User:",userid,"Text:",text,"ACK",uACK)
            isQuote = checkQuote(text)
            isStar = checkStar(text)
            if isQuote:
                CompanyName, lastopen, lasthigh, lastlow, lastclose = getCandleImage(text)
                message = "股票代碼 : " + str(text) + " " + CompanyName
                message = message + "\n" + "開 " + lastopen + " 收 " + lastclose + "\n高 " + lasthigh + " 低 " + lastlow
                if CompanyName != "Error":
                    chgCookie(userid, text)
                    send_img_message(userid,"scripts/ta/Close.png")
                    send_stockquikreply_message(userid, message)
                else:
                    send_text_message(userid, message)
            elif isStar:
                message = getCommand(userid, text)
                if message[0:2] == "理財":
                    send_pfquikreply_message(userid, message)
                elif message == "BOXQuickReply":
                    message = "請選擇你要抽幾個寶箱\n每抽一個寶箱花費 100 點"
                    send_boxquikreply_message(userid, message)
                elif message == "StockInfo":
                    message = "請選擇你要取得的股票資訊"
                    send_stockquikreply_message(userid, message)
                elif message == "OtherFunctions":
                    message = "選擇您想使用的功能"
                    send_funcquikreply_message(userid, message)
                elif message == "FinancialHealth":
                    cookie = getCookie(userid)
                    isQuote = checkQuote(cookie)
                    if isQuote:
                        faanswer,fa = getFA(cookie)
                        message = "股票代碼: " + cookie + faanswer + fa
                        if fa[0] == "抱":
                            send_text_message(userid, message)
                        else:
                            if hasPts(userid, pts):
                                message = message + "\n\n股票「趨勢預測」花費 " + str(pts) + " 點"
                                send_stockquikreply_message(userid, message)
                                subPts(userid, pts)
                            else:
                                message = "抱歉您目前的點數不足\n獲得股票「財務健檢」花費 " + str(pts) + " 點\n請按「功能按鈕」\n「其他功能」\n「目前擁有點數與每日獎勵」\n查詢您目前擁有的點數"
                                send_text_message(userid, message)
                    else:
                        message = "請先輸入輸入 4 位數股票代碼"
                        send_text_message(userid, message)
                elif message == "PricePrediction":
                    cookie = getCookie(userid)
                    isQuote = checkQuote(cookie)
                    if isQuote:
                        message = "股票代號: " + cookie
                        taanswer,direction, name = getTA(cookie)
                        message = message + " " + name + taanswer + direction
                        if hasPts(userid, pts):
                            if direction[0:2] != "目前":
                                send_img_message(userid,"scripts/ta/Pred.png")
                                message = message + "\n\n股票「趨勢預測」花費 " + str(pts) + " 點"
                                send_stockquikreply_message(userid, message)
                                subPts(userid, pts)
                            else:
                                send_text_message(userid, message)
                        else:
                            message = "抱歉您目前的點數不足\n獲得股票「趨勢預測」花費 " + str(pts) + " 點\n請按「功能按鈕」\n「其他功能」\n「目前擁有點數與每日獎勵」\n查詢您目前擁有的點數"
                            send_text_message(userid, message)
                    else:
                        message = "請先輸入輸入 4 位數股票代碼"
                        send_text_message(userid, message)
                else:
                    send_text_message(userid, message)
            else:
                if nUser:
                    time.sleep(0.1)
                    text = "您輸入了：" + text + "\n\n" + helptxt
                    send_text_message(userid, text)
                else:
                    text = "您輸入了：" + text + "\n\n" + helptxt
                    send_text_message(userid, text)
        
if __name__ == '__main__':
    respond()