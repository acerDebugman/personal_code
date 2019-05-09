import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import collections

metrics = collections.defaultdict(int)
def incr(name):
    metrics[name] += 1

def add(name, num):
    metrics[name] += num

def varname(var):
    return list(dict(abc=abc).keys())[0]

def show_metrics():
    for key,val in metrics.items():
        print(": ".join((key,str(val))))

def get(items, idx):
    if items[idx].replace(",","").strip() in ("#DIV/0!", "#NUM!") :
        return 0
    else: 
        return float(items[idx].replace(",","").strip())

class VarObj():
    def __init__(self, name):
        self.name = name
        self.data = []

    def add(self, num):
        self.data.append(num)

    def sum(self):
        return np.sum(self.data)
    
    def mean(self):
        return np.sum(self.data)/len(self.data)

    def median(self):
        if len(self.data) == 1:
            return self.data[0]

        if len(self.data)%2 == 1:
            return self.data[len(self.data)//2]
        else:
            m = len(self.data)//2
            return (self.data[m] + self.data[m - 1])/2
    
    def max(self):
        return max(self.data)

    def min(self):
        return min(self.data)

    def one_quarter(self):
        pos = len(self.data) * 0.25
        if pos.is_integer():
            return (self.data[pos-1] + self.data[pos])/2
        else:
            return self.data[int(pos)]

    def three_quarter(self):
        pos = len(self.data) * 0.75
        if pos.is_integer():
            return (self.data[pos-1] + self.data[pos])/2
        else:
            return self.data[int(pos)]

    def std(self):
        square_error = 0
        for n in self.data:
            square_error += (n - self.mean())**2
        return np.sqrt(square_error)

    def winsor(self, percent):
        pos = len(self.data) * percent
        if pos.is_integer():
            num = (self.data[pos-1] + self.data[pos])/2
            for n in range(0, pos):
                self.data[n] = num

            num = (self.data[len(self.data) - pos] + self.data[len(self.data) - pos + 1])/2
            for n in range(len(self.data) - pos, len(self.data)):
                self.data[n] = num
        else:
            num = self.data[pos]
            for n in range(0, pos):
                self.data[n] = num

            num = self.data[len(self.data) - pos]
            for n in range(len(self.data) - pos, len(self.data)):
                self.data[n] = num

    def __str__(self):
        self.data = sorted(self.data)
        rs=[self.name, self.mean(), self.std(), self.min(), self.one_quarter(), self.median(), 
            self.three_quarter(), self.max()]
        return rs[0] + " , " +  " , ".join(["%0.4f" % x for x in rs[1:]])
    

def accounting_quality():
    keys=["ta","rev","rec","asset","ppe","size","lev","mb","roe","inst","age","turnover","indsize","soe"]
    datas = {
        "ta":VarObj("ta"),
        "rev": VarObj("rev"),
        "rec": VarObj("rec"),
        "asset": VarObj("asset"),
        "ppe":VarObj("ppe"),
        "size":VarObj("size"),
        "lev":VarObj("lev"),
        "mb": VarObj("mb"),
        "roe":VarObj("roe"),
        "inst":VarObj("inst"),
        "age":VarObj("age"),
        "turnover":VarObj("turnover"),
        "indsize":VarObj("indsize"),
        "soe":VarObj("soe")
    }

    X = []
    y = []
    with open("lavender_paris.csv") as fd:
        reader = csv.reader(fd)
        for items in reader:
            if reader.line_num == 1:
                continue
            ta = get(items, 11)
            rev = get(items, 14)
            rec = get(items, 17)
            asset = get(items, 19)
            ppe = get(items, 21)
            size = get(items, 26)
            lev = get(items, 27)
            mb = get(items, 30)
            roe = get(items, 31)
            inst = get(items,32)
            age = get(items, 34)
            turnover = get(items, 35)
            indsize = get(items, 38)
            soe = get(items, 39)

            #illegal sample
            if asset == 0 or ta == 0 or rev == 0 or rec == 0 or ppe == 0 or turnover == 0:
                continue

            incr("total") 

            for k in keys:
                datas[k].add(eval(k))

            #print(",".join((ta, rev, rec, asset, ppe)))
            tmp=[]
            tmp.append(1/float(ta))
            tmp.append(float(rev)/float(asset))
            tmp.append(float(ppe)/float(asset))
            X.append(tmp)
            y.append([float(ta)/float(asset)])
            
        #x_train,x_test, y_train,y_test = train_test_split(X,y, test_size=0.2,)
        x_train,x_test, y_train,y_test = X,X, y,y
        model = LinearRegression()
        model.fit(x_train,y_train)
        y_predict = model.predict(x_test)      
        #print(y_predict)
        print("coeficient and intercept")
        print(y_predict.shape)
        print(model.coef_)
        print(model.intercept_)
        print("RMSE")
        sum_square=0
        for i in range(len(y_predict)):
            sum_square += (y_predict[i][0] - y_test[i][0])**2
        mse=sum_square/len(y_predict)
        print("MSE: " + str(mse))
        print("RMSE: " + str(np.sqrt(mse)))
        
    show_metrics()
    for d in keys:
        print(datas[d])
    pass


def main():
    accounting_quality()
    pass

if __name__ == "__main__":
    main()
