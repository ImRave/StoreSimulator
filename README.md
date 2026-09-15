# 🏪 StoreSimulator

**StoreSimulator** es una aplicación desarrollada en **Python** para simular y administrar las operaciones básicas de un pequeño negocio o tienda de barrio.

El proyecto busca representar de forma sencilla diferentes situaciones que pueden ocurrir en un negocio, como la gestión de productos, inventario, ventas, facturas, cajas y gastos. La información generada puede almacenarse en una base de datos **SQLite**, permitiendo posteriormente consultar y analizar los datos obtenidos.

> 🚧 **Proyecto en desarrollo:** algunas funcionalidades pueden encontrarse en diferentes etapas de implementación.

---

## 📋 Descripción

StoreSimulator nace como un proyecto de aprendizaje enfocado en la combinación de:

* Programación en Python.
* Interfaces gráficas de usuario.
* Manejo de bases de datos.
* Operaciones CRUD.
* Simulación de información de un negocio.
* Recolección y almacenamiento de datos.

La idea principal es contar con un entorno donde sea posible representar las operaciones de una tienda y utilizar los datos generados para realizar posteriormente procesos de consulta y análisis.

---

## ✨ Características

Entre los principales componentes del proyecto se encuentran:

* 📦 **Gestión de productos**

  * Nombre del producto.
  * Precio de compra.
  * Precio de venta.
  * Cantidad disponible.
  * Imagen del producto.

* 🧾 **Gestión de facturas**

  * Identificación de la factura.
  * Caja asociada.
  * Fecha.
  * Total de la venta.

* 🛒 **Registro de productos vendidos**

  * Producto asociado.
  * Cantidad.
  * Factura correspondiente.
  * Caja utilizada.

* 💰 **Registro de ventas**

  * Fecha.
  * Total de la venta.

* 💸 **Registro de gastos**

  * Fecha.
  * Valor total.

* 👤 **Gestión de cajas/vendedores**

  * Nombre del vendedor.
  * Teléfono.
  * Correo electrónico.

* 🗄️ **Persistencia mediante SQLite**

  * La información se almacena en una base de datos local.
  * Se utilizan relaciones entre productos, facturas, cajas y compras.

La estructura actual de la base de datos incluye las tablas `Productos`, `Cajas`, `Facturas`, `Lista_Compra`, `Ventas` y `Gastos`.

---

## 🛠️ Tecnologías utilizadas

| Tecnología  | Uso                          |
| ----------- | ---------------------------- |
| 🐍 Python   | Lenguaje principal           |
| 🗃️ SQLite  | Base de datos                |
| 🖥️ Tkinter | Interfaz gráfica             |
| 📊 SQL      | Consultas y gestión de datos |
| 🔧 Git      | Control de versiones         |
| 🐙 GitHub   | Repositorio y colaboración   |

La aplicación principal utiliza `tkinter` para la interfaz gráfica y `sqlite3` para trabajar con la base de datos.

---

## 🗂️ Estructura del proyecto

```text
StoreSimulator/
│
├── StoreCrudBeta/
│   └── ...
│
├── AdminDatabase.py
├── Aplicacion.py
├── Aplicacion.pyw
├── calculadora.py
├── ejemplo.py
│
├── InvetarioYFacturas.db
├── prueba.db
│
└── README.md
```

### Archivos principales

#### `AdminDatabase.py`

Contiene la lógica relacionada con la creación y configuración de la base de datos SQLite.

Entre las tablas definidas se encuentran:

```text
Productos
Cajas
Facturas
Lista_Compra
Ventas
Gastos
```

También establece relaciones mediante claves foráneas entre productos, facturas, cajas y compras.

#### `Aplicacion.py`

Contiene la aplicación gráfica principal desarrollada utilizando **Tkinter**.

Actualmente establece la ventana principal de la aplicación y configura sus dimensiones y propiedades.

#### `Aplicacion.pyw`

Versión ejecutable del programa mediante Python en Windows sin necesidad de mostrar una consola.

#### `StoreCrudBeta/`

Contiene una versión o desarrollo relacionado con las funcionalidades CRUD del sistema.

#### `InvetarioYFacturas.db`

Base de datos SQLite utilizada por el proyecto para almacenar información relacionada con el inventario y las operaciones de la tienda. El archivo actualmente se encuentra incluido en el repositorio.

---

## 🗄️ Modelo de datos

La aplicación utiliza SQLite para organizar la información del negocio.

Una representación simplificada de las relaciones es:

```text
                  ┌──────────────┐
                  │   PRODUCTOS  │
                  └──────┬───────┘
                         │
                         │
                         ▼
                  ┌──────────────┐
                  │ LISTA_COMPRA │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   FACTURAS   │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │    CAJAS     │
                  └──────────────┘


                  ┌──────────────┐
                  │    VENTAS    │
                  └──────────────┘

                  ┌──────────────┐
                  │    GASTOS    │
                  └──────────────┘
```

Las tablas `Lista_Compra` y `Facturas` utilizan relaciones con `Productos` y `Cajas` mediante claves foráneas.

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/ImRave/StoreSimulator.git
```

### 2. Entrar al proyecto

```bash
cd StoreSimulator
```

### 3. Verificar Python

Se recomienda utilizar una versión reciente de Python 3.

Puedes comprobar la versión instalada con:

```bash
python --version
```

### 4. Ejecutar la aplicación

La aplicación principal puede ejecutarse con:

```bash
python Aplicacion.py
```

También existe una versión `.pyw` para sistemas Windows:

```text
Aplicacion.pyw
```

---

## 🗃️ Base de datos

StoreSimulator utiliza **SQLite**, por lo que no es necesario instalar un servidor de base de datos independiente.

La aplicación crea y utiliza el archivo:

```text
InvetarioYFacturas.db
```

La inicialización de la base de datos se realiza mediante `AdminDatabase.py`.

El sistema define tablas para:

* Productos.
* Cajas.
* Facturas.
* Lista de compras.
* Ventas.
* Gastos.

---

## 🔄 Flujo general

El funcionamiento conceptual del proyecto puede representarse de la siguiente manera:

```text
              ┌─────────────────┐
              │     Usuario     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Interfaz gráfica│
              │    Tkinter      │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Lógica Python   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │     SQLite      │
              │    Database     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Datos del       │
              │ negocio         │
              └─────────────────┘
```

---

## 🎯 Objetivos del proyecto

### Objetivo principal

Desarrollar una aplicación en Python capaz de representar y gestionar las operaciones básicas de un pequeño negocio mediante una interfaz gráfica y una base de datos SQLite.

### Objetivos específicos

* Practicar el desarrollo de aplicaciones con Python.
* Implementar operaciones CRUD.
* Aprender a trabajar con bases de datos SQLite.
* Modelar información relacionada con un negocio.
* Registrar productos, ventas, facturas y gastos.
* Generar información que pueda ser utilizada posteriormente para análisis.
* Aplicar conceptos de desarrollo de software en un proyecto práctico.

---

## 📊 Análisis de datos

Uno de los objetivos del proyecto es utilizar la información generada por la simulación para estudiar el comportamiento de las operaciones del negocio.

A partir de los datos almacenados pueden plantearse análisis como:

* Productos con mayor cantidad de ventas.
* Productos con menor rotación.
* Ingresos por período.
* Gastos realizados.
* Comportamiento de las ventas.
* Horarios o períodos con mayor actividad.
* Relación entre inventario y ventas.

Esto permite utilizar el proyecto como una base para posteriormente aplicar técnicas de **análisis de datos y ciencia de datos**.

---

## 🔮 Próximas mejoras

Algunas funcionalidades que pueden incorporarse al proyecto son:

* [ ] Mejorar la interfaz gráfica.
* [ ] Completar las operaciones CRUD.
* [ ] Implementar autenticación de usuarios.
* [ ] Mejorar la gestión del inventario.
* [ ] Automatizar el registro de ventas.
* [ ] Generar reportes.
* [ ] Agregar gráficos estadísticos.
* [ ] Implementar una simulación más completa de clientes y ventas.
* [ ] Separar la lógica de negocio, interfaz y acceso a datos.
* [ ] Mejorar la estructura y documentación del proyecto.
* [ ] Incorporar pruebas automatizadas.
* [ ] Agregar exportación de datos.

---

## 📚 Propósito académico

StoreSimulator también funciona como un proyecto práctico para reforzar conocimientos relacionados con:

**Python → SQL → Bases de datos → CRUD → Interfaces gráficas → Gestión de información → Análisis de datos**

El proyecto permite integrar diferentes conceptos de programación en una aplicación relacionada con un escenario real.

---

## 👨‍💻 Autor

**ImRave**

GitHub: [@ImRave](https://github.com/ImRave?utm_source=chatgpt.com)

---

## 📄 Licencia

Este proyecto actualmente no muestra una licencia explícita en la raíz del repositorio, por lo que se recomienda agregar una antes de declarar formalmente una licencia de uso o distribución.

---

## 🔗 Repositorio

[StoreSimulator — GitHub](https://github.com/ImRave/StoreSimulator?utm_source=chatgpt.com)
