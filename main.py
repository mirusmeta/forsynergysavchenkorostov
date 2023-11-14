import tkinter as tk
from tkinter import ttk
import sqlite3


# Если что update авто
class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Список сотрудников компании")
        # Создаем объект для работы с базой данных
        self.db = Database()
        # Создаем интерфейс
        self.create_gui()

    def create_gui(self):
        # Виджеты
        self.tree = ttk.Treeview(self.root, columns=('ID', 'ФИО', 'Телефон', 'Email', 'Заработная плата'))
        self.tree.heading('#0', text='ID')
        self.tree.heading('#1', text='ФИО')
        self.tree.heading('#2', text='Телефон')
        self.tree.heading('#3', text='Email')
        self.tree.heading('#4', text='Заработная плата')
        # Listview прокрутки
        yscroll = ttk.Scrollbar(orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=yscroll.set)

        # Располагаем виджеты
        self.tree.grid(row=0, column=0, sticky='nsew')
        yscroll.grid(row=0, column=1, sticky='ns')

        # Кнопки
        add_button = tk.Button(self.root, text='Добавить', command=self.add_employee)
        edit_button = tk.Button(self.root, text='Изменить', command=self.edit_employee)
        delete_button = tk.Button(self.root, text='Удалить', command=self.delete_employee)
        search_button = tk.Button(self.root, text='Поиск', command=self.search_employee)

        add_button.grid(row=1, column=0, pady=5)
        edit_button.grid(row=1, column=1, pady=5)
        delete_button.grid(row=1, column=2, pady=5)
        search_button.grid(row=1, column=3, pady=5)

        # Заполняем column(дерево) данными из базы данных
        self.update_records()

    def add_employee(self):
        """Добавление нового сотрудника."""
        # Получаем данные от пользователя (ваш код)
        fio = input("Введите ФИО сотрудника: ")
        phone = input("Введите номер телефона: ")
        email = input("Введите адрес электронной почты: ")
        salary = input("Введите заработную плату: ")

        # Добавляем нового сотрудника в базу данных
        self.db.add_employee(fio, phone, email, salary)

        # После добавления обновляем отображение
        self.update_records()

    def edit_employee(self):
        """Изменение данных о сотруднике."""
        # Выбираем сотрудника для изменения (ваш код)
        employee_id = input("Введите ID сотрудника для изменения: ")

        # Получаем новые данные от пользователя (ваш код)
        new_fio = input("Введите новое ФИО сотрудника: ")
        new_phone = input("Введите новый номер телефона: ")
        new_email = input("Введите новый адрес электронной почты: ")
        new_salary = input("Введите новую заработную плату: ")

        # Изменяем данные о сотруднике в базе данных
        self.db.edit_employee(employee_id, new_fio, new_phone, new_email, new_salary)

        # После изменения обновляем отображение
        self.update_records()

    def delete_employee(self):
        """Удаление сотрудника."""
        # Выбираем сотрудника для удаления (ваш код)
        employee_id = input("Введите ID сотрудника для удаления: ")

        # Удаляем сотрудника из базы данных
        self.db.delete_employee(employee_id)

        # После удаления обновляем отображение
        self.update_records()

    def search_employee(self):
        """Поиск сотрудника по ФИО."""
        # Получаем ФИО для поиска (ваш код)
        name = input("Введите ФИО сотрудника для поиска: ")

        # Ищем сотрудника в базе данных
        result = self.db.search_employee(name)

        # Выводим результаты поиска
        if result:
            print("Результаты поиска:")
            for row in result:
                print(row)
        else:
            print("Сотрудник не найден.")

    def update_records(self):
        """Обновление записей в виджете Treeview."""
        # Очищаем Treeview перед обновлением
        for record in self.tree.get_children():
            self.tree.delete(record)

        # Получаем все записи из базы данных
        employees = self.db.fetch_all_employees()

        # Вставляем записи в Treeview
        for employee in employees:
            self.tree.insert('', 'end', values=employee)


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("employees.db")
        self.create_table()

    def create_table(self):
        """Создание таблицы в базе данных, если она не существует."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fio TEXT,
                    phone TEXT,
                    email TEXT,
                    salary REAL
                )
            ''')

    def add_employee(self, fio, phone, email, salary):
        """Добавление нового сотрудника в базу данных."""
        with self.conn:
            self.conn.execute('''
                INSERT INTO employees (fio, phone, email, salary)
                VALUES (?, ?, ?, ?)
            ''', (fio, phone, email, salary))

    def edit_employee(self, employee_id, new_fio, new_phone, new_email, new_salary):
        """Изменение данных о сотруднике."""
        with self.conn:
            self.conn.execute('''
                UPDATE employees
                SET fio=?, phone=?, email=?, salary=?
                WHERE id=?
            ''', (new_fio, new_phone, new_email, new_salary, employee_id))

    def delete_employee(self, employee_id):
        """Удаление сотрудника из базы данных. """
        with self.conn:
            self.conn.execute('DELETE FROM employees WHERE id=?', (employee_id,))

    def search_employee(self, name):
        """Поиск сотрудника по ФИО."""
        with self.conn:
            cursor = self.conn.execute('SELECT * FROM employees WHERE fio LIKE ?', ('%' + name + '%',))
            return cursor.fetchall()

    def fetch_all_employees(self):
        """Извлечение всех записей из базы данных."""
        with self.conn:
            cursor = self.conn.execute('SELECT * FROM employees')
            return cursor.fetchall()


root = tk.Tk()
app = EmployeeApp(root)
root.mainloop()