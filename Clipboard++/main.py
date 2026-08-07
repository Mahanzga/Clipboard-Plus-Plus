# IMPORTS
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit, QListWidget, QListWidgetItem, 
                             QVBoxLayout, QHBoxLayout, QMessageBox, QAbstractItemView)
from PyQt5.QtGui import QIcon, QColor
import pyperclip as clipboard
from PyQt5.QtCore import Qt, QTimer
import json

class mainWindow(QWidget):
    def __init__(self):
        # APP SETTINGS
        super().__init__()
        self.setWindowTitle("Clipboard++")
        icon_path = "C:/Users/Mahan Moghimian/Desktop/My files/Icons/clipboard.png"
        self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(1653, 610, 500, 750)
        self.file_path = "C:/Users/Mahan Moghimian/Desktop/My files/Python/Projects/Clipboard++/history.json"

        # ALL WIDGETS
        self.search_bar = QLineEdit()
        self.list = QListWidget()
        # self.list.setSpacing(5)
        self.list.setAlternatingRowColors(True)
        self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.list.verticalScrollBar().setSingleStep(15)
        self.delete_button = QPushButton("Delete ❌️")
        self.clear_button = QPushButton("Clear All ⚠️")
        self.clipboard_log = []

        self.delete_button.setObjectName("delete_button")
        self.clear_button.setObjectName("clear_button")

        self.initUI()
        self.loadFromFile()
        self.watch_clipboard()

    def initUI(self):
        master_layout = QVBoxLayout()

        bottom_row = QHBoxLayout()
        bottom_row.addWidget(self.delete_button, 70)
        bottom_row.addWidget(self.clear_button, 30)

        master_layout.addWidget(self.search_bar)
        master_layout.addWidget(self.list)
        master_layout.addLayout(bottom_row)

        self.setLayout(master_layout)


        self.setStyleSheet("""

            QListWidget::item {
                height: 100px;
            }
            QListWidget {
                font-size: 30px;
            }
            QPushButton#delete_button, #clear_button {
                font-size: 20px;
            }
            QLineEdit {
                font-size: 35px;
                border-radius: 20px;
                padding: 20px 10px;
            }


        """)


        self.delete_button.clicked.connect(self.delete_item)
        self.search_bar.textEdited.connect(self.search_item)
        self.clear_button.clicked.connect(self.clear_all)
        self.list.itemDoubleClicked.connect(self.on_double_click)


    def watch_clipboard(self):
        current = clipboard.paste()

        if current:
            if not self.clipboard_log or current != self.clipboard_log[0]:
                self.clipboard_log.insert(0, current)

                item = QListWidgetItem(current)
                self.list.insertItem(0, item)

        self.saveToFile()
        QTimer.singleShot(500, self.watch_clipboard)

    def saveToFile(self):
        with open(self.file_path, "w") as file:
            json.dump(self.clipboard_log, file)

    def loadFromFile(self):
        self.clipboard_log = []
        try:
            with open(self.file_path, "r") as file:
                self.clipboard_log = json.load(file)
        except FileNotFoundError:
            pass

        for element in self.clipboard_log:
            item = QListWidgetItem(element)
            self.list.addItem(item)

    def delete_item(self):
        selected_row = self.list.currentRow()
        if selected_row == 0:
            QMessageBox.warning(self, "Error", "You cannot delete the last copied item.")
            return
        if selected_row != -1:
            self.list.takeItem(selected_row)
            del self.clipboard_log[selected_row]
            self.list.clearSelection()
            self.list.setCurrentRow(-1)
        else:
            QMessageBox.critical(self, "Error", "No item is selected.")
            self.list.clearSelection()
            self.list.setCurrentRow(-1)

    def search_item(self):
        if self.search_bar.text() == "":
            self.list.clear()
            for element in self.clipboard_log:
                item = QListWidgetItem(element)
                self.list.addItem(item)
        else:
            self.list.clear()
            current = self.search_bar.text()
            for items in self.clipboard_log:
                if current in items:
                    item = QListWidgetItem(items)
                    self.list.addItem(item)

    def clear_all(self):
        confirm = QMessageBox.question(self, "Warning", "This will delete all items except for the last one! continue?", 
                             QMessageBox.Cancel | QMessageBox.Ok)
        if confirm == QMessageBox.Ok:
            self.clipboard_log.clear()
            self.list.clear()
        else:
            pass

    def on_double_click(self, item):
        text = item.text()
        clipboard.copy(text)
        item.setBackground(QColor(200, 255, 200))
        QTimer.singleShot(500, lambda: self.on_double_click_do(item))

    def on_double_click_do(self, item):
        item.setBackground(Qt.transparent)




def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



# icon from: <a href="https://www.flaticon.com/free-icons/clipboard" title="clipboard icons">Clipboard icons created by Dimitry Miroliubov - Flaticon</a>