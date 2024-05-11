import sqlite3

conn = sqlite3.connect("Alita.db")
cursor= conn.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key,name VARCHAR(100),path VARCHAR(1000))"
cursor.execute(query)

# query = "INSERT INTO sys_command VALUES(null,'Jupyter Notebook','C:\\Users\\Girish\\OneDrive\\Desktop\\Jupyter Notebook')"
# cursor.execute(query)
# conn.commit()

# query = "Delete from sys_command where id=2"
# cursor.execute(query)
# conn.commit()

query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key,name VARCHAR(100),url VARCHAR(1000))"
cursor.execute(query)

# query = "INSERT INTO web_command VALUES(null,'YouTube','https://www.youtube.com')"
# cursor.execute(query)
# conn.commit()

# query = "Delete from web_command where id=2"
# cursor.execute(query)
# conn.commit()