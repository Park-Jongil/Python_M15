import sqlite3
import sys
from sqlite3 import Error

Count = 0
Limit = 0
if (len(sys.argv) > 1) : Count = int(sys.argv[1])
if (len(sys.argv) > 2) : Limit = int(sys.argv[2])

db_file = "NaizDB.db"
conn = sqlite3.connect(db_file)
cur = conn.cursor()
cur.execute("select CameraID,count(CameraID),CameraName,ip_addr from StatusChange as A,CameraList as B where A.CameraName==B.name AND substr(ip_addr,1,3)=='10.' group by CameraID order by count(CameraID) desc")
rows = cur.fetchall()
if (len(rows)!=0) : 
    i = 0
    for row in rows :
        i = i + 1
        Chk = row[1]
        if (Limit > 0) : 
            if (int(Chk) > Limit) : print( row )
        else:
            print( row )
        if (i==Count) : break

