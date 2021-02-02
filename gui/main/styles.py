
def inputBoxStyle():
    return """
            QPlainTextEdit {
                border-radius: 6px;
                border: 3px solid #819C0B;
                background-color: #FDFDFD;
                font-size: 16px;
                padding-top: 20px;
                padding-bottom: 20px;
                padding-left: 20px;
            }
            QScrollBar:vertical {
                width: 14px;
                background-color: #819C0B;
            }
            """


def fetchButtonStyle():
    return """
            QPushButton {
                background-color: #B5DC10;
                font-size: 28px;
                font-family: Helvetica;
                border-radius: 10px;
                border: 3px solid #819C0B;
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


def instructionLabelStyle():
    return """
            QLabel {
                font-family: Indie Flower;
                font-size: 25px;
            }
            """


def tabsStyle():
    return """
            QTabBar:tab { 
                height: 50px; 
                width: 135px; 
                font-size: 15px;
            }
            QTabBar:tab:selected {
                font-weight: bold;
            }
            """
