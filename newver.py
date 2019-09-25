import numpy as np
import matplotlib.pyplot as plt

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

data = [amountLableTP,amountLableCD]
columns = dateLable
rows = ['Topup', 'Card']

#values = np.arange(0, 25000, 5000)
#value_increment = 1000

# Get some pastel shades for the colors
colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))
n_rows = len(data)

index = np.arange(len(columns)) + .3

# Initialize the vertical-offset for the stacked bar chart.
y_offset = np.zeros(len(columns))

# Plot bars and create text labels for the table
cell_text = []
for row in range(n_rows):
    y_offset = data[row]
    cell_text.append(['%1.1f' % (x / 1000.0) for x in y_offset])
# Reverse colors and text labels to display the last value at the top.
colors = colors[::-1]
#cell_text.reverse()

# Add a table at the bottom of the axes
the_table = plt.table(cellText=cell_text,
                      rowLabels=rows,
                      rowColours=colors,
                      colLabels=columns,
                      loc='bottom')

# Adjust layout to make room for the table:
plt.subplots_adjust(left=0.2, bottom=0.2)

values = np.arange(0, 475000, 50000)
value_increment = 1000
N = len(columns)
ind = np.arange(N)
width = 0.4

p1 = plt.bar(ind, amountLableTP, width)
p2 = plt.bar(ind, amountLableCD, width, bottom=amountLableTP)
plt.xticks([])
plt.ylabel('Daily Total Amount (Thousand VND)')
plt.yticks(values * value_increment, ['%d' % val for val in values])
plt.title('DCRS\'s Sale Amount Report Weekly')
plt.legend((p1[0], p2[0]), ('TopUp', 'Card'))
plt.grid(b=True, which='major', color='#666666', linestyle='-')

plt.show()