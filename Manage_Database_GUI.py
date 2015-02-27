from Manage_Database import *
import sqlite3
import sys
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class TaskManagerMainGUI(QMainWindow):
    """Main window for task manager program"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")

        #create stacked layout
        self.stacked_layout = QStackedLayout()
        self.stacked_widget = QWidget()
        #create layouts/windows
        self.CreateMainWindow()
        self.stacked_layout.addWidget(self.main_widget)

        #set stacked layout index
        self.stacked_layout.setCurrentIndex(0)

        #add stacked_layout to stacked_widget and set main window central widget to stacked_widget
        self.stacked_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.stacked_widget)

        #create actions
        self.insert_data = QAction("Insert Record",self)
        self.delete_data = QAction("Delete Record",self)
        self.add_project = QAction("Add Project",self)

        #create bars
        self.main_tool_bar_1 = QToolBar()
        self.main_menu_bar = QMenuBar()
        self.main_status_bar = QStatusBar()

        #add actions to toolbar
        self.main_tool_bar_1.addAction(self.add_project)
        self.main_tool_bar_1.addAction(self.insert_data)
        self.main_tool_bar_1.addAction(self.delete_data)

        #add actions to menubars
        self.database_menu = self.main_menu_bar.addMenu("Database")
        self.database_menu.addAction(self.add_project)
        self.database_menu.addAction(self.insert_data)
        self.database_menu.addAction(self.delete_data) 
        
        #add message to statusbar
        self.main_status_bar.showMessage("Task Manager ver1.0")

        #add bars to mainwindow
        self.addToolBar(self.main_tool_bar_1)
        self.setMenuBar(self.main_menu_bar)
        self.setStatusBar(self.main_status_bar)

        #set window size/position
        self.resize(700,500)
        self.move(100,100)

        self.update_components()
        
    def CreateMainWindow(self):
        #components
        self.main_list_view = QListView()
        self.main_table_view = QTableView()
        self.label1 = QLabel("""Details:""")
        self.test = QPushButton("""TEST""")                
        #define layout
        self.main_layout = QGridLayout()
        self.details_layout = QVBoxLayout()
        #define spacings for columns
        self.main_layout.setColumnStretch(0,3)
        self.main_layout.setColumnStretch(1,15)
        self.main_layout.setColumnStretch(2,5)      
        #add details to details widget
        self.details_layout.addWidget(self.label1)
        self.details_layout.addWidget(self.test)
        #create widget to hold details
        self.details_widget = QWidget()
        #add details layout to details widget
        self.details_widget.setLayout(self.details_layout)
        #add components to layout
        self.main_layout.addWidget(self.main_list_view,0,0)
        self.main_layout.addWidget(self.main_table_view,0,1)
        self.main_layout.addWidget(self.details_widget,0,2)
        #create widget to hold layout
        self.main_widget = QWidget()
        #add layout to widget
        self.main_widget.setLayout(self.main_layout)

    def test(self):
        print("test")

    def update_components(self):
        self.update_main_list()
        self.update_main_table()
        self.main_status_bar.showMessage("Task Manager ver1.0")
        
    def update_main_list(self):
        results = select_all_from_project()
        projects = []
        projects.append("All")
        for item in results:
            projects.append(item[1])
        list_model = main_list_view_model(projects)
        self.main_list_view.setModel(list_model)


    def update_main_table(self):
        #display all tasks as default
        _table = "Task"
        with sqlite3.connect("Task_Manager_Database.db") as db:
            cursor = db.cursor()
            cursor.execute("pragma table_info({0})".format(_table))
            results = cursor.fetchall()
        headers = []
        for item in results:
            headers.append(item[1])        
        P_ID = -1
        results = default_view(P_ID)
        columns = len(results[0])
        rows = 0
        for item in results:
            rows = rows+1

        table_data_lists = [[] for index in range(rows)]
        i = 0
        for item in results:
            for item2 in item:
                if i != rows:
                    table_data_lists[i].append(item2)
            i = i + 1            

        table_model = main_table_view_model(table_data_lists,headers,rows,columns,_table)
        self.main_table_view.setModel(table_model)
        self.main_table_view.resizeColumnsToContents()
        #self.main_table_view.sortByColumn("Priority")

        

class main_table_view_model(QAbstractTableModel):
    def __init__(self,table_data_lists,headers,rows,columns,_table):
        super().__init__()
        self._Table = _table
        self._Headers = headers
        self._Records = table_data_lists
        self._Rows = rows
        self._Columns = columns

    def rowCount(self,parent):
        return self._Rows

    def columnCount(self,parent):
        return self._Columns

    def data(self,index,role):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self._Records[row][column]
            return value

    def flags(self,index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self,index,value,role = Qt.EditRole):
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            foreign_id_check = self._Headers[column]
            _table = self._Table
            if len(value) == 0:
                error_message_dialog = QErrorMessage()
                error_message_dialog.setWindowTitle("Error")
                error_message_dialog.showMessage("Cannot be Null")
                error_message_dialog.exec_()
                return False
            elif len(value) > 23:
                error_message_dialog = QErrorMessage()
                error_message_dialog.setWindowTitle("Error")
                error_message_dialog.showMessage("Value must be less than 24 characters.")
                error_message_dialog.exec_()
                return False
            elif foreign_id_check == ("{0}ID".format(_table)):
                error_message_dialog = QErrorMessage()
                error_message_dialog.setWindowTitle("Error")
                error_message_dialog.showMessage("Referential error - Cannot edit Record ID")
                error_message_dialog.exec_()
                return False
            elif foreign_id_check[-2:] == 'ID':
                id_not_name = True
                try:
                    value = int(value)
                except:
                    id_not_name = False
                foreign_table = foreign_id_check[:-2]
                row = row + 1
                if id_not_name:
                    if _table == "Company":
                        results = select_all_from_company()
                    elif _table == "Client":
                        results = select_all_from_client()
                    elif _table == "Project":
                        results = select_all_from_project()
                    elif _table == "Task":
                        results = select_all_from_task()
                    elif _table == "TaskManager":
                        results = select_all_from_taskmanager()
                    elif _table == "TechnicalArea":
                        results = select_all_from_technicalarea()

                    id_check = []
                    for item in results:
                        id_check.append(item[0])

                    if value not in id_check:
                        error_message_dialog = QErrorMessage()
                        error_message_dialog.setWindowTitle("Error")
                        error_message_dialog.showMessage("Referential error - ID '{0}' not not found in table '{1}'. ".format(value,_table))
                        error_message_dialog.exec_()
                        return False
                    else:
                        column = self._Headers[column]
                        foreign_column = None
                        automatic_update_one_for_table_id(id_not_name,row,column,foreign_column,value,_table,foreign_table)
                        row = index.row()
                        column = index.column()
                        self._Records[row][column] = value
                        window.main_status_bar.showMessage("Database updated successfully")
                        window.update_components()
                        self.dataChanged.emit(index,index)
                        return True
                else:
                    column = self._Headers[column]
                    foreign_column = (column[:-2]+"Name")
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
                        
                    valid_check = []
                    for item in results:
                        valid_check.append(item[1])

                    if value not in valid_check:
                        error_message_dialog = QErrorMessage()
                        error_message_dialog.setWindowTitle("Error")
                        error_message_dialog.showMessage("Referential error - '{0}' not not found in table '{1}'. ".format(value,foreign_table))
                        error_message_dialog.exec_()
                        return False
                    else:
                        column = index.column()
                        column = self._Headers[column]
                        foreign_column = None
                        automatic_update_one_for_table_id(id_not_name,row,column,foreign_column,value,_table,foreign_table)
                        column = index.column()
                        row = index.row()
                        self._Records[row][column] = value
                        window.main_status_bar.showMessage("Database updated successfully")
                        window.update_components()
                        self.dataChanged.emit(index,index)
                        return True

            elif len(value) <= 23:
                self._Records[row][column] = value
                row = row + 1
                column = self._Headers[column]
                automatic_update_one_for_table(row,column,value,_table)
                window.main_status_bar.showMessage("Database updated successfully")
                window.update_components()
                self.dataChanged.emit(index,index)
                return True

    def headerData(self,section,orientation,role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._Headers[section]

    

class main_list_view_model(QAbstractListModel):
    def __init__(self,projects):
        super().__init__()
        self._Projects = projects
        self._Selected = 'All'

        self._Projects.clicked.connect(self.onItemSelect)

    def rowCount(self,parent):
        return len(self._Projects)

    def data(self,index,role):
        if role == Qt.DisplayRole:
            row = index.row()
            value = self._Projects[row]
            return value
        
    def flags(self,index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def setData(self,index,value,role):
        if role == Qt.EditRole:
            row = index.row()
            if self._Projects[row] == "All":
                error_message_dialog = QErrorMessage()
                error_message_dialog.setWindowTitle("Error")
                error_message_dialog.showMessage("Cannot edit 'All'.")
                error_message_dialog.exec_()
                return False
            elif len(value) == 0:
                error_message_dialog = QErrorMessage()
                error_message_dialog.setWindowTitle("Error")
                error_message_dialog.showMessage("Cannot be Null")
                error_message_dialog.exec_()
                return False
            elif len(value) <= 23:
                self._Projects[row] = value
                automatic_update_one_for_project(row,value)
                window.main_status_bar.showMessage("Database updated successfully")
                window.update_components()
                self.dataChanged.emit(index,index)
                return True
            else:
                error_message_dialog = QErrorMessage()
                error_message_dialog.setWindowTitle("Error")
                error_message_dialog.showMessage("Value must be less than 24 characters.")
                error_message_dialog.exec_()
                return False
            
        def onItemSelect(self):
            test = self.main_list_view.selectedIndexes()
            print(test)
        
if __name__ == "__main__":
    
    #initialise_database()
    application = QApplication(sys.argv)
    window = TaskManagerMainGUI()
    window.show()
    window.raise_()
    application.exec_()
