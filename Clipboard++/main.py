# IMPORTS
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit, QListWidget, QListWidgetItem, 
                             QVBoxLayout, QHBoxLayout, QMessageBox, QAbstractItemView, QLabel)
from PyQt5.QtGui import QIcon, QColor
import pyperclip as clipboard
from PyQt5.QtCore import Qt, QTimer
import json
import datetime as dt

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
        self.last_copy = clipboard.paste()

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

            QPushButton#delete_button, #clear_button {
                font-size: 20px;
            }
            QLineEdit {
                font-size: 30px;
                font-family: Arial;
                color: #2c3136;
                border-radius: 20px;
                padding: 26px 15px;
            }


        """)


        self.delete_button.clicked.connect(self.delete_item)
        self.search_bar.textEdited.connect(self.search_item)
        self.clear_button.clicked.connect(self.clear_all)
        self.list.itemDoubleClicked.connect(self.on_double_click)
        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self.toggle_pin)


    def watch_clipboard(self):
        current = clipboard.paste()

        if current:
            if current != self.last_copy:

                self.last_copy = current

                timestamp = dt.datetime.now().strftime("%H:%M")
                dictionary = {"text": current,
                              "timestamp": timestamp, 
                              "pinned": False}
                self.clipboard_log.insert(0, dictionary)


                self.refresh()

        self.saveToFile()
        QTimer.singleShot(500, self.watch_clipboard)

    def saveToFile(self):
        with open(self.file_path, "w") as file:
            json.dump(self.clipboard_log, file, indent=4)

    def loadFromFile(self):
        self.clipboard_log = []
        try:
            with open(self.file_path, "r") as file:
                self.clipboard_log = json.load(file)
                self.refresh()
        except FileNotFoundError:
            pass

        for dict in self.clipboard_log:
            item = QListWidgetItem()
            widget = clipboardRow(dict["text"], dict["timestamp"])
            item.setSizeHint(widget.sizeHint())
            self.list.addItem(item)
            self.list.setItemWidget(item, widget)

    def delete_item(self):
        selected_row = self.list.currentRow()
        item = self.list.item(selected_row)
        widget = self.list.itemWidget(item)
        text = getattr(widget, "text", None)

        if text is None:
            return

        if selected_row != -1:
            self.list.takeItem(selected_row)
            for dict in self.clipboard_log:
                if dict.get("text") == text:
                    index = self.clipboard_log.index(dict)
                    del self.clipboard_log[index]
                    break
            self.list.clearSelection()
            self.list.setCurrentRow(-1)
        else:
            QMessageBox.critical(self, "Error", "No item is selected.")
            self.list.clearSelection()
            self.list.setCurrentRow(-1)

    def search_item(self):
        if self.search_bar.text() == "":
            self.list.clear()
            for dict in self.clipboard_log:
                item = QListWidgetItem()
                widget = clipboardRow(dict["text"], dict["timestamp"])
                item.setSizeHint(widget.sizeHint())
                self.list.addItem(item)
                self.list.setItemWidget(item, widget)
                self.refresh()
        else:
            self.list.clear()
            current = self.search_bar.text()
            for dict in self.clipboard_log:
                if current in dict["text"]:
                    item = QListWidgetItem()
                    widget = clipboardRow(dict["text"], dict["timestamp"])
                    item.setSizeHint(widget.sizeHint())
                    self.list.addItem(item)
                    self.list.setItemWidget(item, widget)

    def clear_all(self):
        confirm = QMessageBox.question(self, "Warning", "This will delete all items! continue?", 
                             QMessageBox.Cancel | QMessageBox.Ok)
        if confirm == QMessageBox.Ok:
            self.clipboard_log.clear()
            self.list.clear()
        else:
            pass

    def on_double_click(self, item):
        widget = self.list.itemWidget(item)
        text = widget.text
        clipboard.copy(text)
        self.search_bar.clear()
        self.list.clearSelection()
        self.list.setCurrentRow(-1)
        self.refresh()
        for i in range(self.list.count()):
            current_item = self.list.item(i)
            widget = self.list.itemWidget(current_item)
            current_text = widget.text
            if current_text == text:
                self.list.item(i).setBackground(QColor(200, 255, 200))          # green
                QTimer.singleShot(700, lambda: self.reset_highlight(i))
                return

    def reset_highlight(self, row):
        self.list.item(row).setBackground(Qt.transparent)


    def toggle_pin(self, postion):
        item = self.list.itemAt(postion)
        if not item :
            self.search_bar.clear()
            self.list.clearSelection()
            self.list.setCurrentRow(-1)
            return
        widget = self.list.itemWidget(item)
        text = widget.text
        for dict in self.clipboard_log:
            if dict.get("text") == text:
                dict["pinned"] = not dict["pinned"]
                break
        # row = self.list.row(item)
        # self.clipboard_log[row]["pinned"] = not self.clipboard_log[row]["pinned"]

        self.search_bar.clear()
        self.list.clearSelection()
        self.list.setCurrentRow(-1)
        self.refresh()

    def refresh(self):
        self.clipboard_log.sort(key=lambda x: x["pinned"], reverse=True)        # this method just sorts the list based on the pinned status, it doesn't change the index of the items in the list, they stay in the same order they were before.
        self.list.clear()
        for dict in self.clipboard_log:
            item = QListWidgetItem()
            widget = clipboardRow(dict["text"], dict["timestamp"])
            item.setSizeHint(widget.sizeHint())
            self.list.addItem(item)
            self.list.setItemWidget(item, widget)

            if dict["pinned"] :
                item.setBackground(QColor(255, 201, 201))           # red
            else:
                item.setBackground(Qt.transparent)




class clipboardRow(QWidget):
    def __init__(self, text, timestamp):
        super().__init__()
        self.text = text                        # to access it inside <on_double_click> method

        layout = QHBoxLayout()

        max_len = 30
        display_text = text[:max_len] + ("  ..." if len(text) > max_len else "")
        text_label = QLabel(display_text)
        text_label.setObjectName("text_label")
        timestamp_label = QLabel(timestamp)
        timestamp_label.setObjectName("timestamp_label")
        self.setStyleSheet("""

            QLabel#text_label {
                font-size: 24px;
                font-family: Arial;
            }
            QLabel#timestamp_label {
                color: #727a82;
            }
            
        """)

        layout.addWidget(text_label, 90)
        layout.addWidget(timestamp_label, 10)

        self.setLayout(layout)
        self.setToolTip(f"{text}\n\nCopied at {timestamp}")




def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



# icon from: <a href="https://www.flaticon.com/free-icons/clipboard" title="clipboard icons">Clipboard icons created by Dimitry Miroliubov - Flaticon</a>