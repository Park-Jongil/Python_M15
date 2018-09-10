import sqlite3
from sqlite3 import Error

db_file = "NaizDB.db"
conn = sqlite3.connect(db_file)

cur = conn.cursor()
cur.execute("SELECT * FROM CameraList")
rows = cur.fetchall()
iTotal = len(rows)
iCount = 0
isAlive = 0

for row in rows :
    if (row[2].startswith("10.")) == True :
        if (row[5]==1) : isAlive = isAlive + 1
        iCount = iCount + 1
        print( row )

print("Total    = " + str(iTotal))
print("4 Campus = " + str(iCount))
print("Alive    = " + str(isAlive))
#for row in rows :  print( row )


