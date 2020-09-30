# This Python file uses the following encoding: utf-8
import sys

import db
from woodmodel import WoodModel

from PySide2.QtWidgets import QApplication, QPushButton, QTextEdit, QWidget, QTableView, QVBoxLayout
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        wood_model = WoodModel(list(db.get_all_wood_records()))
        main_layout = QVBoxLayout()
        table_view = QTableView(self)
        table_view.setModel(wood_model)
        main_layout.addWidget(table_view)
        text_edit = QTextEdit(self)
        main_layout.addWidget(text_edit)
        add_button = QPushButton("Add", self)
        main_layout.addWidget(add_button)
        self.setLayout(main_layout)

        def on_add(value):
            records_to_add = text_edit.toPlainText().split("\n")
            for record_to_add in records_to_add:
                columns = record_to_add.split("\t")
                wood = db.Wood.from_text_columns(columns)
                wood_model.add_wood(wood)
                db.add_wood_record(wood)
            text_edit.clear()

        add_button.clicked.connect(on_add)


if __name__ == "__main__":
    db.create_database_structure()
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
