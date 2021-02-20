

def trackerStyle():
    return """
            QLabel {
                font-family: Helvetica;
                font-size: 20px;
            }
            """


def buttonStyle():
    return """
            QPushButton {
                background-color: #B5DC10;
                font-size: 18px;
                font-family: Helvetica;
                border-radius: 5px;
                border: 2px solid #819C0B;
                font-weight: 500;
                color: #333333;
            }
            QPushButton:hover {
                background-color: #a7c912;
            }
            QPushButton:pressed {
                background-color: #96b50d;
            }
        """


def applicantBoxStyle():
    return """
            QGroupBox {
                font-family: Helvetica;
                font-size: 20px;    
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                margin-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 7px;
                padding: 0px 5px 0px 5px;
            }
            """


def finishButtonStyle():
    return """
            QPushButton {
                background-color: #B5DC10;
                border: 1px solid #D9D9D9;
                margin-top: 2px;
                height: 50px; 
                width: 100px; 
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #a7c912;
            }
            QPushButton:pressed {
                background-color: #96b50d;
            }
            """


def applicantPanelStyle():
    return """
            QLabel {
                font-family: Helvetica;
                font-size: 14px;
                font-weight: bold;
            }
            """


def applicantPanelValueStyle():
    return """
            QLabel {
                font-family: Helvetica;
                font-size: 14px;
            }
            """


def highriseButtonStyle():
    return """
            QPushButton {
                font-size: 16px;
                background-color: #F9D129;
                border: 2px solid #888888;
                border-radius: 10px;
                font-family: Helvetica;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dbb727;
            }
            QPushButton:pressed {
                background-color: #c7a622;
            }
            """


def gatewayButtonStyle():
    return """
            QPushButton {
                font-size: 16px;
                background-color: #B5DC10;
                border: 2px solid #888888;
                border-radius: 10px;
                font-family: Helvetica;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #a7c912;
            }
            QPushButton:pressed {
                background-color: #96b50d;
            }
            """

def deleteButtonStyle():
    return """
            QPushButton {
                font-size: 16px;
                background-color: #ff616a;
                border: 2px solid #888888;
                border-radius: 10px;
                font-family: Helvetica;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f5222e;
            }
            QPushButton:pressed {
                background-color: #d41e29;
            }
            """


def applicantTabPanelStyle():
    return """
            QTabBar:tab { 
                height: 30px; 
                width: 75px; 
                font-size: 11px;
            }
            QTabBar:tab:selected {
                font-weight: normal;
            }
            """


def taskPanelStyle():
    return """
            QTreeWidget {
                border: 1px solid #DDDDDD;
                border-radius: 5px;
            }
            """


def inputBoxStyle():
    return """
            QPlainTextEdit {
                border-radius: 6px;
                border: 1px solid #CCCCCC;
                background-color: #FDFDFD;
                font-size: 14px;
            }
            QScrollBar:vertical {
                width: 14px;
                background-color: #819C0B;
            }
            """

def calendarStyle():
    return """
            QCalendarWidget {
                background-color: #DDDDDD;
                border-bottom: 1px solid gray;
            }
            QCalendarWidget QToolButton {
                color: black;
            }
            """

def dateButtonStyle():
    return """
            QPushButton {
                background-color: white;
                border: 1.5px solid #999999;
            }
            """