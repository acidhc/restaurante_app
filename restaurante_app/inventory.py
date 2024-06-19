# restaurante_app/inventory.py
# restaurante_app/inventory.py
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Inventory(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg='#2e2e2e')
        self.controller = controller
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        label = tk.Label(self, text="Inventario", font=('Arial', 18), bg='#2e2e2e', fg='white')
        label.pack(pady=10, padx=10)

        # Formulario de ingreso de productos
        form_frame = tk.Frame(self, bg='#2e2e2e')
        form_frame.pack(pady=10, padx=10, fill='x')

        self.name_var = tk.StringVar()
        self.quantity_var = tk.IntVar()
        self.price_var = tk.DoubleVar()

        name_label = tk.Label(form_frame, text="Nombre del Producto:", bg='#2e2e2e', fg='white')
        name_label.grid(row=0, column=0, pady=5, padx=5)
        name_entry = tk.Entry(form_frame, textvariable=self.name_var)
        name_entry.grid(row=0, column=1, pady=5, padx=5)

        quantity_label = tk.Label(form_frame, text="Cantidad:", bg='#2e2e2e', fg='white')
        quantity_label.grid(row=1, column=0, pady=5, padx=5)
        quantity_entry = tk.Entry(form_frame, textvariable=self.quantity_var)
        quantity_entry.grid(row=1, column=1, pady=5, padx=5)

        price_label = tk.Label(form_frame, text="Precio:", bg='#2e2e2e', fg='white')
        price_label.grid(row=2, column=0, pady=5, padx=5)
        price_entry = tk.Entry(form_frame, textvariable=self.price_var)
        price_entry.grid(row=2, column=1, pady=5, padx=5)

        add_button = tk.Button(form_frame, text="Agregar Producto", command=self.add_product, bg='#4e4e4e', fg='white')
        add_button.grid(row=3, columnspan=2, pady=10)

        # Tabla para mostrar productos
        self.tree = ttk.Treeview(self, columns=('ID', 'Nombre', 'Cantidad', 'Precio'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Cantidad', text='Cantidad')
        self.tree.heading('Precio', text='Precio')

        self.tree.pack(pady=10, padx=10, fill='both', expand=True)

        # Botones de modificar y eliminar
        button_frame = tk.Frame(self, bg='#2e2e2e')
        button_frame.pack(pady=10, padx=10, fill='x')

        modify_button = tk.Button(button_frame, text="Modificar Producto", command=self.modify_product, bg='#4e4e4e', fg='white')
        modify_button.pack(side='left', padx=10)

        delete_button = tk.Button(button_frame, text="Eliminar Producto", command=self.delete_product, bg='#4e4e4e', fg='white')
        delete_button.pack(side='left', padx=10)

    def add_product(self):
        name = self.name_var.get()
        quantity = self.quantity_var.get()
        price = self.price_var.get()

        if not name or quantity <= 0 or price <= 0:
            messagebox.showerror("Error", "Por favor ingrese todos los detalles correctamente.")
            return

        try:
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)
            ''', (name, quantity, price))
            conn.commit()

            messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
            
            # Resetear las variables de entrada
            self.name_var.set("")
            self.quantity_var.set(0)
            self.price_var.set(0.0)
            
            self.load_data()  # Recargar datos después de agregar
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el producto: {e}")
        finally:
            conn.close()

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM inventory')
            for row in cursor.fetchall():
                self.tree.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el inventario: {e}")
        finally:
            conn.close()

    def modify_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor seleccione un producto para modificar.")
            return

        item = self.tree.item(selected_item)
        product_id = item['values'][0]
        EditProductWindow(self, product_id)

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor seleccione un producto para eliminar.")
            return

        item = self.tree.item(selected_item)
        product_id = item['values'][0]

        try:
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM inventory WHERE id = ?
            ''', (product_id,))
            conn.commit()

            messagebox.showinfo("Éxito", "Producto eliminado exitosamente.")
            self.load_data()  # Recargar datos después de eliminar
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")
        finally:
            conn.close()

class EditProductWindow(tk.Toplevel):
    def __init__(self, parent, product_id):
        super().__init__(parent)
        self.title("Modificar Producto")
        self.geometry("400x300")
        self.configure(bg='#2e2e2e')
        self.product_id = product_id

        self.name_var = tk.StringVar()
        self.quantity_var = tk.IntVar()
        self.price_var = tk.DoubleVar()

        # Obtener los datos actuales del producto
        self.load_product_data()

        name_label = tk.Label(self, text="Nombre del Producto:", bg='#2e2e2e', fg='white')
        name_label.pack(pady=5)
        name_entry = tk.Entry(self, textvariable=self.name_var)
        name_entry.pack(pady=5)

        quantity_label = tk.Label(self, text="Cantidad:", bg='#2e2e2e', fg='white')
        quantity_label.pack(pady=5)
        quantity_entry = tk.Entry(self, textvariable=self.quantity_var)
        quantity_entry.pack(pady=5)

        price_label = tk.Label(self, text="Precio:", bg='#2e2e2e', fg='white')
        price_label.pack(pady=5)
        price_entry = tk.Entry(self, textvariable=self.price_var)
        price_entry.pack(pady=5)

        save_button = tk.Button(self, text="Guardar Cambios", command=self.save_changes, bg='#4e4e4e', fg='white')
        save_button.pack(pady=10)

        close_button = tk.Button(self, text="Cerrar", command=self.destroy, bg='#4e4e4e', fg='white')
        close_button.pack(pady=5)

    def load_product_data(self):
        try:
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            cursor.execute('SELECT name, quantity, price FROM inventory WHERE id = ?', (self.product_id,))
            product = cursor.fetchone()
            conn.close()

            if product:
                self.name_var.set(product[0])
                self.quantity_var.set(product[1])
                self.price_var.set(product[2])
            else:
                messagebox.showerror("Error", "No se pudo cargar los datos del producto.")
                self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar los datos del producto: {e}")
            self.destroy()

    def save_changes(self):
        name = self.name_var.get()
        quantity = self.quantity_var.get()
        price = self.price_var.get()

        if not name or quantity <= 0 or price <= 0:
            messagebox.showerror("Error", "Por favor ingrese todos los detalles correctamente.")
            return

        try:
            conn = sqlite3.connect('restaurant.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE inventory SET name = ?, quantity = ?, price = ? WHERE id = ?
            ''', (name, quantity, price, self.product_id))
            conn.commit()

            messagebox.showinfo("Éxito", "Producto modificado exitosamente.")
            self.master.load_data()  # Recargar datos en la ventana principal después de modificar
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar el producto: {e}")
        finally:
            conn.close()
