from PyQt5.QtWidgets import *
app = QApplication([])

app.setStyleSheet("""
    QPushButton {
        background-color: #2a2a2a;
        color: #ffffff;
    }
    QPushButton:hover {
        background-color: #404040;
    }
""")


app.setStyle('Fusion')

Window = QWidget()
layout = QVBoxLayout()

username_line = QLineEdit('Username')
password_line = QLineEdit('Password')

layout.addWidget(username_line)
layout.addWidget(password_line)

currentStatusDropDownBox = QComboBox()
updateLocationDropDownBox = QComboBox()
inTransitToDropDownBox = QComboBox()

loginButton = QPushButton('Login')
scanButton = QPushButton('Scan')
submitButton = QPushButton('Submit')
nextButton = QPushButton('Next')

currentStatus = "" #fetched from API
currentLocation = "" #fetched from API

inTransitFromLabel = QLabel(currentLocation)
loginMessage = QLabel('Logged in as Guard#420')
setStatusMessage = QLabel('Set Status: ')


layout.addWidget(loginButton)
Window.setLayout(layout)
Window.setFixedSize(250, 250)
Window.show()

def login():
    removeWidgets()
    layout.addWidget(loginMessage)
    layout.addWidget(scanButton)
    layout.addWidget(setStatusMessage)
    layout.addWidget(currentStatusDropDownBox)
    createStatusDropDown()
    layout.addWidget(nextButton)

def createStatusDropDown():
    # will always be these values
    currentStatusDropDownBox.addItems(['Table', 'Safe', 'Truck', 'Bank', 'In Transit', 'Counting', 'Ready For Job'])

def createInTransitDropDown():
    # will fetch data from API and add options of all available locations
    # will prefill from location as current location of box
    if(inTransitFromLabel.text() == 'Safe'):
        inTransitToDropDownBox.clear()
        inTransitToDropDownBox.addItems(['Truck 1', 'Truck 2', 'Truck 3'])
    elif(inTransitFromLabel.text() == 'Truck'):
        inTransitToDropDownBox.clear()
        inTransitToDropDownBox.addItems(['Bank 1', 'Bank 2', 'Bank 3'])
    elif(inTransitFromLabel.text() == 'Bank'):
        inTransitToDropDownBox.clear()
        inTransitToDropDownBox.addItem('Counting')
    elif(inTransitFromLabel.text() == 'Counting'):
        inTransitToDropDownBox.clear()
        inTransitToDropDownBox.addItem('Ready For Job')
    elif(inTransitFromLabel.text() == 'Ready For Job'):
        inTransitToDropDownBox.clear()
        inTransitToDropDownBox.addItems(['Table 1', 'Table 2', 'Table 3'])
    elif(inTransitFromLabel.text() == 'Table'):
        inTransitToDropDownBox.clear()
        inTransitToDropDownBox.addItems(['Safe 1', 'Safe 2', 'Safe 3'])

def createUpdateLocationDropDown():
    if(currentStatusDropDownBox.currentText() == 'Safe'):
        updateLocationDropDownBox.clear()
        updateLocationDropDownBox.addItems(['Truck 1', 'Truck 2', 'Truck 3'])
    elif(currentStatusDropDownBox.currentText() == 'Truck'):
        updateLocationDropDownBox.clear()
        updateLocationDropDownBox.addItems(['Bank 1', 'Bank 2', 'Bank 3'])
    elif(currentStatusDropDownBox.currentText() == 'Bank'):
        updateLocationDropDownBox.clear()
        updateLocationDropDownBox.addItem('Counting')
    elif(currentStatusDropDownBox.currentText()  == 'Counting'):
        updateLocationDropDownBox.clear()
        updateLocationDropDownBox.addItem('Ready For Job')
    elif(currentStatusDropDownBox.currentText()  == 'Ready For Job'):
        updateLocationDropDownBox.clear()
        updateLocationDropDownBox.addItems(['Table 1', 'Table 2', 'Table 3'])
    elif(currentStatusDropDownBox.currentText()  == 'Table'):
        updateLocationDropDownBox.clear()
        updateLocationDropDownBox.addItems(['Safe 1', 'Safe 2', 'Safe 3'])

def checkData():
    if(currentStatusDropDownBox.currentText() == 'In Transit'):
        layout.addWidget(QLabel('From: '))
        layout.addWidget(inTransitFromLabel)
        layout.addWidget(QLabel('To: '))
        createInTransitDropDown()
        layout.addWidget(inTransitToDropDownBox)
        layout.addWidget(updateLocationDropDownBox)
    elif(currentStatusDropDownBox.currentText() == 'Counting'):
        layout.addWidget(QLabel('Amount: '))
        layout.addWidget(QTextEdit())
        
    
def updateLocation(index):
    global currentLocation
    currentLocation = updateLocationDropDownBox.itemText(index)

def nextButtonClicked():
    checkData()
    createUpdateLocationDropDown()
    layout.addWidget(updateLocationDropDownBox)
    layout.addWidget(submitButton)

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
    layout.addWidget(setStatusMessage)
    layout.addWidget(currentStatusDropDownBox)
    layout.addWidget(nextButton)


def updateStatus(index):
    global currentLocation
    currentLocation = currentStatusDropDownBox.itemText(index)

loginButton.clicked.connect(login)
nextButton.clicked.connect(nextButtonClicked)
submitButton.clicked.connect(submitButtonClicked)
updateLocationDropDownBox.currentIndexChanged.connect(updateLocation)
currentStatusDropDownBox.currentIndexChanged.connect(updateStatus)

app.exec_()
