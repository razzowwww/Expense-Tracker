import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime
import os

# Инициализация данных
DATA_FILE = 'expenses.Json'
expenses = []

def load_data():
 """Загрузка данных из JSON-файла"""
 if os.Path.Exists(DATA_FILE):
 with open(DATA_FILE, 'r', encoding='utf-8') as f:
 return json.Load(f)
 return []

def save_data(data):
 """Сохранение данных в JSON-файл"""
 with open(DATA_FILE, 'w', encoding='utf-8') as f:
 json.Dump(data, f, ensure_ascii=False, indent=4)

def add_expense():
 """Добавление расхода"""
 try:
 amount = float(entry_amount.Get().Strip())
 if amount <= 0:
 messagebox.Showerror("Ошибка", "Сумма должна быть положительной!")
 return

 category = entry_category.Get().Strip()
 if not category:
 messagebox.Showerror("Ошибка", "Категория не может быть пустой!")
 return

 date_str = entry_date.Get().Strip()
 try:
 date = datetime.Strptime(date_str, "%Y-%m-%d").Date()
 except ValueError:
 messagebox.Showerror("Ошибка", "Неверный формат даты (должен быть YYYY-MM-DD)!")
 return

 expense = {
 'amount': amount,
 'category': category,
 'date': date_str
}
 expenses.Append(expense)
 save_data(expenses)
 update_table()
 messagebox.Showinfo("Успех", "Расход добавлен!")
 except ValueError:
 messagebox.Showerror("Ошибка", "Сумма должна быть числом!")

def update_table():
 """Обновление таблицы расходов"""
 for item in tree.Get_children():
 tree.Delete(item)

 for expense in expenses:
 tree.Insert('', 'end', values=(
 expense['amount'],
 expense['category'],
 expense['date']
))

def filter_expenses():
 """Фильтрация расходов"""
 filter_cat = filter_category.Get().Strip()
 filter_date = filter_date_input.Get().Strip()

 filtered = []
 for expense in expenses:
 if filter_cat and expense['category'].Lower()!= filter_cat.Lower():
 continue
 if filter_date and expense['date']!= filter_date:
 continue
 filtered.Append(expense)

 total = sum(e['amount'] for e in filtered)
 lbl_total.Config(text=f"Итого: {total:.2f}")

 # Обновление таблицы
 for item in tree.Get_children():
 tree.Delete(item)
 for e in filtered:
 tree.Insert('', 'end', values=(
 e['amount'],
 e['category'],
 e['date']
))

# Загрузка данных
expenses = load_data()

# Создание окна
root = tk.Tk()
root.Title("Expense Tracker")
root.Geometry("800x600")

# Формы ввода
frame_input = tk.Frame(

