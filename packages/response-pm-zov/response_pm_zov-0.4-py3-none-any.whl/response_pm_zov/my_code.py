def get_code():
    return """
   ---апишка---------------------
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import json

app = Flask(__name__)
api = Api(app)

# Загрузка данных о пользователях из файла
def load_users():
    with open('users.json', 'r') as file:
        return json.load(file)


# Ресурс для авторизации пользователя
class UserAuth(Resource):
    def post(self):
        data = request.get_json()
        user_code = data.get('code')
        users = load_users()

        # Поиск пользователя по коду
        user = next((user for user in users if user['code'] == user_code), None)
        if user:
            return jsonify({"status": "success", "message": "User authenticated", "user": user})
        else:
            return jsonify({"status": "error", "message": "User not found"}), 404

# Ресурс для получения информации о пользователе
class UserInfo(Resource):
    def get(self, user_code):
        users = load_users()

        # Поиск пользователя по коду
        user = next((user for user in users if user['code'] == user_code), None)
        if user:
            return jsonify({"status": "success", "user": user})
        else:
            return jsonify({"status": "error", "message": "User not found"}), 404

# Добавление ресурсов к API
api.add_resource(UserAuth, '/auth')
api.add_resource(UserInfo, '/user/<string:user_code>')

if __name__ == '__main__':
    app.run(debug=True)



----админ панель------------------

class AdminPanel(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Admin Panel')
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        # Кнопка для открытия окна добавления пользователей
        self.add_user_button = QPushButton('Add User', self)
        self.add_user_button.clicked.connect(self.open_add_user_window)
        layout.addWidget(self.add_user_button)

        # Кнопка для открытия окна добавления книг
        self.add_book_button = QPushButton('Add Book', self)
        self.add_book_button.clicked.connect(self.open_add_book_window)
        layout.addWidget(self.add_book_button)

        # Кнопка для отображения списка книг
        self.view_books_button = QPushButton('View Books', self)
        self.view_books_button.clicked.connect(self.open_view_books_window)
        layout.addWidget(self.view_books_button)

        self.setLayout(layout)

    def open_add_user_window(self):
        self.add_user_window = AddUserWindow()
        self.add_user_window.show()

    def open_add_book_window(self):
        self.add_book_window = AddBookWindow()
        self.add_book_window.show()

    def open_view_books_window(self):
        self.view_books_window = ViewBooksWindow()
        self.view_books_window.show()


class AddUserWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add User')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        self.code_input = QLineEdit(self)
        self.code_input.setPlaceholderText('User Code')
        layout.addWidget(self.code_input)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText('User Name')
        layout.addWidget(self.name_input)

        self.address_input = QLineEdit(self)
        self.address_input.setPlaceholderText('User Address')
        layout.addWidget(self.address_input)

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText('User Phone')
        layout.addWidget(self.phone_input)

        self.book_code_input = QLineEdit(self)
        self.book_code_input.setPlaceholderText('Book Code')
        layout.addWidget(self.book_code_input)

        self.date_taken_input = QDateEdit(self)
        self.date_taken_input.setDate(QDate.currentDate())
        self.date_taken_input.setCalendarPopup(True)
        layout.addWidget(QLabel('Date Taken:'))
        layout.addWidget(self.date_taken_input)

        self.date_return_input = QDateEdit(self)
        self.date_return_input.setDate(QDate.currentDate())
        self.date_return_input.setCalendarPopup(True)
        layout.addWidget(QLabel('Date Return:'))
        layout.addWidget(self.date_return_input)

        self.add_user_button = QPushButton('Add User', self)
        self.add_user_button.clicked.connect(self.add_user)
        layout.addWidget(self.add_user_button)

        self.setLayout(layout)

    def add_user(self):
        user_data = {
            "code": self.code_input.text(),
            "name": self.name_input.text(),
            "address": self.address_input.text(),
            "phone": self.phone_input.text(),
            "book_code": self.book_code_input.text(),
            "date_taken": self.date_taken_input.date().toString("yyyy-MM-dd"),
            "date_return": self.date_return_input.date().toString("yyyy-MM-dd")
        }

        if not all(user_data.values()):
            QMessageBox.warning(self, 'Error', 'All fields are required!')
            return

        try:
            with open('users.json', 'r') as file:
                users_data = json.load(file)
        except FileNotFoundError:
            users_data = []

        users_data.append(user_data)

        try:
            with open('users.json', 'w') as file:
                json.dump(users_data, file, indent=4)
            QMessageBox.information(self, 'Success', 'User added successfully!')
            self.clear_inputs()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save user: {e}')

    def clear_inputs(self):
        self.code_input.clear()
        self.name_input.clear()
        self.address_input.clear()
        self.phone_input.clear()
        self.book_code_input.clear()
        self.date_taken_input.setDate(QDate.currentDate())
        self.date_return_input.setDate(QDate.currentDate())


class AddBookWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add Book')
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        self.code_input = QLineEdit(self)
        self.code_input.setPlaceholderText('Book Code')
        layout.addWidget(self.code_input)

        self.author_input = QLineEdit(self)
        self.author_input.setPlaceholderText('Author')
        layout.addWidget(self.author_input)

        self.title_input = QLineEdit(self)
        self.title_input.setPlaceholderText('Title')
        layout.addWidget(self.title_input)

        self.year_input = QLineEdit(self)
        self.year_input.setPlaceholderText('Year of Publication')
        layout.addWidget(self.year_input)

        self.price_input = QLineEdit(self)
        self.price_input.setPlaceholderText('Price')
        layout.addWidget(self.price_input)

        self.annotation_input = QTextEdit(self)
        self.annotation_input.setPlaceholderText('Brief Annotation')
        layout.addWidget(self.annotation_input)

        self.add_book_button = QPushButton('Add Book', self)
        self.add_book_button.clicked.connect(self.add_book)
        layout.addWidget(self.add_book_button)

        self.setLayout(layout)

    def add_book(self):
        book_data = {
            "code": self.code_input.text(),
            "author": self.author_input.text(),
            "title": self.title_input.text(),
            "year": self.year_input.text(),
            "price": self.price_input.text(),
            "annotation": self.annotation_input.toPlainText()
        }

        if not all(book_data.values()):
            QMessageBox.warning(self, 'Error', 'All fields are required!')
            return

        try:
            with open('books.json', 'r') as file:
                books_data = json.load(file)
        except FileNotFoundError:
            books_data = []

        books_data.append(book_data)

        try:
            with open('books.json', 'w') as file:
                json.dump(books_data, file, indent=4)
            QMessageBox.information(self, 'Success', 'Book added successfully!')
            self.clear_inputs()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save book: {e}')

    def clear_inputs(self):
        self.code_input.clear()
        self.author_input.clear()
        self.title_input.clear()
        self.year_input.clear()
        self.price_input.clear()
        self.annotation_input.clear()


class ViewBooksWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('View Books')
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        self.books_list = QListWidget(self)
        layout.addWidget(self.books_list)

        self.load_books()

        self.setLayout(layout)

    def load_books(self):
        try:
            with open('books.json', 'r') as file:
                books_data = json.load(file)
                self.books_list.clear()
                for book in books_data:
                    book_info = (
                        f"Code: {book['code']}, Author: {book['author']}, Title: {book['title']}, "
                        f"Year: {book['year']}, Price: {book['price']}, Annotation: {book['annotation']}"
                    )
                    item = QListWidgetItem(book_info)
                    self.books_list.addItem(item)
        except FileNotFoundError:
            QMessageBox.warning(self, 'Error', 'No books found!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AdminAuthWindow()
    window.show()
    sys.exit(app.exec_())

----ксамл-----------------


<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">

    <!-- Поле для ввода кода -->
    <EditText
        android:id="@+id/codeInput"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Введите код" />

    <!-- Кнопка для отправки запроса -->
    <Button
        android:id="@+id/submitButton"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Отправить" />

    <!-- Текстовое поле для отображения результата -->
    <TextView
        android:id="@+id/resultText"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="16dp"
        android:text="Результат"
        android:textSize="16sp" />
</LinearLayout>


----мобилка-----------

package com.example.timer_krisa

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.android.volley.Request
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import org.json.JSONObject

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Находим элементы макета
        val codeInput = findViewById<EditText>(R.id.codeInput)
        val submitButton = findViewById<Button>(R.id.submitButton)
        val resultText = findViewById<TextView>(R.id.resultText)

        // Обработка нажатия кнопки
        submitButton.setOnClickListener {
            val code = codeInput.text.toString()
            if (code.isNotEmpty()) {
                sendRequest(code, resultText)
            } else {
                resultText.text = "Введите код"
            }
        }
    }

    private fun sendRequest(code: String, resultText: TextView) {
        val url = "http://10.0.2.2:5000/auth" // URL вашего сервера
        val queue = Volley.newRequestQueue(this)

        // Создаем JSON-тело запроса
        val jsonBody = JSONObject().apply {
            put("code", code)
        }

        // Создаем запрос
        val request = JsonObjectRequest(
            Request.Method.POST, url, jsonBody,
            { response ->
                // Обработка успешного ответа
                val status = response.optString("status", "error")
                if (status == "success") {
                    val user = response.optJSONObject("user")
                    if (user != null) {
                        val name = user.optString("name", "Нет данных")
                        val address = user.optString("address", "Нет данных")
                        val phone = user.optString("phone", "Нет данных")
                        val bookCode = user.optString("book_code", "Нет данных")
                        val dateTaken = user.optString("date_taken", "Нет данных")
                        val dateReturn = user.optString("date_return", "Нет данных")

                        // Формируем текст для отображения
                        val userInfo = ""
                            Имя: $name
                            Адрес: $address
                            Телефон: $phone
                            Шифр книги: $bookCode
                            Дата взятия: $dateTaken
                            Дата возврата: $dateReturn
                        "".trimIndent()

                        resultText.text = userInfo
                    } else {
                        resultText.text = "Ошибка: данные пользователя отсутствуют"
                    }
                } else {
                    val message = response.optString("message", "Ошибка авторизации")
                    resultText.text = message
                }
            },
            { error ->
                // Обработка ошибки
                error.printStackTrace()
                resultText.text = "Ошибка: ${error.message}"
            }
        )

        // Добавляем запрос в очередь
        queue.add(request)
    }
}
    """