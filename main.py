import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
from datetime import datetime


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.data = []
        self.load_data()

        # --- Поля ввода ---
        ttk.Label(root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text="Категория:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.category_entry = ttk.Entry(root)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text="Дата:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.date_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(root, text="Добавить расход", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)

        # --- Таблица расходов ---
        self.tree = ttk.Treeview(root, columns=("Сумма", "Категория", "Дата"), show='headings')
        self.tree.heading("Сумма", text="Сумма")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Дата", text="Дата")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # --- Фильтрация и сумма ---
        ttk.Label(root, text="Фильтр по категории:").grid(row=5, column=0, padx=5, pady=5, sticky='e')
        self.filter_category = ttk.Entry(root)
        self.filter_category.grid(row=5, column=1, padx=5, pady=5)
        ttk.Button(root, text="Фильтровать", command=self.filter_expenses).grid(row=6, column=0, columnspan=2, pady=5)

        ttk.Label(root, text="Период (с):").grid(row=7, column=0, padx=5, pady=5, sticky='e')
        self.date_from = DateEntry(root, date_pattern='yyyy-mm-dd')
        self.date_from.grid(row=7, column=1, padx=5, pady=5)

        ttk.Label(root, text="Период (по):").grid(row=8, column=0, padx=5, pady=5, sticky='e')
        self.date_to = DateEntry(root, date_pattern='yyyy-mm-dd')
        self.date_to.grid(row=8, column=1, padx=5, pady=5)

        ttk.Button(root, text="Сумма за период", command=self.sum_for_period).grid(row=9, column=0, columnspan=2,
                                                                                   pady=10)

        self.sum_label = ttk.Label(root, text="Сумма: 0")
        self.sum_label.grid(row=10, column=0, columnspan=2, pady=5)

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()

        if not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
            messagebox.showerror("Ошибка", "Сумма должна быть положительным числом!")
            return
        if not category:
            messagebox.showerror("Ошибка", "Введите категорию!")
            return

        date = self.date_entry.get_date().strftime('%Y-%m-%d')

        self.data.append({"amount": float(amount), "category": category.lower(), "date": date})
        self.save_data()
        self.update_table()

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for expense in self.data:
            self.tree.insert("", "end", values=(f"{expense['amount']:.2f}", expense['category'], expense['date']))

    def filter_expenses(self):
        category = self.filter_category.get().lower()
        filtered = [e for e in self.data if category in e["category"]]

        for i in self.tree.get_children():
            self.tree.delete(i)

        for expense in filtered:
            self.tree.insert("", "end", values=(f"{expense['amount']:.2f}", expense['category'], expense['date']))

    def sum_for_period(self):
        date_from = self.date_from.get_date().strftime('%Y-%m-%d')
        date_to = self.date_to.get_date().strftime('%Y-%m-%d')

        total = sum(e["amount"] for e in self.data if date_from <= e["date"] <= date_to)

        # Восстанавливаем полный список после фильтрации или подсчёта
        self.update_table()

        self.sum_label.config(text=f"Сумма за период: {total:.2f}")

    def save_data(self):
        with open("expenses.json", "w") as f:
            json.dump(self.data, f)

    def load_data(self):
        try:
            with open("expenses.json", "r") as f:
                self.data = json.load(f)
                # Обновляем таблицу сразу после загрузки данных
                self.update_table()
                return
        except FileNotFoundError (json.JSONDecodeError):
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
