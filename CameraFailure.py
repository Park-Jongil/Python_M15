import sqlite3
import sys
from sqlite3 import Error

db_file = "NaizDB.db"
conn = sqlite3.connect(db_file)

Count = int(sys.argv[1])
cur = conn.cursor()
cur.execute("select CameraID,count(CameraID),CameraName,ip_addr from StatusChange as A,CameraList as B where A.CameraName==B.name AND substr(ip_addr,1,3)=='10.' group by CameraID order by count(CameraID) desc")
rows = cur.fetchall()

i = 0
for row in rows :
    i = i + 1
    print( row )
    if (i==Count) : break

