import sqlite3


def CrearDB():
    conn = sqlite3.connect("InvetarioYFacturas.db")
    conn.commit()
    conn.close()
    CreateTables()

def CreateTables():
    conn = sqlite3.connect("InvetarioYFacturas.db")
    cursor =conn.cursor()

    #cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
    #tablas = cursor.fetchall()
    
    # Eliminar cada tabla existente
    #for tabla in tablas:
    #    cursor.execute(f"DROP TABLE IF EXISTS {tabla[0]}")

    conn = sqlite3.connect("InvetarioYFacturas.db")  # Conectar a la base de datos
    cursor = conn.cursor()

    # Crear la tabla Productos
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS Productos (
        Id_Producto INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT,
        Precio_Venta FLOAT,
        Precio_Compra FLOAT,
        Cantidad INT,
        Imagen_producto BLOB
    )
    """)

    # Crear la tabla Cajas
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS Cajas (
        Id_Caja INTEGER PRIMARY KEY AUTOINCREMENT,
        N_vendedor TEXT,
        Telefono TEXT,  
        Email TEXT
    )
    """)

    # Crear la tabla Facturas
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS Facturas (
        Id_Factura INTEGER,
        Id_caja INTEGER,
        Fecha DATE,
        Total FLOAT,
        PRIMARY KEY(Id_Factura, Id_caja),
        FOREIGN KEY(Id_caja) REFERENCES Cajas(Id_Caja)
    );
    """)

    # Crear la tabla Lista_Compra
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS Lista_Compra (
        Id_Compra INTEGER PRIMARY KEY AUTOINCREMENT,
        Id_Factura INTEGER,
        Id_Caja INTEGER,
        Id_Producto INTEGER,
        Cantidad INT,
        FOREIGN KEY (Id_Factura, Id_Caja) REFERENCES Facturas(Id_Factura, Id_caja), 
        FOREIGN KEY (Id_Producto) REFERENCES Productos(Id_Producto)
    )
    """)

    # Crear la tabla Ventas
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS Ventas (
        Id_Ventas INTEGER PRIMARY KEY AUTOINCREMENT,
        Fecha DATE,
        Total FLOAT
    )
    """)

    # Crear la tabla Gastos
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS Gastos (
        Id_Gastos INTEGER PRIMARY KEY AUTOINCREMENT,
        Fecha DATE,
        Total FLOAT
    )
    """)

    # Inserción inicial en la tabla Cajas
    cursor.execute(""" 
    INSERT OR IGNORE INTO Cajas (Id_Caja, N_vendedor, Telefono, Email)
    VALUES (1, 'Juan Pérez', '123456789', 'juan@example.com'),
           (2, 'Nathalia Gomez', '32612380', 'natha@gmail.com')
    """)

    # Guardar cambios y cerrar la conexión
    conn.commit()
    conn.close()

# Llamada a la función para crear la base de datos
CrearDB()
