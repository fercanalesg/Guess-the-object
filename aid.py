
import sqlite3
conn= sqlite3.connect('other.db')
cursorObj= conn.cursor()

conn2= sqlite3.connect('other.db')
cursorObj2= conn2.cursor()


cursorObj.execute('''CREATE TABLE IF NOT EXISTS gameTable
                        (number integer, question text, answer text)''')

cursorObj.execute("DELETE FROM gameTable")
cursorObj.execute('''INSERT INTO gameTable VALUES 
                        (1, 'Is the object black?', 'Yes') ''')

conn.commit()

num = 6
q = "Holaa?>>>>>>>"
a = "Simon"

cursorObj2.execute("INSERT INTO gameTable VALUES(?,?,?)", (num, q, a))
conn2.commit()

for row in cursorObj.execute(''' SELECT * FROM gameTable ''' ):
    print(row)



cursorObj.execute("SELECT * FROM gameTable")
message = cursorObj.fetchall()
#print(type(message[0]))
#print(message)
