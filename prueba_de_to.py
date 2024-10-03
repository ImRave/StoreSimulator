import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Funciones del CRUD

def conectar():
    conn = sqlite3.connect("crud.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            edad INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insertar():
    conn = sqlite3.connect("crud.db")
    cursor = conn.cursor()
    item = tabla.selection()[0]
    seleccionado = tabla.item(item, 'values')

    if (id_entry.get()==seleccionado[0]):
        messagebox.showwarning("Advertencia", "No puedes insertar una persona ya insertada.")
        limpiar_campos()
    elif (nombre.get() == "" or apellido.get() == "" or edad.get() == ""):
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
    else:
        cursor.execute("INSERT INTO personas (nombre, apellido, edad) VALUES (?, ?, ?)",
                       (nombre.get(), apellido.get(), edad.get()))
        conn.commit()
        conn.close()
        limpiar_campos()
        mostrar_datos_persona()

def mostrar_datos_persona():
    for item in tabla.get_children():
        tabla.delete(item)

    conn = sqlite3.connect("crud.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personas")
    registros = cursor.fetchall()
    for row in registros:
        tabla.insert('', 'end', values=row)
    conn.close()

def limpiar_campos():
    nombre.set("")
    apellido.set("")
    edad.set("")
    id_entry.config(state=NORMAL)
    id_entry.delete(0, END)
    id_entry.config(state=DISABLED)

def eliminar():
    conn = sqlite3.connect("crud.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personas WHERE id = ?", (id_entry.get(),))
    conn.commit()
    conn.close()
    limpiar_campos()
    mostrar_datos_persona()

def actualizar():
    conn = sqlite3.connect("crud.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE personas
        SET nombre = ?, apellido = ?, edad = ?
        WHERE id = ?
    """, (nombre.get(), apellido.get(), edad.get(), id_entry.get()))
    conn.commit()
    conn.close()
    limpiar_campos()
    mostrar_datos_persona()

def seleccionar(event):
    try:
        item = tabla.selection()[0]
        seleccionado = tabla.item(item, 'values')
        id_entry.config(state=NORMAL)
        id_entry.delete(0, END)
        id_entry.insert(END, seleccionado[0])
        id_entry.config(state=DISABLED)
        nombre.set(seleccionado[1])
        apellido.set(seleccionado[2])
        edad.set(seleccionado[3])
    except IndexError:
        pass

# Interfaz gráfica

root = Tk()
root.title("CRUD con Tkinter y SQLite")

# Variables
nombre = StringVar()
apellido = StringVar()
edad = StringVar()

# Campos de entrada
Label(root, text="ID").grid(row=0, column=0, padx=10, pady=10)
id_entry = Entry(root, state=DISABLED)
id_entry.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Nombre").grid(row=1, column=0, padx=10, pady=10)
Entry(root, textvariable=nombre).grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Apellido").grid(row=2, column=0, padx=10, pady=10)
Entry(root, textvariable=apellido).grid(row=2, column=1, padx=10, pady=10)

Label(root, text="Edad").grid(row=3, column=0, padx=10, pady=10)
Entry(root, textvariable=edad).grid(row=3, column=1, padx=10, pady=10)

# Botones
Button(root, text="Insertar", command=insertar).grid(row=4, column=0, padx=10, pady=10)
Button(root, text="Actualizar", command=actualizar).grid(row=4, column=1, padx=10, pady=10)
Button(root, text="Eliminar", command=eliminar).grid(row=4, column=2, padx=10, pady=10)
Button(root, text="Limpiar", command=limpiar_campos).grid(row=4, column=3, padx=10, pady=10)

# Tabla para mostrar los registros
tabla = ttk.Treeview(root, columns=("ID", "Nombre", "Apellido", "Edad"), show='headings')
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Apellido", text="Apellido")
tabla.heading("Edad", text="Edad")

tabla.column("ID", width=50)
tabla.column("Nombre", width=150)
tabla.column("Apellido", width=150)
tabla.column("Edad", width=50)

tabla.grid(row=5, column=0, columnspan=4, padx=10, pady=10)
tabla.bind('<<TreeviewSelect>>', seleccionar)

# Mostrar los registros al iniciar
conectar()
mostrar_datos_persona()

root.mainloop()
