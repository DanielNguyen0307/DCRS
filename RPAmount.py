import cx_Oracle
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

sid = 'dcrs/dcrs#201912@10.1.8.133/dcrs' 
con = cx_Oracle.connect(sid)
cur = con.cursor()

##Get Query statement
def defSQL(offset):
	x = 'SELECT SUM(REAL_AMOUNT) FROM SALES_HISTORY WHERE TRUNC(TRANS_TIME) = TRUNC(SYSDATE-' + str(offset) + ')'
	return x
	
## Get timeline Lable
def defTimelable(offset):
	return datetime.strftime(datetime.now() - timedelta(offset), '%d/%m')

	
amountLable = []
for offset in range(7):
	query=defSQL(offset)
	for i in cur.execute(query):
		amountLable.append(i[0])

dateLable=[defTimelable(i) for i in range(7)]
amountLable.reverse()
dateLable.reverse()
fig, ax = plt.subplots()
ax.set_ylabel('Sale Real Amount')
#ax.set_xlable('')
ax.bar(dateLable,amountLable)
ax.set_title('DCRS Amount Sale Number Weekly Report')
ax.yaxis.grid(True)
ax.set_xticklabels(dateLable)
plt.tight_layout()
plt.show()
