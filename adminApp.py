from PyQt5.QtWidgets import *
app = QApplication([])

app.setStyleSheet("""
    QPushButton {
        background-color: #2a2a2a;
        color: #ffffff;
        font-family: Arial;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #404040;
    }
    QLabel, QLineEdit, QComboBox, QTextEdit {
        font-family: Arial;
        font-size: 14px;
    }
    QLabel {
        font-weight: bold;
    }
""")


app.setStyle('Fusion')

Window = QWidget()
layout = QVBoxLayout()

tab_widget = QTabWidget()
tab1 = QWidget()
tab2 = QWidget()
tab3 = QWidget()
tab_widget.addTab(tab1, "Scan")
tab_widget.addTab(tab2, "Stocktake")
tab_widget.addTab(tab3, "Logs")
tab1.layout = QVBoxLayout()
tab1.setLayout(tab1.layout)
tab2.layout = QVBoxLayout()
tab2.setLayout(tab2.layout)
tab3.layout = QVBoxLayout()
tab3.setLayout(tab3.layout) 

username_line = QLineEdit()
username_line.setPlaceholderText('Enter Username')

password_line = QLineEdit()
password_line.setPlaceholderText('Enter Password')


layout.addWidget(username_line)
layout.addWidget(password_line)

updateLocationDropDownBox = QComboBox()
inTransitToDropDownBox = QComboBox()
boxIdDropDownBox = QComboBox()

loginButton = QPushButton('Login')
scanButton = QPushButton('Scan')
submitButton = QPushButton('Submit')
searchButton = QPushButton('Search')

currentStatus = "Safe" #fetched from API
currentLocation = "" #fetched from API

inTransitFromLabel = QLabel(currentStatus)
loginMessage = QLabel('Logged in as Admin')


layout.addWidget(loginButton)
Window.setLayout(layout)
Window.setFixedSize(1920, 1080)
Window.show()
tab2.layout.addWidget(QLabel('Select Box To Query:'))
tab2.layout.addWidget(boxIdDropDownBox)
tab2.layout.addWidget(searchButton)


def createboxIdDropDown():
    # will fetch all boxes from API
    boxIdDropDownBox.addItems(['1','2','3'])

createboxIdDropDown()
def login():
    removeWidgets()
    layout.addWidget(tab_widget)
    tab1.layout.addWidget(loginMessage)
    tab1.layout.addWidget(loginMessage)
    tab1.layout.addWidget(scanButton)

def createInTransitDropDown():
    # will fetch data from API and add options of all available locations
    # will prefill from location as current location of box
    if(inTransitFromLabel.text() == 'Ready For Job'):
        inTransitToDropDownBox.clear()
        inTransitToDropDownBox.addItems(['Table 1', 'Table 2', 'Table 3'])
    elif(inTransitFromLabel.text() == 'Idle'):
        inTransitToDropDownBox.clear()
        inTransitToDropDownBox.addItem('Ready For Job')

def createUpdateLocationDropDown():
    if(currentStatus  == 'Ready For Job'):
        updateLocationDropDownBox.clear()
        updateLocationDropDownBox.addItems(['Table 1', 'Table 2', 'Table 3'])
    elif(inTransitFromLabel.text() == 'Idle'):
        inTransitToDropDownBox.clear()
        inTransitToDropDownBox.addItem('Ready For Job')

def checkData():
    if(currentStatus == 'In Transit'):
        layout.addWidget(QLabel('From: '))
        layout.addWidget(inTransitFromLabel)
        layout.addWidget(QLabel('To: '))
        layout.addWidget(inTransitToDropDownBox)
        createInTransitDropDown()
        layout.addWidget(submitButton)
    elif(currentStatus == 'Counting'):
        layout.addWidget(QLabel('Amount: '))
        layout.addWidget(QTextEdit())
        layout.addWidget(submitButton)
        
    
def updateLocation(index):
    global currentLocation
    currentLocation = updateLocationDropDownBox.itemText(index)

def removeWidgets():
    for i in reversed(range(layout.count())): 
        widgetToRemove = layout.itemAt(i).widget()
        
        layout.removeWidget(widgetToRemove)
        
        widgetToRemove.setParent(None)

def submitButtonClicked():
    #Sends updatedStatus and UpdatedLocation + Amount if applicable to API
    removeWidgets()
    layout.addWidget(loginMessage)
    layout.addWidget(scanButton)


loginButton.clicked.connect(login)
submitButton.clicked.connect(submitButtonClicked)
updateLocationDropDownBox.currentIndexChanged.connect(updateLocation)

app.exec_()
