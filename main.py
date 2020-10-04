# This Python file uses the following encoding: utf-8
import sys

import db
from woodmodel import WoodModel

from PySide2.QtWidgets import QApplication, QDesktopWidget, QLabel, QPushButton, QTextEdit, QWidget, QTableView, QVBoxLayout
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1024, 600)
        wood_model = WoodModel(list(db.get_all_wood_records()))
        main_layout = QVBoxLayout()
        table_view = QTableView(self)
        table_view.setModel(wood_model)
        main_layout.addWidget(table_view)
        text_edit = QTextEdit(self)
        main_layout.addWidget(text_edit)
        message_label = QLabel("", self)
        main_layout.addWidget(message_label)
        add_button = QPushButton("Add", self)
        main_layout.addWidget(add_button)
        self.setLayout(main_layout)

        def on_add(value):
            records_to_add = text_edit.toPlainText().split("\n")
            for record_to_add in records_to_add:
                columns = record_to_add.split("\t")
                try:
                    wood = db.Wood.from_text_columns(columns)
                    db.add_wood_record(wood)
                    wood_model.add_wood(wood)
                except db.DwellingException as e:
                    print(e.message)
                    message_label.setText(e.message)
            text_edit.clear()

        add_button.clicked.connect(on_add)


if __name__ == "__main__":
    db.create_database_structure()
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
