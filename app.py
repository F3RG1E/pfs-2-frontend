from PyQt5.QtWidgets import *

app = QApplication([])
app.setStyle("Fusion")

Window = QWidget()
layout = QVBoxLayout()

username_line = QLineEdit('Username')
password_line = QLineEdit('Password')

layout.addWidget(username_line)
layout.addWidget(password_line)

dropDownBox = QComboBox()
inTransitToDropDownBox = QComboBox()
loginButton = QPushButton('Login')
scanButton = QPushButton('Scan')
inTransitFromLabel = QLabel('Truck')
layout.addWidget(loginButton)


nextButton = QPushButton('Next')

Window.setLayout(layout)
Window.show()

def createLocationDropDown():
    # will always be these values
    dropDownBox.addItems(['Table', 'Safe', 'Truck', 'Bank', 'In Transit', 'Idle', 'Ready For Job'])

def createInTransitDropDown():
    # will fetch data from API and add options of all available locations
    # will prefill from location as current location of box
    if(inTransitFromLabel.text() == 'Safe'):
        inTransitToDropDownBox.addItems(['Truck 1', 'Truck 2', 'Truck 3'])
    elif(inTransitFromLabel.text() == 'Truck'):
        inTransitToDropDownBox.addItems(['Bank 1', 'Bank 2', 'Bank 3'])
    elif(inTransitFromLabel.text() == 'Bank'):
        inTransitToDropDownBox.addItem('Idle')
    elif(inTransitFromLabel.text() == 'Idle'):
        inTransitToDropDownBox.addItem('Ready For Job')
    elif(inTransitFromLabel.text() == 'Ready For Job'):
        inTransitToDropDownBox.addItems(['Table 1', 'Table 2', 'Table 3'])
    elif(inTransitFromLabel.text() == 'Table'):
        inTransitToDropDownBox.addItems(['Safe 1', 'Safe 2', 'Safe 3'])



def login():
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

    layout.addWidget(QLabel('Logged in'))
    layout.addWidget(scanButton)
    layout.addWidget(QLabel('Update Location: '))
    layout.addWidget(dropDownBox)
    createLocationDropDown()
    layout.addWidget(nextButton)

def checkData():
    if(dropDownBox.currentText() == 'In Transit'):
        layout.addWidget(QLabel('From: '))
        layout.addWidget(inTransitFromLabel)
        layout.addWidget(QLabel('To: '))
        createInTransitDropDown()
        layout.addWidget(inTransitToDropDownBox)
        print(inTransitFromLabel.text())
        
    else:
        print(dropDownBox.currentText())

loginButton.clicked.connect(login)
nextButton.clicked.connect(checkData)

app.exec_()
