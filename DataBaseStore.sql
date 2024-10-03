create database tienda
use tienda

create table proveedores(	
    idProveedor int primary key IDENTITY(1,1),
    empresa varchar(60) not null,
    direccion varchar(60) not null, 
    numeroTelefonoPrincipal varchar(40) not null,
    numeroTelefonoSecudario varchar(40),
    email varchar(60) not null
);

CREATE table tipo (
    idTipo INT PRIMARY KEY IDENTITY(1,1),
    tipo varchar(60) not null
)

CREATE TABLE producto (
    idProducto INT PRIMARY KEY IDENTITY(1,1),
    idProveedor int not null,
    nombre VARCHAR(100) not null,
    idTipo int not null,-- bebidas, almacen, carnes y pescados, frutas y verduras, etc 
    precioVenta FLOAT not null,
    precioCompra FLOAT not null,
    cantidad INT not null,

    foreign key(idProveedor) references proveedores(idProveedor), 
    foreign key(idTipo) references tipo(idTipo) 
);

CREATE TABLE empleado (
    idEmpleado INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(30) not null,
    apellido varchar(30) not null,
    edad int not null,
    direccion varchar(40) not null, 
    email varchar(40) not null,
    fechaIngreso date not null,
    numeroTelefonoPrincipal varchar(40) not null,
    numeroTelefonoSecudario varchar(40)
)

create table clientes(	
    idCliente int primary key IDENTITY(1,1),
    nombre varchar(30) not null,
    apellido varchar(30) not null,
    numeroTelefonoPrincipal varchar(40) not null,
    numeroTelefonoSecudario varchar(40),
    email varchar(40) not null
);

CREATE TABLE caja (
    idCaja INT PRIMARY KEY IDENTITY(1,1),
    idEmpleado int not null,
    ubicacion varchar(60) not null,

    foreign key (idEmpleado) references empleado(idEmpleado)
);

CREATE TABLE factura (
    idFactura INT PRIMARY KEY IDENTITY(1,1),
    idCaja INT not null,
    idCliente int not null
    fecha DATE not null,
    total FLOAT,

    FOREIGN KEY (idCaja) REFERENCES caja(idCaja), -- Coma a�adida antes de la clave for�nea
    foreign key (idCliente) references Cliente(idCliente)
);

CREATE TABLE listaCompra (
    idListaCompra int PRIMARY key IDENTITY(1,1),
    idFactura INT,
    idProducto INT,
    cantidad INT,

    FOREIGN KEY (idFactura) REFERENCES factura(idFactura),
    FOREIGN KEY (idProducto) REFERENCES producto(idProducto)
);


--Esto no sé qué es
CREATE TABLE Venta (
    idVenta INT PRIMARY KEY IDENTITY(1,1),
    idEmpleado int not null,
    id_factura int not null
);

CREATE TABLE Gasto (
    Id_Gastos INT PRIMARY KEY IDENTITY(1,1),
    Fecha DATE,
    Total FLOAT
);

INSERT INTO proveedores (empresa, direccion, numeroTelefonoPrincipal, numeroTelefonoSecudario, email)
VALUES 
('Distribuidora Central', 'Av. Siempre Viva 123', '655-1234', '655-5678', 'info@distribuidora.com'),
('Frutas y Verduras SA', 'Calle Falsa 456', '655-9876', NULL, 'contacto@fyv.com'),
('Carnes y Pescados El Marino', 'Boulevard del Mar 789', '655-3456', '655-6543', 'ventas@elmarino.com'),
('Bebidas del Valle', 'Av. Libertad 101', '655-1122', NULL, 'contacto@bebidasvalle.com'),
('Lácteos Frescos', 'Calle 5 de Mayo 987', '655-7788', '655-5566', 'ventas@lacteosfrescos.com');

INSERT INTO tipo (tipo)
VALUES 
('Bebidas'),
('Almacén'),
('Carnes y Pescados'),
('Frutas y Verduras'),
('Lácteos');

INSERT INTO Producto (idProveedor, nombre, tipo, precioVenta, precioCompra, cantidad)
VALUES 
(1, 'Coca-Cola 2.5L', 1, 8200, 8000, 100),
(2, 'Manzana Roja', 4, 2400, 2200, 200),
(3, 'Filete de Res', 3, 28000, 24000, 50),
(4, 'Yogurt Natural 1L', 5, 16000, 15000, 80),
(1, 'Agua Mineral 500ml', 1, 3600, 3400, 150);

INSERT INTO empleado (nombre, apellido, edad, direccion, email, fechaIngreso, numeroTelefonoPrincipal, numeroTelefonoSecudario)
VALUES 
('Juan', 'Pérez', 30, 'Calle Luna 123', 'juan.perez@mail.com', '2020-01-15', '655-4321', NULL),
('Ana', 'García', 28, 'Calle Sol 456', 'ana.garcia@mail.com', '2021-05-20', '655-9876', '655-1234'),
('Luis', 'Martínez', 35, 'Av. Principal 789', 'luis.martinez@mail.com', '2019-10-10', '655-5555', NULL),

INSERT INTO clientes (nombre, apellido, numeroTelefonoPrincipal, numeroTelefonoSecudario, email)
VALUES 
('Carlos', 'López', '655-2222', NULL, 'carlos.lopez@mail.com'),
('María', 'Fernández', '655-3333', '655-4444', 'maria.fernandez@mail.com'),
('Pedro', 'Gómez', '655-5555', NULL, 'pedro.gomez@mail.com'),
('Laura', 'Vega', '655-6666', '655-7777', 'laura.vega@mail.com'),
('Andrea', 'Castillo', '655-8888', '655-9999', 'andrea.castillo@mail.com');

INSERT INTO caja (idEmpleado, ubicacion)
VALUES 
(1, 'Caja Principal'),
(2, 'Caja Secundaria'),
(3, 'Caja Tercera'),

INSERT INTO factura (idCaja, idCliente, fecha, total)
VALUES 
(1, 1, '2023-09-25', 94000),
(3, 2, '2023-09-26', 56000),
(2, 3, '2023-09-27', 48000),
(2, 4, '2023-09-28', 21600),

INSERT INTO listaCompra (idFactura, idProducto, cantidad)
VALUES 
(1, 1, 10),
(1, 2, 5),
(2, 3, 2),
(3, 4, 3),
(4, 5, 6);

/* 


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
 */