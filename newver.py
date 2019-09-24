import cx_Oracle
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

sid = 'dcrs/dcrs#201912@10.1.8.133/dcrs'
con = cx_Oracle.connect(sid)
cur = con.cursor()


## Get Query statement##
def defSQLcard(offset):
    x = 'SELECT SUM(REAL_AMOUNT) FROM SALES_HISTORY WHERE TRUNC(TRANS_TIME) = TRUNC(SYSDATE-' + str(
        offset) + ')' + 'AND TRANS_TYPE=\'CARD\''
    return x


def defSQLtopup(offset):
    x = 'SELECT SUM(REAL_AMOUNT) FROM SALES_HISTORY WHERE TRUNC(TRANS_TIME) = TRUNC(SYSDATE-' + str(
        offset) + ')' + 'AND TRANS_TYPE=\'TOPUP\''
    return x


## Get timeline Lable
def defTimelable(offset):
    return datetime.strftime(datetime.now() - timedelta(offset), '%d/%m')


##########################################################################
amountLableCD = []
amountLableTP = []
for offset in range(7):
    query1 = defSQLcard(offset)
    query2 = defSQLtopup(offset)
    for i in cur.execute(query1):
        amountLableCD.append(i[0])

    for j in cur.execute(query2):
        amountLableTP.append(j[0])
        # amountLableTP.append(j[0])

## Declare Data
dateLable = [defTimelable(i) for i in range(7)]
amountLableCD.reverse()
amountLableTP.reverse()
dateLable.reverse()

## Processing Data And Draw
N = 5
menMeans = (20, 35, 30, 35, 27)
womenMeans = (25, 32, 34, 20, 25)

menStd = (2, 3, 4, 1, 2)
womenStd = (3, 5, 2, 3, 3)
ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, menMeans, width, yerr=menStd)
p2 = plt.bar(ind, womenMeans, width,
             bottom=menMeans, yerr=womenStd)

plt.ylabel('Doanh Thu')
plt.title('DCRS Sale Amount Weekly Reporting')
plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5'))
plt.yticks(np.arange(0, 81, 10))
plt.legend((p1[0], p2[0]), ('Men', 'Women'))

plt.show()
