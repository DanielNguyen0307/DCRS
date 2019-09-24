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
## Refer link: https://matplotlib.org/3.1.1/gallery/lines_bars_and_markers/bar_stacked.html#sphx-glr-gallery-lines-bars-and-markers-bar-stacked-py
N = 7
card = amountLableCD
topup = amountLableTP
timeline = dateLable
note1=(2, 3, 4, 1, 2, 4, 3)
note2=(3, 5, 2, 3, 3, 5, 3)

ind = np.arange(N)
width = 0.35
p1 = plt.bar(ind, topup, width, yerr=note1)
p2 = plt.bar(ind, card, width, bottom=topup, yerr=note2)

plt.ylabel('Daily Total Amount')
plt.title('DCRS Sale Amount Report Weekly')
plt.xticks(ind, timeline)
plt.yticks(np.arange(0, 500000000, 100000000))

plt.legend((p1[0], p2[0]), ('TopUp', 'Card'))

plt.show()



