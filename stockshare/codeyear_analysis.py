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

class AiqObj:
    def __init__(self):
        self.data={}
        self.data_predict={}

    def add(self, code, year, item):
        self.data[(code,year)]=item
        pass

    def get(self, code, year):
        return self.data_predict[(code, year)]

    def predict(self):
        #acc_dict[code].add(code, year, [ta, asset, rev, rec, ppe]) 
        dataset=[]
        for k,v in sorted(self.data.items(), key=lambda kv: kv[0][1]):
            dataset.append(v)
        
        X = np.array(dataset)
        axis0,axis1 = X.shape
        x_train = np.zeros((axis0,3)) 
        y_train = np.zeros((axis0,1))
        
        x_train[:,0]=1/X[:,1]
        x_train[:,1]=X[:,2]/X[:,1]
        x_train[:,2]=X[:,4]/X[:,1]
        y_train[:,0]=X[:,0]/X[:,1]
        
        regressor = LinearRegression()
        regressor.fit(x_train, y_train)
        #print(regressor.coef_)
        #print(regressor.intercept_)
        coef=regressor.coef_
        intercept=regressor.intercept_
        nda_predict = np.zeros((axis0,1))
        nda_predict = coef[0,0] * (1/X[:,1]) + coef[0,1]*((X[:,2]-X[:,3])/X[:,1]) + coef[0,2]*(X[:,4]/X[:,1]) + intercept[0]
        
        acc_predict = np.zeros((axis0, 1))
        acc_predict = y_train - nda_predict 
        
        return acc_predict[:,0]
        pass 

    def predict_all(self):
        acc = self.predict()
        cnt = 0
        for k,v in sorted(self.data.items(), key=lambda kv: kv[0][1]):
            self.data_predict[(k[0],k[1])] = "%0.2f" % acc[cnt]
            cnt+=1

    def __str__(self):
        acc = self.predict()
        cnt = 0
        rs=[]
        for k,v in sorted(self.data.items(), key=lambda kv: kv[0][1]):
            self.data_predict[(k[0],k[1])] = "%0.2f" % acc[cnt]

            rs.append(",".join((k[0],k[1],"%0.2f" % acc[cnt])))
            cnt+=1
        return "\n".join(rs)

def accounting_quality():
    keys=["ta","rev","rec","asset","ppe","size","lev","mb","roe","inst","age","turnover","indsize","soe"]
    
    ind_year_dict = collections.defaultdict(set)
    X = []
    y = []
    with open("lavender_paris.csv") as fd:
        reader = csv.reader(fd)
        for items in reader:
            if reader.line_num == 1:
                continue
            code = items[0]
            year = items[3]
            ind = items[5]
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
            if asset == 0 or ta == 0:
                continue

            incr("total") 
            
            #ind_year_dict[ind,year].add(code)
            ind_year_dict[ind,year].add(code)

        
    show_metrics()
    #for n in acc_dict:
    #    print(acc_dict[n])
    #for k,v in sorted(ind_year_dict.items(), key=lambda kv:(int(kv[0][1].split("-")[0]),kv[0][0])):
        #print("%s %s %d" % (k[1].split("-")[0], k[0], len(v)))
        #ind_year_dict[k,v].predict_all()
    year_cnt=collections.defaultdict(int)
    for k,v in sorted(ind_year_dict.items(), key=lambda kv:(int(kv[0][1].split("-")[0]),kv[0][0])):
        year_cnt[k[0]] += len(v)
        #print("%s %s %d" % (k[1].split("-")[0], k[0], len(v)))

    for k,v in sorted(year_cnt.items(), key=lambda kv: k[0]):
        print("%s %d" % (k, v))
    

        
    pass


def main():
    accounting_quality()
    pass

if __name__ == "__main__":
    main()
