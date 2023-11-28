# pyuic5 .\untitled.ui -o project_interface.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
import sqlite3
from datetime import datetime
from project_interface import Ui_OlympiadApp

conn = sqlite3.connect('olympiads.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS olympiads
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, name TEXT, date DATE, level TEXT)''')


class OlympiadApp(QMainWindow, Ui_OlympiadApp):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_button.clicked.connect(self.add_olympiad)
        self.delete_button.clicked.connect(self.delete_olympiad)
        self.sort_button.clicked.connect(self.sort_table)
        self.load_olympiads()

    def load_olympiads(self):
        # загрузка данных из базы данных и отображение в таблице
        cursor.execute("SELECT * FROM olympiads")
        olympiads = cursor.fetchall()

        self.table.setRowCount(len(olympiads))
        for row, olympiad in enumerate(olympiads):
            for column, data in enumerate(olympiad):
                item = QTableWidgetItem(str(data))
                self.table.setItem(row, column, item)

    def add_olympiad(self):
        # добавление элемента в таблицу
        subject = self.subject_input.text()
        name = self.name_input.text()
        date_string = self.date_input.text()
        level = self.level_input.text()

        try:
            date = datetime.strptime(date_string, "%d.%m.%Y")
            formatted_date = datetime.strftime(date, "%d.%m.%Y")
            cursor.execute("INSERT INTO olympiads (subject, name, date, level) VALUES (?, ?, ?, ?)",
                           (subject, name, formatted_date, level))
            conn.commit()
            self.subject_input.setText("")
            self.name_input.setText("")
            self.date_input.setText("")
            self.level_input.setText("")
            self.load_olympiads()

        except ValueError:
            QMessageBox.warning(self, "Ошибка!", "Неверный формат даты, введите дату в формате ДД.ММ.ГГГГ")

    def delete_olympiad(self):
        # удаление выбранной олимпиады
        selected_row = self.table.currentRow()

        if selected_row >= 0:
            olympiad_id = self.table.item(selected_row, 0).text()
            # print(olympiad_id)
            cursor.execute("DELETE FROM olympiads WHERE id=?", (olympiad_id,))
            conn.commit()
            self.table.removeRow(selected_row)
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите олимпиаду для удаления")

    def sort_table(self):
        # сортировка элементов таблицв по дате и уровню олимпиады
        self.table.sortItems(3)
        self.table.sortItems(4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = OlympiadApp()
    ex.show()
    sys.exit(app.exec_())

conn.close()
