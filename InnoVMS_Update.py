import urllib.request
import xml.etree.ElementTree as ET
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def Check_InnoData_vs_CameraList_Sync(conn):
    try :
        cur = conn.cursor()
        cur.execute("Select * from tbl_InnoVMS where device_name not in ( Select name from CameraList )")
        conn.commit()
    except :
        return None

def select_name_by_CamList(conn, key):
    try :
        cur = conn.cursor()
        cur.execute("select seq,name,ip_addr from CameraList where seq=?",(int(key),) )
        row = cur.fetchone()
        if (row==None) : return None
        return row[1]
    except :
        return None

def select_name_by_key(conn, key):
    try :
        cur = conn.cursor()
        cur.execute("select id,device_name,device_ip from tbl_InnoVMS where id=?",(key,) )
        row = cur.fetchone()
        if (row==None) : return None
        return row[1]
    except :
        return None

def insert_data_VMS_List(conn, rowdata ):
    sql_stmt = "insert into tbl_InnoVMS(id,device_name,device_ip,vms_ip,vms_ch) values(?,?,?,?,?)"
    cur = conn.cursor()
    cur.execute( sql_stmt,(rowdata[0],rowdata[1],rowdata[2],rowdata[7],rowdata[8]) )
    conn.commit()

def update_data_VMS_List(conn, rowdata ):
    sql_stmt = "update tbl_InnoVMS Set device_name=?,device_ip=?,vms_ip=?,vms_ch=? Where id = ?"
    cur = conn.cursor()
    cur.execute( sql_stmt,(rowdata[1],rowdata[2],rowdata[7],rowdata[8],rowdata[0]) )
    conn.commit()

def main():
    database = "NaizDB.db"
    conn = create_connection(database)

# tbl_InnoVMS 에 존재하지만 CameraList 에는 삭제된 리스트를 찾아서 지워주는 작업
    Check_InnoData_vs_CameraList_Sync( conn )

# 기준 카메라테이블에서 쿼리를 수행하여 데이터를 수집하여 Inno_VMS 테이블에 업데이트
    cur = conn.cursor()
    cur.execute("SELECT * FROM CameraList")
    rows = cur.fetchall()
    iTotal = len(rows)
    for row in rows :
        CheckName = select_name_by_key( conn , row[0] ) 
# 기존에 있는지 확인하여 데이터 업데이트 처리.
        if (CheckName==None) :
# "*" 로 시작하는 데이터는 처리하지 않는다.            
            if (row[1].startswith("*") != True) :
                insert_data_VMS_List( conn , row )         
                print("Data Append : " + row[1] , )
        else :
            if (row[1].startswith("*") != True) :
                CamName = select_name_by_CamList( conn , row[0] )
                if (CheckName != CamName ) :
                    update_data_VMS_List( conn , row )         
                    print("Name Change : " + row[1] )

# 데이터베이스 종료
    conn.close()

if __name__ == '__main__':
    main()
    
