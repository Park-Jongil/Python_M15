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

def select_name_by_key(conn, key):
    try :
        cur = conn.cursor()
        cur.execute("select seq,name,ip_addr from CameraList where seq=?",(int(key),) )
        row = cur.fetchone()
        if (row==None) : return None
        return row[1]
    except :
        return None

def select_ipaddr_by_key(conn, key):
    try :
        cur = conn.cursor()
        cur.execute("select seq,name,ip_addr from CameraList where seq=?",(int(key),) )
        row = cur.fetchone()
        if (row==None) : return None
        return row[2]
    except :
        return None


def main():
    database = "NaizDB.db"

    naiz_url = 'http://172.18.200.36:80/camera/list.cgi?id=admin&password=spdlwm1234&key=all&method=get'
    conn = create_connection(database)
    cur = conn.cursor()

    file = urllib.request.urlopen( naiz_url ).read().decode('euc-kr')
    root = ET.fromstring(file)
    iCount = 0

    for child in root :
        for sub in child :
            for item in sub :
                if (item.tag == 'Key') :      
                    UniqueKey = item.text
                if (item.tag == 'Name') :      
                    Name = item.text
                if (item.tag == 'Address') :      
                    IP_Addr = item.text
                if (item.tag == 'RTSP_URL1') :    
                    RTSP_URL1 = item.text  
                if (item.tag == 'RTSP_URL2') :      
                    RTSP_URL2 = item.text  
            iCount = iCount + 1
    # sqlite test.db 에 해당내용 저장        
            try :
                findname = select_name_by_key( conn , UniqueKey )
                if (findname==None) :
                    print("UniqueKey = " + UniqueKey)
                    sql_stmt = "insert into CameraList(seq,name,ip_addr,rtsp_url1,rtsp_url2,status) values(?,?,?,?,?,?)"
                    cur.execute( sql_stmt,(int(UniqueKey),Name,IP_Addr,RTSP_URL1,RTSP_URL2,0))
                    conn.commit()
                    print("Insert Name = " + Name)
                    print("Address = " + IP_Addr)
                    print("RTSP_URL #1 = " + RTSP_URL1)
                    print("RTSP_URL #2 = " + RTSP_URL2)
                else :
                    ipaddr = select_ipaddr_by_key( conn , UniqueKey )
                    if (findname != Name) or (ipaddr != IP_Addr) :
                        print("UniqueKey = " + UniqueKey)
                        sql_stmt = "update CameraList set name=?,ip_addr=?,rtsp_url1=?,rtsp_url2=? where seq = ?"
                        cur.execute( sql_stmt,(Name,IP_Addr,RTSP_URL1,RTSP_URL2,int(UniqueKey)))
                        conn.commit()
                        print("Update Name = " + Name)
            except :
                print(" DB 에러 ")

    print("\n전체갯수 = " + str(iCount))
    conn.close()


if __name__ == '__main__':
    main()
    
    
