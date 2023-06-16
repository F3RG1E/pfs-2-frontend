from PyQt5.QtWidgets import *
import requests


API = "http://127.0.0.1:8000"
ACCESS_TOKEN = None
REFRESH_TOKEN = None


# Make a POST request to the API
def postReq(data, endpoint, headers):
    
    if headers == True:
        headers = {
            "authorization" : "Bearer "+ ACCESS_TOKEN, 
            "accept": "application/json"

        }
    response = requests.post(API+"/"+endpoint, data=data, headers=headers)

    if response.status_code == 200:
        result = response.json()  
        return result
    else:
        print('Error:', response.status_code)


app = QApplication([])

app.setStyleSheet("""
    QPushButton {
        background-color: #337ab7;
        color: #ffffff;
        padding: 10px;
        font-size: 16px;
        font-weight: bold;
        border: none;
    }
    QPushButton:hover {
        background-color: #23527c;
    }
    QLabel, QLineEdit, QComboBox, QTextEdit {
        background-color: #ffffff;
            border: 1px solid #cccccc;
            padding: 6px;
            font-size: 16px;
            color: #333333;
    }
    QLabel {
        font-weight: bold;
    }
    QMainWindow {
            background-color: #f2f2f2;
        }
""")


app.setStyle('Fusion')

Window = QWidget()
layout = QVBoxLayout()

username_line = QLineEdit()
username_line.setPlaceholderText('Enter Username')

password_line = QLineEdit()
password_line.setPlaceholderText('Enter Password')


layout.addWidget(username_line)
layout.addWidget(password_line)

currentStatusDropDownBox = QComboBox()
updateLocationDropDownBox = QComboBox()
inTransitToDropDownBox = QComboBox()

loginButton = QPushButton('Login')
scanButton = QPushButton('Scan')
submitButton = QPushButton('Submit')
nextButton = QPushButton('Next')

currentStatus = "Safe" #fetched from API
currentLocation = "" #fetched from API

inTransitFromLabel = QLabel(currentStatus)
setStatusMessage = QLabel('Set Status: ')


layout.addWidget(loginButton)
Window.setLayout(layout)
Window.setFixedSize(320, 570)
Window.show()
wrongDeats = QLabel("You must Enter Values")

def login():
    if(username_line.text() == "" or password_line.text() == ""):
        layout.addWidget(wrongDeats)
    else:
        layout.removeWidget(wrongDeats)
        data = {
            'username': username_line.text(),
            'password': password_line.text()
        }

        tokens = postReq(data, "login", False)
        ACCESS_TOKEN = tokens["access_token"]
        REFRESH_TOKEN = tokens["refresh_token"]
        
        removeWidgets()
        layout.addWidget(scanButton)

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

def nextButtonClicked():
    checkData()
    if(currentStatus == 'In Transit' or currentStatus == 'Counting'):
        pass
    else:
        layout.addWidget(QLabel('Set Location: '))
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
    layout.addWidget(scanButton)

loginButton.clicked.connect(login)
nextButton.clicked.connect(nextButtonClicked)
submitButton.clicked.connect(submitButtonClicked)
updateLocationDropDownBox.currentIndexChanged.connect(updateLocation)

app.exec_()
