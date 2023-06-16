from PyQt5.QtWidgets import *
import requests
import json
import random



API = "http://127.0.0.1:8000"
ACCESS_TOKEN = None
REFRESH_TOKEN = None
RFID = ''


def getDaMoneyBock(endpoint):
    

    response = requests.get(API+"/"+endpoint)

    if response.status_code == 200:
        result = response.json()  
        return result
    else:
        print('Error:', response.status_code)
print(getDaMoneyBock("moneyboxes"))
MoneyMoneyMoney = getDaMoneyBock("moneyboxes")
print(getDaMoneyBock("moneyboxes"))
list = []
for item in MoneyMoneyMoney:
    list.append((str(item['RFID'])))

random_index = random.randint(0, len(list) - 1)
RFID = list[random_index]
print(RFID)




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

def getReq(endpoint, headers):
    
    if headers == True:
        headers = {
            "authorization" : "Bearer "+ ACCESS_TOKEN, 
            "accept": "application/json"

        }
    response = requests.get(API+"/"+endpoint, headers=headers)

    if response.status_code == 200:
        result = response.json()  
        return result
    else:
        print('Error:', response.status_code)


def putReq(data, endpoint, headers):
    
    if headers == True:
        headers = {
            "authorization" : "Bearer "+ ACCESS_TOKEN, 
            "accept": "application/json"

        }
    response = requests.put(API+"/"+endpoint, data=data, headers=headers)

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
statusValue = ""

currentStatusDropDownBox = QComboBox()
updateLocationDropDownBox = QComboBox()
inTransitToDropDownBox = QComboBox()

loginButton = QPushButton('Login')
scanButton = QPushButton('Scan')
submitButton = QPushButton('Submit')
changeStatusToIn = QPushButton('In')
changeStatusToOut = QPushButton('Out')
optionsDropDownBox = QComboBox()
anotherButton = QPushButton('Submit')

amountField = QLineEdit()


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
        global ACCESS_TOKEN 
        ACCESS_TOKEN = tokens["access_token"]
        global REFRESH_TOKEN 
        REFRESH_TOKEN = tokens["refresh_token"]
        
        removeWidgets()
        layout.addWidget(scanButton)
    
def updateLocation(index):
    global currentLocation
    currentLocation = updateLocationDropDownBox.itemText(index)

def removeWidgets():
    for i in reversed(range(layout.count())): 
        widgetToRemove = layout.itemAt(i).widget()
        
        layout.removeWidget(widgetToRemove)
        
        widgetToRemove.setParent(None)

def submitButtonClicked():
    if moneybox['current_location'] != '4':

        data = {
        
            "location_id" : optionsDropDownBox.currentText().split(', ')[1],
            "location_status" : statusValue
        }
        print(data)
        updateInfo = putReq(json.dumps(data), "location/"+RFID,True)
        removeWidgets()
        layout.addWidget(scanButton)

    else:
        isCounting()


def isCounting():
    removeWidgets()
    layout.addWidget(QLabel("Enter Counted Amount: "))
    layout.addWidget(amountField)
    layout.addWidget(anotherButton)
def scanButtonClicked():
    global moneybox
    moneybox = getReq("scan/"+RFID,True)
    removeWidgets()
    moneyBoxStatusLabel = QLabel(moneybox['location_status'] + " " + moneybox['current_location'])
    layout.addWidget(moneyBoxStatusLabel)
    
    optionsReq = getReq("locations", True)
    optionsDropDownBox.clear()
    for item in optionsReq:
        optionsDropDownBox.addItem((str(item['location_name']) + ", " + str(item['location_id'])))

    layout.addWidget(changeStatusToIn)
    layout.addWidget(changeStatusToOut)
    layout.addWidget(optionsDropDownBox)
    layout.addWidget(submitButton)

def toOutClicked():
    global statusValue
    statusValue = "out"

def toInClicked():
    global statusValue
    statusValue = "in"

def anotherButtonClicked():
    dataForCount = {
        "value_at_end": amountField.text()
    }
    print(dataForCount)
    putReq(json.dumps(dataForCount), "count/"+RFID,True)
    removeWidgets()
    layout.addWidget(scanButton)



    

loginButton.clicked.connect(login)
scanButton.clicked.connect(scanButtonClicked)
anotherButton.clicked.connect(anotherButtonClicked)
submitButton.clicked.connect(submitButtonClicked)
changeStatusToOut.clicked.connect(toOutClicked)
changeStatusToIn.clicked.connect(toInClicked)
updateLocationDropDownBox.currentIndexChanged.connect(updateLocation)

app.exec_()
