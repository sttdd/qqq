import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLineEdit, QHBoxLayout
from db import Connect, User, add_user, edit_user, delete_user  # Импортируем необходимые классы и функции

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Установка заголовка окна и его размера
        self.setWindowTitle("Главное окно с таблицей")
        self.setGeometry(100, 100, 600, 400)

        # Создание таблицы для отображения пользователей
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)  # Устанавливаем количество столбцов
        self.table_widget.setHorizontalHeaderLabels(["ID", "ФИО", "Email", "Телефон", "Дата создания"])  # Заголовки столбцов

        # Заполнение таблицы данными из базы данных
        self.load_data_from_db()

        # Установка вертикального макета
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        # Поля для ввода данных
        self.full_name_input = QLineEdit(self)  # Поле для ввода полного имени
        self.email_input = QLineEdit(self)  # Поле для ввода email
        self.phone_input = QLineEdit(self)  # Поле для ввода номера телефона
        self.id_input = QLineEdit(self)  # Поле для ввода ID пользователя (для редактирования)

        # Кнопки для добавления, редактирования и удаления пользователей
        add_button = QPushButton("Добавить", self)
        add_button.clicked.connect(self.add_user)  # Привязываем действие к кнопке

        edit_button = QPushButton("Редактировать", self)
        edit_button.clicked.connect(self.edit_user)  # Привязываем действие к кнопке

        delete_button = QPushButton("Удалить", self)
        delete_button.clicked.connect(self.delete_user)  # Привязываем действие к кнопке

        # Макет для кнопок и полей ввода
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.id_input)  # Добавляем поле ID
        input_layout.addWidget(self.full_name_input)  # Добавляем поле ФИО
        input_layout.addWidget(self.email_input)  # Добавляем поле Email
        input_layout.addWidget(self.phone_input)  # Добавляем поле Телефон
        input_layout.addWidget(add_button)  # Добавляем кнопку "Добавить"
        input_layout.addWidget(edit_button)  # Добавляем кнопку "Редактировать"
        input_layout.addWidget(delete_button)  # Добавляем кнопку "Удалить"

        layout.addLayout(input_layout)  # Добавляем макет с полями и кнопками в основной макет

        # Создание виджета-контейнера и установка макета
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)  # Устанавливаем контейнер как центральный виджет

    def load_data_from_db(self):
        # Функция для загрузки данных из базы данных
        session = Connect.create_connection()  # Создаем сессию
        users = session.query(User).all()  # Получаем всех пользователей из базы данных
        session.close()  # Закрываем сессию

        self.table_widget.setRowCount(len(users))  # Устанавливаем количество строк в таблице

        # Заполнение таблицы данными из пользователей
        for row, user in enumerate(users):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(user.id)))  # ID
            self.table_widget.setItem(row, 1, QTableWidgetItem(user.full_name))  # ФИО
            self.table_widget.setItem(row, 2, QTableWidgetItem(user.email))  # Email
            self.table_widget.setItem(row, 3, QTableWidgetItem(user.phone_number))  # Телефон
            self.table_widget.setItem(row, 4, QTableWidgetItem(str(user.created_at)))  # Дата создания

    def add_user(self):
        # Функция для добавления нового пользователя
        full_name = self.full_name_input.text()  # Получаем полное имя из поля ввода
        email = self.email_input.text()  # Получаем email из поля ввода
        phone_number = self.phone_input.text()  # Получаем номер телефона из поля ввода
        add_user(full_name, email, phone_number)  # Вызываем функцию добавления пользователя
        self.load_data_from_db()  # Обновляем таблицу

    def edit_user(self):
        # Функция для редактирования существующего пользователя
        user_id = self.id_input.text()  # Получаем ID пользователя из поля ввода
        full_name = self.full_name_input.text()  # Получаем полное имя
        email = self.email_input.text()  # Получаем email
        phone_number = self.phone_input.text()  # Получаем номер телефона
        edit_user(user_id, full_name, email, phone_number)  # Вызываем функцию редактирования пользователя
        self.load_data_from_db()  # Обновляем таблицу

    def delete_user(self):
        # Функция для удаления пользователя
        user_id = self.id_input.text()  # Получаем ID пользователя из поля ввода
        delete_user(user_id)  # Вызываем функцию удаления пользователя
        self.load_data_from_db()  # Обновляем таблицу

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создаем экземпляр приложения
    window = MainWindow()  # Создаем главное окно
    window.show()  # Отображаем окно
    sys.exit(app.exec())  # Запускаем приложение