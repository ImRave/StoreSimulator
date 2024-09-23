create database tienda
use tienda

CREATE TABLE Productos (
    Id_Producto INT PRIMARY KEY IDENTITY(1,1),
    Nombre VARCHAR(100),
    Precio_Venta INT,
    Precio_Compra INT,
    Cantidad INT
);

CREATE TABLE Cajas (
    Id_Caja INT PRIMARY KEY IDENTITY(1,1),
    N_vendedor VARCHAR(100),
    Telefono VARCHAR(15), -- Cambiado de INT a VARCHAR
    Email VARCHAR(100)
);

CREATE TABLE Facturas (
    Id_Factura INT PRIMARY KEY IDENTITY(1,1),
    Id_caja INT,
    Fecha DATE,
    Total INT,
    FOREIGN KEY (Id_caja) REFERENCES Cajas(Id_Caja) -- Coma añadida antes de la clave foránea
);

CREATE TABLE Lista_Compra (
    Id_Compra INT PRIMARY KEY IDENTITY(1,1),
    Id_Factura INT,
    Id_Producto INT,
    Cantidad INT,
    FOREIGN KEY (Id_Factura) REFERENCES Facturas(Id_Factura),
    FOREIGN KEY (Id_Producto) REFERENCES Productos(Id_Producto)
);

CREATE TABLE Ventas (
    Id_Ventas INT PRIMARY KEY IDENTITY(1,1),
    Fecha DATE,
    Total BIGINT
);

CREATE TABLE Gastos (
    Id_Gastos INT PRIMARY KEY IDENTITY(1,1),
    Fecha DATE,
    Total BIGINT
);


INSERT INTO Productos (Nombre, Precio_Venta, Precio_Compra, Cantidad) VALUES
('Producto A', 15000, 10000, 100),
('Producto B', 25000, 20000, 50),
('Producto C', 30000, 25000, 75),
('Producto D', 20000, 15000, 200);

INSERT INTO Cajas (N_vendedor, Telefono, Email) VALUES
('Vendedor 1', 1234567890, 'vendedor1@example.com'),
('Vendedor 2', 2345678901, 'vendedor2@example.com'),
('Vendedor 3', 3456789012, 'vendedor3@example.com');

INSERT INTO Facturas (Id_caja, Fecha, Total) VALUES
(1, '2024-09-01', 50000),
(2, '2024-09-02', 75000),
(1, '2024-09-03', 100000);

INSERT INTO Lista_Compra (Id_Factura, Id_Producto, Cantidad) VALUES
(1, 1, 3),  -- 3 unidades de Producto A en la Factura 1
(1, 2, 2),  -- 2 unidades de Producto B en la Factura 1
(2, 1, 4),  -- 4 unidades de Producto A en la Factura 2
(3, 3, 1);  -- 1 unidad de Producto C en la Factura 3

INSERT INTO Ventas (Fecha, Total) VALUES
('2024-09-01', 500000),
('2024-09-02', 300000),
('2024-09-03', 450000);

INSERT INTO Gastos (Fecha, Total) VALUES
('2024-09-01', 20000),
('2024-09-02', 15000),
('2024-09-03', 30000);
