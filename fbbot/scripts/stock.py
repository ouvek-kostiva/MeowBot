from scripts.ta.tapred import getPred
from scripts.fa.cusum import getplt
from scripts.user import *
from scripts.templates import *

def getTA(text):
    preds, avgpred, name, CloseList, thresh = getPred(text)
    taanswer = "\n\n預期未來五日趨勢："
    if preds != "Error":
        if (preds > 0.5) & (preds < thresh[1]):
            direction = "橫走 ▷\n"
        elif (preds >= thresh[1]) & (preds < thresh[0]):
            direction = "橫偏漲 📈\n"
        elif (preds > thresh[0]):
            direction = "上漲 📈\n"
        elif (preds <= 0.5):
            direction = "下跌 📉\n"
    else:
        direction = "目前同時太多人使用或代號不在資料庫中，請查明後再試 ✋\n\n非個股(大盤及ETF)因未收集資料無法預測"
    return taanswer,direction, name
    
def getFA(text):
    C = getplt(int(text))
    faanswer = "\n財務狀況估計："
    if C != 10:
        if C <= -5000: #517606
            fa = "注意 🚨" + "\n財務 C 值: " + str(C)
        elif C > -5000:
            fa = "良好 ✅" + "\n財務 C 值: " + str(C) 
    else:
        fa = "抱歉,目前無該公司財報資料 😞"
    return faanswer,fa
    
def getStock(userid,text):
    pts = 75
    hasP = hasPts(userid, pts)
    if hasP:
        taanswer,direction,name = getTA(text)
        extra = ""
        if direction[0] != "目":
            subPts(userid, pts)
            extra = "\n查詢股票資訊花費" + str(pts) + "點\n"
            send_img_message(userid,"scripts/ta/Close.png")
            send_img_message(userid,"scripts/ta/Pred.png")
        faanswer,fa = getFA(text)
        return "公司名稱：" + name + "\n" + extra + faanswer + fa + taanswer + direction + "\n"
    else:
        return "查詢股票資訊需要 "+ str(pts) +" 點\n抱歉您目前沒有足夠的點數 😞"
    
    