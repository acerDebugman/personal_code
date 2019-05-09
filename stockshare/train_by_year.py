import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import collections


def analysis():
    yeardata=collections.defaultdict(list)
    #X = []
    #with open("sec_level2.data") as fd:
    with open("sec_level_gt12.data") as fd:
        for line in fd:
            line = line.strip()
            if not line:
                continue
            
            #(code, year, r2, syn, aiq, size, lev, mb, roe, inst, age, turnover, indsize, soe)
            code, year, r2, *arr = line.split(",")
            yeardata[year].append(list(arr))

    for year, X in yeardata.items(): 
        if int(year) != 2017:
            continue

        X = np.array(X).astype(float)

        x_train = X[:,1:]
        y_train = X[:,0]
        print(x_train.shape)
        print(y_train.shape)
        reg = LinearRegression()
        reg.fit(x_train,y_train)
        print("syn, aiq, size, lev, mb, roe, inst, age, turnover, indsize, soe")
        names=["aiq","size","lev","mb","roe","inst","age","turnover","indsize","soe"]
        pairs = dict(zip(names,reg.coef_))
        print(reg.coef_)
        print(reg.intercept_)
        for k,v in pairs.items():
            print(k + "\t" + str(v))
        print("year:", year)
        y_predict=reg.predict(x_train)
        show_r2(y_train, y_predict)

        y_mean=np.mean(np.abs(y_predict-y_train))
        print("y_mean", y_mean)
        y_gt=np.abs(y_predict-y_train) < y_mean*1.2
        print("y_gt true size",y_train[y_gt].shape)
        show_r2(y_train[y_gt], y_predict[y_gt])
        
        #print(y_gt)
        #print(x_train[y_gt])

        cnt=-1
        with open("sec_level_gt12.data") as fd, open("third_level_17.data", "w") as ofd:
            for line in fd:
                line = line.strip()
                if not line:
                    continue

                code, year, r2, *arr = line.split(",")
                if int(year) != 2017:
                    continue

                cnt+=1

                if y_gt[cnt]:
                    ofd.write(line + "\n")

    #show_r2(y_train, y_predict)
    pass

def show_r2(y_train, y_predict):
    #y_predict = reg.predict(x_train)
    rss = np.dot(y_predict - y_train, y_predict - y_train)
    #print(np.sum((y_predict - y_train)**2))
    #print(rss)
    tss = np.dot(y_train - np.mean(y_train), y_train - np.mean(y_train))
    #print(np.sum((y_train - np.mean(y_train))**2))
    #print(tss)
    r2 = 1 - rss/tss
    print("r2 is : %0.4f" % r2)
    fig,ax = plt.subplots()
    ax.scatter(y_train, y_predict)
    ax.plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()], 'k--', lw=4)
    ax.set_xlabel("Mmeasured")
    ax.set_ylabel("Predicted")
    plt.show()


def main():
    analysis()
    pass

if __name__ == "__main__":
    main()

