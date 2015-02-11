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
        self.insert_data = QAction("Insert Data",self)
        self.update_data = QAction("Update Data",self)
        self.delete_data = QAction("Delete Data",self)

        #create bars
        self.main_tool_bar_1 = QToolBar()
        self.main_menu_bar = QMenuBar()
        self.main_status_bar = QStatusBar()

        #add actions to toolbar
        self.main_tool_bar_1.addAction(self.insert_data)
        self.main_tool_bar_1.addAction(self.update_data)
        self.main_tool_bar_1.addAction(self.delete_data)

        #add actions to menubars
        self.database_menu = self.main_menu_bar.addMenu("Database")
        self.database_menu.addAction(self.insert_data)
        self.database_menu.addAction(self.update_data)
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
        self.main_layout.addWidget(self.main_list_view,0,0)
        self.main_layout.addWidget(self.main_table_view,0,1)
        self.main_layout.addWidget(self.details_widget,0,2)
        #create widget to hold layout
        self.main_widget = QWidget()
        #add layout to widget
        self.main_widget.setLayout(self.main_layout)

        self.update_components()

    def update_components(self):
        self.update_main_list()
        self.update_main_table()
        
    def update_main_list(self):
        results = select_all_from_project()
        projects = []
        for item in results:
            projects.append(item[1])
        list_model = main_list_view_model(projects)
        self.main_list_view.setModel(list_model)

    def update_main_table(self):
        #display all tasks as default
        results = select_all_from_task()

class main_table_view_model(QAbstractTableModel):
    def __init__(self):
        super().__init__()

class main_list_view_model(QAbstractListModel):
    def __init__(self,projects):
        super().__init__()
        self._Projects = projects

    def rowCount(self,parent):
        return len(self._Projects)

    def data(self,index,role):
        if role == Qt.DisplayRole:
            row = index.row()
            value = self._Projects[row]
            return value
        
##    def flags(self,index):
##        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
##
##    def setData(self,index,value,role = Qt.EditRole):
##        if role == Qt.EditRole:
##            row = index.row()
##            
##            update_one_for_Table(row,"Project")
##            self.dataChanged.emit(index,index)
        
if __name__ == "__main__":
    application = QApplication(sys.argv)
    window = TaskManagerMainGUI()
    window.show()
    window.raise_()
    application.exec_()
