from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QClipboard
import requests
import re
import json
app = QApplication([])


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

# Make a GET request to the API
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
tab4 = QWidget()
tab5 = QWidget()
tab6 = QWidget()
tab7 = QWidget()
tab_widget.addTab(tab1, "Scan")
tab_widget.addTab(tab2, "Users")
tab_widget.addTab(tab3, "Logs")
tab_widget.addTab(tab4, "Alerts")
tab_widget.addTab(tab7, "MoneyBoxes")
tab_widget.addTab(tab5, "Create box")
tab_widget.addTab(tab6, "Jobs")
tab1.layout = QVBoxLayout()
tab1.setLayout(tab1.layout)
tab2.layout = QVBoxLayout()
tab2.setLayout(tab2.layout)
tab3.layout = QVBoxLayout()
tab3.setLayout(tab3.layout)
tab4.layout = QVBoxLayout()
tab4.setLayout(tab4.layout)
tab5.layout = QVBoxLayout()
tab5.setLayout(tab5.layout)
tab6.layout = QVBoxLayout()
tab6.setLayout(tab6.layout)
tab7.layout = QVBoxLayout()
tab7.setLayout(tab7.layout)

username_line = QLineEdit()
username_line.setPlaceholderText('Enter Username')

password_line = QLineEdit()
password_line.setPlaceholderText('Enter Password')
password_line.setEchoMode(QLineEdit.Password)


layout.addWidget(username_line)
layout.addWidget(password_line)

updateLocationDropDownBox = QComboBox()
inTransitToDropDownBox = QComboBox()
boxIdDropDownBox = QComboBox()

loginButton = QPushButton('Login')
scanButton = QPushButton('Scan')
submitButton = QPushButton('Submit')
searchButton = QPushButton('Search')

loginMessage = QLabel('Logged in as Admin')


layout.addWidget(loginButton)
Window.setLayout(layout)
Window.setFixedSize(1280, 720)
Window.show()

# boxes tab
boxes_table = None

def search_location_by_id(data, location_id):
    for location in data:
        if location['location_id'] == location_id:
            return location['location_name']+location['location_id']
        elif location_id=="1":
            return "idle"
        elif location_id=="2":
            return "ready"
    return "Null"

def get_boxes_data():
    global boxes_table
    if boxes_table is None:
        boxes_table = QTableWidget()
        tab7.layout.addWidget(boxes_table)
    boxes_table.clear()

    records = getReq("moneyboxes", True)
    if records is None:
        return

    boxes_table.setRowCount(len(records))
    boxes_table.setColumnCount(len(records[0]))

    headers = list(records[0].keys())
    boxes_table.setHorizontalHeaderLabels(headers)

    location_names = getReq("locations", True)

    for row, record in enumerate(records):
        for col, value in enumerate(record.values()):
            if col == 1:  # Assuming 'current_location' is always at index 1
                location_name= search_location_by_id(location_names,value)
                item = QTableWidgetItem(str(location_name))
            else:
                item = QTableWidgetItem(str(value))
            boxes_table.setItem(row, col, item)
    boxes_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    tab7.layout.addWidget(boxes_table)
    
    boxes_table.cellClicked.connect(copy_cell_value_to_clipboard)

def copy_cell_value_to_clipboard(row, column):
    if column != 0:
        return
    item = boxes_table.item(row, column)
    if item is not None:
        value = item.text()
        clipboard = QApplication.clipboard()
        clipboard.setText(value)
        
get_boxes_button = QPushButton('Get Boxes')
tab7.layout.addWidget(get_boxes_button)
get_boxes_button.clicked.connect(lambda: get_boxes_data())


# jobs tab
create_job_button = QPushButton('Create Job')
tab6.layout.addWidget(QLabel('RFID of box:'))
rfid_input = QLineEdit()
spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
tab6.layout.addWidget(rfid_input)
tab6.layout.addWidget(create_job_button)
tab6.layout.addItem(spacer)

def create_job(RFID):
        records = postReq({},"create/job/"+RFID,True)
        if records is None:
            jobs_result_label = QLabel('Job failed to create.')
            jobs_result_label.setStyleSheet('color: red;')
            tab6.layout.addWidget(jobs_result_label)
            return
        else:
            jobs_result_label = QLabel('Job created successfully. This box is ready to be placed into a table.')
            jobs_result_label.setStyleSheet('color: green;')
            tab6.layout.addWidget(jobs_result_label)

create_job_button.clicked.connect(lambda: create_job(rfid_input.text()))


# moneybox tab
create_moneybox_button = QPushButton('Create MoneyBox')
tab5.layout.addWidget(create_moneybox_button)
moneybox_result_label = QLabel()
moneybox_rfid_label = QLabel()

def create_moneybox():
    response = postReq(json.dumps({}), 'create/box', True)

    if response is not None:
        moneybox_rfid_label.setText("RFID value of the new box: "+response["RFID"])
        moneybox_rfid_label.setTextInteractionFlags(Qt.TextSelectableByMouse) 
        moneybox_result_label.setText('Moneybox created successfully.')
        moneybox_result_label.setStyleSheet('color: green;')
    else:
        moneybox_result_label.setText('Failed to create Moneybox.')
        moneybox_result_label.setStyleSheet('color: red;')

create_moneybox_button.clicked.connect(create_moneybox)

tab5.layout.addWidget(moneybox_result_label)
tab5.layout.addWidget(moneybox_rfid_label)


# users tab
create_user_button = QPushButton('Create User')
tab2.layout.addWidget(QLabel('Username:'))
username_input = QLineEdit()
tab2.layout.addWidget(username_input)
tab2.layout.addWidget(QLabel('Password:'))
password_input = QLineEdit()
password_input.setEchoMode(QLineEdit.Password)
tab2.layout.addWidget(password_input)
tab2.layout.addWidget(QLabel('Role:'))
role_dropdown = QComboBox()
role_dropdown.addItems(['guard', 'admin'])
tab2.layout.addWidget(role_dropdown)
tab2.layout.addWidget(create_user_button)

users_result_label = QLabel()

def create_user():
    username = username_input.text()
    password = password_input.text()
    role = role_dropdown.currentText()

    data = {
        "username": username,
        "password": password,
        "role": role
    }
    if len(password) < 5:
        users_result_label.setText('Password must be at least 5 characters long.')
        users_result_label.setStyleSheet('color: red;')
        return

    response = postReq(json.dumps(data), 'signup', True)

    if response is not None:
        users_result_label.setText('User created successfully.')
        users_result_label.setStyleSheet('color: green;')
    else:
        users_result_label.setText('Failed to create user.')
        users_result_label.setStyleSheet('color: red;')

create_user_button.clicked.connect(create_user)

tab2.layout.addWidget(users_result_label)

# Logs tab
logs_table = None
invalid_job_id_label = None

def get_log_data(job_id):
    pattern = r'^[1-9]\d*$'
    if re.match(pattern, job_id) is not None:
        global logs_table
        if logs_table is None:
            logs_table = QTableWidget()
            tab3.layout.addWidget(logs_table)
        logs_table.clear()
        
        global invalid_job_id_label
        if invalid_job_id_label is not None:
            tab3.layout.removeWidget(invalid_job_id_label)
            invalid_job_id_label.setParent(None)
            invalid_job_id_label = None

        records = postReq({},"logs/"+job_id,True)
        if records is None:
            invalid_job_id_label = QLabel('Invalid job ID')
            invalid_job_id_label.setStyleSheet('color: red;')
            tab3.layout.addWidget(invalid_job_id_label)
            logs_table.clear()
            return
        
        logs_table.setRowCount(len(records))
        logs_table.setColumnCount(len(records[0]))

        headers = list(records[0].keys())
        logs_table.setHorizontalHeaderLabels(headers)

        for row, record in enumerate(records):
            for col, value in enumerate(record.values()):
                item = QTableWidgetItem(str(value))
                logs_table.setItem(row, col, item)
        #logs_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        logs_table.setColumnWidth(1, 400)
        logs_table.setColumnWidth(2, 160)
        logs_table.setColumnWidth(3, 160)
        logs_table.setColumnWidth(4, 200)
        logs_table.setColumnWidth(5, 200)
        tab3.layout.addWidget(logs_table)
    else:
        job_id_input.setPlaceholderText('Job ID Invalid')
        
search_logs_button = QPushButton('Search Logs')
job_id_input = QLineEdit()
job_id_input.setPlaceholderText('Enter Job ID')
tab3.layout.addWidget(job_id_input)
tab3.layout.addWidget(search_logs_button)
search_logs_button.clicked.connect(lambda: get_log_data(job_id_input.text()))

# alerts tab
alerts_table = None
def get_alerts_data():
    global alerts_table
    if alerts_table is None:
        alerts_table = QTableWidget()
        tab4.layout.addWidget(alerts_table)
    alerts_table.clear()

    records = getReq("differences",True)
    if records is None:
        invalid_alert_label = QLabel('Error')
        invalid_alert_label.setStyleSheet('color: red;')
        tab4.layout.addWidget(invalid_alert_label)
        alerts_table.clear()
        return
    
    alerts_table.setRowCount(len(records))
    alerts_table.setColumnCount(len(records[0]))

    headers = list(records[0].keys())
    alerts_table.setHorizontalHeaderLabels(headers)

    for row, record in enumerate(records):
        for col, value in enumerate(record.values()):
            item = QTableWidgetItem(str(value))
            alerts_table.setItem(row, col, item)
    alerts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    tab4.layout.addWidget(alerts_table)

get_alerts_button = QPushButton('Get Alerts')
tab4.layout.addWidget(get_alerts_button)
get_alerts_button.clicked.connect(lambda: get_alerts_data())

# login
wrongDeats = QLabel("You must Enter Values")
def login():
    global ACCESS_TOKEN, REFRESH_TOKEN
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
        layout.addWidget(tab_widget)
        tab1.layout.addWidget(loginMessage)
        tab1.layout.addWidget(loginMessage)
        tab1.layout.addWidget(scanButton)


def removeWidgets():
    for i in reversed(range(layout.count())): 
        widgetToRemove = layout.itemAt(i).widget()
        
        layout.removeWidget(widgetToRemove)
        
        widgetToRemove.setParent(None)

loginButton.clicked.connect(login)

app.exec_()
