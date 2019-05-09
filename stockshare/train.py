import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


def analysis():
    X = []
    with open("sec_level.data") as fd:
        for line in fd:
            line = line.strip()
            if not line:
                continue
            
            #(code, year, r2, syn, aiq, size, lev, mb, roe, inst, age, turnover, indsize, soe)
            code, year, r2, *arr = line.split(",")
            X.append(list(arr))
            
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

    show_r2(y_train, reg.predict(x_train))
    pass

def show_r2(y_train, y_predict):
    #y_predict = reg.predict(x_train)
    rss = np.dot(y_predict - y_train, y_predict - y_train)
    print(np.sum((y_predict - y_train)**2))
    print(rss)
    tss = np.dot(y_train - np.mean(y_train), y_train - np.mean(y_train))
    print(np.sum((y_train - np.mean(y_train))**2))
    print(tss)
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

