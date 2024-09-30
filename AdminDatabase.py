import sqlite3, random


def CrearDB():
    conn = sqlite3.connect("DataBases/InvetarioYFacturas.db")
    conn.commit()
    conn.close()

def CreateTabel():
    conn = sqlite3.connect("DataBases/InvetarioYFacturas.db")
    cursor =conn.cursor()
    # Crear la tabla Productos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Productos (
        Id_Producto INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT,
        Precio_Venta  FLOAT,
        Precio_Compra FLOAT,
        Cantidad INT
    )
    """)

    # Crear la tabla Cajas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Cajas (
        Id_Caja INTEGER PRIMARY KEY AUTOINCREMENT,
        N_vendedor TEXT,
        Telefono TEXT,  -- Cambiado a TEXT para evitar problemas con el formato
        Email TEXT
    )
    """)

    # Crear la tabla Facturas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Facturas (
        Id_Factura INTEGER PRIMARY KEY AUTOINCREMENT,
        Id_caja INTEGER,
        Fecha DATE,
        Total  FLOAT,
        FOREIGN KEY (Id_caja) REFERENCES Cajas(Id_Caja)
    )
    """)

    # Crear la tabla Lista_Compra
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Lista_Compra (
        Id_Compra INTEGER PRIMARY KEY AUTOINCREMENT,
        Id_Factura INTEGER,
        Id_Producto INTEGER,
        Cantidad INT,
        FOREIGN KEY (Id_Factura) REFERENCES Facturas(Id_Factura),
        FOREIGN KEY (Id_Producto) REFERENCES Productos(Id_Producto)
    )
    """)

    # Crear la tabla Ventas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Ventas (
        Id_Ventas INTEGER PRIMARY KEY AUTOINCREMENT,
        Fecha DATE,
        Total  FLOAT
    )
    """)

    # Crear la tabla Gastos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Gastos (
        Id_Gastos INTEGER PRIMARY KEY AUTOINCREMENT,
        Fecha DATE,
        Total  FLOAT
    )
    """)
    conn.commit()
    conn.close()

def Insert(nombre,precio):
    conn = sqlite3.connect("DataBases/InvetarioYFacturas.db")
    cursor =conn.cursor()
    cantidad = random.randint(75, 500)
    precio_venta = float(precio)+(float(precio)*0.3)
    insertAuto =f"""
    INSERT INTO Productos (Nombre, Precio_Venta, Precio_Compra, Cantidad) VALUES
    ('{nombre}', {precio_venta}, {precio}, {cantidad})
    """
    cursor.execute(insertAuto)
    conn.commit()
    conn.close()

def Select_productos():
    conn = sqlite3.connect("DataBases/InvetarioYFacturas.db")
    cursor =conn.cursor()
    consulta = f"""
    Select * From Productos
    """
    cursor.execute(consulta)
    datos = cursor.fetchall()
    conn.commit()
    conn.close()
    return datos


if __name__ == "__main__":
    productos =[("manzana",1000),("pera",700),("banano",1500)]
    print(productos)
    NomYPre = ", ".join(map(str, productos[2]))
    nombreYprecio = NomYPre.split(",")
    print(nombreYprecio[0],nombreYprecio[1])
    CrearDB()
    CreateTabel()
    Insert(nombreYprecio[0],nombreYprecio[1])
    for a in productos:
        Insert(a[0], a[1])
    DBproductos = Select_productos()
    print(DBproductos)
