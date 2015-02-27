#database management program
#daniel rees

#08/12/14 started
#16/01/15 completed

import sqlite3

def create_table(db_name,table_name,sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("Select name from sqlite_master where name=?",(table_name,))
        result = cursor.fetchall()
        keep_table = True
        if len(result) == 1:
            response = input("The table {0} already exists, do you wish to recreate it (y/n): ".format(table_name))
            if response == "y":
                keep_table = False
                print("The '{0}' table will be recreated - all existing data will be lost".format(table_name))
                cursor.execute("drop table if exists {0}".format(table_name))
                db.commit()
            else:
                print("The existing table was kept")
        else:
            keep_table = False
        if not keep_table:
            cursor.execute(sql)
            db.commit()

def initialise_database():
    db_name = "Task_Manager_Database.db"
    sql = """create table Company
             (CompanyID integer,
             CompanyName text,
             primary key(CompanyID))"""
    create_table(db_name,"Company",sql)

    sql = """create table Client
         (ClientID integer,
         ClientName text,
         ClientContactNo text,
         CompanyID integer,
         foreign key(CompanyID) references Company(CompanyID)
         on update cascade on delete set null
         primary key (ClientID))"""
    create_table(db_name,"Client",sql)

    sql = """create table Project
             (ProjectID integer,
             ProjectName text,
             ClientID integer,
             foreign key(ClientID) references Client(ClientID)
             on update cascade on delete set null
             primary key(ProjectID))"""
    create_table(db_name,"Project",sql)

    sql = """create table Task
             (TaskID integer,
             TaskName text,
             DueDate text,
             Priority integer,
             TechnicalAreaID integer,
             ProjectID integer,
             TaskManagerID integer,
             foreign key(TechnicalAreaID) references TechnicalArea(TechnicalAreaID)
             on update cascade on delete set null
             foreign key(ProjectID) references Project(ProjectID)
             on update cascade on delete set null
             foreign key(TaskManagerID) references TaskManager(TaskManagerID)
             on update cascade on delete set null
             primary key(TaskID))"""
    create_table(db_name,"Task",sql)

    sql = """create table TaskTags
             (TaskTagsID integer,
             TaskID integer,
             CustomTagID integer,
             foreign key(TaskID) references Task(TaskID)
             on update cascade on delete set null
             foreign key(CustomTagID) references CustomTag(CustomTagID)
             on update cascade on delete set null
             primary key(TaskTagsID))"""
    create_table(db_name,"TaskTags",sql)

    sql = """create table CustomTag
             (CustomTagID integer,
             TagName text,
             TagValue text,
             primary key(CustomTagID))"""
    create_table(db_name,"CustomTag",sql)

    sql = """create table TaskManager
             (TaskManagerID integer,
             TaskManagerName text,
             TaskManagerContactNo text,
             primary key(TaskManagerID))"""
    create_table(db_name,"TaskManager",sql)

    sql = """create table TechnicalArea
            (TechnicalAreaID integer,
            TechnicalAreaName text,
            TechnicalAreaContactNo text,
            primary key(TechnicalAreaID))"""
    create_table(db_name,"TechnicalArea",sql)

############################################################################################################################### DISPLAY/GET INPUT


def display_menu():
    print("""=====================================
Database Manager 

1. default view
2. select from database
3. insert to database
4. delete from database
5. update data for database
6. exit program

=====================================""")

def get_input():
    valid = False
    while not valid:
        try:
            user_input = int(input(""))
            if user_input in [1,2,3,4,5,6]:
                valid = True
            else:
                print("Choice not valid.")
        except:
            print("Choice not valid.")
    return user_input

############################################################################################################################### SELECT FROM TABLE


def select_table():
    print("""1. Company
2. Client
3. Project
4. Task
5. TaskManager
6. TechnicalArea
7. GO BACK""")
    print("Please enter which Table you would like to interact with: ")
    valid = False
    while not valid:
        try: 
            _table = int(input(""))
            if _table in [1,2,3,4,5,6,7]:
                valid = True
            else:
                print("Choice not valid.")
        except:
            print("Choice not valid. ")
    #========================
    _1 = 'Company'
    _2 = 'Client'
    _3 = 'Project'
    _4 = 'Task'
    _5 = 'TaskManager'
    _6 = 'TechnicalArea'

    if _table == 1:
        _table = _1
        return _table
    elif _table == 2:
        _table = _2
        return _table
    elif _table == 3:
        _table = _3
        return _table
    elif _table == 4:
        _table = _4
        return _table
    elif _table == 5:
        _table = _5
        return _table
    elif _table == 6:
        _table = _6
        return _table
    elif _table == 7:
        return _table
    #========================

def select_statement(_table):
    print("1. Select ALL")
    print("2. Select ONE")
    print("3. Select FILTER")
    valid = False
    while not valid:
        try:
            user_input = int(input(""))
            if user_input in [1,2,3]:
                valid = True
            else:
                print("Choice not valid.")
        except:
            print("Choice not valid.")
    if user_input == 1:
        if _table == "Company":
            results = select_all_from_company()
            input("")
        elif _table == "Client":
            results = select_all_from_client()
            input("")
        elif _table == "Project":
            results = select_all_from_project()
            input("")
        elif _table == "Task":
            results = select_all_from_task()
            input("")
        elif _table == "TaskManager":
            results = select_all_from_taskmanager()
            input("")
        elif _table == "TechnicalArea":
            results = select_all_from_technicalarea()
            input("")
    elif user_input == 2:
        id_not_name,id_to_get = display_existing(_table)
        if _table == "Company":
            result = select_one_from_company(id_not_name,id_to_get)
            input("")
        elif _table == "Client":
            result = select_one_from_client(id_not_name,id_to_get)
            input("")
        elif _table == "Project":
            result = select_one_from_project(id_not_name,id_to_get)
            input("")
        elif _table == "Task":
            result = select_one_from_task(id_not_name,id_to_get)
            input("")
        elif _table == "TaskManager":
            result = select_one_from_taskmanager(id_not_name,id_to_get)
            input("")
        elif _table == "TechnicalArea":
            result = select_one_from_technicalarea(id_not_name,id_to_get)
            input("")

    elif user_input == 3:
        select_with_filter_from_table(_table)

def select_all_from_company():
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(Company)")
        results = cursor.fetchall()

    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("""select * from Company""")
        results = cursor.fetchall()

    for item in results:
        for item2 in item:
            try:
                print("| {0:<22} ".format(item2),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return results

def select_all_from_client():
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(Client)")
        results = cursor.fetchall()

    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("""select a.ClientID,a.ClientName,a.ClientContactNo,b.CompanyName
from Client a
join Company b
on a.CompanyID= b.CompanyID""")
        results = cursor.fetchall()

    for item in results:
        for item2 in item:
            try:
                print("| {0:<22} ".format(item2),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return results

def select_all_from_project():
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(Project)")
        results = cursor.fetchall()

    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("""select a.ProjectID,a.ProjectName,b.ClientName 
from Project a
join Client b
on a.ClientID = b.ClientID""")
        results = cursor.fetchall()

    for item in results:
        for item2 in item:
            try:
                print("| {0:<22} ".format(item2),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return results

def select_all_from_task():
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(Task)")
        results = cursor.fetchall()

    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("""select a.TaskID,a.TaskName,a.DueDate,a.Priority,b.TechnicalAreaName,d.ProjectName,c.TaskManagerName
from Task a
join TechnicalArea b 
on a.TechnicalAreaID = b.TechnicalAreaID
join TaskManager c
on a.TaskManagerID = c.TaskManagerID
join Project d
on a.ProjectID = d.ProjectID""")
        results = cursor.fetchall()

    for item in results:
        for item2 in item:
            try:
                print("| {0:<22} ".format(item2),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return results

def select_all_from_taskmanager():
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(TaskManager)")
        results = cursor.fetchall()

    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("""select * from TaskManager""")
        results = cursor.fetchall()

    for item in results:
        for item2 in item:
            try:
                print("| {0:<22} ".format(item2),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return results

def select_all_from_technicalarea():
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(TechnicalArea)")
        results = cursor.fetchall()

    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("""select * from TechnicalArea""")
        results = cursor.fetchall()

    for item in results:
        for item2 in item:
            try:
                print("| {0:<22} ".format(item2),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return results
 
def display_existing(_table):
    id_check = []
    name_check = []
    id_not_name = True
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("select {0}ID,{0}Name from {0}".format(_table))
        results = cursor.fetchall()
    print("Existing ID's: ")
    for item in results:
        print("| {0} - {1}" .format(item[0],item[1]))
        id_check.append(str(item[0]))
        name_check.append(item[1])
    valid = False
    while not valid:
        try:
            id_to_get = input("Enter {0}ID or {0}Name: ".format(_table))
            if id_to_get in id_check:
                valid = True
            elif id_to_get in name_check:
                id_not_name = False
                valid = True
            else:
                print("Choice not valid.")
        except:
            print("Choice not valid.")
    return id_not_name,id_to_get


def select_one_from_company(id_not_name,id_to_get):
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(Company)")
        results = cursor.fetchall()
    
    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    if id_not_name:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("""select * from Company where CompanyID = ?""",(id_to_get,))
            result = cursor.fetchone()
            
        for item in result:
            try:
                print("| {0:<22} ".format(item),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")
        
    elif not id_not_name:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("""select * from Company where CompanyName = ?""",(id_to_get,))
            result = cursor.fetchone()

        for item in result:
            try:
                print("| {0:<22} ".format(item),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return result

def select_one_from_client(id_not_name,id_to_get):
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(Client)")
        results = cursor.fetchall()
    
    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    if id_not_name:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("""select a.ClientID,a.ClientName,a.ClientContactNo,b.CompanyName
from Client a
join Company b
on a.CompanyID= b.CompanyID
where ClientID = ?""",(id_to_get,))
            result = cursor.fetchone()
            
        for item in result:
            try:
                print("| {0:<22} ".format(item),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")
        
    elif not id_not_name:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("""select a.ClientID,a.ClientName,a.ClientContactNo,b.CompanyName
from Client a
join Company b
on a.CompanyID= b.CompanyID
where ClientName = ?""",(id_to_get,))
            result = cursor.fetchone()

        for item in result:
            try:
                print("| {0:<22} ".format(item),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return result
    
def select_one_from_project(id_not_name,id_to_get):
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(Project)")
        results = cursor.fetchall()
    
    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    if id_not_name:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("""select a.ProjectID,a.ProjectName,b.ClientName 
from Project a
join Client b
on a.ClientID = b.ClientID
where ProjectID = ?""",(id_to_get,))
            result = cursor.fetchone()
            
        for item in result:
            try:
                print("| {0:<22} ".format(item),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")
        
    elif not id_not_name:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("""select a.ProjectID,a.ProjectName,b.ClientName 
from Project a
join Client b
on a.ClientID = b.ClientID
where ProjectName = ?""",(id_to_get,))
            result = cursor.fetchone()

        for item in result:
            try:
                print("| {0:<22} ".format(item),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return result

def select_one_from_task(id_not_name,id_to_get):
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(Task)")
        results = cursor.fetchall()
    
    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    if id_not_name:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("""select a.TaskID,a.TaskName,a.DueDate,a.Priority,b.TechnicalAreaName,c.TaskManagerName,d.ProjectName
from Task a
join TechnicalArea b 
on a.TechnicalAreaID = b.TechnicalAreaID
join TaskManager c
on a.TaskManagerID = c.TaskManagerID
join Project d
on a.ProjectID = d.ProjectID
where TaskID = ?""",(id_to_get,))
            result = cursor.fetchone()
            
        for item in result:
            try:
                print("| {0:<22} ".format(item),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")
        
    elif not id_not_name:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("""select a.TaskID,a.TaskName,a.DueDate,a.Priority,b.TechnicalAreaName,c.TaskManagerName,d.ProjectName
from Task a
join TechnicalArea b 
on a.TechnicalAreaID = b.TechnicalAreaID
join TaskManager c
on a.TaskManagerID = c.TaskManagerID
join Project d
on a.ProjectID = d.ProjectID
where TaskName = ?""",(id_to_get,))
            result = cursor.fetchone()

        for item in result:
            try:
                print("| {0:<22} ".format(item),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return result

def select_one_from_taskmanager(id_not_name,id_to_get):
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(TaskManager)")
        results = cursor.fetchall()
    
    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    if id_not_name:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("""select * from TaskManager where TaskManagerID = ?""",(id_to_get,))
            result = cursor.fetchone()
            
        for item in result:
            try:
                print("| {0:<22} ".format(item),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")
        
    elif not id_not_name:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("""select * from TaskManager where TaskManagerName = ?""",(id_to_get,))
            result = cursor.fetchone()

        for item in result:
            try:
                print("| {0:<22} ".format(item),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return result

def select_one_from_technicalarea(id_not_name,id_to_get):
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(TechnicalArea)")
        results = cursor.fetchall()
    
    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    if id_not_name:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("""select * from TechnicalArea where TechnicalAreaID = ?""",(id_to_get,))
            result = cursor.fetchone()
            
        for item in result:
            try:
                print("| {0:<22} ".format(item),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")
        
    elif not id_not_name:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("""select * from TechnicalArea where TechnicalAreaName = ?""",(id_to_get,))
            result = cursor.fetchone()

        for item in result:
            try:
                print("| {0:<22} ".format(item),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return result

def select_with_filter_from_table(_table):
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info({0})".format(_table))
        results = cursor.fetchall()

    filter_check = []
    _filters = []
    index = 1
    for item in results:
        print("{0}. {1}".format(index,item[1]))
        filter_check.append(index)
        _filters.append(item[1])
        index = index + 1

    valid = False
    while not valid:
        try:
            choice = int(input("Filter: "))
            if choice in filter_check:
                valid = True
            else:
                print("Choice not valid. ")
        except:
            print("Choice not valid. ")

    _filter = _filters[choice-1]

    valid = False
    while not valid:
        
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("select {0} from {1}".format(_filter,_table))
            results = cursor.fetchall()

        print("Existing IDs: ")
        filter_value_check = []
        existing_values_printed = []
        index = 0
        for item in results:
            item = item[0]
            filter_value_check.append(str(item))
            if item not in existing_values_printed:
                print("| {0} ".format(item),end='')
                existing_values_printed.append(item)
            index = index + 1
        print("|")

        _filter_value = input("Enter filter value: ")

        if _filter_value not in filter_value_check:
            print("Choice not valid. ")
        else:
            valid = True
    print("=====================================")
    print()

    if _table == "Company":
        results = select_all_from_company_filter(_filter,_filter_value)
        input("")
    elif _table == "Client":
        results = select_all_from_client_filter(_filter,_filter_value)
        input("")
    elif _table == "Project":
        results = select_all_from_project_filter(_filter,_filter_value)
        input("")
    elif _table == "Task":
        results = select_all_from_task_filter(_filter,_filter_value)
        input("")
    elif _table == "TaskManager":
        results = select_all_from_taskmanager_filter(_filter,_filter_value)
        input("")
    elif _table == "TechnicalArea":
        results = select_all_from_technicalarea_filter(_filter,_filter_value)
        input("")

def select_all_from_company_filter(_filter,_filter_value):
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("select * from Company where {0} = ? order by {0} asc".format(_filter),(_filter_value,))
        results = cursor.fetchall()

    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("""select {0} from Company""".format(_filter))
        results = cursor.fetchall()

    for item in results:
        for item2 in item:
            try:
                print("| {0:<22} ".format(item2),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return results
        
def select_all_from_client_filter(_filter,_filter_value):
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(Client)")
        results = cursor.fetchall()

    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("""select a.ClientID,a.ClientName,a.ClientContactNo,b.CompanyName
from Client a
join Company b
on a.CompanyID= b.CompanyID
where a.{0} = ? order by a.{0} asc""".format(_filter),(_filter_value,))
        results = cursor.fetchall()

    for item in results:
        for item2 in item:
            try:
                print("| {0:<22} ".format(item2),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return results

def select_all_from_project_filter(_filter,_filter_value):
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(Project)")
        results = cursor.fetchall()

    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("""select a.ProjectID,a.ProjectName,b.ClientName 
from Project a
join Client b
on a.ClientID = b.ClientID
where a.{0} = ? order by a.{0} asc""".format(_filter),(_filter_value,))
        results = cursor.fetchall()

    for item in results:
        for item2 in item:
            try:
                print("| {0:<22} ".format(item2),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return results

def select_all_from_task_filter(_filter,_filter_value):
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(Task)")
        results = cursor.fetchall()

    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("""select a.TaskID,a.TaskName,a.DueDate,a.Priority,b.TechnicalAreaName,d.ProjectName,c.TaskManagerName
from Task a
join TechnicalArea b 
on a.TechnicalAreaID = b.TechnicalAreaID
join TaskManager c
on a.TaskManagerID = c.TaskManagerID
join Project d
on a.ProjectID = d.ProjectID
where a.{0} = ? order by a.{0} asc""".format(_filter),(_filter_value,))
        results = cursor.fetchall()

    for item in results:
        for item2 in item:
            try:
                print("| {0:<22} ".format(item2),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return results

def select_all_from_taskmanager_filter(_filter,_filter_value):
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(TaskManager)")
        results = cursor.fetchall()

    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("""select * from TaskManager
where a.{0} = ? order by a.{0} asc""".format(_filter),(_filter_value,))
        results = cursor.fetchall()

    for item in results:
        for item2 in item:
            try:
                print("| {0:<22} ".format(item2),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return results

def select_all_from_technicalarea_filter(_filter,_filter_value):
    print("=====================================")
    print()
    
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(TechnicalArea)")
        results = cursor.fetchall()

    for item in results:
        print("| {0:<22} ".format(item[1]),end='')
    print("|")
    for item in results:
        print("|------------------------",end='')
    print("|")

    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("""select * from TechnicalArea
where a.{0} = ? order by a.{0} asc""".format(_filter),(_filter_value,))
        results = cursor.fetchall()

    for item in results:
        for item2 in item:
            try:
                print("| {0:<22} ".format(item2),end='')
            except:
                print("| {0:^22} ".format("NULL - please update"),end='')
        print("|")

    return results

############################################################################################################################### INSERT TO TABLE

def get_table_values(_table):
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info({0})".format(_table))
        results = cursor.fetchall()

    item_value_list = []
    for item in results:
        valid = False
        while not valid:
            if item[1] != ("{0}ID".format(_table)):
                item_value = input("{0} ({1}): ".format(item[1],item[2]))
                if len(str(item_value)) <= 22:
                    item_value_list.append(item_value)
                    valid = True
                else:
                    print("Value must be less than 23 characters")
            else:
                valid = True


    if _table == 'Company':
        insert_to_Company(item_value_list,_table)
    elif _table == 'Client':
        insert_to_Client(item_value_list,_table)
    elif _table == 'Project':
        insert_to_Project(item_value_list,_table)
    elif _table == 'Task':
        insert_to_Task(item_value_list,_table)
    elif _table == 'TaskManager':
        insert_to_TaskManager(item_value_list,_table)
    elif _table == 'TechnicalArea':
        insert_to_TechnicalArea(item_value_list,_table)
        
def insert_to_Company(item_value_list,_table):
    print("=====================================")
    values = (item_value_list[0],)
    try:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = "insert into Company(CompanyName) values (?)"
            cursor.execute(sql,values)
            db.commit()
        print("Inserted values into table '{0}'.".format(_table))
        input("")
    except:
        print("REFERENTIAL ERROR - Foreign Keys not valid, references non existing record. ")
        input("")
    
def insert_to_Client(item_value_list,_table):
    print("=====================================")
    values = (item_value_list[0],item_value_list[1],item_value_list[2],)
    try:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = "insert into Client(ClientName,ClientContactNo,CompanyID) values (?,?,?)"
            cursor.execute(sql,values)
            db.commit()
        print("Inserted values into table '{0}'.".format(_table))
        input("")
    except:
        print("REFERENTIAL ERROR - Foreign Keys not valid, references non existing record. ")
        input("")
        
def insert_to_Project(item_value_list,_table):
    print("=====================================")
    values = (item_value_list[0],item_value_list[1],)
    try:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = "insert into Project(ProjectName,ClientID) values (?,?)"
            cursor.execute(sql,values)
            db.commit()
        print("Inserted values into table '{0}'.".format(_table))
        input("")
    except:
        print("REFERENTIAL ERROR - Foreign Keys not valid, references non existing record. ")
        input("")
    
def insert_to_Task(item_value_list,_table):
    print("=====================================")
    values = (item_value_list[0],item_value_list[1],item_value_list[2],item_value_list[3],item_value_list[4],item_value_list[5],)
    try:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = "insert into Task(TaskName,DueDate,Priority,TechnicalAreaID,ProjectID,TaskManagerID) values (?,?,?,?,?,?)"
            cursor.execute(sql,values)
            db.commit()
        print("Inserted values into table '{0}'.".format(_table))
        input("")
    except:
        print("REFERENTIAL ERROR - Foreign Keys not valid, references non existing record. ")
        input("")
    
def insert_to_TaskManager(item_value_list,_table):
    print("=====================================")
    values = (item_value_list[0],item_value_list[1],)
    try:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = "insert into TaskManager(TaskManagerName,TaskManagerContactNo) values (?,?)"
            cursor.execute(sql,values)
            db.commit()
        print("Inserted values into table '{0}'.".format(_table))
        input("")
    except:
        print("REFERENTIAL ERROR - Foreign Keys not valid, references non existing record. ")
        input("")
    
def insert_to_TechnicalArea(item_value_list,_table):
    print("=====================================")
    values = (item_value_list[0],item_value_list[1],)
    try:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = "insert into TechnicalArea(TechnicalAreaName,TechnicalAreaContactNo) values (?,?)"
            cursor.execute(sql,values)
            db.commit()
        print("Inserted values into table '{0}'.".format(_table))
        input("")
    except:
        print("REFERENTIAL ERROR - Foreign Keys not valid, references non existing record. ")
        input("")

############################################################################################################################### DELETE FROM TABLE

def delete_statement(_table):
    print("WARNING any places where the record is referenced will be set to NULL. Continue? y/n: ")
    valid = False
    while not valid:
        sure_yn = input("")
        if sure_yn.upper() not in ['Y','N']:
            print("Choice not valid. ")
        elif sure_yn.upper() == 'Y':
            valid = True
            delete_one_from_table(_table)
        else:
            valid = True

def delete_one_from_table(_table):

    if _table == "Company":
        select_all_from_company()
    elif _table == "Client":
        select_all_from_client()
    elif _table == "Project":
        select_all_from_project()
    elif _table == "Task":
        select_all_from_task()
    elif _table == "TaskManager":
        select_all_from_taskmanager()
    elif _table == "TechnicalArea":
        select_all_from_technicalarea()

    valid = False
    while not valid:
        try:
            item_to_be_deleted = int(input("Enter {0}ID: ".format(_table)))
            valid = True
        except:
            print("Choice not valid.")
            
    data = (item_to_be_deleted,)
    print("=====================================")
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        sql = ('delete from {0} where {0}ID=?'.format(_table,_table))
        cursor.execute(sql,data)
        db.commit()
    print("Item with ID '{0}' from table '{1}' deleted.".format(item_to_be_deleted,_table))
    input("")

############################################################################################################################### UPDATE DATA FOR DATABASE

def update_data_for_database(_table):
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
    
    id_check = []
    for item in results:
        index = 0
        id_check.append(item[0])
        
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
                print("| {0:<22} ".format("NULL - please update"),end='')
                index = index + 1
        print("|")

    input("")

    valid = False
    while not valid:
        try:
            id_to_update = int(input("Enter unique identifier of value to be updated: "))
            if id_to_update not in id_check:
                print("Choice not valid.")
            else:
                valid = True
        except:
            print("Choice not valid.")

    print()
    print("1. Update ALL Values")
    print("2. Update ONE Value")
    valid = False
    while not valid:
        try:
            all_or_one = int(input(""))
            if all_or_one not in [1,2]:
                print("Choice not valid")
            else:
                valid = True
        except:
            print("Choice not valid")

    if all_or_one == 1:
        if _table == 'Company':
            update_for_Company(id_to_update,_table)
        elif _table == 'Client':
            update_for_Client(id_to_update,_table)
        elif _table == 'Project':
            update_for_Project(id_to_update,_table)
        elif _table == 'Task':
            update_for_Task(id_to_update,_table)
        elif _table == 'TaskManager':
            update_for_TaskManager(id_to_update,_table)
        elif _table == 'TechnicalArea':
            update_for_TechnicalArea(id_to_update,_table)
    else:
        update_one_for_Table(id_to_update,_table)

def automatic_update_one_for_project(id_to_update,_value):
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("pragma table_info(Project)")
        results = cursor.fetchall()

    item = results[1]
    _column = item[1]
    values = (_value,id_to_update,)
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        sql = ("update Project set {0}=? where ProjectID = ?".format(_column))
        cursor.execute(sql,values)
        db.commit()
    
    print("Database updated successfully")

def automatic_update_one_for_table(id_to_update,_column,value,_table):
    
    values = (value,id_to_update,)
    with sqlite3.connect("Task_Manager_Database.db") as db:
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        sql = ("update {1} set {0}=? where {1}ID = ?".format(_column,_table))
        cursor.execute(sql,values)
        db.commit()
    print("Database updated successfully")

def automatic_update_one_for_table_id(id_not_name,id_to_update,_column,foreign_column,value,_table,foreign_table):

    if id_not_name:
        values = (value,id_to_update,)
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = ("update {1} set {0}=? where {1}ID = ?".format(_column,_table))
            cursor.execute(sql,values)
            db.commit()
        print("Database updated successfully")

    elif not id_not_name: 
        if foreign_table == "Company":
            results = select_all_from_company()
        elif foreign_table == "Client":
            results = select_all_from_client()
        elif foreign_table == "Project":
            results = select_all_from_project()
        elif foreign_table == "Task":
            results = select_all_from_task()
        elif foreign_table == "TaskManager":
            results = select_all_from_taskmanager()
        elif foreign_table == "TechnicalArea":
            results = select_all_from_technicalarea()
        id_match = []
        for item in results:
            id_match.append(item[1])
        index = 0
        for item in id_match:
            if value == item:
                value = index + 1
            index = index + 1

        values = (value,id_to_update,)
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = ("update {1} set {0}=? where {1}ID = ?".format(_column,_table))
            cursor.execute(sql,values)
            db.commit()
        print("Database updated successfully")

def update_one_for_Table(id_to_update,_table):
    print("=====================================")
    try:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("pragma table_info({0})".format(_table))
            results = cursor.fetchall()

        column_check = []
        column = []
        data_types = []
        index = 1
        for item in results:
            if item[1] != "{0}ID".format(_table):
                print("{0}. {1} ({2})".format(index,item[1],item[2]))
                column_check.append(index)
                column.append(item[1])
                data_type = item[2]
                data_types.append(data_type)
                index = index + 1
        

        valid = False
        while not valid:
            try:
                choice = int(input("Column to update: "))
                if choice in column_check:
                    valid = True
                    chosen_column = column[choice-1]
                    data_type = data_types[choice-1]
                else:
                    print("Choice not valid. ")
            except:
                print("Choice not valid. ")
                
        valid = False
        while not valid:            
            if data_type == "integer":
                try:
                    print()
                    update_value = int(input("Value: "))
                    if update_value > 23:
                        print("Value must be less than 23 characters")
                    else:
                        valid = True
                except:
                    print("Data type not valid.")          
            if data_type == "text":
                print()
                update_value = input("Value: ")
                if len(update_value) > 23:
                    print("Value must be less than 23 characters")
                else:
                    valid = True
                    
        valid = False
        while not valid:                
            if data_type == "integer" and type(update_value) != int:
                print("Data type not valid.")
            elif data_type == "text" and type(update_value) != str:
                print("Data type not valid.")
            else:
                valid = True
                
        values = (update_value,id_to_update,)
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = ("update {1} set {0}=? where {1}ID = ?".format(chosen_column,_table))
            cursor.execute(sql,values)
            db.commit()

        print()
        print("Values updated for '{0}ID = {1}'.".format(_table,id_to_update))
        input("")
    except sqlite3.IntegrityError:
        print("REFERENTIAL ERROR - Foreign Keys not valid, references non existing record. ")
        input("")

def update_for_Company(id_to_update,_table):
    data = (id_to_update,)
    print("=====================================")
    try:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("pragma table_info({0})".format(_table))
            results = cursor.fetchall()

        item_value_list = []
        for item in results:
            valid = False
            while not valid:
                if item[1] != ("{0}ID".format(_table)):
                    item_value = input("{0} ({1}): ".format(item[1],item[2]))
                    if len(str(item_value)) <= 22:
                        item_value_list.append(item_value)
                        valid = True
                    else:
                        print("Value must be less than 23 characters")
                else:
                    valid = True

        values = (item_value_list[0],id_to_update,)
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = "update Company set CompanyName = ? where CompanyID = ?"
            cursor.execute(sql,values)
            db.commit()

        print()
        print("Values updated for '{0}ID = {1}'.".format(_table,id_to_update))
        input("")
    except sqlite3.IntegrityError:
        print("REFERENTIAL ERROR - Foreign Keys not valid, references non existing record. ")
        input("")

def update_for_Client(id_to_update,_table):
    data = (id_to_update,)
    print("=====================================")
    try:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("pragma table_info({0})".format(_table))
            results = cursor.fetchall()

        item_value_list = []
        for item in results:
            valid = False
            while not valid:
                if item[1] != ("{0}ID".format(_table)):
                    item_value = input("{0} ({1}): ".format(item[1],item[2]))
                    if len(str(item_value)) <= 22:
                        item_value_list.append(item_value)
                        valid = True
                    else:
                        print("Value must be less than 23 characters")
                else:
                    valid = True

        values = (item_value_list[0],item_value_list[1],item_value_list[2],id_to_update,)
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = "update Client set ClientName=?,ClientContactNo=?,CompanyID=? where ClientID = ?"
            cursor.execute(sql,values)
            db.commit()

        print()
        print("Values updated for '{0}ID = {1}'.".format(_table,id_to_update))
        input("")
    except sqlite3.IntegrityError:
        print("REFERENTIAL ERROR - Foreign Keys not valid, references non existing record. ")
        input("")

def update_for_Project(id_to_update,_table):
    data = (id_to_update,)
    print("=====================================")
    try:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("pragma table_info({0})".format(_table))
            results = cursor.fetchall()

        item_value_list = []
        for item in results:
            valid = False
            while not valid:
                if item[1] != ("{0}ID".format(_table)):
                    item_value = input("{0} ({1}): ".format(item[1],item[2]))
                    if len(str(item_value)) <= 22:
                        item_value_list.append(item_value)
                        valid = True
                    else:
                        print("Value must be less than 23 characters")
                else:
                    valid = True

        values = (item_value_list[0],item_value_list[1],id_to_update,)
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = "update Project set ProjectName=?,ClientID=? where ProjectID = ?"
            cursor.execute(sql,values)
            db.commit()

        print()
        print("Values updated for '{0}ID = {1}'.".format(_table,id_to_update))
        input("")
    except sqlite3.IntegrityError:
        print("REFERENTIAL ERROR - Foreign Keys not valid, references non existing record. ")
        input("")

def update_for_Task(id_to_update,_table):
    data = (id_to_update,)
    print("=====================================")
    try:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("pragma table_info({0})".format(_table))
            results = cursor.fetchall()

        item_value_list = []
        for item in results:
            valid = False
            while not valid:
                if item[1] != ("{0}ID".format(_table)):
                    item_value = input("{0} ({1}): ".format(item[1],item[2]))
                    if len(str(item_value)) <= 22:
                        item_value_list.append(item_value)
                        valid = True
                    else:
                        print("Value must be less than 23 characters")
                else:
                    valid = True

        values = (item_value_list[0],item_value_list[1],item_value_list[2],item_value_list[3],item_value_list[4],item_value_list[5],id_to_update,)
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = "update Task set TaskName=?,DueDate=?,Priority=?,TechnicalAreaID=?,ProjectID=?,TaskManagerID=? where TaskID = ?"
            cursor.execute(sql,values)
            db.commit()

        print()
        print("Values updated for '{0}ID = {1}'.".format(_table,id_to_update))
        input("")
    except sqlite3.IntegrityError:
        print("REFERENTIAL ERROR - Foreign Keys not valid, references non existing record. ")
        input("")

def update_for_TaskManager(id_to_update,_table):
    data = (id_to_update,)
    print("=====================================")
    try:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("pragma table_info({0})".format(_table))
            results = cursor.fetchall()

        item_value_list = []
        for item in results:
            valid = False
            while not valid:
                if item[1] != ("{0}ID".format(_table)):
                    item_value = input("{0} ({1}): ".format(item[1],item[2]))
                    if len(str(item_value)) <= 22:
                        item_value_list.append(item_value)
                        valid = True
                    else:
                        print("Value must be less than 23 characters")
                else:
                    valid = True

        values = (item_value_list[0],item_value_list[1],id_to_update,)
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = "update TaskManager set TaskManagerName=?,TaskManagerContactNo=? where TaskManagerID = ?"
            cursor.execute(sql,values)
            db.commit()

        print()
        print("Values updated for '{0}ID = {1}'.".format(_table,id_to_update))
        input("")
    except sqlite3.IntegrityError:
        print("REFERENTIAL ERROR - Foreign Keys not valid, references non existing record. ")
        input("")

def update_for_TechnicalArea(id_to_update,_table):
    data = (id_to_update,)
    print("=====================================")
    try:
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("pragma table_info({0})".format(_table))
            results = cursor.fetchall()

        item_value_list = []
        for item in results:
            valid = False
            while not valid:
                if item[1] != ("{0}ID".format(_table)):
                    item_value = input("{0} ({1}): ".format(item[1],item[2]))
                    if len(str(item_value)) <= 22:
                        item_value_list.append(item_value)
                        valid = True
                    else:
                        print("Value must be less than 23 characters")
                else:
                    valid = True

        values = (item_value_list[0],item_value_list[1],id_to_update,)
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            sql = "update TechnicalArea set TechnicalAreaName=?,TechnicalAreaContactNo=? where TechnicalAreaID = ?"
            cursor.execute(sql,values)
            db.commit()

        print()
        print("Values updated for '{0}ID = {1}'.".format(_table,id_to_update))
        input("")
    except sqlite3.IntegrityError:
        print("REFERENTIAL ERROR - Foreign Keys not valid, references non existing record. ")
        input("")

############################################################################################################################### DEFAULT VIEW

def default_view(P_ID):
    if P_ID == -1:
        results = select_all_from_task()
    else:
        results = select_all_from_task_filter("ProjectID",P_ID)
    return results

############################################################################################################################### MAIN PROGRAM

if __name__ == "__main__":
    initialise_database()
    finish_program = False
    while not finish_program:
        display_menu()
        user_input = get_input()
        if user_input == 1:
            results = select_all_from_project()
            _all = ['-1','All Projects','All Clients']
            try:
                for item in _all:
                    print("| {0:<22} ".format(item),end='')
                print("|")
                P_ID = int(input("ID: "))
                default_view(P_ID)
                input("")
            except:
                print("Choice not valid")
        elif user_input == 2:
            _table = select_table()
            if _table != 7:
                select_statement(_table)
        elif user_input == 3:
            _table = select_table()
            if _table != 7:
                get_table_values(_table)
        elif user_input == 4:
            _table = select_table()
            if _table != 7:
                delete_statement(_table)
        elif user_input == 5:
            _table = select_table()
            if _table != 7:
                update_data_for_database(_table)
        elif user_input == 6:
            finish_program = True
