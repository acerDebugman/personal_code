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
        
        #reg = LinearRegression(fit_intercept=False)
        reg = LinearRegression()
        reg.fit(x_train, y_train)
        
        #print(y_train)
        #print(reg.predict(x_train))
        #show_r2(y_train, reg.predict(x_train))

        print(reg.coef_)
        print(reg.intercept_)
        coef=reg.coef_
        intercept=reg.intercept_
        nda_predict = np.zeros((axis0,1))
        nda_predict = coef[0,0] * (1/X[:,1]) + coef[0,1]*((X[:,2]-X[:,3])/X[:,1]) + coef[0,2]*(X[:,4]/X[:,1]) + intercept[0]
        #nda_predict = coef[0,0] * (1/X[:,1]) + coef[0,1]*((X[:,2]-X[:,3])/X[:,1]) + coef[0,2]*(X[:,4]/X[:,1])
        
        acc_predict = np.zeros((axis0, 1))
        acc_predict = y_train - nda_predict 
        
        #show_r2(y_train, nda_predict)

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
    acc_dict = collections.defaultdict(AiqObj)
    X = []
    y = []
    with open("lavender_paris.csv") as fd:
        reader = csv.reader(fd)
        for items in reader:
            if reader.line_num == 1:
                continue
            code = items[0]
            year = items[3]
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

            acc_dict[code].add(code, year, [ta, asset, rev, rec, ppe]) 

            #print(",".join((ta, rev, rec, asset, ppe)))
            '''
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
        '''
        
    show_metrics()
    #for n in acc_dict:
    #    print(acc_dict[n])
    for n in acc_dict:
        acc_dict[n].predict_all()
    
    rs=[]
    with open("lavender_paris.csv") as fd, open("weekly/out_r2_syn.csv") as wfd, open("sec_level.data", "w") as ofd:
        r2map = {}
        for line in wfd:
            line = line.strip()
            if not line:
                continue
            code, year, r2, syn = line.split(",")
            r2map[code,year] = (r2,syn)

        reader = csv.reader(fd)
        for items in reader:
            if reader.line_num == 1:
                continue
            code = items[0]
            year = items[3]
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
            if asset == 0 or ta == 0 :
                continue
            aiq = acc_dict[code].get(code, year)
            year = year.split("-")[0] 
            r2 = 0
            syn = 0
            if (code,year) in r2map:
                r2 = r2map[code,year][0]
                syn = r2map[code,year][1]

            rs.append((code, year, r2, syn, aiq, size, lev, mb, roe, inst, age, turnover, indsize, soe))
            
        for item in sorted(rs, key=lambda x:(x[0],x[1])):
            ofd.write(",".join([str(x) for x in item]) + "\n")
    
    pass

def show_r2(y_train, y_predict):
    #y_predict = reg.predict(x_train)
    #rss = np.dot(y_predict - y_train, y_predict - y_train)
    #tss = np.dot(y_train - np.mean(y_train), y_train - np.mean(y_train))
    rss = np.sum((y_predict - y_train)**2)
    tss = np.sum((y_train - np.mean(y_train))**2)
    #print(rss,tss)
    r2 = 1 - rss/tss
    print("r2 is:\t%0.4f" % r2)
    fig,ax = plt.subplots()
    ax.scatter(y_train, y_predict)
    ax.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'k--', lw=4)
    ax.set_xlabel("Mmeasured")
    ax.set_ylabel("Predicted")
    plt.show()


def main():
    accounting_quality()
    pass

if __name__ == "__main__":
    main()
