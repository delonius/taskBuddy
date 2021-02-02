

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
            }
            """


def finishButtonStyle():
    return """
            QPushButton {
                background-color: #B5DC10;
                border: 1px solid #D9D9D9;
                margin-top: 2px;
                height: 48px; 
                width: 70px; 
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
