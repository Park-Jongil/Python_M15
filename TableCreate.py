import urllib.request
import xml.etree.ElementTree as ET
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

def CheckTable_Exist(conn,tblname):
    try :
        cur = conn.cursor()
        sql_stmt = "Select count(*) from sqlite_master Where Name = '" + tblname + "'"
        cur.execute(sql_stmt)
        row = cur.fetchone()
        print( row[0] )
        if (row[0]==0) :
            cur = conn.cursor()
            sql_stmt = "CREATE TABLE " + tblname + " ( `CheckTime` TEXT NOT NULL, `CameraID` INTEGER, `CameraName` TEXT, `PrevStatus` INTEGER, `CurrStatus` INTEGER )"
            cur.execute(sql_stmt)        
            conn.commit()
            print( "Table Create ")
        else :
            print( "Table Exist ")
    except :
        print( "Table Exist Error " )
        return None


def main():
    database  = "NaizDB.db"
    tablename = "StatusChange" + datetime.today().strftime("%Y%m%d")

    conn = create_connection(database)
    CheckTable_Exist( conn , tablename )


 
if __name__ == '__main__':
    main()
   