import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
import socket
import sqlite3
from sqlite3 import Error
from time import sleep

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def select_status_by_key(conn, key):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT seq,status FROM CameraList WHERE seq=?", (key,))
    row = cur.fetchone()
    if (row==None) : return None
    return row[1]

def select_name_by_key(conn, key):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT seq,name FROM CameraList WHERE seq=?", (key,))
    row = cur.fetchone()
    return row[1]


def update_status_by_key(conn, key , status):
    cur = conn.cursor()
    cur.execute("UPDATE CameraList SET status=? WHERE seq=?", (status, key))        
    conn.commit()

def Insert_StatusChange(conn, ChkTime , key , name , prev , curr):
    cur = conn.cursor()
    sql_stmt = "insert into StatusChange(CheckTime,CameraID,CameraName,PrevStatus,CurrStatus) values(?,?,?,?,?)"
    cur.execute( sql_stmt,(ChkTime,key,name,prev,curr))
    conn.commit()

def TcpSocket_AlarmNotify_Status(ip_Addr,port,CamKey,CamStatus):
    try :
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(( ip_Addr , port ))
        SendMsg = CamKey + "," + CamStatus
        sock.send( SendMsg )
    except :
        print(" TCP/IP 통신에러 ")


def main():
    database = "NaizDB.db"
    naiz_url = 'http://172.18.200.36:80/event/status.cgi?id=admin&password=spdlwm1234&key=all&method=get'
    Notify_Addr = "127.0.0.1"
    Notify_Port = 9990

    conn = create_connection(database)

    file = urllib.request.urlopen( naiz_url ).read().decode('euc-kr')
    root = ET.fromstring(file)
    iCount = 0
    isAlive = 0
    iPrevStatus = 0

    for child in root :
        for sub in child :
            HighStreamConnection = '0'
            LowStreamConnection  = '0'
            iCurrStatus = 0
            for item in sub :
                if (item.tag == 'Key') :      
                    UniqueKey = item.text
                if (item.tag == 'HighStreamConnection') :    
                    HighStreamConnection = item.text  
                if (item.tag == 'LowStreamConnection') :      
                    LowStreamConnection = item.text  
#            print("UniqueKey = " + UniqueKey)
#            print("HighStreamConnection  = " + HighStreamConnection)
#            print("LowStreamConnection   = " + LowStreamConnection)
            if (HighStreamConnection=='1') and (LowStreamConnection=='1')  :
                isAlive = isAlive + 1   
                iCurrStatus = 1
            iPrevStatus = select_status_by_key( conn , int(UniqueKey) )
            if (iPrevStatus != iCurrStatus) and (iPrevStatus!=None):
                print(" 상태값 변이가 발생함 Key = " + UniqueKey )
                print("   Prev = " + str(iPrevStatus) ) 
                print("   Current = " + str(iCurrStatus) )                
                update_status_by_key( conn , int(UniqueKey) , iCurrStatus )

                CameraName = select_name_by_key( conn , int(UniqueKey) )
                CheckTime = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
                Insert_StatusChange(conn,CheckTime,int(UniqueKey),CameraName,iPrevStatus,iCurrStatus)

#                if (Notify_Addr != "") :
#                    TcpSocket_AlarmNotify_Status(Notify_Addr,Notify_Port,UniqueKey,iCurrStatus)
            iCount = iCount + 1

    print("전체갯수 = " + str(iCount))
    print("활성화   = " + str(isAlive))
    conn.close()

if __name__ == '__main__':
    while True:
        main()
        sleep(5)
    
    
