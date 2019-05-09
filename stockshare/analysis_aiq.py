import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import collections
import json

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
    
    def size(self):
        return len(self.data)

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
            pos = int(pos)
            return (self.data[pos-1] + self.data[pos])/2
        else:
            return self.data[int(pos)]

    def three_quarter(self):
        pos = len(self.data) * 0.75
        if pos.is_integer():
            pos = int(pos)
            return (self.data[pos-1] + self.data[pos])/2
        else:
            return self.data[int(pos)]

    def std(self):
        square_error = 0
        mean = self.mean()
        for n in self.data:
            square_error += (n - mean)**2
        return np.sqrt(square_error)

    def winsor(self, percent):
        if len(self.data) == 0:
            return
        pos = len(self.data) * percent
        if pos.is_integer():
            pos = int(pos)
            num = (self.data[pos-1] + self.data[pos])/2
            for n in range(0, pos + 1):
                self.data[n] = num

            num = (self.data[len(self.data) - pos] + self.data[len(self.data) - pos + 1])/2
            for n in range(len(self.data) - pos, len(self.data)):
                self.data[n] = num
        else:
            pos = int(pos)
            num = self.data[pos]
            for n in range(0, pos):
                self.data[n] = num

            num = self.data[len(self.data) - pos]
            for n in range(len(self.data) - pos, len(self.data)):
                self.data[n] = num

    def __str__(self):
        self.data = sorted(self.data)
        self.winsor(0.01)
        rs=[self.mean(), self.std(), self.min(), self.one_quarter(), self.median(), 
            self.three_quarter(), self.max()]
        return "\t".join(["%0.4f" % x for x in rs])

    def __dict__(self):
        return {"no":"obj"}
    

def accounting_quality():
    keys=["r2","syn","aiq","size","lev","mb","roe","inst","age","turnover","indsize","soe"]
    datas = {
        "r2":VarObj("r2"),
        "syn":VarObj("syn"),
        "aiq":VarObj("aiq"),
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

    year_metrics=["r2", "syn", "aiq"]
    year_dict = collections.defaultdict(dict)
    for year in range(2008, 2018):
        for name in year_metrics:
            year_dict[str(year)][name] = VarObj(name)
    
    with open("sec_level.data") as fd:
        reader = csv.reader(fd)
        for items in reader:
            code = items[0]
            year = items[1]
            r2 = get(items, 2)
            syn = get(items, 3)
            aiq = get(items, 4)
            size = get(items, 5)
            lev = get(items, 6)
            mb = get(items, 7)
            roe = get(items, 8)
            inst = get(items, 9)
            age = get(items, 10)
            turnover = get(items, 11)
            indsize = get(items, 12)
            soe = get(items, 13)

            incr("total") 

            for k in keys:
                datas[k].add(eval(k))

            #print(json.dumps(year_dict, default=lambda obj:obj.__dict__))
            #print(year_dict[year])
            for name in year_metrics:
                #print(year, name)
                #if name in 
                #print(year_dict[name])
                year_dict[year][name].add(eval(name))

    show_metrics()
    for d in keys:
        print("%s\t%s" % (d, datas[d]))

    print("stats by year:")
    with open("stats_by_year.txt", "w") as ofd:
        for year in year_dict:
            for name in year_dict[year]:
                print("%s\t%s\t%0.4f\t%d\t%s" % (year, name, year_dict[year][name].sum(), year_dict[year][name].size(), year_dict[year][name]))
                ofd.write("%s\t%s\t%d\t%s\n" % (year, name, year_dict[year][name].size(), year_dict[year][name]))
    pass


def main():
    accounting_quality()
    pass

if __name__ == "__main__":
    main()
