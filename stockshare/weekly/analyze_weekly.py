import sys
import datetime as dt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import collections
import numpy as np

def loadmap():
    rs = {}
    with open("code_ind_map.txt") as fd:
        for line in fd:
            line = line.strip()
            if not line:
                continue
            code, ind = line.split(",")   
            rs[code] = ind

    return rs

def etl():
    cimap = loadmap()
    rs=collections.defaultdict(list)
    with open("c_weekly.csv") as cfd, open("m_weekly.csv") as mfd, open("i_weekly.csv") as ifd, open("out_weekly.csv", "w") as ofd:
        m_rate={}
        for line in mfd:
            line = line.strip()
            if not line:
                continue
            day,mror = line.split(",")
            y,w,d=dt.datetime.strptime(day, "%Y-%m-%d").isocalendar()
            key = str(y)+"-"+"%02d" % w
            m_rate[key]=mror


        i_rate={}   
        ikeys=["农、林、牧、渔业","采矿业","制造业","电力、热力、燃气及水生产和供应业","建筑业","批发和零售业","交通运输、仓储和邮政业","住宿和餐饮业","信息传输、软件和信息技术服务业","证监会金融业","房地产业","租赁和商务服务业","科学研究和技术服务业","水利、环境和公共设施管理业","卫生和社会工作","文化、体育和娱乐业","综合","教育"]
        cnt=0
        for line in ifd:
            line = line.strip()
            if not line:
                continue
            cnt += 1
            if cnt == 1:
                continue
            arr = line.split(",")
            day=arr[0]
            y,w,d = dt.datetime.strptime(day, "%Y-%m-%d").isocalendar() 
            week = str(y) + "-" + "%02d" % w
            for i in range(0,len(ikeys)):
                ind = ikeys[i]
                i_rate[ind, week] = arr[i+1] 

        for line in cfd:
            line = line.strip()
            if not line:
                continue

            code,name,week,day,cror = line.split(",")
            code = code + ".SH" 
            ind=cimap[code]
            #if code == "601588.SH":
            #    print()
            if week in m_rate and (ind,week) in i_rate:
                mror = m_rate[week]
                rs[code,week].append(cror)
                rs[code,week].append(mror)
                
                iror=i_rate[ind, week]
                rs[code,week].append(iror)

        for k,v in sorted(rs.items(), key=lambda kv: (kv[0],kv[1])):
            ofd.write(",".join((k[0], k[1], ",".join([str(x) for x in v]))) + "\n") 

    pass


def analysis():
    datas = collections.defaultdict(dict)
    with open("out_weekly.csv") as fd, open("out_r2_syn.csv", "w") as ofd:
        for line in fd:
            line = line.strip()
            if not line:
                continue
            
            code,week,cror,mror,iror = line.split(",")
            year = week.split("-")[0]
            if year not in datas[code]:
                datas[code][year] = []
            datas[code][year].append([float(cror), float(mror), float(iror)])

        r2dict = collections.defaultdict(dict)
        for code,yeardata in datas.items():
            for year,X in yeardata.items():
                x_data = np.array(X)
                x_train = x_data[:,1:]
                y_train = x_data[:,0]
                #print(code + "-" + year)
                #print(x_train.shape)
                #x_train,x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.1)
                reg = LinearRegression()
                reg.fit(x_train, y_train)
                #print(reg.coef_)
                #print(reg.intercept_)
                #r2 
                y_predict = reg.predict(x_train)
                mean = np.mean(y_train)
                TSS = np.dot(y_train - mean, y_train - mean)
                RSS = np.dot(y_train - y_predict, y_train - y_predict)

                #if TSS == 0:
                #    print(code + "," + year + "," + str(mean) + "," + str(y_train))
                #print(TSS)
                #print(RSS)
                # 只有一个点时，TSS=0
                if TSS == 0: 
                    r2 = 1
                else:
                    r2 = 1 - float(RSS) / TSS
                #print("%4f %4f %4f %4f" % (r2, RSS, TSS, mean))
                #r2_s = r2_score(y_train, y_predict)
                #print("%4f %4f %4f %4f %4f" % (r2, r2_s,  RSS, TSS, mean))
                if 1==r2:
                    print(code,year,r2)
                    r2=0.999
                syn = np.log(r2/(1-r2))
                ofd.write("%s,%s,%0.4f,%0.4f\n" %(code, year, r2, syn))
            
    pass

def main():
    etl()
    analysis()

if __name__ == "__main__":
    main()
