from Manage_Database import *
import sys
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
        self.main_tool_bar = QToolBar()
        self.main_menu_bar = QMenuBar()
        self.main_status_bar = QStatusBar()

        #add actions to toolbar
        self.main_tool_bar.addAction(self.insert_data)
        self.main_tool_bar.addAction(self.update_data)
        self.main_tool_bar.addAction(self.delete_data)

        #add actions to menubars
        self.database_menu = self.main_menu_bar.addMenu("Database")
        self.database_menu.addAction(self.insert_data)
        self.database_menu.addAction(self.update_data)
        self.database_menu.addAction(self.delete_data)
        
        #add message to statusbar
        self.main_status_bar.showMessage("Task Manager ver1.0")

        #add bars to mainwindow
        self.addToolBar(self.main_tool_bar)
        self.setMenuBar(self.main_menu_bar)
        self.setStatusBar(self.main_status_bar)

        #set window size/position
        self.resize(700,500)
        self.move(100,100)

    def CreateMainWindow(self):
        #components
        self.main_tree_view = QTreeView()
        self.main_table = QTableView()
        self.label1 = QLabel("""Details:""")
        self.test = QPushButton("""TEST""")

        #treeview functions
        self.
        self.main_tree_view.setHeader()        
        
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
        self.main_layout.addWidget(self.main_table,0,1)
        self.main_layout.addWidget(self.details_widget,0,2)
        #create widget to hold layout
        self.main_widget = QWidget()
        #add layout to widget
        self.main_widget.setLayout(self.main_layout)
        
if __name__ == "__main__":
    application = QApplication(sys.argv)
    window = TaskManagerMainGUI()
    window.show()
    window.raise_()
    application.exec_()
