from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QWidget, QVBoxLayout, \
    QLabel, QCheckBox, QHBoxLayout

from app.service.clipboard_transfer import ClipboardTransfer


class View(QMainWindow):
    def __init__(self, clipboard_transfer: ClipboardTransfer):
        super().__init__()
        self.__clipboard_transfer = clipboard_transfer
        self.__widget_messages = []
        uic.loadUi(r"app/view/src/mainmenu.ui", self)
        self.init_ui()
        self.update_local_messages_view()

    def init_ui(self):
        self.create_widget_layout()
        self.updateButton.clicked.connect(self.update_local_messages_view)

    def create_widget_layout(self):
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        widget_container = QWidget(scroll_area)
        scroll_area.setWidget(widget_container)

        container_layout = QVBoxLayout(widget_container)
        self.verticalLayout.addWidget(scroll_area)
        return container_layout

    def update_local_messages_view(self):
        self.verticalLayout.takeAt(0).widget().deleteLater()
        self.update_messages_widgets()
        layout = self.create_widget_layout()
        self.show_widget_messages(layout)

    def show_widget_messages(self, layout):
        for widget in self.__widget_messages:
            layout.addLayout(widget)

    def generate_message_widget(self, message):
        formatted_text = "\n".join([message[i:i + 50] for i in range(0, len(message), 50)])
        label = QLabel(formatted_text)
        checkbox = QCheckBox()

        layout = QHBoxLayout()
        layout.addWidget(label)

        layout.addStretch(1)
        layout.addWidget(checkbox)

        return layout

    def update_messages_widgets(self):
        self.__widget_messages = []
        for message in self.__clipboard_transfer.get_local_messages():
            self.__widget_messages.append(self.generate_message_widget(message.data))