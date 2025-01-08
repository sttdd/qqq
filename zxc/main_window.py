import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from db import Connect, User  # Импортируем класс Connect и модель User

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Установка заголовка окна и его размера
        self.setWindowTitle("Главное окно с таблицей")
        self.setGeometry(100, 100, 600, 400)

        # Создание таблицы (с количеством строк и столбцов, равным количеству пользователей)
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["ID", "ФИО", "Email", "Телефон", "Дата создания"])#название столбцов в таблице

        # Заполнение таблицы данными из базы данных
        self.load_data_from_db()

        # Установка вертикального макета
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        # Создание виджета-контейнера и установка макета
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_data_from_db(self):
        # Создание сессии через класс Connect
        session = Connect.create_connection()
        
        # Получаем данные пользователей из базы данных
        users = session.query(User).all()

        # Закрытие сессии после выполнения запроса
        session.close()

        # Установка количества строк в таблице в зависимости от количества пользователей
        self.table_widget.setRowCount(len(users))

        # Заполнение таблицы данными из пользователей
        for row, user in enumerate(users):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(user.id)))
            self.table_widget.setItem(row, 1, QTableWidgetItem(user.full_name))
            self.table_widget.setItem(row, 2, QTableWidgetItem(user.email))
            self.table_widget.setItem(row, 3, QTableWidgetItem(user.phone_number))
            self.table_widget.setItem(row, 4, QTableWidgetItem(str(user.created_at)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()  # Отображение окна
    sys.exit(app.exec())  # Запуск приложения
