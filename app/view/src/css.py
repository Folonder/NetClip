from PyQt5.QtGui import QFont
from PyQt5 import QtGui

QTabWidget_style = """
QTabBar::tab {
    height: 70px;
    font-size: 16px;
    font-weight: bold;                      
                   
    background-color: qlineargradient(x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(253,250,250), stop:0.2 rgb(253,250,250), stop:1 rgb(255,249,234));
    border-top-left-radius: 7px;
    border-top-right-radius: 7px;
    
    min-width: 8ex;
    padding: 5px;
}

QTabBar::tab:selected {
    background-color: rgb(253,250,250);
    color: brown
}

QTabBar::tab:!selected {
    margin-top: 5px;
    background: qlineargradient(x1:0.5, y1:1, x2:0.5, y2:0, stop:0 rgb(253,250,250), stop:0.2 rgb(253,250,250), stop:1 rgb(250,244,229));
    color: black
}


QTabWidget::pane {
    
    border-top-left-radius: 7px; 
    border-top-right-radius: 7px;
}
"""

font = QtGui.QFont("Times", 10, QFont.Bold)
