import sqlite3
from sqlite3 import Error

def Search_by_key(conn, key):
    try :
        cur = conn.cursor()
        cur.execute("select * from CameraList where seq=?",(int(key),) )
        rows = cur.fetchall()
        if (rows==None) : return None
        for row in rows : print( row )
    except :
        return None

def Search_by_Name(conn, name):
    try :
        cur = conn.cursor()
        cur.execute("select * from CameraList where name like ?", ('%'+name+'%',))
        rows = cur.fetchall()
        for row in rows : print( row )
        print("Count = " + str(len(rows)))
    except :
        return None

def main():
    db_file = "NaizDB.db"
    conn = sqlite3.connect(db_file)
#    Search_by_Name( conn , "M15")
    while True :
        Choice = input("[Q] Quit [K] Key [N] Name = ")
        if (Choice=='Q') or (Choice=='q') : break
        if (Choice=='K') or (Choice=='k') :
            Key = input("Key = ") 
            Search_by_key(conn , Key)
        if (Choice=='N') or (Choice=='n'):
            Name1 = input("Name = ") 
            Search_by_Name(conn , Name1)

if __name__ == '__main__':
    main()
    