import sys
import sqlite3
from sqlite3 import Error

Limit = 0
if (len(sys.argv) > 1) : Limit = int(sys.argv[1])

db_file = "NaizDB.db"
conn = sqlite3.connect(db_file)

cur = conn.cursor()
cur.execute("update CameraList set cntError = ( Select count(CameraID) from StatusChange where StatusChange.CameraName==CameraList.name group by CameraID)")
conn.commit()
cur.execute("SELECT * FROM CameraList order by cntError desc")
rows = cur.fetchall()
iTotal = len(rows)
iCount = 0
isAlive = 0
for row in rows :
    if (row[2].startswith("10.")) == True :
        if (row[5]==1) : isAlive = isAlive + 1
        iCount = iCount + 1
        if (iCount==Limit) : break
        print( row )

conn.close()
print("Total    = " + str(iTotal))
print("4 Campus = " + str(iCount))
print("Alive    = " + str(isAlive))
