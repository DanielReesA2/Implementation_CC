from Manage_Database import *
import sqlite3
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class TaskManagerMainGUI(QMainWindow):
    """Main window for task manager program"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")

        #database file related attributes
        self.database_opened = False
        self.database_path = None

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
        self.open_database = QAction("Open Database",self)
        self.close_database = QAction("Close Database",self)
        self.insert_data = QAction("Insert Data",self)
        self.update_data = QAction("Update Data",self)
        self.delete_data = QAction("Delete Data",self)

        #create bars
        self.main_tool_bar_1 = QToolBar()
        self.main_tool_bar_2 = QToolBar()
        self.main_menu_bar = QMenuBar()
        self.main_status_bar = QStatusBar()

        #add actions to toolbar
        self.main_tool_bar_2.addAction(self.open_database)
        self.main_tool_bar_2.addAction(self.close_database)
        self.main_tool_bar_1.addAction(self.insert_data)
        self.main_tool_bar_1.addAction(self.update_data)
        self.main_tool_bar_1.addAction(self.delete_data)

        #add actions to menubars
        self.database_menu = self.main_menu_bar.addMenu("Database")
        self.database_menu.addAction(self.open_database)
        self.database_menu.addAction(self.close_database)
        self.database_menu.addAction(self.insert_data)
        self.database_menu.addAction(self.update_data)
        self.database_menu.addAction(self.delete_data)
        
        #add message to statusbar
        self.main_status_bar.showMessage("Task Manager ver1.0")

        #add bars to mainwindow
        self.addToolBar(self.main_tool_bar_1)
        self.addToolBar(self.main_tool_bar_2)
        self.setMenuBar(self.main_menu_bar)
        self.setStatusBar(self.main_status_bar)

        #set window size/position
        self.resize(700,500)
        self.move(100,100)

        #connections
        self.open_database.triggered.connect(self._open_database)

    def _open_database(self):
        file_name = QFileDialog.getOpenFileName()
        print("{0} Opened".format(file_name))
        self.main_status_bar.showMessage("{0} Opened".format(file_name))
        self.database_opened = True
        self.database_path = file_name
        self.update_main_table()

    def CreateMainWindow(self):
        #components
        self.main_tree_view = QTreeView()
        self.main_table_view = QTableView()
        self.label1 = QLabel("""Details:""")
        self.test = QPushButton("""TEST""")                
        #define layout
        self.main_layout = QGridLayout()
        self.details_layout = QVBoxLayout()
        #define spacings for columns
        self.main_layout.setColumnStretch(0,0)
        self.main_layout.setColumnStretch(1,10)
        self.main_layout.setColumnStretch(2,5)      
        #add details to details widget
        self.details_layout.addWidget(self.label1)
        self.details_layout.addWidget(self.test)
        #create widget to hold details
        self.details_widget = QWidget()
        #add details layout to details widget
        self.details_widget.setLayout(self.details_layout)
        #add components to layout
        self.main_layout.addWidget(self.main_tree_view,0,0)
        self.main_layout.addWidget(self.main_table_view,0,1)
        self.main_layout.addWidget(self.details_widget,0,2)
        #create widget to hold layout
        self.main_widget = QWidget()
        #add layout to widget
        self.main_widget.setLayout(self.main_layout)

        self.update_main_table()

    def update_main_table(self):
        if self.database_opened:
            

##            with sqlite3.connect("Task_Manager_Database.db") as db:
##                cursor = db.cursor()
##                cursor.execute("pragma table_info(Task)")
##                results = cursor.fetchall()
##                
##            horHeaders = []
##            for item in results:
##                horHeaders.append(item[1])
##            self.main_table_widget.setHorizontalHeaderLabels(horHeaders)
##        
##            with sqlite3.connect(self.database_path) as db:
##                cursor = db.cursor()
##                cursor.execute("""select a.TaskID,a.TaskName,a.DueDate,a.Priority,b.TechnicalAreaName,d.ProjectName,c.TaskManagerName
##from Task a
##join TechnicalArea b 
##on a.TechnicalAreaID = b.TechnicalAreaID
##join TaskManager c
##on a.TaskManagerID = c.TaskManagerID
##join Project d
##on a.ProjectID = d.ProjectID""")
##                data = cursor.fetchall()
##
##                for item in data:
##                    row = 0
##                    for item2 in item:
##                        column = 0
##                        new_item = QTableWidgetItem(item2)
##                        self.main_table_widget.setItem(column,row,new_item)
##                        column = column + 1
##                    row = row + 1
                        

        
        
if __name__ == "__main__":
    application = QApplication(sys.argv)
    window = TaskManagerMainGUI()
    window.show()
    window.raise_()
    application.exec_()
