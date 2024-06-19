# restaurante_app/utils.py
import sqlite3
from datetime import datetime

def get_db_connection():
    """Establece y retorna una conexión a la base de datos SQLite."""
    return sqlite3.connect('restaurant.db')

def format_currency(value):
    """Formatea un número como moneda."""
    return f"${value:,.2f}"

def calculate_total_with_taxes_and_tips(subtotal):
    """Calcula el total con IVA y propinas."""
    iva = 0.19
    propina = 0.10
    iva_value = subtotal * iva
    propina_value = subtotal * propina
    total = subtotal + iva_value + propina_value
    return subtotal, iva_value, propina_value, total

def get_sales_by_period(period='day'):
    """
    Retorna las ventas totales agrupadas por día, semana, mes o año.
    
    period: 'day', 'week', 'month', 'year'
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if period == 'day':
        query = "SELECT strftime('%Y-%m-%d', date), SUM(total) FROM sales GROUP BY strftime('%Y-%m-%d', date)"
    elif period == 'week':
        query = "SELECT strftime('%Y-%W', date), SUM(total) FROM sales GROUP BY strftime('%Y-%W', date)"
    elif period == 'month':
        query = "SELECT strftime('%Y-%m', date), SUM(total) FROM sales GROUP BY strftime('%Y-%m', date)"
    elif period == 'year':
        query = "SELECT strftime('%Y', date), SUM(total) FROM sales GROUP BY strftime('%Y', date)"
    else:
        raise ValueError("Período no válido. Use 'day', 'week', 'month' o 'year'.")
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def record_sale(total):
    """Registra una venta en la base de datos."""
    conn = get_db_connection()
    cursor = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO sales (date, total) VALUES (?, ?)", (date, total))
    conn.commit()
    conn.close()

def update_inventory(product_id, quantity):
    """Actualiza la cantidad de un producto en el inventario."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET quantity = quantity - ? WHERE id = ?", (quantity, product_id))
    conn.commit()
    conn.close()
