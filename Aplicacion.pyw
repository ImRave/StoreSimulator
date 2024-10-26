import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk  # Para trabajar con imágenes
import sqlite3
import io  # Agregar esta línea para gestionar bytes de imagen
import AdminDatabase


# Funciones de base de datos
def agregar_producto(nombre_producto, precio_venta, precio_compra, cantidad, imagen_ruta):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    with open(imagen_ruta, 'rb') as file:
        imagen = file.read()
    cursor.execute("INSERT INTO Productos (Nombre, Precio_Venta, Precio_Compra, Cantidad, Imagen_producto) VALUES (?, ?, ?, ?, ?)",
                   (nombre_producto, precio_venta, precio_compra, cantidad, imagen))
    conn.commit()
    conn.close()
    mostrar_productos()

def editar_producto(id_producto, nombre_producto, precio_venta, precio_compra, cantidad, imagen_ruta=None):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    if imagen_ruta:
        with open(imagen_ruta, 'rb') as file:
            imagen = file.read()
        cursor.execute("UPDATE Productos SET Nombre=?, Precio_Venta=?, Precio_Compra=?, Cantidad=?, Imagen_producto=? WHERE Id_Producto=?",
                       (nombre_producto, precio_venta, precio_compra, cantidad, imagen, id_producto))
    else:
        cursor.execute("UPDATE Productos SET Nombre=?, Precio_Venta=?, Precio_Compra=?, Cantidad=? WHERE Id_Producto=?",
                       (nombre_producto, precio_venta, precio_compra, cantidad, id_producto))
    conn.commit()
    conn.close()
    mostrar_productos()

def eliminar_producto(id_producto):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Productos WHERE Id_Producto=?", (id_producto,))
    conn.commit()
    conn.close()
    mostrar_productos()

def mostrar_productos():
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Productos")
    rows = cursor.fetchall()
    for row in tree.get_children():
        tree.delete(row)
    for row in rows:
        tree.insert("", "end", values=row[:5])  # Mostrar solo datos sin imagen
    conn.close()

def cargar_imagen():
    global imagen_ruta
    imagen_ruta = filedialog.askopenfilename(title="Seleccionar imagen",
                                             filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png")])
    if imagen_ruta:
        img = Image.open(imagen_ruta)
        img.thumbnail((100, 100))
        img = ImageTk.PhotoImage(img)
        img_label.config(image=img)
        img_label.image = img

def seleccionar_fila(event):
    selected_item = tree.selection()[0]
    valores = tree.item(selected_item, 'values')
    
    id_producto.config(state=tk.NORMAL)
    id_producto.delete(0, tk.END)
    id_producto.insert(0, valores[0])
    id_producto.config(state='readonly')
    
    nombre_producto.delete(0, tk.END)
    nombre_producto.insert(0, valores[1])
    
    precio_venta.delete(0, tk.END)
    precio_venta.insert(0, valores[2])

    precio_compra.delete(0, tk.END)
    precio_compra.insert(0, valores[3])

    cantidad.delete(0, tk.END)
    cantidad.insert(0, valores[4])

    # Cargar imagen de la base de datos
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Imagen_producto FROM Productos WHERE Id_Producto=?", (valores[0],))
    imagen = cursor.fetchone()[0]
    conn.close()

    if imagen:
        img = Image.open(io.BytesIO(imagen))
        img.thumbnail((100, 100))
        img = ImageTk.PhotoImage(img)
        img_label.config(image=img)
        img_label.image = img

def limpiar_campos():
    id_producto.config(state=tk.NORMAL)
    id_producto.delete(0, tk.END)
    id_producto.config(state='readonly')
    nombre_producto.delete(0, tk.END)
    precio_venta.delete(0, tk.END)
    precio_compra.delete(0, tk.END)
    cantidad.delete(0, tk.END)
    img_label.config(image='')

def obtener_productos():
    """Obtiene los productos de la base de datos y devuelve una lista de tuplas (id_producto, nombre, precio_venta)"""
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Id_Producto, Nombre, Precio_Venta,Imagen_producto FROM Productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def actualizar_precio_imagen(event):
    """Actualiza el campo de precio y la imagen al seleccionar un producto del combobox"""
    seleccion = combobox_producto.get()
    for producto in productos:
        if producto[1] == seleccion:  # Compara el nombre del producto
            precio.set(producto[2])  # Actualiza el precio
            if producto[2]:  # Si hay imagen
                imagen_binaria = producto[3]
                imagen = Image.open(io.BytesIO(imagen_binaria))
                imagen.thumbnail((100, 100))  # Redimensionar la imagen
                imagen_tk = ImageTk.PhotoImage(imagen)
                label_imagen.config(image=imagen_tk)
                label_imagen.image = imagen_tk  # Mantener referencia de la imagen
            else:
                label_imagen.config(image=None)
            break



# Crear la ventana principal
ventana = tk.Tk()
AdminDatabase.CrearDB()
AdminDatabase.CreateTabels()
ventana.title("Interfaz con Pestañas")

# Crear el widget Notebook (pestañas)
notebook = ttk.Notebook(ventana)
notebook.pack(expand=True, fill="both")

# Crear el contenido de las pestañas
tab1 = tk.Frame(notebook)
tab2 = tk.Frame(notebook)
tab3 = tk.Frame(notebook)

# Agregar las pestañas al notebook
notebook.add(tab1, text="Compras Y facturas")
notebook.add(tab2, text="Pestaña 2")
notebook.add(tab3, text="Administración de Productos")

#Contenido de la pestaña 1(compra y facturas)
tk.Label(tab1, text="Selecciona un producto:").grid(row=0, column=0, padx=5, pady=5)
precio = tk.StringVar()  # Variable para almacenar el precio de venta

# Cargar productos de la base de datos
productos = obtener_productos()
lista_nombres_productos = [producto[1] for producto in productos]  # Extraer solo los nombres

# Crear el combobox para seleccionar productos
combobox_producto = ttk.Combobox(tab1, values=lista_nombres_productos)
combobox_producto.grid(row=0, column=1, padx=5, pady=5)
combobox_producto.bind("<<ComboboxSelected>>", actualizar_precio_imagen)  # Evento al seleccionar

# Campo de texto para mostrar el precio (no editable)
tk.Label(tab1, text="Precio de Venta:").grid(row=0, column=2, padx=5, pady=5)
textbox_precio = tk.Entry(tab1, textvariable=precio, state="readonly")
textbox_precio.grid(row=0, column=3, padx=5, pady=5)

# Etiqueta para mostrar la imagen
label_imagen = tk.Label(tab1)
label_imagen.grid(row=0, column=4, padx=5, pady=5)

# Contenido de la pestaña 3 (Administración de Productos)
tk.Label(tab3, text="ID Producto").grid(row=0, column=0)
id_producto = tk.Entry(tab3, state='readonly')
id_producto.grid(row=0, column=1)

tk.Label(tab3, text="Nombre Producto").grid(row=1, column=0)
nombre_producto = tk.Entry(tab3)
nombre_producto.grid(row=1, column=1)

tk.Label(tab3, text="Precio Venta").grid(row=2, column=0)
precio_venta = tk.Entry(tab3)
precio_venta.grid(row=2, column=1)

tk.Label(tab3, text="Precio Compra").grid(row=3, column=0)
precio_compra = tk.Entry(tab3)
precio_compra.grid(row=3, column=1)

tk.Label(tab3, text="Cantidad").grid(row=4, column=0)
cantidad = tk.Entry(tab3)
cantidad.grid(row=4, column=1)

# Imagen
tk.Label(tab3, text="Imagen del Producto").grid(row=5, column=0)
img_label = tk.Label(tab3)
img_label.grid(row=5, column=1)
imagen_ruta = ""
tk.Button(tab3, text="Cargar Imagen", command=cargar_imagen).grid(row=5, column=2)

# Botones de control
tk.Button(tab3, text="Agregar", command=lambda: agregar_producto(nombre_producto.get(), float(precio_venta.get()),
                                                                 float(precio_compra.get()), int(cantidad.get()), imagen_ruta)).grid(row=6, column=0)
tk.Button(tab3, text="Editar", command=lambda: editar_producto(id_producto.get(), nombre_producto.get(),
                                                              float(precio_venta.get()), float(precio_compra.get()), int(cantidad.get()), imagen_ruta)).grid(row=6, column=1)
tk.Button(tab3, text="Eliminar", command=lambda: eliminar_producto(id_producto.get())).grid(row=6, column=2)
tk.Button(tab3, text="Limpiar", command=limpiar_campos).grid(row=6, column=3)

# Tabla para mostrar productos
tree = ttk.Treeview(tab3, columns=("ID", "Nombre", "Precio Venta", "Precio Compra", "Cantidad"), show="headings")
tree.grid(row=7, column=0, columnspan=4)
tree.heading("ID", text="ID")
tree.heading("Nombre", text="Nombre")
tree.heading("Precio Venta", text="Precio Venta")
tree.heading("Precio Compra", text="Precio Compra")
tree.heading("Cantidad", text="Cantidad")

# Evento para seleccionar una fila
tree.bind("<ButtonRelease-1>", seleccionar_fila)

# Llamada para mostrar productos al iniciar
mostrar_productos()

# Ejecutar la ventana principal
ventana.mainloop()
