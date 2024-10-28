import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk  # Para trabajar con imágenes "Hay que 'pip install pillow' en la terminal"
import sqlite3
import io  # Agregar esta línea para gestionar bytes de imagen
import AdminDatabase
from datetime import datetime

# Funciones 

# Configurar evento para actualizar productos al abrir cada tab
def on_tab_selected(event):
    selected_tab = event.widget.nametowidget(event.widget.select())
    if selected_tab == tab1:
        productos = obtener_productos()
        lista_nombres_producto = [producto[1] for producto in productos]  # Extraer solo los nombres
        combobox_producto['values'] = lista_nombres_producto
    elif selected_tab == tab3:
        mostrar_productos()
        limpiar_campos()

#--------------------------------------------------Pestaña 1 (Compra y facturas)-----------------------------------------------------#

def obtener_cajas():
    """Obtiene los cajas de la base de datos y devuelve una lista de tuplas (id_caja, n_vendedor, telefono)"""
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cajas")
    cajas = cursor.fetchall()
    conn.close()
    return cajas

def obtener_numero_factura(caja):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()

    # Obtener el último Id_Factura para la caja especificada
    cursor.execute("SELECT MAX(Id_Factura) FROM Facturas WHERE Id_caja = ?", (caja))
    ultimo_id_factura = cursor.fetchone()[0]
    
    # Si no hay facturas previas, comenzamos con 1, de lo contrario sumamos 1
    if ultimo_id_factura is None:
        nuevo_id_factura = 1
        cursor.execute("insert into facturas (id_factura, id_caja, fecha, total) values (?,?,?,?)", (nuevo_id_factura, caja, datetime.now(), 0))
        
    else:
        nuevo_id_factura = ultimo_id_factura + 1
        cursor.execute("insert into facturas (id_factura, id_caja, fecha, total) values (?,?,?,?)", (nuevo_id_factura, caja, datetime.now(), 0))
    conn.commit()
    conn.close()
    return nuevo_id_factura

def actualizar_nombre_vendedor_numero_factura(event):
    """Actualiza el nombre del vendedor seleccionar una caja del combobox"""
    seleccion = combobox_cajas.get()
    for caja in cajas:
        if caja[0] == int(seleccion):  # Compara el numero de la caja
            nombre_vendedor.set(caja[1])  # Actualiza el nombre

            numero_factura.set(obtener_numero_factura(seleccion)) 

    mostrar_compra(caja[0], numero_factura.get())


def obtener_productos():
    """Obtiene los productos de la base de datos y devuelve una lista de tuplas (id_producto, nombre, precio_venta)"""
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Id_Producto, Nombre, Precio_Venta, Imagen_producto, cantidad FROM Productos where cantidad > 0 ")
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

def agregar_producto_compra(id_factura, id_producto, cantidad):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    with open(imagen_ruta, 'rb') as file:
        imagen = file.read()
    cursor.execute("INSERT INTO Lista_Compra (id_factura, id_producto, Cantidad) VALUES (?, ?, ?)",
                   (id_factura, id_producto, cantidad))
    conn.commit()
    conn.close()
    mostrar_compra(combobox_cajas.get, textbox_factura.get)

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

def mostrar_compra(caja, factura):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            Lista_Compra.Cantidad, 
            Productos.Nombre, 
            Productos.Precio_Venta, 
            SUM(Lista_Compra.Cantidad * Productos.Precio_Venta) AS Importe
        FROM 
            Lista_Compra 
        JOIN 
            Productos ON Lista_Compra.Id_Producto = Productos.Id_Producto 
        WHERE 
            Lista_Compra.Id_Factura = ? AND Lista_Compra.Id_Caja = ?
        GROUP BY 
            Lista_Compra.Cantidad, Productos.Nombre, Productos.Precio_Venta
    """, (factura, caja))
    
    rows = cursor.fetchall()
    
    # Limpia el treeview
    for row in trees.get_children():  # Asegúrate de que `tree` es el nombre correcto de tu Treeview
        tree.delete(row)
        
    # Insertar los nuevos datos
    for row in rows:
        tree.insert("", "end", values=row)  # Asegúrate de que los valores coinciden con el número de columnas de tu treeview

    conn.close()

def conseguir_id_producto(nombre):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("select id_producto FROM Productos WHERE nombre=?", (nombre))
    id = cursor.fetchone()[0]
    conn.close()
    return id
#------------------------------------------------Pestaña 3 (Administración de Productos)----------------------------------------------------#

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
    for row in tree.get_children():  #Limpia el treeView (la tabla)
        tree.delete(row)
    for row in rows:
        tree.insert("", "end", values=row[:5])  # Mostrar solo datos sin imagen (soplo mustra las 5 primeras columbas)
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
    mostrar_productos()


# Crear la ventana principal
ventana = tk.Tk()
AdminDatabase.CrearDB()
AdminDatabase.CreateTables()
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

notebook.bind("<<NotebookTabChanged>>", on_tab_selected)

#--------------------------------------------------Pestaña 1 (Compra y facturas)-----------------------------------------------------#

#Contenido de la pestaña 1(compra y facturas)
# Cargar caja en la que se hace la factura
cajas = obtener_cajas()
numero_factura = tk.StringVar()  # Variable para almacenar nombre del vendedor
lista_cajas = [caja[0] for caja in cajas]  # Extraer solo el numero de la caja

tk.Label(tab1, text="Selecciona caja:").grid(row=0, column=0, padx=5, pady=5)
combobox_cajas = ttk.Combobox(tab1, values=lista_cajas)
combobox_cajas.grid(row=0, column=1, padx=5, pady=5)
combobox_cajas.bind("<<ComboboxSelected>>", actualizar_nombre_vendedor_numero_factura)  # Evento al seleccionar

nombre_vendedor = tk.StringVar()  # Variable para almacenar nombre del vendedor
tk.Label(tab1, text="Vendedor:").grid(row=0, column=3, padx=5, pady=5)
textbox_vendedor = tk.Entry(tab1, textvariable=nombre_vendedor, state="readonly")
textbox_vendedor.grid(row=0, column=4, padx=5, pady=5)

# Saber el numero de la factura
tk.Label(tab1, text="Factura #").grid(row=0, column=6, padx=5, pady=5)
textbox_factura = tk.Entry(tab1, textvariable=numero_factura, state="readonly")
textbox_factura.grid(row=0, column=7, padx=5, pady=5)

tk.Label(tab1, text="").grid(row=1, column=0, padx=5, pady=5)

#Campo de texto para escoger el producto
tk.Label(tab1, text="Selecciona un producto:").grid(row=2, column=0, padx=5, pady=5)
precio = tk.StringVar()  # Variable para almacenar el precio de venta

# Cargar productos de la base de datos
productos = obtener_productos()
lista_nombres_productos = [producto[1] for producto in productos]  # Extraer solo los nombres

# Crear el combobox para seleccionar productos
combobox_producto = ttk.Combobox(tab1, values=lista_nombres_productos)
combobox_producto.grid(row=2, column=1, padx=5, pady=5)
combobox_producto.bind("<<ComboboxSelected>>", actualizar_precio_imagen)  # Evento al seleccionar

# Campo de texto para mostrar el precio (no editable)
tk.Label(tab1, text="Precio de Venta:").grid(row=2, column=2, padx=5, pady=5)
textbox_precio = tk.Entry(tab1, textvariable=precio, state="readonly")
textbox_precio.grid(row=2, column=3, padx=5, pady=5)

# Etiqueta para mostrar la imagen
label_imagen = tk.Label(tab1)
label_imagen.grid(row=2, column=4, padx=5, pady=5)

# Campo de texto para la cantidad a comprar 
tk.Label(tab1, text="Cantidad:").grid(row=2, column=5, padx=5, pady=5)
textbox_cantidad = tk.Entry(tab1)
textbox_cantidad.grid(row=2, column=6, padx=5, pady=5)

# Botones de control
tk.Button(tab1, text="Agregar", command=lambda: agregar_producto_compra(textbox_factura.get(), float(conseguir_id_producto(combobox_producto)),
                                                                 float(textbox_cantidad.get()))).grid(row=6, column=0)
tk.Button(tab1, text="Editar", command=lambda: editar_producto(id_producto.get(), nombre_producto.get(),
                                                              float(precio_venta.get()), float(precio_compra.get()), int(cantidad.get()), imagen_ruta)).grid(row=6, column=1)
tk.Button(tab1, text="Eliminar", command=lambda: eliminar_producto(id_producto.get())).grid(row=6, column=2)
tk.Button(tab1, text="Limpiar", command=limpiar_campos).grid(row=6, column=3)

# Tabla para mostrar productos
trees = ttk.Treeview(tab1, columns=("Cantidad", "Producto", "Precio Unitario", "Importe"), show="headings")
trees.grid(row=7, column=0, columnspan=4)
trees.heading("Cantidad", text="Cantidad")
trees.heading("Producto", text="Producto")
trees.heading("Precio Unitario", text="Precio Unitario")
trees.heading("Importe", text="Importe")

# Evento para seleccionar una fila

# trees.bind("<ButtonRelease-1>", seleccionar_fila_compra)

#------------------------------------------------Pestaña 3 (Administración de Productos)----------------------------------------------------#

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
