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
        obtener_productos()
        productos = obtener_productos()
        lista_nombres_producto = [producto[1] for producto in productos]  # Extraer solo los nombres
        combobox_producto['values'] = lista_nombres_producto
    elif selected_tab == tab3:
        mostrar_productos()
        limpiar_campos()

#--------------------------------------------------Pestaña 1 (Compra y facturas)-----------------------------------------------------#

def combobox_selected(event):
    actualizar_nombre_vendedor_numero_factura()
    mostrar_compra(combobox_cajas.get(), textbox_factura.get())

def obtener_cajas():
    """Obtiene los cajas de la base de datos y devuelve una lista de tuplas (id_caja, n_vendedor, telefono)"""
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cajas")
    cajas = cursor.fetchall()
    conn.close()
    return cajas

def generar_factura(caja):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    
    # Obtener el último ID de factura
    cursor.execute("SELECT MAX(id_factura) FROM facturas WHERE id_caja = ?", (caja,))
    ultimo_id_factura = cursor.fetchone()[0]
    
    # Verificar si la última factura tiene compras en Lista_Compra
    if ultimo_id_factura is not None:
        cursor.execute("SELECT * FROM lista_compra WHERE id_factura = ? AND id_caja = ?", (ultimo_id_factura, caja))
        lista_compra = cursor.fetchall()
        
        # Si la lista de compras está vacía, devolver el último id de factura
        if not lista_compra:
            conn.close()
            return ultimo_id_factura
    
    # Generar un nuevo ID de factura si no hay facturas o si la última tiene registros en Lista_Compra
    nuevo_id_factura = 1 if ultimo_id_factura is None else ultimo_id_factura + 1
    
    # Insertar la nueva factura con fecha y hora
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO facturas (id_factura, id_caja, fecha, total) VALUES (?, ?, ?, ?)",
        (nuevo_id_factura, caja, fecha_actual, 0)
    )

    conn.commit()
    conn.close()
    
    return nuevo_id_factura

def actualizar_nombre_vendedor_numero_factura():
    """Actualiza el nombre del vendedor seleccionar una caja del combobox"""
    seleccion = combobox_cajas.get()
    for caja in cajas:
        if caja[0] == int(seleccion):  # Compara el numero de la caja
            nombre_vendedor.set(caja[1])  # Actualiza el nombre

            numero_factura.set(generar_factura(seleccion)) 

            mostrar_compra(caja[0], int(seleccion))

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
    productos = obtener_productos()
    lista_nombres_producto = [producto[1] for producto in productos]  # Extraer solo los nombres
    combobox_producto['values'] = lista_nombres_producto
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
    mostrar_compra(combobox_cajas.get(), textbox_factura.get())
    textbox_cantidad.delete(0, tk.END)

def cantidad_producto(id_producto):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    
    # Ejecutar la consulta
    cursor.execute("SELECT cantidad FROM Productos WHERE id_producto=?", (id_producto,))
    resultado = cursor.fetchone()
    
    conn.close()
    
    # Verificar si el resultado no es None y devolver el id
    if resultado:
        return resultado[0]
    else:
        raise ValueError("Producto no encontrado en la base de datos")

def agregar_producto_compra(id_factura, id_caja, id_producto, cantidad):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()

    if (cantidad_producto(id_producto) - cantidad) >= 0:
        cursor.execute("INSERT INTO Lista_Compra (id_factura, id_caja, id_producto, Cantidad) VALUES (?, ?, ?, ?)",
                   (id_factura, id_caja, id_producto, cantidad,))
    
        cursor.execute("UPDATE Productos SET Cantidad=? WHERE Id_Producto=?",
                       ((cantidad_producto(id_producto) - cantidad), id_producto,))
        
        conn.commit()
        conn.close()
        mostrar_compra(combobox_cajas.get(), textbox_factura.get())
        limpiar_campos_tab1()
    else:
        raise ValueError("No hay sufiente producto")

def editar_producto_compra(id_factura, id_caja, id_producto, cantidad):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()

    selected_item = trees.selection()[0]
    valores = trees.item(selected_item, 'values')
    cantidad_antes = int(valores[0])
    cantidad_ahora = cantidad
    cantidad_d = cantidad_antes - cantidad_ahora

    if cantidad_d >= 0 or (cantidad_antes + cantidad_producto(id_producto)) >= cantidad_ahora:
        cursor.execute("UPDATE Lista_Compra SET id_producto=?, Cantidad=? WHERE Id_Producto=? and Id_Factura=? and Id_Caja=?",
                    (id_producto, cantidad, id_producto, id_factura, id_caja))

        cursor.execute("UPDATE Productos SET Cantidad=? WHERE Id_Producto=?",
                        ((cantidad_producto(id_producto) + (cantidad_d)), id_producto,))
    else:
        raise ValueError("No hay sufiente producto")

    conn.commit()
    conn.close()

    limpiar_campos_tab1()

def eliminar_producto_compra(id_factura, id_caja, id_producto, cantidad):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Lista_Compra WHERE Id_Factura=? and id_caja=? and Id_Producto=?", (id_factura, id_caja, id_producto,))
    
    cursor.execute("UPDATE Productos SET Cantidad=? WHERE Id_Producto=?",
        ((cantidad_producto(id_producto) + cantidad), id_producto,))

    conn.commit()
    conn.close()

    limpiar_campos_tab1()

def mostrar_compra(caja, factura):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            Lista_Compra.Cantidad, 
            Productos.Nombre, 
            Productos.Precio_Venta, 
            (Lista_Compra.Cantidad * Productos.Precio_Venta) AS Importe
        FROM 
            Lista_Compra 
        JOIN 
            Productos ON Lista_Compra.Id_Producto = Productos.Id_Producto 
		JOIN
			Facturas ON Lista_Compra.Id_Factura = Facturas.Id_Factura and Lista_Compra.Id_Caja = Facturas.Id_Caja
        WHERE 
            Lista_Compra.Id_Factura = ? AND Lista_Compra.Id_Caja = ?
    """, (factura, caja))
    
    rows = cursor.fetchall()
    
    # Limpia el treeview
    for row in trees.get_children():  # Asegúrate de que `trees` es el nombre correcto de tu Treeview
        trees.delete(row)
        
    # Insertar los nuevos datos
    for row in rows:
        trees.insert("", "end", values=row)  # Asegúrate de que los valores coinciden con el número de columnas de tu treeview

    # Mostrar el total
    # Ejecutar la consulta
    cursor.execute("""SELECT 
            sum(Lista_Compra.Cantidad * Productos.Precio_Venta) AS Importe
        FROM 
            Lista_Compra 
        JOIN 
            Productos ON Lista_Compra.Id_Producto = Productos.Id_Producto 
		JOIN
			Facturas ON Lista_Compra.Id_Factura = Facturas.Id_Factura and Lista_Compra.Id_Caja = Facturas.Id_Caja
        WHERE 
            Lista_Compra.Id_Factura = ? AND Lista_Compra.Id_Caja = ?"""
                   , (factura, caja,))
    resultado = cursor.fetchone() 
    total_value = resultado[0] if resultado[0] is not None else 0  # Establecer total a 0 si no hay resultados

    # Suponiendo que 'total' es un StringVar, actualiza su valor
    total.set(total_value)
              
    cursor.execute("""
        UPDATE Facturas
        SET Total = ?
        WHERE Id_Factura = ? AND Id_caja = ?
    """, (total_value, factura, caja))

    conn.commit()
    conn.close()

def conseguir_id_producto(nombre):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    
    # Ejecutar la consulta
    cursor.execute("SELECT Id_Producto FROM Productos WHERE Nombre=?", (nombre,))
    resultado = cursor.fetchone()
    
    conn.close()
    
    # Verificar si el resultado no es None y devolver el id
    if resultado:
        return resultado[0]
    else:
        raise ValueError("Producto no encontrado en la base de datos")
    
def seleccionar_fila_compra(event):
    selected_item = trees.selection()[0]
    valores = trees.item(selected_item, 'values')
    
    obtener_productos()
    combobox_producto.delete(0, tk.END)
    combobox_producto.insert(0, valores[1])
    productos = obtener_productos()
    lista_nombres_producto = [producto[1] for producto in productos]  # Extraer solo los nombres
    combobox_producto['values'] = lista_nombres_producto
    precio.set(valores[2])
    textbox_cantidad.delete(0, tk.END)
    textbox_cantidad.insert(0, valores[0])

    # Cargar imagen de la base de datos
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Imagen_producto FROM Productos WHERE Id_Producto=?", (conseguir_id_producto(valores[1]),))
    imagen = cursor.fetchone()[0]
    conn.close()

    if imagen:
        img = Image.open(io.BytesIO(imagen))
        img.thumbnail((100, 100))
        img = ImageTk.PhotoImage(img)
        label_imagen.config(image=img)
        label_imagen.image = img

def limpiar_campos_tab1():
    obtener_productos()
    combobox_producto.delete(0, tk.END)
    productos = obtener_productos()
    lista_nombres_producto = [producto[1] for producto in productos]  # Extraer solo los nombres
    combobox_producto['values'] = lista_nombres_producto
    precio.set("")
    textbox_cantidad.delete(0, tk.END)
    label_imagen.config(image='')
    mostrar_compra(combobox_cajas.get(), textbox_factura.get())

def guardar_factura(factura, caja):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    
    cursor.execute("""SELECT 
            sum(Lista_Compra.Cantidad * Productos.Precio_Venta) AS Importe
        FROM 
            Lista_Compra 
        JOIN 
            Productos ON Lista_Compra.Id_Producto = Productos.Id_Producto 
		JOIN
			Facturas ON Lista_Compra.Id_Factura = Facturas.Id_Factura and Lista_Compra.Id_Caja = Facturas.Id_Caja
        WHERE 
            Lista_Compra.Id_Factura = ? AND Lista_Compra.Id_Caja = ?"""
                   , (factura, caja,))
    
    resultado = cursor.fetchone() 
    total_value = resultado[0] if resultado[0] is not None else 0  # Establecer total a 0 si no hay resultados
    
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        UPDATE Facturas
        SET Total = ?, Fecha=?
        WHERE Id_Factura = ? AND Id_caja = ?
    """, (total_value, fecha_actual, factura, caja))

    conn.commit()
    conn.close()

    actualizar_nombre_vendedor_numero_factura()
    limpiar_campos_tab1()

#------------------------------------------------Pestaña 2 (Registro)-------------------------------------------------------#

def caja_selected(event):
    mostrar_facturas(combo_cajas.get())
    actualizar_vendedor()
    quitar_lista()

def quitar_lista():
    fecha.set("")
    total_tab2.set("")
    for row in tr.get_children():  # Asegúrate de que `tre` es el nombre correcto de tu Treeview
        tr.delete(row)

def actualizar_vendedor():
    """Actualiza el nombre del vendedor al seleccionar una caja del combobox"""
    seleccion = combo_cajas.get()
    for caja in ob_cajas:
        if caja[0] == int(seleccion):  # Compara el numero de la caja
            vendedor.set(caja[1])  # Actualiza el nombre

def mostrar_facturas(caja):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            Id_factura, fecha, total
        FROM 
            Facturas 
        WHERE 
            Id_Caja = ? and total != 0
    """, (caja))
    
    rows = cursor.fetchall()
    # Limpia el treeview
    for row in tre.get_children():  # Asegúrate de que `tre` es el nombre correcto de tu Treeview
        tre.delete(row)
    # Insertar los nuevos datos
    for row in rows:
        tre.insert("", "end", values=row)  # Asegúrate de que los valores coinciden con el número de columnas de tu treeview

    conn.close()
    
def seleccionar_fila_lista(event):
    selected_item = tre.selection()[0]
    valores = tre.item(selected_item, 'values')
    
    id_factura = valores[0]
    caja = combo_cajas.get()
    fecha.set(valores[1])
    total_tab2.set(valores[2])

    # Cargar la lista
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            Lista_Compra.Cantidad, 
            Productos.Nombre, 
            Productos.Precio_Venta, 
            (Lista_Compra.Cantidad * Productos.Precio_Venta) AS Importe
        FROM 
            Lista_Compra 
        JOIN 
            Productos ON Lista_Compra.Id_Producto = Productos.Id_Producto 
		JOIN
			Facturas ON Lista_Compra.Id_Factura = Facturas.Id_Factura and Lista_Compra.Id_Caja = Facturas.Id_Caja
        WHERE 
            Lista_Compra.Id_Factura = ? AND Lista_Compra.Id_Caja = ?
    """, (id_factura, caja))
    
    rows = cursor.fetchall()
    # Limpia el treeview
    for row in tr.get_children():  # Asegúrate de que `tre` es el nombre correcto de tu Treeview
        tr.delete(row)
    # Insertar los nuevos datos
    for row in rows:
        tr.insert("", "end", values=row)  # Asegúrate de que los valores coinciden con el número de columnas de tu treeview

    conn.close()

def limpiar_tab2():
    obtener_cajas()
    combo_cajas.delete(0, tk.END)
    ob_cajas = obtener_cajas()
    list_cajas = [caja[0] for caja in ob_cajas]  # Extraer solo los nombres
    combo_cajas['values'] = list_cajas
    fecha.set("")
    total_tab2.set("")
    vendedor.set("")

    for row in tr.get_children():  # Asegúrate de que `tre` es el nombre correcto de tu Treeview
        tr.delete(row)
    for row in tre.get_children():  # Asegúrate de que `tre` es el nombre correcto de tu Treeview
        tre.delete(row)


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
    limpiar_campos()

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
    limpiar_campos()
    mostrar_productos()

def eliminar_producto(id_producto):
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Productos WHERE Id_Producto=?", (id_producto,))
    conn.commit()
    conn.close()
    limpiar_campos()
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
notebook.add(tab1, text="Compras y facturas")
notebook.add(tab2, text="Registro")
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
combobox_cajas.bind("<<ComboboxSelected>>", combobox_selected)  # Evento al seleccionar

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
# Cargar productos de la base de datos
productos = obtener_productos()
lista_nombres_productos = [producto[1] for producto in productos]  # Extraer solo los nombres

# Crear el combobox para seleccionar productos
combobox_producto = ttk.Combobox(tab1, values=lista_nombres_productos)
combobox_producto.grid(row=2, column=1, padx=5, pady=5)
combobox_producto.bind("<<ComboboxSelected>>", actualizar_precio_imagen)  # Evento al seleccionar

# Campo de texto para mostrar el precio (no editable)
precio = tk.StringVar()  # Variable para almacenar el precio de venta
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
tk.Button(tab1, text="Agregar", command=lambda: agregar_producto_compra(int(textbox_factura.get()), int(combobox_cajas.get()), conseguir_id_producto(combobox_producto.get()),
                                                                 float(textbox_cantidad.get()))).grid(row=3, column=0)
tk.Button(tab1, text="Editar", command=lambda: editar_producto_compra(int(textbox_factura.get()), int(combobox_cajas.get()), conseguir_id_producto(combobox_producto.get()),
                                                                 float(textbox_cantidad.get()))).grid(row=3, column=1)
tk.Button(tab1, text="Eliminar", command=lambda: eliminar_producto_compra(int(textbox_factura.get()), int(combobox_cajas.get()), conseguir_id_producto(combobox_producto.get()),
                                                                 float(textbox_cantidad.get()))).grid(row=3, column=2)
tk.Button(tab1, text="Limpiar", command=limpiar_campos_tab1).grid(row=3, column=3)
tk.Button(tab1, text="Guardar", command=lambda: guardar_factura(int(textbox_factura.get()), int(combobox_cajas.get()))).grid(row=4, column=6)

# Tabla para mostrar productos
trees = ttk.Treeview(tab1, columns=("Cantidad", "Producto", "Precio Unitario", "Importe"), show="headings")
trees.grid(row=4, column=0, columnspan=4)
trees.heading("Cantidad", text="Cantidad")
trees.heading("Producto", text="Producto")
trees.heading("Precio Unitario", text="Precio Unitario")
trees.heading("Importe", text="Importe")

# Campo de texto para mostrar el total (no editable)
total = tk.StringVar()  # Variable para almacenar el precio de venta
tk.Label(tab1, text="Total:").grid(row=4, column=4, padx=5, pady=5)
textbox_total = tk.Entry(tab1, textvariable=total, state="readonly")
textbox_total.grid(row=4, column=5, padx=5, pady=5)



# Evento para seleccionar una fila
trees.bind("<ButtonRelease-1>", seleccionar_fila_compra)

#-----------------------------------------------Pestaña 2 (Registro)-------------------------------------------------#

ob_cajas = obtener_cajas()
list_cajas = [caja[0] for caja in cajas]  # Extraer solo el numero de la caja

tk.Label(tab2, text="Selecciona caja:").grid(row=0, column=0, padx=5, pady=5)
combo_cajas = ttk.Combobox(tab2, values=list_cajas)
combo_cajas.grid(row=0, column=1, padx=5, pady=5)
combo_cajas.bind("<<ComboboxSelected>>", caja_selected)

vendedor = tk.StringVar()  # Variable para almacenar nombre del vendedor
tk.Label(tab2, text="Vendedor:").grid(row=0, column=2, padx=5, pady=5)
text_vendedor = tk.Entry(tab2, textvariable=vendedor, state="readonly")
text_vendedor.grid(row=0, column=3, padx=5, pady=5)

tk.Label(tab2, text="Infomacion de la Factura").grid(row=0, column=7, padx=5, pady=5)

tk.Button(tab2, text="Limpiar", command=limpiar_tab2).grid(row=3, column=1)

fecha = tk.StringVar()  # Variable para almacenar el precio de venta
tk.Label(tab2, text="Fecha:").grid(row=3, column=6, padx=5, pady=5)
text_fecha = tk.Entry(tab2, textvariable=fecha, state="readonly")
text_fecha.grid(row=3, column=7, padx=5, pady=5)


total_tab2 = tk.StringVar()  # Variable para almacenar el precio de venta
tk.Label(tab2, text="Total:").grid(row=5, column=6, padx=5, pady=5)
text_total = tk.Entry(tab2, textvariable=total_tab2, state="readonly")
text_total.grid(row=5, column=7, padx=5, pady=5)


tre = ttk.Treeview(tab2, columns=("ID Factura", "Fecha", "Total"), show="headings")
tre.grid(row=2, column=0, columnspan=4)
tre.heading("ID Factura", text="ID Factura")
tre.heading("Fecha", text="Fecha")
tre.heading("Total", text="Total")

tr = ttk.Treeview(tab2, columns=("Cantidad", "Producto", "Precio Unitario", "Importe"), show="headings")
tr.grid(row=2, column=6, columnspan=4)
tr.heading("Cantidad", text="Cantidad")
tr.heading("Producto", text="Producto")
tr.heading("Precio Unitario", text="Precio Unitario")
tr.heading("Importe", text="Importe")

# Evento para seleccionar una fila
tre.bind("<ButtonRelease-1>", seleccionar_fila_lista)

#----------------------------------------------Pestaña 3 (Administración de Productos)----------------------------------------------#

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
