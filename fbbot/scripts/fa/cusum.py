import matplotlib
matplotlib.use('Agg')

def reacs(folderName,quote):
    import csv
    failData = []
    import os.path
    if os.path.isfile("{}/{}.csv".format(folderName,quote)):
        with open("{}/{}.csv".format(folderName,quote), 'r',encoding = 'big5') as f:
            reader = csv.reader(f)
            failData.append(list(reader))
    else:
        return 0
    itemList = []
    for ind, com in enumerate(failData):
        for jnd, line in enumerate(com[1:]):
            line[3] = line[3].replace(",", "")
            line[4] = line[4].replace(",", "")
            line[5] = line[5].replace(",", "")
            line[6] = line[6].replace(",", "")
            line[7] = line[7].replace(",", "")
            line[8] = line[8].replace(",", "")
            itemList.append([line[3],line[4],line[5],line[6],line[7],line[8]])

    window = []
    tempwin = []

    for ind, com in enumerate(itemList):
        window.append(itemList[ind][0:7])
    pane = window
    return pane

def getC(pane):
    if isinstance(pane, list):
        b0 = [0.1917]
        b1 = [0.7566,0.0011,-0.003,-0.8431,-0.0001,-0.0079]
        Phi1 = []
        Phi1.append([0.36437,1.420783,0.240501,-0.002924,9.344033,-1.363767])
        Phi1.append([0.000508,0.85898,0.002938,0.000007,-0.135205,-0.005493])
        Phi1.append([-0.069138,-0.383791,0.000174,0.00088,-1.883033,0.320583])
        Phi1.append([1.467505,27.482416,4.866191,0.692084,-40.786387,2.037398])
        Phi1.append([-0.00002,0.002878,0.00013,-0.000005,0.807607,-0.000598])
        Phi1.append([0.00048,0.012308,0.002768,-0.000029,0.309621,0.039565])
        Phi2 = [[0.258137,0.950464,0.794741,0.000791,15.159671,0.809634],[-0.000719,-0.077864,-0.003733,-0.000026,0.15991,0.000389],[-0.030049,-0.072468,-0.042722,0.000211,-2.515629,-0.259009],[-1.06488,0.213824,-3.215639,0.115096,-34.602186,-2.970978],[0.000221,-0.007259,0.0003,0.000007,0.110873,-0.001076],[0.000869,-0.003049,0.003025,0.000011,0.117504,0.004719]] 
        Phi3 = [[-0.052335,-0.554754,-0.104028,0.000965,-0.811227,3.720094],[0.00033,-0.023018,0.003618,0.000037,-0.379003,-0.000117],[0.017152,0.165856,0.031485,-0.000086,0.368426,-1.05871],[0.647814,16.437724,2.282131,0.071711,78.564178,-0.742905],[-0.000226,0.011569,-0.000322,-0.000008,0.036894,0.001357],[0.000586,0.006241,0.002737,0.00006,0.11068,0.003657]]
        Phi4 = [[0.030402,-1.848534,-0.056561,-0.001766,-4.216355,-0.444247],[-0.000127,0.155613,-0.002682,-0.000002,0.696842,-0.003065],[0.008448,0.284718,0.099813,0.000527,1.479985,0.280994],[-2.124892,13.677176,-7.661211,0.068413,-48.38935,-4.825657],[-0.000128,-0.005574,-0.000598,-0.000002,-0.010353,-0.0004],[0.000869,-0.014484,0.002061,0.000023,0.031116,-0.001281]]  
        Phi5 = [[-0.029475,0.211721,-0.084832,0.002972,7.270682,-0.761321],[0.000442,0.030174,0.002292,0.000018,-0.443332,-0.001869],[0.010448,-0.043055,0.036424,-0.00125,-0.344308,0.232771],[1.187866,-9.640474,3.946243,-0.056007,155.753862,-3.902689],[0.000163,-0.00354,0.000457,0.000009,0.011948,-0.00046],[-0.000278,0.008088,0.00009,0.00002,0.039097,0.000211]]
        Phi6 = [[0.022431,1.5873,-0.008524,-0.002231,1.844766,0.892036],[-0.000136,-0.082442,-0.000728,0.000007,0.056728,-0.00203],[-0.0022,0.111049,0.007749,0.000466,-0.004911,-0.202618],[0.453137,4.275127,1.762032,0.030274,-13.248728,5.2216],[0.000021,0.002789,0.000147,0.000003,-0.011466,0.000444],[-0.000842,-0.02173,-0.003161,-0.00004,-0.061449,0.002143]]
        d = 0.2957
        k = 0.14
        from numpy import array
        import numpy as np
        comArr = array(pane)
        comArr = comArr.astype(np.float)
        #comArr = normalize(comArr, axis=0, norm='max')
        #comArr = (comArr - comArr.min(0)) / comArr.ptp(0)
        Phi1 = array(Phi1)
        Phi2 = array(Phi2)
        Phi3 = array(Phi3)
        Phi4 = array(Phi4)
        Phi5 = array(Phi5)
        Phi6 = array(Phi6)
        b0 = array(b0)
        b1 = array(b1)
        comArr = np.matrix(comArr)
        Phi1 = np.matrix(Phi1)
        Phi2 = np.matrix(Phi2)
        Phi3 = np.matrix(Phi3)
        Phi4 = np.matrix(Phi4)
        Phi5 = np.matrix(Phi5)
        Phi6 = np.matrix(Phi6)
        b0 = np.matrix(b0)
        b1 = np.matrix(b1)
        z = b0 + b1 * (comArr[6].conj().T - (Phi1 * comArr[5].conj().T + Phi2 * comArr[4].conj().T + Phi3 * comArr[3].conj().T
                                        + Phi4 * comArr[2].conj().T + Phi5 * comArr[1].conj().T + Phi6 * comArr[0].conj().T))
        if z - k > 0:
            return 0
        else:
            return int(z - k)
    else:
        return -1
      
def getplt(quote):
    import matplotlib
    import numpy as np
    import matplotlib.pyplot as plt
    import pickle
    pane = reacs("scripts/fa/listed","{}".format(quote))
    C = getC(pane)
    if C != -1:
        cusu3 = pickle.load(open( "scripts/fa/cusu3.pkl", "rb" ))
        repeat = len(cusu3[0])
        for line in cusu3:
            plt.plot(line,color='blue')
        plt.plot([C]*repeat,color='orange')
        plt.savefig('scripts/fa/CUSUM.png')
        plt.gcf().clear()
        return C
    else:
        return 10
        
#print(getplt(1301))
# 0 