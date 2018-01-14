from matplotlib.finance import candlestick2
import matplotlib
import numpy as np

def getTWSEdata(stockCode="1301", monthDate="20170801"):
    # monthDate = 20170801
    import requests
    import pickle
    import os
    import json
    import time
    try:
        r = requests.get('http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={}&stockNo={}'.format(monthDate,stockCode), headers={'Connection':'close'})
        print('http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={}&stockNo={}'.format(monthDate,stockCode))
    except requests.exceptions.ConnectionError:
        print("Connection Refused")
    time.sleep(1)
    data = json.loads(r.text)
    if data['stat'] == 'OK':
        prices = data['data']
        name = data['title'].split()[2]
        price = []
        for i in prices:
            price.append(i)
        
        tmp2 = []
        for line in prices:
            tmp1 = []
            for item in line:
                tmp1.append(item)
            tmp2.append((tmp1))
        price = tmp2    
        prices = price
        print("Name",name)
        return prices,name
    else:
        return "代碼不存在","不存在"
    #"代號  名稱 日期       成交股數   成交金額     開盤價 最高價 最低價 收盤價 漲跌差 成交筆數"

def getThisMonth(daysAgo=31):
    from datetime import datetime, date, time, timedelta
    today = datetime.today()
    todate = today.strftime("%d")
    if todate != "01":
        first = today.replace(day=1)
        lastMonth = first - timedelta(days=daysAgo)
        dateStr = lastMonth.strftime("%Y%m01")
        return dateStr
    else:
        return "FirstDay"

def moving_average(x, n, type='simple'):
    from numpy import array
    import numpy as np
    #compute an n period moving average.
    #type is 'simple' | 'exponential'
    x = np.asarray(x)
    if type == 'simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))
    weights /= weights.sum()
    a = np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a

def moving_average_convergence(x, nslow=26, nfast=12):
    from numpy import array
    import numpy as np
    #compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    #return value is emaslow, emafast, macd which are len(x) arrays
    emaslow = moving_average(x, nslow, type='exponential')
    emafast = moving_average(x, nfast, type='exponential')
    return emaslow, emafast, emafast - emaslow

def relative_strength(prices, n=14):
    from numpy import array
    import numpy as np
    #compute the n period relative strength indicator
    #http://stockcharts.com/school/doku.php?id=chart_school:glossary_r#relativestrengthindex
    #http://www.investopedia.com/terms/r/rsi.asp
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed >= 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1. + rs)
    for i in range(n, len(prices)):
        delta = deltas[i - 1]  # cause the diff is 1 shorter
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
        up = (up*(n - 1) + upval)/n
        down = (down*(n - 1) + downval)/n
        rs = up/down
        rsi[i] = 100. - 100./(1. + rs)
    return rsi

def getTA(fh, nslow=20, nfast=5, nema=10):
    from numpy import array
    import numpy as np
    fh = array(fh)
    prices = fh.astype(np.float) # Price from Str to float
    emaslow, emafast, macd = moving_average_convergence(prices, nslow=nslow, nfast=nfast)
    rsi = relative_strength(prices) # RSI
    revMACD = list(reversed(macd))
    revRSI = list(reversed(rsi))
    revDalist = list(reversed(fh))
    dalistTA = []
    for i in range(len(fh)):
        dalistTA.append([fh[i],revMACD[i],revRSI[i]])
    reversed(dalistTA)
    return dalistTA

def predictAnswer(code,file,thresh=0.5):
    import xgboost as xgb
    nameofMODEL = 'scripts/ta/models/data5day'+str(code)+'.model'
    bst = xgb.Booster({'nthread': 4})
    bst.load_model(nameofMODEL)
    dtest = xgb.DMatrix(file)
    preds = bst.predict(dtest)
    return preds

#https://stackoverflow.com/questions/42553891/function-for-simple-moving-average-sma
def calcSma(data, smaPeriod):
    j = next(i for i, x in enumerate(data) if x is not None)
    our_range = range(len(data))[j + smaPeriod - 1:]
    empty_list = [None] * (j + smaPeriod - 1)
    sub_result = [np.mean(data[i - smaPeriod + 1: i + 1]) for i in our_range]
    return np.array(empty_list + sub_result)

def getCandleImage(code):
    try:
        dateStr = getThisMonth(32)
        prices,CompanyName = getTWSEdata(stockCode=code, monthDate=dateStr)
        if prices != "代碼不存在":
            dateStr = getThisMonth(30)
            prices2, CompanyName = getTWSEdata(stockCode=code, monthDate=dateStr)
            prices.extend(prices2)
            dateStr = getThisMonth(0)
            if dateStr == "FirstDay":
                dateStr = getThisMonth(1)
            prices2, CompanyName = getTWSEdata(stockCode=code, monthDate=dateStr)
            prices.extend(prices2)
            print(type(prices))
            CloseList = []
            predictions = []
            prices = prices[:]
            Op = []
            Hi = []
            Lw = []
            for i,val in enumerate(prices):
                item1 = prices[i][6].replace(',','')
                Ope = prices[i][3].replace(',','')
                Hig = prices[i][4].replace(',','')
                Low = prices[i][5].replace(',','')
                if (item1 != "--") & (Ope != "--") & (Hig != "--") & (Low != "--"):
                    CloseList.append(item1)
                    Op.append(Ope)
                    Hi.append(Hig)
                    Lw.append(Low)
            print(CloseList)
            import matplotlib
            import numpy as np
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            ax = plt.gca()
            title = code + " Daily K Chart"
            ax.set_title(title)
            opens = Op
            closes = CloseList
            highs = Hi
            lows = Lw
            cl = np.asarray(closes)
            cl = cl.astype(float)
            sma5 = calcSma(cl, 5)
            sma5 = sma5.tolist()
            plt.plot(sma5, label="MA 5")
            sma5 = calcSma(cl, 10)
            sma5 = sma5.tolist()
            plt.plot(sma5, label="MA 10")
            sma5 = calcSma(cl, 20)
            sma5 = sma5.tolist()
            plt.plot(sma5, label="MA 20")
            plt.legend(loc='upper left')
            matplotlib.finance.candlestick2(ax, opens, closes, highs, lows, width=0.5, colorup='r', colordown='g', alpha=1)
            plt.grid()
            plt.savefig('scripts/ta/Close.png')
            plt.gcf().clear()
            lastclose = CloseList[-1]
            lastopen = Op[-1]
            lasthigh = Hi[-1]
            lastlow = Lw[-1]
            return CompanyName, lastopen, lasthigh, lastlow, lastclose
        else:
            return "Error","Error","Error","Error","Error"
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        #typ, value, traceback = sys.exc_info()
        print("出錯","Err:")
        return "Error","Error","Error","Error","Error"

def getPred(code):
    # dateStr = getThisMonth(301)
    # prices.extend(getTWSEdata(stockCode=code, monthDate=dateStr))
    # dateStr = getThisMonth(271)
    # prices.extend(getTWSEdata(stockCode=code, monthDate=dateStr))
    # dateStr = getThisMonth(241)
    # prices.extend(getTWSEdata(stockCode=code, monthDate=dateStr))
    # dateStr = getThisMonth(211)
    # prices.extend(getTWSEdata(stockCode=code, monthDate=dateStr))
    # dateStr = getThisMonth(181)
    # prices.extend(getTWSEdata(stockCode=code, monthDate=dateStr))
    # dateStr = getThisMonth(151)
    # prices.extend(getTWSEdata(stockCode=code, monthDate=dateStr))
    # dateStr = getThisMonth(121)
    # prices.extend(getTWSEdata(stockCode=code, monthDate=dateStr))
    # dateStr = getThisMonth(91)
    # prices.extend(getTWSEdata(stockCode=code, monthDate=dateStr))
    # dateStr = getThisMonth(61)
    # prices.extend(getTWSEdata(stockCode=code, monthDate=dateStr))
    # dateStr = getThisMonth(31)
    # prices.extend(getTWSEdata(stockCode=code, monthDate=dateStr))
    
    try:
        dateStr = getThisMonth(32)
        prices,CompanyName = getTWSEdata(stockCode=code, monthDate=dateStr)
        if prices != "代碼不存在":
            dateStr = getThisMonth(30)
            prices2, CompanyName = getTWSEdata(stockCode=code, monthDate=dateStr)
            prices.extend(prices2)
            dateStr = getThisMonth(0)
            if dateStr == "FirstDay":
                dateStr = getThisMonth(1)
            prices2, CompanyName = getTWSEdata(stockCode=code, monthDate=dateStr)
            prices.extend(prices2)
            print(type(prices))
            CloseList = []
            predictions = []
            prices = prices[:]
            Op = []
            Hi = []
            Lw = []
            for i,val in enumerate(prices):
                item1 = prices[i][6].replace(',','')
                Ope = prices[i][3].replace(',','')
                Hig = prices[i][4].replace(',','')
                Low = prices[i][5].replace(',','')
                if (item1 != "--") & (Ope != "--") & (Hig != "--") & (Low != "--"):
                    CloseList.append(item1)
                    Op.append(Ope)
                    Hi.append(Hig)
                    Lw.append(Low)
            #print(CloseList)
            dalistTA = getTA(CloseList, nslow=20, nfast=5, nema=10)
            for i,val in enumerate(dalistTA):
                dtest = "1:"+str(dalistTA[i][0])+" 2:"+str(dalistTA[i][1])+" 3:"+str(dalistTA[i][2])+'\n'
                with open('scripts/ta/temp.csv', 'w') as f:
                    f.write(dtest)
                preds = predictAnswer(code,'scripts/ta/temp.csv')
                #print(i," ",preds," ",dalistTA[i][0])
                predictions.append(preds)
            #print("Average:",sum(predictions)/float(len(predictions)),"")
            avgpred = sum(predictions)/float(len(predictions))
            avgli = [avgpred] * len(predictions)
            median = (max(predictions) + min(predictions))/2
            upthresh = [avgpred + ((max(predictions) - abs(median))/2)] * len(predictions)
            lowthresh = [avgpred - ((max(predictions) - abs(median))/2)] * len(predictions)
            thresh = [float(avgpred + ((max(predictions) - abs(median))/2)), median]
            
            import matplotlib
            import numpy as np
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            ax = plt.gca()
            ax.set_title('Future 5 Day Prediction')
            plt.plot(predictions)
            plt.plot(upthresh)
            plt.plot(avgli)
            plt.plot(lowthresh)
            plt.savefig('scripts/ta/Pred.png')
            plt.gcf().clear()
            #
            #plt.plot(CloseList)
            ax = plt.gca()
            title = code + " Daily K Chart"
            ax.set_title(title)
            opens = Op
            closes = CloseList
            highs = Hi
            lows = Lw
            cl = np.asarray(closes)
            cl = cl.astype(float)
            sma5 = calcSma(cl, 5)
            sma5 = sma5.tolist()
            plt.plot(sma5, label="MA 5")
            sma5 = calcSma(cl, 10)
            sma5 = sma5.tolist()
            plt.plot(sma5, label="MA 10")
            sma5 = calcSma(cl, 20)
            sma5 = sma5.tolist()
            plt.plot(sma5, label="MA 20")
            plt.legend(loc='upper left')
            matplotlib.finance.candlestick2(ax, opens, closes, highs, lows, width=0.5, colorup='r', colordown='g', alpha=1)
            plt.grid()
            plt.savefig('scripts/ta/Close.png')
            plt.gcf().clear()
            return preds, avgpred, CompanyName, CloseList, thresh
        else:
            print("代碼不存在 == True")
            return "Error","Error","Error", "Error", "Error"
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        #typ, value, traceback = sys.exc_info()
        print("出錯","Err:")
        return "Error","Error","Error", "Error", "Error"

        
#preds, avgpred, CompanyName, CloseList, thresh = getPred(1301)
#print(preds, avgpred, CompanyName, CloseList, thresh)

#[ 0.62619627] [ 0.61691052] 台塑 ['91.80', '91.20', '91.20', '92.00', '94.40', '94.60', '93.50', '93.20', '93.50', '93.00', '92.80', '92.80', '91.70', '92.00', '92.00', '92.00', '91.90', '91.60', '91.90', '91.80', '91.20', '91.20', '92.00', '94.40', '94.60', '93.50', '93.20', '93.50', '93.00', '92.80', '92.80', '91.70', '92.00'] [0.6278542280197144, 0.6059668064117432]