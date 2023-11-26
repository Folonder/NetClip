import time

import keyboard
from PyQt5 import uic
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QScrollArea, QWidget, QVBoxLayout, \
    QLabel, QCheckBox, QHBoxLayout, QInputDialog, QListWidgetItem, QDialog
from app.view.src.css import *
from app.service.clipboard_transfer import ClipboardTransfer
from app.utils import get_local_ip


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

    def update_ip(self):
        self.ipLabel.setText("Ваш IP-адрес \n" + get_local_ip())
        self.ipLabel.setStyleSheet("color: white")

    def open_ip_manager(self):
        ip_manager = IPManager()
        ip_manager.exec_()

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
        with open('app/view/src/ip.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                ip = line.strip().split(" ")
                if ip[0] == "*":
                    return ip[1]
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


    # def update_remote_messages_widgets(self):
    #     self.__widget_messages = []
    #     for i, message in enumerate(self.__clipboard_transfer.get_remote_messages()):
    #         self.__widget_messages.append(self.generate_message_widget(message.data, i))

class KeyboardThread(QThread):
    key_pressed = pyqtSignal(str)

    def run(self):
        keyboard.hook(self.on_key_event)

    def on_key_event(self, event):
        if event.event_type == keyboard.KEY_DOWN and event.name == 'c' and keyboard.is_pressed('ctrl'):
            self.key_pressed.emit("Ctrl+C pressed")



class IPManager(QDialog):
    def __init__(self, parent=None):
        super(IPManager, self).__init__(parent)
        uic.loadUi('app/view/src/ip_window.ui', self)
        self.seed_ip_manager()

        self.markButton.clicked.connect(self.mark_main_ip)
        self.addButton.clicked.connect(self.add_ip)
        self.deleteButton.clicked.connect(self.delete_ip)
        self.changeButton.clicked.connect(self.edit_ip)


    def add_ip(self):
        ip_text, ok = QInputDialog.getText(self, 'Добавить IP', 'Введите IP:')
        if ok and ip_text:
            item = QListWidgetItem(ip_text)
            if not self.check_item_in_list(item):  # Если элемента нет списке
                self.ipList.addItem(item)
        # Каждый раз сэйв при добавлении ip
        self.save_to_file()

    def delete_ip(self):
        selected = self.ipList.currentRow()
        if selected >= 0:
            self.ipList.takeItem(selected)
        self.save_to_file()

    def edit_ip(self):
        selected = self.ipList.currentRow()
        if selected >= 0:
            new_text, ok = QInputDialog.getText(self, 'Редактировать IP', 'Введите новый IP:',
                                                text=self.ipList.item(selected).text())
            if ok and new_text:
                item = QListWidgetItem(new_text)
                if (not self.check_item_in_list(item)):
                    self.ipList.item(selected).setText(new_text)
                    self.save_to_file()

    def save_to_file(self):
        file_path = 'app/view/src/ip.txt'
        with open(file_path, 'w') as file:
                for index in range(self.ipList.count()):
                    item = self.ipList.item(index)
                    file.write(f"{item.text()}\n")

    def seed_ip_manager(self):
        file_path = 'app/view/src/ip.txt'
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                item = QListWidgetItem(line.strip())
                if item.text().split(" ")[0] == "*":
                    item.setForeground(QColor("red"))
                self.ipList.addItem(item)

    def mark_main_ip(self):
        selected_item = self.ipList.selectedItems()
        index_main_item = self.check_main_item()
        if selected_item and index_main_item == -1:
            selected_item[0].setForeground(QColor("red"))
            selected_item[0].setText("* " + selected_item[0].text())

        else:
            item = self.ipList.item(index_main_item)
            item.setText(item.text().split(" ")[1])
            item.setForeground(QColor("black"))
            self.mark_main_ip()
        self.save_to_file()

    def check_item_in_list(self, item):
        for i in range(self.ipList.count()):
            if self.ipList.item(i).text() == item.text():
                return True
        return False

    def check_main_item(self):
        for i in range(self.ipList.count()):
            if self.ipList.item(i).text().split(" ")[0] == "*":
                return i
        return -1
