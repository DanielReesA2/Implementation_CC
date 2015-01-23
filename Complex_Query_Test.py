import sqlite3
_table = "Task"
print("=====================================")
print()

with sqlite3.connect("Task_Manager_Database.db") as db:
    cursor = db.cursor()
    cursor.execute("pragma table_info({0})".format(_table))
    results = cursor.fetchall()

foreign_key_columns = []

for item in results:
    print("| {0:<22} ".format(item[1]),end='')
    check = item[1]
    if check[-2:] == "ID" and check != ("{0}ID".format(_table)):
        foreign_key_columns.append(item[1])
    else:
        foreign_key_columns.append("-")
print("|")
for item in results:
    print("|------------------------",end='')
print("|")

with sqlite3.connect("Task_Manager_Database.db") as db:
    cursor = db.cursor()
    cursor.execute("select * from {0}".format(_table))
    results = cursor.fetchall()

for item in results:
    index = 0
    for item2 in item:
        try:
            if foreign_key_columns[index] != "-":
                temp_table = foreign_key_columns[index]
                temp_table = temp_table[:-2]
                with sqlite3.connect("Task_Manager_Database.db") as db:
                    cursor = db.cursor()
                    cursor.execute("select * from {0} where {0}ID = ?".format(temp_table,item),(item2,))
                    result = cursor.fetchone()
                print("| {0:<22} ".format(result[1]),end='')
            else:
                print("| {0:<22} ".format(item[index]),end='')
            index = index + 1
        except:
            print("| {0:^22} ".format("NULL - please update"),end='')
            index = index + 1
    print("|")

input("")

with sqlite3.connect("Task_Manager_Database.db") as db:
    cursor = db.cursor()
    cursor.execute("pragma table_info({0})".format(_table))
    results = cursor.fetchall()

foreign_key_columns = []

column_count = 0
for item in results:
    column_count = column_count + 1
    print("| {0:<22} ".format(item[1]),end='')
    check = item[1]
    if check[-2:] == "ID" and check != ("{0}ID".format(_table)):
        foreign_key_columns.append(item[1])
    else:
        foreign_key_columns.append("-")
print("|")
for item in results:
    print("|------------------------",end='')
print("|")


with sqlite3.connect("Task_Manager_Database.db") as db:
    cursor = db.cursor()
    cursor.execute("select * from {0},Project".format(_table))
    results = cursor.fetchall()

row_count = 0
for item in results:
    row_count = row_count + 1

for index in range(row_count):
    for index2 in range(column_count):
        item = results[index]
        print("| {0:<22} ".format(item[index2]),end='')
        


##for item in results:
##    index = 0
##    for item2 in item:
##        try:
##            if foreign_key_columns[index] != "-":
##                print("| {0:<22} ".format(item[index]),end='')
##            else:
##                print("| {0:<22} ".format(item[index]),end='')
##            if index+1 != column_count:
##                index = index + 1
##        except:
##            print("| {0:^22} ".format("NULL - please update"),end='')
##            if index+1 != column_count:
##                index = index + 1
    print("|")
