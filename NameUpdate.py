from datetime import datetime
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def main():
    database = "NaizDB.db"

    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT seq,prevName,name,CheckTime FROM CameraUpdate Where append = '변경' and CheckTime > '2018/09/21'")
    rows = cur.fetchall()
    print("변경된 내역")
    print(" Sequence    Name  <==  PrevName")
    for row in rows :
        sql_stmt = "Update tb_skh_point_cctv set  device_name = '" + row[2] + "' Where id = " + str(row[0]) + ";"
#        print( row[3] )
        print( sql_stmt )

    conn.close()    


if __name__ == '__main__':
    main()