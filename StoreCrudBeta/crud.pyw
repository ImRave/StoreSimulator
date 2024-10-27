import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

# Funciones del CRUD con Tkinter
def agregar_producto():
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Productos (Nombre, Precio_Venta, Precio_Compra, Cantidad) VALUES (?, ?, ?, ?)",
                   (nombre_producto.get(), float(precio_venta.get()), float(precio_compra.get()), int(cantidad.get())))
    conn.commit()
    conn.close()
    mostrar_productos()
    limpiar_campos()

def editar_producto():
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Productos SET Nombre=?, Precio_Venta=?, Precio_Compra=?, Cantidad=? WHERE Id_Producto=?",
                   (nombre_producto.get(), float(precio_venta.get()), float(precio_compra.get()), int(cantidad.get()), int(id_producto.get())))
    conn.commit()
    conn.close()
    mostrar_productos()
    limpiar_campos()

def eliminar_producto():
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Productos WHERE Id_Producto=?", (id_producto.get(),))
    conn.commit()
    conn.close()
    mostrar_productos()
    limpiar_campos()

def mostrar_productos():
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Productos")
    rows = cursor.fetchall()
    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert("", END, values=row)
    conn.close()

def limpiar_campos():
    id_producto.delete(0, END)
    nombre_producto.delete(0, END)
    precio_venta.delete(0, END)
    precio_compra.delete(0, END)
    cantidad.delete(0, END)

def seleccionar_fila(event):
    selected_item = tree.selection()[0]
    valores = tree.item(selected_item, 'values')
    
    # Rellenar los campos con los valores seleccionados
    id_producto.config(state=NORMAL)
    id_producto.delete(0, END)
    id_producto.insert(0, valores[0])
    id_producto.config(state='readonly')  # Hacer el campo de ID solo de lectura
    
    nombre_producto.delete(0, END)
    nombre_producto.insert(0, valores[1])

    precio_venta.delete(0, END)
    precio_venta.insert(0, valores[2])

    precio_compra.delete(0, END)
    precio_compra.insert(0, valores[3])

    cantidad.delete(0, END)
    cantidad.insert(0, valores[4])

# Interfaz gráfica con Tkinter
root = Tk()
root.title("Gestión de Inventario")

# Campos de entrada
Label(root, text="ID Producto").grid(row=0, column=0)
id_producto = Entry(root)
id_producto.grid(row=0, column=1)
id_producto.config(state='readonly')  # Hacer que el ID sea solo de lectura

Label(root, text="Nombre Producto").grid(row=1, column=0)
nombre_producto = Entry(root)
nombre_producto.grid(row=1, column=1)

Label(root, text="Precio Venta").grid(row=2, column=0)
precio_venta = Entry(root)
precio_venta.grid(row=2, column=1)

Label(root, text="Precio Compra").grid(row=3, column=0)
precio_compra = Entry(root)
precio_compra.grid(row=3, column=1)

Label(root, text="Cantidad").grid(row=4, column=0)
cantidad = Entry(root)
cantidad.grid(row=4, column=1)

# Botones
Button(root, text="Agregar", command=agregar_producto).grid(row=5, column=0)
Button(root, text="Editar", command=editar_producto).grid(row=5, column=1)
Button(root, text="Eliminar", command=eliminar_producto).grid(row=5, column=2)

# Tabla para mostrar productos
tree = ttk.Treeview(root, columns=("ID", "Nombre", "Precio Venta", "Precio Compra", "Cantidad"), show="headings")
tree.grid(row=6, column=0, columnspan=3)
tree.heading("ID", text="ID")
tree.heading("Nombre", text="Nombre")
tree.heading("Precio Venta", text="Precio Venta")
tree.heading("Precio Compra", text="Precio Compra")
tree.heading("Cantidad", text="Cantidad")

# Evento para seleccionar una fila
tree.bind("<ButtonRelease-1>", seleccionar_fila)

# Mostrar productos al iniciar
mostrar_productos()

root.mainloop()