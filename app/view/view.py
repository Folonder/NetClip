import json
import time
import socket
import keyboard
from PyQt5 import uic
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QWidget, QVBoxLayout, \
    QLabel, QCheckBox, QHBoxLayout, QInputDialog, QListWidgetItem, QDialog, QMessageBox, QLineEdit, QListWidget, \
    QPushButton, QFormLayout, QDialogButtonBox, QTableWidgetItem, QButtonGroup, QRadioButton

from app.view.src.css import *
from app.service.clipboard_transfer import ClipboardTransfer
from app.utils import get_local_ip
from app.service.ip_model import IpModel


class View(QMainWindow):
    def __init__(self, clipboard_transfer: ClipboardTransfer):
        super().__init__()
        self.__clipboard_transfer = clipboard_transfer
        self.__local_messages_widgets = []
        self.__remote_messages_widgets = []
        uic.loadUi(r"app/view/src/mainmenu.ui", self)
        self.init_ui()

        self.keyboard_thread = KeyboardThread()
        self.keyboard_thread.key_pressed.connect(self.on_key_pressed)
        self.keyboard_thread.start()

    def on_key_pressed(self, message):
        time.sleep(0.5)
        self.update_local_messages_view()

    def init_ui(self):
        self.tabWidget.tabBar().setDocumentMode(True)
        self.tabWidget.tabBar().setExpanding(True)

        self.update_ip()

        self.updateGetTabButton.setFont(font)
        self.updateSendTabButton.setFont(font)
        self.ipManagerButton.setFont(font)
        self.sendButton.setFont(font)
        self.getButton.setFont(font)

        self.tabWidget.setStyleSheet(QTabWidget_style)
        self.updateSendTabButton.clicked.connect(self.update_local_messages_view)
        self.updateGetTabButton.clicked.connect(self.update_remote_messages_view)
        self.ipManagerButton.clicked.connect(self.open_ip_manager)
        self.sendButton.clicked.connect(self.send_messages)
        self.getButton.clicked.connect(self.receive_messages)
        self.tabWidget.currentChanged.connect(self.tab_changed)

        self.update_local_messages_view()

    def open_ip_manager(self):
        ip_manager = IPManager()
        ip_manager.exec_()

    def update_ip(self):
        self.ipLabel.setText("Ваш IP-адрес \n" + get_local_ip())
        self.ipLabel.setStyleSheet("color: white")

    def tab_changed(self, index):
        if index == 0:
            self.update_local_messages_view()
        else:
            self.update_remote_messages_view()

    def update_local_messages_view(self):
        self.update_ip()
        if self.sendVerticalLayout.count() != 0:
            self.sendVerticalLayout.takeAt(0).widget().deleteLater()
        self.update_local_messages_widgets()
        scroll_area, layout = self.create_widget_layout()
        self.sendVerticalLayout.addWidget(scroll_area)
        self.show_widget_messages(layout, self.__local_messages_widgets)

    def update_remote_messages_view(self):
        self.update_ip()
        if self.getVerticalLayout.count() != 0:
            self.getVerticalLayout.takeAt(0).widget().deleteLater()
        self.update_remote_messages_widgets()
        scroll_area, layout = self.create_widget_layout()
        self.getVerticalLayout.addWidget(scroll_area)
        self.show_widget_messages(layout, self.__remote_messages_widgets)

    def update_local_messages_widgets(self):
        self.__local_messages_widgets = []
        for i, message in enumerate(self.__clipboard_transfer.get_local_messages()):
            self.__local_messages_widgets.append(self.generate_message_widget(message.content, i))

    def update_remote_messages_widgets(self):
        self.__remote_messages_widgets = []
        for i, message in enumerate(self.__clipboard_transfer.get_remote_messages()):
            self.__remote_messages_widgets.append(self.generate_message_widget(message.content, i))

    def create_widget_layout(self):
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        widget_container = QWidget(scroll_area)
        scroll_area.setWidget(widget_container)

        container_layout = QVBoxLayout(widget_container)
        return scroll_area, container_layout

    def show_widget_messages(self, layout, messages_widgets):
        for widget in messages_widgets:
            layout.addWidget(widget)

    def send_messages(self):
        return self.__clipboard_transfer.post_messages(self.send_local_checked_messages())

    def receive_messages(self):
        return self.__clipboard_transfer.paste_messages(self.get_remote_checked_messages())

    def generate_message_widget(self, message, index):
        formatted_text = self.format_text(message)
        label = QLabel(formatted_text)
        checkbox = QCheckBox()
        checkbox.setObjectName("checkBox_" + str(index))

        layout = QHBoxLayout()
        layout.addWidget(label)

        layout.addStretch(1)
        layout.addWidget(checkbox)

        container = QWidget()
        container.setLayout(layout)
        container.setStyleSheet("background-color: lightblue;")

        return container

    def send_local_checked_messages(self):
        checked_checkboxes_indexes = self.get_checked_checkboxes_indexes(self.__local_messages_widgets)
        checked_messages = []
        local_messages = self.__clipboard_transfer.get_local_messages()
        local_ip = get_local_ip()
        for i in checked_checkboxes_indexes:
            local_messages[i].receiver = self.get_receiver_ip()
            local_messages[i].sender = local_ip
            checked_messages.append(local_messages[i])
        return checked_messages

    def get_receiver_ip(self):
        with open('app/view/src/ip.json', 'r') as file:
            data = json.load(file)

            for item in data:
                ip = item['IP']
                alias = item['Alias']
                is_main = item['Main']
                if is_main:
                    return ip
        return get_local_ip()

    def get_checked_checkboxes_indexes(self, messages_widgets):
        checked_checkboxes_indexes = []
        for i, widget in enumerate(messages_widgets):
            checkbox = widget.findChild(QCheckBox, "checkBox_" + str(i))
            if checkbox.isChecked():
                checked_checkboxes_indexes.append(i)
        return checked_checkboxes_indexes

    def get_remote_checked_messages(self):
        checked_checkboxes_indexes = self.get_checked_checkboxes_indexes(self.__remote_messages_widgets)
        checked_messages = []
        remote_messages = self.__clipboard_transfer.get_remote_messages()
        for i in checked_checkboxes_indexes:
            checked_messages.append(remote_messages[i])
        return checked_messages

    def format_text(self, message):
        max_lines = 5
        max_line_length = 65
        formatted_lines = []
        lines = message.split('\n')
        for line in lines[:max_lines]:
            formatted_lines.append(line[:max_line_length])

        return "\n".join(formatted_lines)


class KeyboardThread(QThread):
    key_pressed = pyqtSignal(str)

    def run(self):
        keyboard.hook(self.on_key_event)

    def on_key_event(self, event):
        if event.event_type == keyboard.KEY_DOWN and event.name == 'c' and keyboard.is_pressed('ctrl'):
            self.key_pressed.emit("Ctrl+C pressed")


class AddIpWindow(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('app/view/src/add_ip_window.ui', self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);

        layout = QFormLayout(self)
        layout.addWidget(buttonBox)
        self.verticalLayout.addLayout(layout)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)


    def get_inputs(self):
        return self.ipLineEdit.text(), self.aliasLineEdit.text()

    def set_inputs(self, ip, alias):
        self.ipLineEdit.setText(ip)
        self.aliasLineEdit.setText(alias)


class IPManager(QDialog):
    def __init__(self):
        super(IPManager, self).__init__()
        uic.loadUi('app/view/src/ip_window.ui', self)
        self.main_button_group = QButtonGroup()
        self.read_data_from_file()
        self.addButton.clicked.connect(self.open_add_ip_window)
        self.deleteButton.clicked.connect(self.delete_ip)
        self.main_button_group.buttonClicked.connect(self.save_data_to_file)
        self.changeButton.clicked.connect(self.open_edit_ip_window)

    def valid_ip(self, address):
        try:
            host_bytes = address.split('.')
            valid = [int(b) for b in host_bytes]
            valid = [b for b in valid if b >= 0 and b <= 255]
            return len(host_bytes) == 4 and len(valid) == 4
        except:
            return False

    def read_data_from_file(self):
        file_path = 'app/view/src/ip.json'
        with open(file_path, 'r') as file:
            data = json.load(file)

        for item in data:
            ip = item['IP']
            alias = item['Alias']
            is_main = item['Main']

            row_position = self.ipList.rowCount()
            self.ipList.insertRow(row_position)

            is_main_button = QRadioButton()
            self.main_button_group.addButton(is_main_button)

            self.ipList.setCellWidget(row_position, 0, is_main_button)
            self.ipList.setItem(row_position, 1, QTableWidgetItem(ip))
            self.ipList.setItem(row_position, 2, QTableWidgetItem(alias))
            is_main_button.setChecked(is_main)

    def open_add_ip_window(self):
        add_ip_window = AddIpWindow()
        if add_ip_window.exec():
            self.add_ip(add_ip_window.get_inputs())

    def open_edit_ip_window(self):
        edit_ip_window = AddIpWindow()
        ip = self.ipList.item(self.ipList.currentRow(), 1).text()
        alias = self.ipList.item(self.ipList.currentRow(), 2).text()
        edit_ip_window.set_inputs(ip, alias)
        if edit_ip_window.exec():
            self.edit_ip(edit_ip_window.get_inputs())

    def add_ip(self, inputs):
        is_main = QRadioButton()
        self.main_button_group.addButton(is_main)

        row_position = self.ipList.rowCount()

        if self.valid_ip(inputs[0]):
            self.ipList.insertRow(row_position)
            if self.ipList.rowCount() == 1:
                is_main.setChecked(True)
            self.ipList.setCellWidget(row_position, 0, is_main)
            self.ipList.setItem(row_position, 1, QTableWidgetItem(inputs[0]))
            self.ipList.setItem(row_position, 2, QTableWidgetItem(inputs[1]))
        else:
            self.show_validation_error()

        self.save_data_to_file()

    def edit_ip(self, inputs):
        current_row = self.ipList.currentRow()
        if self.valid_ip(inputs[0]):
            self.ipList.setItem(current_row, 1, QTableWidgetItem(inputs[0]))
            self.ipList.setItem(current_row, 2, QTableWidgetItem(inputs[1]))
        else:
            self.show_validation_error()
        self.save_data_to_file()

    def delete_ip(self):
        selected = self.ipList.currentRow()
        is_main = False
        if self.ipList.cellWidget(selected, 0).isChecked():
            is_main = True
        if selected >= 0:
            self.ipList.removeRow(selected)
        if is_main and self.ipList.rowCount():
            self.ipList.cellWidget(selected, 0).setChecked(True)
        self.save_data_to_file()

    def save_data_to_file(self):
        data = []

        for row in range(self.ipList.rowCount()):
            ip = self.ipList.item(row, 1).text()
            alias = self.ipList.item(row, 2).text()
            is_main = self.ipList.cellWidget(row, 0).isChecked()

            data.append({'IP': ip, 'Alias': alias, 'Main': is_main})

        file_path = 'app/view/src/ip.json'
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

    def show_validation_error(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Ошибка")
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText("Неверно введен IP-адрес")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
