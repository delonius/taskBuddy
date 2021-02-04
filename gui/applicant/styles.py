

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


def applicantPanelMerchantStyle():
    return """
            QLabel {
                font-family: Indie Flower;
                font-size: 18px;
            }
            """
